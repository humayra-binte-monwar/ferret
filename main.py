from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from rag import answer
import ingest

DATA_DIR = Path("data")

app = FastAPI(title="Ferret", description="Document Q&A API with cited sources")


class AskRequest(BaseModel):
    question: str
    top_k: int = 4


class AskResponse(BaseModel):
    answer: str
    sources: list[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        result = answer(request.question, top_k=request.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    DATA_DIR.mkdir(exist_ok=True)
    dest = DATA_DIR / file.filename
    dest.write_bytes(await file.read())

    try:
        documents = ingest.load_pdfs(DATA_DIR)
        texts, metadatas = ingest.chunk_documents(documents)
        ingest.build_index(texts, metadatas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    return {"message": f"Uploaded and indexed '{file.filename}' successfully."}
