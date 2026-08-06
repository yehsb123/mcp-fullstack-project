from agent.state import AgentState
from app.core.database import SessionLocal
from app.services import access_service
from app.db.models.user import User


def intake_node(state: AgentState) -> dict:
    """사용자 정보와 현재 권한을 조회해서 state에 저장한다."""

    db = SessionLocal()

    user_id = state["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    permissions = access_service.get_user_permissions(db, user_id)

    db.close()

    if user is None:
        return {
            "user_info": {},
            "decision": "reject",
            "reasoning": "등록되지 않은 사용자입니다. (user_id 확인 필요)",
        }

    user_info = {
        "name": user.name,
        "department": user.department,
        "role": user.role,
        "permissions": [
            {"resource": p.resource_name, "level": p.access_level}
            for p in permissions
        ],
    }
    return {"user_info": user_info}
