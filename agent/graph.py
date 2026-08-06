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

    # --- 1단계: 빈 그래프 만들기 ---
    graph = StateGraph(AgentState) #AgentState 모양을 주고받는 빈 그래프 생성

    # --- 2단계: 노드 5개 등록 ---
    # ★ add_node("이름", 함수) 형태입니다, 노드 다섯 개 등록
    graph.add_node("intake", intake_node)
    graph.add_node("search_policy", search_policy_node)
    graph.add_node("decide", decide_node)
    graph.add_node("execute", execute_node)
    graph.add_node("log", log_node)

    # --- 3단계: 시작점(intake) 설정 ---
    graph.set_entry_point("intake")

    # --- 4단계: 엣지 연결 (조건부 엣지 포함) ---
    # ★ add_edge("A", "B") = A 끝나면 B 실행
    # ★ add_conditional_edges = 조건에 따라 다른 노드로 분기
    def after_intake(state: AgentState):
        if state.get("decision") == "reject":
            return "execute"
        return "search_policy"

    graph.add_conditional_edges("intake", after_intake, {"execute": "execute", "search_policy": "search_policy"})
    graph.add_edge("search_policy", "decide") #search_policy 끝나면 decide로
    graph.add_edge("decide", "execute")
    graph.add_edge("execute", "log")
    graph.add_edge("log", END)

    # --- 5단계: 그래프 컴파일 ---
    return graph.compile()


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
