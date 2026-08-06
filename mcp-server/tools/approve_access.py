from app.core.database import SessionLocal
from app.services import access_service


def approve_access(request_id: int, decision: str) -> dict:
    """권한 신청을 승인하거나 반려한다. decision은 'approved' 또는 'rejected' 중 하나."""
    db = SessionLocal()
    try:
        if decision == "approved":
            result = access_service.approve_request(db, request_id)
        elif decision == "rejected":
            result = access_service.reject_request(db, request_id)
        else:
            return {"error": f"invalid decision: {decision} (use 'approved' or 'rejected')"}

        if result is None:
            return {"error": f"request_id {request_id} not found"}

        return {
            "id": result.id,
            "user_id": result.user_id,
            "resource_name": result.resource_name,
            "access_level": result.access_level,
            "status": result.status,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
