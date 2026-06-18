from dotenv import load_dotenv
from groq import Groq
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

load_dotenv()

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "ferret_docs"
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a helpful assistant that answers questions strictly from the provided context.
Rules:
- Answer ONLY using the context below.
- If the answer is not in the context, say "I don't know based on the provided documents."
- Cite which chunk(s) you used by referencing the source file name."""


def get_collection():
    client = PersistentClient(path=CHROMA_DIR)
    return client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction(),
    )


def retrieve(question: str, top_k: int = 4) -> tuple[list[str], list[str]]:
    collection = get_collection()
    results = collection.query(query_texts=[question], n_results=top_k)
    chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    return chunks, sources


def answer(question: str, top_k: int = 4) -> dict:
    chunks, sources = retrieve(question, top_k)

    context = "\n\n".join(
        f"[Source: {src}]\n{chunk}" for src, chunk in zip(sources, chunks)
    )
    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    client = Groq()
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    answer_text = resp.choices[0].message.content
    source_excerpts = [
        {"source": src, "excerpt": chunk[:200]}
        for src, chunk in zip(sources, chunks)
    ]

    return {"answer": answer_text, "sources": source_excerpts}


if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is this document about?"
    print(f"Question: {question}\n")
    result = answer(question)
    print(f"Answer:\n{result['answer']}\n")
    print("Sources:")
    for s in result["sources"]:
        print(f"  [{s['source']}] {s['excerpt']}...")
