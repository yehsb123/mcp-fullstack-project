# 정책 검색 노드 — Agent 파이프라인 2번째 단계
# 3주차에 구현

from agent.state import AgentState
from rag.scripts.search import search_policies


def search_policy_node(state: AgentState) -> dict:
    """신청 내용으로 관련 보안 정책을 검색해서 state에 저장한다."""

    # TODO: 아래 단계를 구현하세요

    # --- 1단계: state에서 사용자 메시지 가져오기 ---
    query = state["user_message"]

    # --- 2단계: RAG 검색 실행 ---
    results = search_policies(query, n_results=3)
    # ★ search_policies()는 rag/scripts/search.py에서 내가 만든 함수임

    # --- 3단계: 검색 결과에서 문서 내용만 뽑기 ---
    policy_texts = [r["content"] for r in results] if results else [] #없으면 빈 리스트

    # --- 4단계: 반환 ---
    return {"policy_results": policy_texts} #이 필드만 state에 반영

