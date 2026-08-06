import os
import chromadb

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name="access_policies")


def search_policies(query: str, n_results: int = 3) -> list[dict]:
    """질문과 관련된 보안 정책 문서를 검색한다."""

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    if not results["ids"] or not results["ids"][0]:
        return []

    output = []
    for doc_id, content, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["distances"][0],
    ):
        output.append({"id": doc_id, "content": content, "distance": distance})
    return output


if __name__ == "__main__":
    query = "마케팅 대시보드 read 권한"
    print(f"\n검색어: {query}\n")
    results = search_policies(query)
    if results:
        for r in results:
            print(f"  {r['id']} (거리: {r['distance']:.4f})")
            print(f"  {r['content'][:80]}...\n")
    else:
        print("  검색 결과 없음 (ingest.py를 먼저 실행하세요)")
