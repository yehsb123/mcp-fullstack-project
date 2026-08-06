# MCP Tool: 알림 발송
# 2주차에 구현

# 이 Tool은 services/notification_service.py의 send_notification()을 호출
# TODO: Tool 정의 (이름, 설명, 파라미터)
# TODO: services/ 연동

from app.services import notification_service


def send_notification(user_id: int, message: str) -> dict:
    """사용자에게 알림을 발송한다 (승인/반려 결과 등)."""
    return notification_service.send_notification(user_id, message)
