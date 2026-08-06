import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "rag"))

from scripts.search import search_policies


def search_policy(query: str, n_results: int = 3) -> dict:
    """보안 정책 문서를 검색한다. 자연어 질문을 받아 관련 정책을 RAG로 찾아 반환한다."""
    results = search_policies(query, n_results=n_results)
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
