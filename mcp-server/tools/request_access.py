# MCP Tool: 권한 신청 접수
# 2주차에 구현

# 이 Tool은 services/access_service.py의 create_request()를 호출
# TODO: Tool 정의 (이름, 설명, 파라미터)
# TODO: services/ 연동

from app.core.database import SessionLocal
from app.schemas.access_request import AccessRequestCreate
from app.services import access_service


def request_access(user_id: int, resource_name: str, access_level: str, reason: str) -> dict:
    """권한 신청을 접수한다. 사용자가 특정 리소스에 대한 접근 권한을 요청할 때 사용한다."""
    db = SessionLocal()
    try:
        data = AccessRequestCreate(
            user_id=user_id,
            resource_name=resource_name,
            access_level=access_level,
            reason=reason,
        )
        result = access_service.create_request(db, data)
        return {
            "id": result.id,
            "user_id": result.user_id,
            "resource_name": result.resource_name,
            "access_level": result.access_level,
            "status": result.status,
            "reason": result.reason,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
