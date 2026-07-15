from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 신청 시 입력받는 양식 (id/status는 서버가 정하므로 제외)
class AccessRequestCreate(BaseModel):
    user_id: int          # 신청자 번호
    resource_name: str    # 신청 대상
    access_level: str     # 권한 레벨
    reason: str           # 사유

# 상태 변경(승인/반려) 시 입력
class AccessRequestUpdate(BaseModel):
    status: str           # approved / rejected 등

# 응답으로 내보내는 양식 (전체 정보)
class AccessRequestResponse(BaseModel):
    id: int
    user_id: int
    resource_name: str
    access_level: str
    status: str
    reason: Optional[str] = None   # 없을수도 있음
    created_at: datetime

    model_config = {"from_attributes": True}  # ORM 객체 --> 스키마 자동 변환 허용


# 권한 응답 양식
class PermissionResponse(BaseModel):
    id: int
    user_id: int
    resource_name: str
    access_level: str
    granted_at: datetime
    expires_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
