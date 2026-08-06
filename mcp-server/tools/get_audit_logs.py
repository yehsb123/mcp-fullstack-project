# MCP Tool: 판단 이력 조회
# 4주차에 구현

# [4주차 TODO] Agent 판단 이력 조회 Tool 만들기
# ★ 이 Tool은 access_service를 안 쓰고 직접 AuditLog 모델을 query함
# ★ 왜? audit_log_service.py에는 create만 있고 조회 함수가 없거든
# ★ order_by + limit 패턴 익혀두기

from app.core.database import SessionLocal
from app.db.models.audit_log import AuditLog


def get_audit_logs(limit: int = 20) -> dict:
    """Agent의 판단 이력(audit logs)을 최신순으로 조회한다."""
    db = SessionLocal()
    try:
        # --- 1단계: 최신순 정렬 + limit 적용해서 조회 ---
        # ★ order_by(컬럼.desc()) = 내림차순(최신이 위로)
        # ★ .limit(N) = 최대 N개만 가져오기
        logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()

        # --- 2단계: dict로 변환해서 반환 ---
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
