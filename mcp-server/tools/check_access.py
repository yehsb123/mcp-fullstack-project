# MCP Tool: 현재 권한 조회
# 2주차에 구현

# 이 Tool은 services/access_service.py의 get_user_permissions()를 호출
# TODO: Tool 정의 (이름, 설명, 파라미터)
# TODO: services/ 연동

from app.core.database import SessionLocal
from app.services import access_service


def check_access(user_id: int) -> dict:
    """특정 사용자가 현재 보유한 권한 목록을 조회한다."""
    db = SessionLocal()
    try:
        permissions = access_service.get_user_permissions(db, user_id)
        return {
            "user_id": user_id,
            "permissions": [
                {
                    "id": p.id,
                    "resource_name": p.resource_name,
                    "access_level": p.access_level,
                    "granted_at": p.granted_at.isoformat() if p.granted_at else None,
                    "expires_at": p.expires_at.isoformat() if p.expires_at else None,
                }
                for p in permissions
            ],
        }
    finally:
        db.close()
