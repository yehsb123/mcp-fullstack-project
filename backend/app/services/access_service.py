from sqlalchemy.orm import Session
from app.db.models.access_request import AccessRequest
from app.schemas.access_request import AccessRequestCreate
from app.db.models.permission import Permission


def create_request(db: Session, data: AccessRequestCreate):
    new_request = AccessRequest(
        user_id=data.user_id,
        resource_name=data.resource_name,
        access_level=data.access_level,
        reason=data.reason,
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


def get_requests(db: Session):
    return db.query(AccessRequest).all()


def get_request_by_id(db: Session, request_id: int):
    return db.query(AccessRequest).filter(AccessRequest.id == request_id).first()


def approve_request(db: Session, request_id: int):
    request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if request is None:
        return None
    request.status = "approved"

    new_permission = Permission(
        user_id=request.user_id,
        resource_name=request.resource_name,
        access_level=request.access_level,
    )
    db.add(new_permission)
    db.commit()
    db.refresh(request)
    return request


def reject_request(db: Session, request_id: int):
    request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if request is None:
        return None
    request.status = "rejected"
    db.commit()
    db.refresh(request)
    return request


def get_user_permissions(db: Session, user_id: int):
    return db.query(Permission).filter(Permission.user_id == user_id).all()
