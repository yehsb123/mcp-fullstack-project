# Agent 채팅 API 엔드포인트

import sys
import os
import logging
import traceback as tb

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
sys.path.insert(0, os.path.abspath(PROJECT_ROOT))

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    user_id: int


class ChatResponse(BaseModel):
    decision: str
    reasoning: str
    actions_taken: list[str]


router = APIRouter(prefix="/api/v1", tags=["agent"])


@router.post("/agent/chat", response_model=ChatResponse)
def agent_chat(data: ChatRequest):
    try:
        from agent.graph import run_agent
        result = run_agent(user_message=data.message, user_id=data.user_id)
        return ChatResponse(
            decision=result.get("decision", ""),
            reasoning=result.get("reasoning", ""),
            actions_taken=result.get("actions_taken", []),
        )
    except Exception as e:
        logging.error(f"agent/chat error: {tb.format_exc()}")
        return JSONResponse(status_code=500, content={"detail": str(e)})
