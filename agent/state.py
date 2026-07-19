# LangGraph Agent 상태 정의
# 3주차에 구현

from typing import TypedDict


class AgentState(TypedDict):
    """Agent 노드들이 공유하는 상태 객체.
    각 노드는 자기 담당 필드만 채우고, 다음 노드가 읽어서 쓴다."""

    # TODO: 아래 7개 필드를 정의하세요
    # ★ TypedDict 필드 정의법: 필드이름: 타입
    #
    # 1. user_message   → str          사용자가 입력한 메시지
    # 2. user_id        → int          신청자 ID
    # 3. user_info      → dict         신청자 정보 (intake 노드가 채움)
    # 4. policy_results → list[str]    관련 정책 문서 (search_policy 노드가 채움)
    # 5. decision       → str          판단 결과 (decide 노드가 채움)
    # 6. reasoning      → str          판단 근거 (decide 노드가 채움)
    # 7. actions_taken  → list[str]    실행 결과 (execute 노드가 채움)
    #
    # 예시:
    #   user_message: str
    #   user_id: int
    #   ...
    pass
