from agent.state import AgentState
from app.core.database import SessionLocal
from app.services import access_service
from app.schemas.access_request import AccessRequestCreate


def execute_node(state: AgentState) -> dict:
    """판단 결과에 따라 권한 부여/반려/에스컬레이션을 실행한다."""

    decision = state.get("decision", "escalate")
    user_id = state.get("user_id", 0)
    user_message = state.get("user_message", "")
    reasoning = state.get("reasoning", "")
    actions_taken = []

    db = SessionLocal()
    try:
        data = AccessRequestCreate(
            user_id=user_id,
            resource_name=user_message,
            access_level="read",
            reason=f"[Agent] {reasoning[:200]}",
        )
        request = access_service.create_request(db, data)
        actions_taken.append(f"신청 #{request.id} 접수 완료")

        if decision == "approve":
            access_service.approve_request(db, request.id)
            actions_taken.append(f"신청 #{request.id} 자동 승인 완료")
            actions_taken.append("신청자에게 승인 알림 발송")

        elif decision == "reject":
            access_service.reject_request(db, request.id)
            actions_taken.append(f"신청 #{request.id} 반려 처리")
            actions_taken.append("신청자에게 반려 사유 알림 발송")

        else:
            actions_taken.append(f"신청 #{request.id} 에스컬레이션 — 관리자 검토 필요")
            actions_taken.append("보안팀/부서장에게 검토 요청 발송")

    except Exception as e:
        db.rollback()
        actions_taken.append(f"실행 오류: {str(e)}")
    finally:
        db.close()

    return {"actions_taken": actions_taken}
