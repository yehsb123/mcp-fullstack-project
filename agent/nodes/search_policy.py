# 정책 검색 노드 — Agent 파이프라인 2번째 단계
# 3주차에 구현

from agent.state import AgentState
from rag.scripts.search import search_policies


def search_policy_node(state: AgentState) -> dict:
    """신청 내용으로 관련 보안 정책을 검색해서 state에 저장한다."""

    query = state["user_message"]
    results = search_policies(query, n_results=3)
    policy_texts = [r["content"] for r in results] if results else []
    return {"policy_results": policy_texts}

