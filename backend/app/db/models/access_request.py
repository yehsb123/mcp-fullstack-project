# AccessRequest 모델 (권한 신청)
from app.schemas.permission import PermissionResponse

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class AccessRequest(Base):
    __tablename__ = "access_requests"  # 표 이름

    id = Column(Integer, primary_key=True, index=True)           # 고유번호(PK)
    user_id = Column(Integer, ForeignKey("users.id"))            # 신청자 (users.id 참조 FK)
    resource_name = Column(String, nullable=False)               # 신청 대상 (필수)
    access_level = Column(String, nullable=False)                # 권한 레벨 read/write/admin (필수)
    status = Column(String, default="pending")                   # 상태 (기본값 대기중)
    reason = Column(String)                                      # 신청 사유
    created_at = Column(DateTime, server_default=func.now())     # 생성시각 자동
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())  # 수정시각 자동갱신
