# Permission 모델 (부여된 권한)

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Permission(Base):
    __tablename__ = "permissions"  # 표 이름

    id = Column(Integer, primary_key=True, index=True)       # 고유번호(PK)
    user_id = Column(Integer, ForeignKey("users.id"))        # 권한 소유자 (users.id 참조 FK)
    resource_name = Column(String, nullable=False)           # 권한 대상 (필수)
    access_level = Column(String, nullable=False)            # 권한 레벨 (필수)
    granted_at = Column(DateTime, server_default=func.now()) # 부여 시각 자동
    expires_at = Column(DateTime)                            # 만료 시각 (없으면 무기한)
