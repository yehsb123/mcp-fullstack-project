# 신청 접수 노드 — Agent 파이프라인 1번째 단계
# 3주차에 구현
# ★ 참고: MCP Tool의 check_access.py와 비슷한 패턴 (DB 세션 직접 관리)

from agent.state import AgentState
from app.core.database import SessionLocal
from app.services import access_service
from app.db.models.user import User


def intake_node(state: AgentState) -> dict:
    """사용자 정보와 현재 권한을 조회해서 state에 저장한다."""

    # TODO: 아래 단계를 구현하세요
    
    # --- 1단계: DB 세션 열기 ---
    db = SessionLocal() #MCP tool때랑 동일 패턴 
    #
    # --- 2단계: 사용자 정보 조회 ---
    user_id = state["user_id"] #state 서류철에서 신청자 id 꺼내기 
    user = db.query(User).filter(User.id == user_id).first() #users 표에서 그 사람 조회 

    # ★ 이 패턴은 access_service.py의 get_request_by_id()와 동일합니다
    
    # --- 3단계: 현재 권한 조회 ---
    permissions = access_service.get_user_permissions(db, user_id) #그 사람의 현재 권한들 조회 
    
    # --- 4단계: DB 세션 닫기 ---
    db.close()
    
    # --- 5단계: user_info 딕셔너리 만들어서 반환 ---
    user_info = {
        "name": user.name if user else "알 수 없음",
        "department": user.department if user else "알 수 없음",
        "role": user.role if user else "알 수 없음",
        "permissions": [
            {"resource": p.resource_name, "level": p.access_level}
            for p in permissions
        ],
    }
    return {"user_info": user_info}
    
    # ★ 주의: return은 dict로! state 전체가 아니라 업데이트할 필드만 반환


