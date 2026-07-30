# RAG 검색 스크립트
# 3주차에 구현

import os
import chromadb

# --- 멘토 제공: ChromaDB 연결 (수정하지 마세요) ---
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name="access_policies")


def search_policies(query: str, n_results: int = 3) -> list[dict]:
    """질문과 관련된 보안 정책 문서를 검색한다."""

    # TODO: ChromaDB에서 검색하고 결과를 반환하세요
    #
    # --- 1단계: 검색 실행 ---
    results = collection.query(         # ChromaDB에 검색 요청
        query_texts=[query],            # 질문 (리스트로 감싸야 함, 여러 개 질문 가능한 구조라서)
        n_results=n_results,            # 몇 개까지 받아올지
    )
    #
    # --- 2단계: 결과가 비어있으면 빈 리스트 반환 ---
    if not results["ids"] or not results["ids"][0]:
        return []
    #
    # --- 3단계: 결과 정리해서 반환 ---
    # ★ results 구조:
    # {
    #     "ids": [["파일1.md", "파일2.md"]],       ← [0]으로 꺼내야 함!
    #     "documents": [["내용1", "내용2"]],        ← [0]으로 꺼내야 함!
    #     "distances": [[0.11, 0.25]],             ← [0]으로 꺼내야 함!
    # }
    #
    output = []
    for doc_id, content, distance in zip(     # id, 내용, 거리(유사도)를 한 쌍씩 묶어서
        results["ids"][0],                    # [0] = 첫 번째(유일한) 질문의 결과 꺼내기
        results["documents"][0],
        results["distances"][0],
    ):
        output.append({"id": doc_id, "content": content, "distance": distance})  # 보기 편한 dict로 정리
    return output


# --- 테스트용: 직접 실행해서 검색 확인 완료 ---
if __name__ == "__main__":
    query = "마케팅 대시보드 read 권한"
    print(f"\n검색어: {query}\n")
    results = search_policies(query)
    if results:
        for r in results:
            print(f"  {r['id']} (거리: {r['distance']:.4f})")  #0에 가까울수록 좋음!
            print(f"  {r['content'][:80]}...\n")
    else:
        print("  검색 결과 없음 (ingest.py를 먼저 실행하세요)")
