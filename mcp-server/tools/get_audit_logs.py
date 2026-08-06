from app.core.database import SessionLocal
from app.db.models.audit_log import AuditLog


def get_audit_logs(limit: int = 20) -> dict:
    """Agent의 판단 이력(audit logs)을 최신순으로 조회한다."""
    db = SessionLocal()
    try:
        logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
        return {
            "count": len(logs),
            "logs": [
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
            ],
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
