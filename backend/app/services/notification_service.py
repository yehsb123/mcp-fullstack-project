def send_notification(user_id: int, message: str) -> dict:
    print(f"[NOTIFICATION] to user_id={user_id}: {message}")
    return {"user_id": user_id, "message": message, "status": "sent"}
