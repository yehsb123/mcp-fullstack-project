# MCP Tool: 보안 정책 RAG 검색
# 4주차에 구현

# [4주차 TODO] RAG 검색 Tool 만들기
# ★ 이 Tool은 다른 Tool들과 패턴이 다름!
# ★ services/ 대신 rag/scripts/search.py의 search_policies()를 가져다 씀
# ★ sys.path에 rag/ 경로를 추가해야 import가 됨

import os
import sys

# ★ rag/ 폴더를 import 경로에 추가 (mcp-server/tools/ 에서 rag/까지 가려면 ../../rag)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "rag"))

from scripts.search import search_policies


def search_policy(query: str, n_results: int = 3) -> dict:
    """보안 정책 문서를 검색한다. 자연어 질문을 받아 관련 정책을 RAG로 찾아 반환한다."""

    # --- 1단계: RAG 검색 실행 ---
    # ★ 3주차에 만든 search_policies() 함수를 그대로 재활용
    results = search_policies(query, n_results=n_results)

    # --- 2단계: 결과 정리해서 반환 ---
    # ★ distance는 소수점 4자리로 반올림 (0에 가까울수록 유사)
    return {
        "query": query,
        "count": len(results),
        "policies": [
            {
                "id": r["id"],
                "content": r["content"],
                "distance": round(r["distance"], 4),
            }
            for r in results
        ],
    }
