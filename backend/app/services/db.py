import faiss
import numpy as np
import pickle
import os

# Paths for storing FAISS index and document metadata
FAISS_INDEX_PATH = "backend/data/faiss_index.bin"
METADATA_PATH = "backend/data/faiss_metadata.pkl"

# Update this based on the actual embedding size from Gemini
EMBEDDING_DIM = 768

# Load existing FAISS index and metadata if present
if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(METADATA_PATH):
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)
else:
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    metadata = []

def save_faiss_state():
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

def save_document(doc: dict):
    """
    Save document metadata locally and return a unique string ID.
    """
    doc_id = str(len(metadata))
    # Store the chunk as an independent doc, with filename and chunk text
    metadata.append({
        "id": doc_id,
        "filename": doc.get("filename"),
        "text": doc.get("text"),
        "upload_time": doc.get("upload_time"),
        "used_ocr": doc.get("used_ocr"),
    })
    save_faiss_state()
    return doc_id

def index_document_embedding(doc_id: str, embedding: list):
    """
    Add an embedding vector to the FAISS index.
    """
    try:
        embedding_np = np.array(embedding).astype('float32').reshape(1, -1)
        index.add(embedding_np)
        save_faiss_state()
    except Exception as e:
        print(f"Error indexing embedding for doc_id={doc_id}: {e}")

def search_similar_documents(query_embedding: list, top_k: int = 5):
    """
    Return top_k most similar documents based on FAISS vector similarity.
    """
    query_np = np.array(query_embedding).astype('float32').reshape(1, -1)
    distances, indices = index.search(query_np, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1 or idx >= len(metadata):
            continue
        doc_meta = metadata[idx]
        results.append({
            "id": doc_meta["id"],
            "filename": doc_meta["filename"],
            "snippet": doc_meta["text"][:200] + "...",
            "score": round(float(dist), 4)
        })
    return results

def get_document_by_id(doc_id: str):
    for doc in metadata:
        if doc["id"] == doc_id:
            return doc
    return None
