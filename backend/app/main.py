# AccessGuard - FastAPI 백엔드 엔트리포인트
# 1주차에 구현 시작

import sys
import os

# 3주차: 프로젝트 루트를 Python 경로에 추가 (agent/, rag/ import용)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.db.models import user, access_request, permission,audit_log  # 모델 등록(테이블 생성에 필요)

# TODO (3주차): audit_log 모델도 import 하세요 — 테이블 자동 생성에 필요합니다

from app.api import access_requests

# TODO (3주차): agent 라우터도 import 하세요
from app.api import agent  # agent.py 안의 router 가져오기

# 테이블 생성 — DB에 실제 표 생성함
Base.metadata.create_all(bind=engine)

# FastAPI 앱(서버) 생성
app = FastAPI(title="AccessGuard API")

# CORS 설정 — 프론트(3000)가 백엔드(8000)에 접근하도록 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],                       # 모든 방식 허용
    allow_headers=["*"],
)

# 라우터 등록 — api 파일의 주소들을 앱에 연결
app.include_router(access_requests.router)

# TODO (3주차): agent 라우터도 등록하세요
app.include_router(agent.router)   # /api/v1/agent/chat 엔드포인트를 앱에 연결

# 접속 확인용 기본 경로
@app.get("/")
def root():
    return {"message": "AccessGuard API 실행 중"}
