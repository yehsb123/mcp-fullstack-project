# AuditLog 모델 (Agent 판단 이력)
# 3주차에 구현
# ★ 참고: access_request.py와 동일한 패턴입니다! 열어서 비교하면서 작성하세요.

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    # TODO: 아래 8개 컬럼을 정의하세요
    # ★ access_request.py의 Column 정의를 그대로 따라하면 됩니다
    #
    # 1. id                → Column(Integer, primary_key=True, index=True)
    # 2. request_id        → Column(Integer, ForeignKey("access_requests.id"))
    # 3. action            → Column(String)                    예: "자동 승인"
    # 4. decision          → Column(String)                    예: "approve"
    # 5. reasoning         → Column(String)                    판단 근거
    # 6. policy_referenced → Column(String)                    예: "auto_approve_policy.md"
    # 7. decided_by        → Column(String, default="agent")
    # 8. created_at        → Column(DateTime, server_default=func.now())
    pass
