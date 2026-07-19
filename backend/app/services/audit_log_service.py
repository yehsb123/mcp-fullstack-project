# Agent 판단 이력 서비스
# 3주차에 구현
# ★ 참고: access_service.py의 create_request() 함수와 동일한 패턴입니다!

from sqlalchemy.orm import Session
from app.db.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    request_id: int,
    action: str,
    decision: str,
    reasoning: str,
    policy_referenced: str,
    decided_by: str = "agent",
) -> AuditLog:
    """Agent의 판단 과정을 audit_logs 테이블에 기록한다."""

    # TODO: AuditLog 객체를 만들고 DB에 저장하세요
    # ★ access_service.py의 create_request()를 열어서 똑같이 따라하면 됩니다
    #
    # 1단계: new_log = AuditLog(
    #            request_id=request_id,
    #            action=action,
    #            decision=decision,
    #            reasoning=reasoning,
    #            policy_referenced=policy_referenced,
    #            decided_by=decided_by,
    #        )
    # 2단계: db.add(new_log)
    # 3단계: db.commit()
    # 4단계: db.refresh(new_log)
    # 5단계: return new_log
    pass
