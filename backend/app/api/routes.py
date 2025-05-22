import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from datetime import datetime
from app.services import processing
from app.core import db
from app.core.embedding_utils import get_embedding
from pydantic import BaseModel

router = APIRouter(
    prefix="/api",
    tags=["Theme Identifier API"]
)

UPLOAD_DIR = "backend/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def chunk_text(text: str, max_words: int = 500) -> List[str]:
    """
    Split text into chunks of max_words words.
    """
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    uploaded_docs = []
    for file in files:
        filename = file.filename
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        if filename.lower().endswith(".pdf"):
            text, used_ocr = processing.extract_text_from_pdf(file_path)
        elif filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
            text = processing.extract_text_from_image(file_path)
            used_ocr = True
        else:
            os.remove(file_path)
            continue

        if not text.strip():
            os.remove(file_path)
            continue

        # Chunk the text
        chunks = chunk_text(text, max_words=500)

        chunk_ids = []
        for chunk in chunks:
            embedding_vector = get_embedding(chunk)
            if embedding_vector is None:
                continue

            doc_entry = {
                "filename": filename,
                "upload_time": datetime.utcnow(),
                "text": chunk,
                "used_ocr": used_ocr,
            }

            inserted_id = db.save_document(doc_entry)
            db.index_document_embedding(inserted_id, embedding_vector)
            chunk_ids.append(inserted_id)

        if not chunk_ids:
            os.remove(file_path)
            continue

        uploaded_docs.append({"filename": filename, "chunks_indexed": len(chunk_ids)})

    if not uploaded_docs:
        raise HTTPException(status_code=400, detail="No valid files uploaded")

    return {
        "message": f"{len(uploaded_docs)} document(s) uploaded and processed with chunking successfully.",
        "documents": uploaded_docs
    }


# =======================
# Query Endpoint
# =======================

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/query")
async def query_similar_documents(query_request: QueryRequest):
    query = query_request.query
    top_k = query_request.top_k

    if not query.strip():
        raise HTTPException(status_code=400, detail="Empty query provided.")

    query_embedding = get_embedding(query)
    if query_embedding is None:
        raise HTTPException(status_code=500, detail="Failed to generate query embedding.")

    results = db.search_similar_documents(query_embedding, top_k=top_k)

    if not results:
        return {"message": "No similar documents found."}

    return {
        "query": query,
        "top_k": top_k,
        "results": [
            {
                "id": doc["id"],
                "filename": doc["filename"],
                "score": doc["score"],
                "snippet": doc["snippet"],
            }
            for doc in results
        ]
    }
