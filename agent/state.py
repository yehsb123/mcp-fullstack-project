# LangGraph Agent 상태 정의
# 3주차에 구현

from typing import TypedDict


class AgentState(TypedDict):
    """Agent 노드들이 공유하는 상태 객체.
    각 노드는 자기 담당 필드만 채우고, 다음 노드가 읽어서 쓴다."""

    user_message: str
    user_id: int
    user_info: dict
    policy_results: list[str]
    decision: str
    reasoning: str
    actions_taken: list[str]
