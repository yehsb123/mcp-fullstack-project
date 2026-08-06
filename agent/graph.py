from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.intake import intake_node
from agent.nodes.search_policy import search_policy_node
from agent.nodes.decide import decide_node
from agent.nodes.execute import execute_node
from agent.nodes.log import log_node


def build_graph():
    """Agent 그래프를 만들고 컴파일한다."""

    graph = StateGraph(AgentState)

    graph.add_node("intake", intake_node)
    graph.add_node("search_policy", search_policy_node)
    graph.add_node("decide", decide_node)
    graph.add_node("execute", execute_node)
    graph.add_node("log", log_node)

    graph.set_entry_point("intake")

    def after_intake(state: AgentState):
        if state.get("decision") == "reject":
            return "execute"
        return "search_policy"

    graph.add_conditional_edges("intake", after_intake, {"execute": "execute", "search_policy": "search_policy"})
    graph.add_edge("search_policy", "decide")
    graph.add_edge("decide", "execute")
    graph.add_edge("execute", "log")
    graph.add_edge("log", END)

    return graph.compile()


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
