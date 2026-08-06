# LangGraph Agent 상태 정의
# 3주차에 구현

from typing import TypedDict


class AgentState(TypedDict):
    """Agent 노드들이 공유하는 상태 객체.
    각 노드는 자기 담당 필드만 채우고, 다음 노드가 읽어서 쓴다."""

    # TODO: 아래 7개 필드를 정의하세요
    # ★ TypedDict 필드 정의법: 필드이름: 타입

    user_message: str        # 사용자가 채팅으로 입력한 메시지
    user_id: int              # 신청자 ID
    user_info: dict           # 신청자 정보(intake 노드가 조회해서 채우는)
    policy_results: list[str] #  관련 정책 문서(search_policy 노드가 RAG로 찾아온)
    decision: str              # decide 노드가 내린 판단 결과 (승인/반려/에스컬레이션)
    reasoning: str             # decide 노드가 왜 그렇게 판단했는지 판단 근거
    actions_taken: list[str]  # 실행 결과 (execute 노드가 실제로 실행한 MCP Tools들 기록)
