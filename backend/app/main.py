# AccessGuard - FastAPI 백엔드 엔트리포인트

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.db.models import user, access_request, permission, audit_log

from app.api import access_requests
from app.api import agent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AccessGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(access_requests.router)
app.include_router(agent.router)


@app.get("/")
def root():
    return {"message": "AccessGuard API 실행 중"}
