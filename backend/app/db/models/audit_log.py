# AuditLog 모델 (Agent 판단 이력)
# 3주차에 구현


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    # TODO: 아래 8개 컬럼을 정의하세요
    # ★ access_request.py(실제 db 테이블 구조)의 Column 정의를 그대로 따라하기
    id=Column(Integer,primary_key=True, index=True)
    request_id=Column(Integer,ForeignKey("access_requests.id"), nullable=True)
    action=Column(String)
    decision = Column(String)
    reasoning = Column(String)
    policy_referenced = Column(String)
    decided_by = Column(String, default="agent")
    created_at = Column(DateTime, server_default=func.now())