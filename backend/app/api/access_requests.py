# 권한 신청 API 엔드포인트

# TODO: POST /api/v1/access-requests (권한 신청)
# TODO: GET /api/v1/access-requests (신청 목록 조회)
# TODO: GET /api/v1/access-requests/{id} (신청 상세 조회)
# TODO: PATCH /api/v1/access-requests/{id} (신청 상태 변경 - 승인/반려)

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

# 이 파일의 API들을 묶는 라우터 (주소 앞에 공통으로 /api/v1)
router = APIRouter(prefix="/api/v1", tags=["access-requests"])


# 권한 신청 (POST)
@router.post("/access-requests", response_model=AccessRequestResponse)
def create_access_request(data: AccessRequestCreate, db: Session = Depends(get_db)):
    return access_service.create_request(db, data)


# 신청 목록 조회 (GET)
@router.get("/access-requests", response_model=list[AccessRequestResponse])
def list_access_requests(db: Session = Depends(get_db)):
    return access_service.get_requests(db)


# 신청 상세 조회 (GET)
@router.get("/access-requests/{request_id}", response_model=AccessRequestResponse)
def get_access_request(request_id: int, db: Session = Depends(get_db)):
    request = access_service.get_request_by_id(db, request_id)
    if request is None:                                    # 없으면 404 에러
        raise HTTPException(status_code=404, detail="신청을 찾을 수 없습니다")
    return request


# 신청 상태 변경 - 승인/반려 (PATCH)
@router.patch("/access-requests/{request_id}", response_model=AccessRequestResponse)
def update_access_request(
    request_id: int, data: AccessRequestUpdate, db: Session = Depends(get_db)
):
    if data.status == "approved":                          # 승인이면
        request = access_service.approve_request(db, request_id)
    elif data.status == "rejected":                        # 반려일 경우 
        request = access_service.reject_request(db, request_id)
    else:                                                  # 그 외 값은 거절
        raise HTTPException(status_code=400, detail="status는 approved 또는 rejected여야 합니다")

    if request is None:                                    # 없는 신청이면 404
        raise HTTPException(status_code=404, detail="신청을 찾을 수 없습니다")
    return request


# 사용자 현재 권한 조회 (GET)
@router.get("/users/{user_id}/permissions", response_model=list[PermissionResponse])
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    return access_service.get_user_permissions(db, user_id)

