from app.services import notification_service


def send_notification(user_id: int, message: str) -> dict:
    """사용자에게 알림을 발송한다 (승인/반려 결과 등)."""
    return notification_service.send_notification(user_id, message)
