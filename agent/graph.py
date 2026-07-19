# LangGraph 워크플로우 정의
# 3주차에 구현

from langgraph.graph import StateGraph, END
from agent.state import AgentState

# --- 멘토 제공: 노드 함수 import (수정하지 마세요) ---
from agent.nodes.intake import intake_node
from agent.nodes.search_policy import search_policy_node
from agent.nodes.decide import decide_node
from agent.nodes.execute import execute_node
from agent.nodes.log import log_node


def build_graph():
    """Agent 그래프를 만들고 컴파일한다."""

    # TODO: 아래 5단계를 구현하세요
    #
    # --- 1단계: 빈 그래프 만들기 ---
    # graph = StateGraph(AgentState)
    #
    # --- 2단계: 노드 5개 등록 ---
    # ★ add_node("이름", 함수) 형태입니다
    # graph.add_node("intake", intake_node)
    # graph.add_node("search_policy", search_policy_node)
    # graph.add_node("decide", decide_node)
    # graph.add_node("execute", execute_node)
    # graph.add_node("log", log_node)
    #
    # --- 3단계: 시작점 설정 ---
    # graph.set_entry_point("intake")
    #
    # --- 4단계: 엣지 연결 (순서대로 연결) ---
    # ★ add_edge("A", "B") = A 끝나면 B 실행
    # graph.add_edge("intake", "search_policy")
    # graph.add_edge("search_policy", "decide")
    # graph.add_edge("decide", "execute")
    # graph.add_edge("execute", "log")
    # graph.add_edge("log", END)
    #
    # --- 5단계: 그래프 컴파일 ---
    # return graph.compile()

    pass


# --- 멘토 제공: Agent 실행 함수 (수정하지 마세요) ---
def run_agent(user_message: str, user_id: int) -> dict:
    """Agent를 실행하고 결과를 반환한다."""
    app = build_graph()
    result = app.invoke({
        "user_message": user_message,
        "user_id": user_id,
        "user_info": {},
        "policy_results": [],
        "decision": "",
        "reasoning": "",
        "actions_taken": [],
    })
    return result
