from app.core.database import SessionLocal
from app.services import access_service


def list_requests(status: str = "") -> dict:
    """권한 신청 목록을 조회한다. status를 지정하면 해당 상태만 필터링한다 (pending/approved/rejected)."""
    db = SessionLocal()
    try:
        all_requests = access_service.get_requests(db)
        if status:
            all_requests = [r for r in all_requests if r.status == status]
        return {
            "count": len(all_requests),
            "requests": [
                {
                    "id": r.id,
                    "user_id": r.user_id,
                    "resource_name": r.resource_name,
                    "access_level": r.access_level,
                    "status": r.status,
                    "reason": r.reason,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in all_requests
            ],
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
