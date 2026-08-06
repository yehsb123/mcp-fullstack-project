# 판단 노드 — Agent 파이프라인 3번째 단계
# 3주차 — 멘토 제공 (LLM 호출 로직)

import os
import json
from dotenv import load_dotenv
from agent.state import AgentState
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "backend", ".env")
load_dotenv(_env_path)

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "system_prompt.md")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


def decide_node(state: AgentState) -> dict:
    """정책 기반으로 LLM이 승인/반려/에스컬레이션을 판단한다."""

    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=1024,
    )

    user_info = state.get("user_info", {})
    policies = state.get("policy_results", [])
    user_message = state.get("user_message", "")

    policies_text = "\n\n---\n\n".join(policies) if policies else "관련 정책을 찾지 못했습니다."

    human_message = f"""## 신청 정보
- 신청자: {user_info.get('name', '알 수 없음')}
- 부서: {user_info.get('department', '알 수 없음')}
- 역할: {user_info.get('role', '알 수 없음')}
- 현재 권한: {json.dumps(user_info.get('permissions', []), ensure_ascii=False)}
- 신청 내용: {user_message}

## 관련 보안 정책
{policies_text}

위 정보를 바탕으로 이 권한 신청을 심사해주세요. JSON으로만 응답하세요."""

    try:
        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=human_message),
        ])
    except Exception as e:
        return {
            "decision": "escalate",
            "reasoning": f"AI 판단 서비스 오류 — 관리자 수동 검토 필요 ({type(e).__name__})",
        }

    try:
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        result = json.loads(content.strip())
        decision = result.get("decision", "escalate")
        reasoning = result.get("reasoning", "판단 근거 파싱 실패")
    except (json.JSONDecodeError, AttributeError, IndexError):
        decision = "escalate"
        reasoning = "LLM 응답 파싱 실패, 안전을 위해 에스컬레이션"

    return {"decision": decision, "reasoning": reasoning}
