from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

DATA_DIR = Path("data")
CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "ferret_docs"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def load_pdfs(data_dir: Path) -> list[dict]:
    documents = []
    for pdf_path in data_dir.glob("*.pdf"):
        reader = PdfReader(pdf_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        documents.append({"source": pdf_path.name, "text": text})
        print(f"Loaded: {pdf_path.name} ({len(reader.pages)} pages)")
    return documents


def chunk_documents(documents: list[dict]) -> tuple[list[str], list[dict]]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    texts, metadatas = [], []
    for doc in documents:
        chunks = splitter.split_text(doc["text"])
        texts.extend(chunks)
        metadatas.extend({"source": doc["source"]} for _ in chunks)
        print(f"  → {len(chunks)} chunks from {doc['source']}")
    return texts, metadatas


def build_index(texts: list[str], metadatas: list[dict]) -> None:
    client = PersistentClient(path=str(CHROMA_DIR))

    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction(),
    )
    ids = [str(i) for i in range(len(texts))]
    collection.add(documents=texts, metadatas=metadatas, ids=ids)
    print(f"\nStored {len(texts)} chunks in ChromaDB.")
    return collection


def sanity_check(collection) -> None:
    test_query = "What is this document about?"
    results = collection.query(query_texts=[test_query], n_results=3)
    print("\n--- Sanity check: top 3 chunks for test query ---")
    for i, (doc, meta) in enumerate(
        zip(results["documents"][0], results["metadatas"][0])
    ):
        print(f"\n[{i+1}] Source: {meta['source']}")
        print(doc[:300])


if __name__ == "__main__":
    if not DATA_DIR.exists() or not any(DATA_DIR.glob("*.pdf")):
        print(f"No PDFs found in ./{DATA_DIR}/.")
        raise SystemExit(1)

    print("=== Ferret Ingestion Pipeline ===\n")
    documents = load_pdfs(DATA_DIR)
    texts, metadatas = chunk_documents(documents)
    collection = build_index(texts, metadatas)
    sanity_check(collection)
    print("\nIngestion complete. Run main.py to start the API.")
