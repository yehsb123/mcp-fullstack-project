# 로깅 노드 — Agent 파이프라인 5번째(마지막) 단계
# 3주차에 구현
# ★ 참고: audit_log_service.py의 create_audit_log() 함수를 호출하는 겁니다

from agent.state import AgentState
from app.core.database import SessionLocal
from app.services.audit_log_service import create_audit_log


def log_node(state: AgentState) -> dict:
    """Agent의 판단 과정을 audit_logs 테이블에 기록한다."""

    # TODO: 아래 단계를 구현하세요

    # --- 1단계: DB 세션 열기 ---
    db = SessionLocal()

    # --- 2단계: audit_log 생성 ---
    # ★ 내가 만든 create_audit_log() 함수를 호출하기
    create_audit_log(
        db=db,
        request_id=None, #지금은 임시로 None-실제 request_id 연결은 나중 단계
        action=state.get("decision", "unknown"), #state에서 안전하게 꺼내기(없으면 기본값)
        decision=state.get("decision", "unknown"),
        reasoning=state.get("reasoning", ""),
        policy_referenced="",
        decided_by="agent",
    )

    # --- 3단계: DB 세션 닫기 ---
    db.close()

    # --- 4단계: 빈 dict 반환 (log 노드는 새 필드 없음) ---
    return {}
