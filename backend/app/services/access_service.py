# 권한 신청 비즈니스 로직 (서비스 레이어)
# MCP Tool과 API 엔드포인트 모두 이 서비스를 호출

# TODO: create_request() - 권한 신청 생성
# TODO: get_requests() - 신청 목록 조회
# TODO: get_request_by_id() - 신청 상세 조회
# TODO: approve_request() - 승인 처리
# TODO: reject_request() - 반려 처리
# TODO: get_user_permissions() - 사용자 현재 권한 조회


from sqlalchemy.orm import Session
from app.db.models.access_request import AccessRequest
from app.schemas.access_request import AccessRequestCreate
from app.db.models.permission import Permission 


# 권한 신청 생성 
def create_request(db: Session, data: AccessRequestCreate):
    new_request = AccessRequest(          # 모델(설계도)로 새 신청 만들기
        user_id=data.user_id,             # 스키마로 들어온 데이터를 넣음
        resource_name=data.resource_name,
        access_level=data.access_level,
        reason=data.reason,
    )
    db.add(new_request)      # 장바구니에 담기
    db.commit()              # 저장 확정 
    db.refresh(new_request)  # 저장된 최신 정보(id 등)로 갱신
    return new_request       # 결과 돌려줌

# 신청 목록 조회 
def get_requests(db: Session):
    return db.query(AccessRequest).all()   # access_requests 표 전체 가져오기

# 신청 상세 조회 
def get_request_by_id(db: Session, request_id: int):
    return db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    # id가 일치하는 것 하나만 가져오기

# 승인 처리 
def approve_request(db: Session, request_id: int):
    request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if request is None:          # 없는 신청이면 None 반환
        return None
    request.status = "approved"  # 상태를 승인으로 변경

    # 승인됐으니까 실제 권한(permissions)도 부여
    new_permission = Permission(
        user_id=request.user_id,
        resource_name=request.resource_name,
        access_level=request.access_level,
    )
    db.add(new_permission)
    db.commit()
    db.refresh(request)
    return request

# 반려 처리 
def reject_request(db: Session, request_id: int):
    request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if request is None:
        return None
    request.status = "rejected"  # 상태를 반려로 변경
    db.commit()
    db.refresh(request)
    return request

# 사용자 현재 권한 조회 
def get_user_permissions(db: Session, user_id: int):
    return db.query(Permission).filter(Permission.user_id == user_id).all()
    # 그 사용자의 권한 전부 가져오기
