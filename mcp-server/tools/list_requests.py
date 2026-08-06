# MCP Tool: 신청 목록 조회
# 4주차에 구현

# [4주차 TODO] 신청 목록 조회 Tool 만들기
# ★ 기존 request_access.py 패턴을 참고해서 만들기
# ★ 추가 기능: status 파라미터로 필터링 (pending/approved/rejected)

from app.core.database import SessionLocal
from app.services import access_service


def list_requests(status: str = "") -> dict:
    """권한 신청 목록을 조회한다. status를 지정하면 해당 상태만 필터링한다 (pending/approved/rejected)."""
    db = SessionLocal()
    try:
        # --- 1단계: 전체 신청 목록 가져오기 ---
        all_requests = access_service.get_requests(db)

        # --- 2단계: status 필터링 (파라미터가 있으면) ---
        # ★ 리스트 컴프리헨션으로 조건에 맞는 것만 골라내기
        if status:
            all_requests = [r for r in all_requests if r.status == status]

        # --- 3단계: dict로 변환해서 반환 ---
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
