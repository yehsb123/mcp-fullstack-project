# RAG 문서 임베딩 + ChromaDB 저장 스크립트
# 3주차에 구현
# 실행법: 프로젝트 루트에서 → python rag/scripts/ingest.py

import os
import chromadb

# --- 멘토 제공: ChromaDB 설정 (수정하지 마세요) ---
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(
    name="access_policies",
    metadata={"hnsw:space": "cosine"},
)


def ingest_documents():
    """rag/docs/ 폴더의 .md 파일을 읽어서 ChromaDB에 저장한다."""

    # TODO: 아래 4단계를 구현하세요
    
    
    # --- 1단계: .md 파일 목록 가져오기 ---
    md_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]  # docs 폴더에서 .md 파일명만 골라내기

    # --- 2단계: 각 파일 내용 읽어서 리스트에 담기 ---
    documents = []  # 각 파일의 실제 텍스트 내용을 담을 리스트
    ids = []        # 각 문서를 구분할 고유 id (파일명으로 씀)

    for filename in md_files:
        file_path = os.path.join(DOCS_DIR, filename)   # 파일 전체 경로 조립
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()      # 파일 내용을 문자열로 읽기
        documents.append(content)   # 읽은 내용을 리스트에 추가
        ids.append(filename)        # 파일명을 id로 추가

    # --- 3단계: ChromaDB에 저장 ---
    collection.upsert(documents=documents, ids=ids)  # ChromaDB에 저장 (내부적으로 임베딩 자동 처리)

    # --- 4단계: 결과 출력 ---
    print(f"총 {len(documents)}개 문서 임베딩 완료!")
    for doc_id in ids:
        print(f"  - {doc_id}")


if __name__ == "__main__":
    ingest_documents()
