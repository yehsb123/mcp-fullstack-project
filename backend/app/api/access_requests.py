from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.access_request import (
    AccessRequestCreate,
    AccessRequestUpdate,
    AccessRequestResponse,
    PermissionResponse,
)
from app.services import access_service
from app.db.models.audit_log import AuditLog

router = APIRouter(prefix="/api/v1", tags=["access-requests"])


@router.post("/access-requests", response_model=AccessRequestResponse)
def create_access_request(data: AccessRequestCreate, db: Session = Depends(get_db)):
    return access_service.create_request(db, data)


@router.get("/access-requests", response_model=list[AccessRequestResponse])
def list_access_requests(db: Session = Depends(get_db)):
    return access_service.get_requests(db)


@router.get("/access-requests/{request_id}", response_model=AccessRequestResponse)
def get_access_request(request_id: int, db: Session = Depends(get_db)):
    request = access_service.get_request_by_id(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="신청을 찾을 수 없습니다")
    return request


@router.patch("/access-requests/{request_id}", response_model=AccessRequestResponse)
def update_access_request(
    request_id: int, data: AccessRequestUpdate, db: Session = Depends(get_db)
):
    if data.status == "approved":
        request = access_service.approve_request(db, request_id)
    elif data.status == "rejected":
        request = access_service.reject_request(db, request_id)
    else:
        raise HTTPException(status_code=400, detail="status는 approved 또는 rejected여야 합니다")

    if request is None:
        raise HTTPException(status_code=404, detail="신청을 찾을 수 없습니다")
    return request


@router.get("/users/{user_id}/permissions", response_model=list[PermissionResponse])
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    return access_service.get_user_permissions(db, user_id)


@router.get("/audit-logs")
def list_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
    return [
        {
            "id": log.id,
            "request_id": log.request_id,
            "action": log.action,
            "decision": log.decision,
            "reasoning": log.reasoning,
            "policy_referenced": log.policy_referenced,
            "decided_by": log.decided_by,
            "created_at": str(log.created_at) if log.created_at else None,
        }
        for log in logs
    ]
