# Agent 채팅 API 엔드포인트
# 3주차에 구현
# ★ 참고: access_requests.py와 동일한 라우터 패턴입니다!

import sys
import os

# --- 멘토 제공: 프로젝트 루트 경로 추가 (수정하지 마세요) ---
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
sys.path.insert(0, os.path.abspath(PROJECT_ROOT))

from fastapi import APIRouter
from pydantic import BaseModel


# --- 멘토 제공: 요청/응답 스키마 ---
class ChatRequest(BaseModel):
    message: str
    user_id: int


class ChatResponse(BaseModel):
    decision: str
    reasoning: str
    actions_taken: list[str]


# --- 멘토 제공: 라우터 ---
router = APIRouter(prefix="/api/v1", tags=["agent"])


# TODO: POST /agent/chat 엔드포인트를 만드세요
# ★ access_requests.py의 create_access_request() 함수를 참고하세요
#
# @router.post("/agent/chat", response_model=ChatResponse)
# def agent_chat(data: ChatRequest):
#     # 1단계: Agent 실행
#     from agent.graph import run_agent
#     result = run_agent(user_message=data.message, user_id=data.user_id)
#
#     # 2단계: 결과 반환
#     return ChatResponse(
#         decision=result.get("decision", ""),
#         reasoning=result.get("reasoning", ""),
#         actions_taken=result.get("actions_taken", []),
#     )
