# AccessGuard - FastAPI 백엔드 엔트리포인트
# 1주차에 구현 시작

# TODO: FastAPI 앱 생성
# TODO: 라우터 등록
# TODO: CORS 미들웨어 설정
# TODO: DB 연결 설정

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.db.models import user, access_request, permission  # 모델 등록(테이블 생성에 필요)
from app.api import access_requests

# 테이블 생성 — DB에 실제 표 생성함 
Base.metadata.create_all(bind=engine)

# FastAPI 앱(서버) 생성
app = FastAPI(title="AccessGuard API")

# CORS 설정 — 프론트(3000)가 백엔드(8000)에 접근하도록 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 허용할 프론트 주소
    allow_credentials=True,
    allow_methods=["*"],                       # 모든 방식 허용
    allow_headers=["*"],
)

# 라우터 등록 — api 파일의 주소들을 앱에 연결
app.include_router(access_requests.router)

# 접속 확인용 기본 경로
@app.get("/")
def root():
    return {"message": "AccessGuard API 실행 중"}
