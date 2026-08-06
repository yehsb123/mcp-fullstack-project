import os
import chromadb

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(
    name="access_policies",
    metadata={"hnsw:space": "cosine"},
)


def ingest_documents():
    """rag/docs/ 폴더의 .md 파일을 읽어서 ChromaDB에 저장한다."""

    md_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]

    documents = []
    ids = []

    for filename in md_files:
        file_path = os.path.join(DOCS_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        documents.append(content)
        ids.append(filename)

    collection.upsert(documents=documents, ids=ids)

    print(f"총 {len(documents)}개 문서 임베딩 완료!")
    for doc_id in ids:
        print(f"  - {doc_id}")


if __name__ == "__main__":
    ingest_documents()
