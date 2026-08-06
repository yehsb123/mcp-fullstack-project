from sqlalchemy.orm import Session
from app.db.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    request_id: int,
    action: str,
    decision: str,
    reasoning: str,
    policy_referenced: str,
    decided_by: str = "agent",
) -> AuditLog:
    # TODO: AuditLog 객체를 만들고 DB에 저장하세요
    # ★ access_service.py의 create_request()를 열어서 똑같이 따라하기.

    new_log = AuditLog(  #AuditLog 모양의 파이썬 객체 하나 생성..아직 db에는 없음
        request_id=request_id, #어떤 신청 건에 대한 기록인지
        action=action, #어떤 행동(ex)자동 승인)
        decision=decision, #최종 결론
        reasoning=reasoning, #판단 근거
        policy_referenced=policy_referenced, #참고한 정책 문서
        decided_by=decided_by, #판단 주체
    )
    db.add(new_log) #세션에 저장 예약
    db.commit() #실제 db에 insert 실행
    db.refresh(new_log) #db가 채운 id, created_at 값 다시 가져옴
    return new_log #완성된 객체 반환
