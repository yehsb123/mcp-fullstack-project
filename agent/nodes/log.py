# 로깅 노드 — Agent 파이프라인 마지막 단계

from agent.state import AgentState
from app.core.database import SessionLocal
from app.services.audit_log_service import create_audit_log


def log_node(state: AgentState) -> dict:
    """Agent의 판단 과정을 audit_logs 테이블에 기록한다."""

    db = SessionLocal()

    create_audit_log(
        db=db,
        request_id=None,
        action=state.get("decision", "unknown"),
        decision=state.get("decision", "unknown"),
        reasoning=state.get("reasoning", ""),
        policy_referenced="",
        decided_by="agent",
    )

    db.close()
    return {}
