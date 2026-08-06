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
    new_log = AuditLog(
        request_id=request_id,
        action=action,
        decision=decision,
        reasoning=reasoning,
        policy_referenced=policy_referenced,
        decided_by=decided_by,
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log
