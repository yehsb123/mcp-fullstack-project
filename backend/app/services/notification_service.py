# 알림 발송 서비스
# 2주차에 구현

# TODO: send_notification() - 승인자/신청자에게 알림

# 알림 발송 (지금은 콘솔 출력으로 대체, 추후 이메일/슬랙 등으로 확장 가능)
def send_notification(user_id: int, message: str) -> dict:
    print(f"[NOTIFICATION] to user_id={user_id}: {message}")
    return {"user_id": user_id, "message": message, "status": "sent"}
