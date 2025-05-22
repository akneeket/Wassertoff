


# Wassertoff

Wassertoff is a document management and search system that allows users to upload PDFs and images, extract text (with OCR support), generate embeddings, and perform semantic search using FAISS. It includes a FastAPI backend for processing and indexing, along with a Streamlit-based user interface for easy interaction.


## Features

- Upload PDFs and images for text extraction
- Automatic OCR for images and scanned PDFs
- Text chunking for improved embedding and search accuracy
- Generate document embeddings using Gemini API (or any embedding model)
- Index embeddings using FAISS for fast similarity search
- Search for semantically similar documents based on user queries
- Streamlit UI for uploading documents and querying the database

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akneeket/Wassertoff.git
   cd Wassertoff


2. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (if any), e.g. for embedding API keys.**

---

## Running the Project

### Start the backend API server

```bash
uvicorn app.main:app --reload
```

This will start the FastAPI backend at `http://localhost:8000`.

---

### Run the Streamlit UI

```bash
streamlit run app/ui/app.py
```

This will launch a web-based user interface at `http://localhost:8501` where you can upload documents and perform semantic search.

---

## Project Structure

* `app/core/` – Core modules for FAISS indexing and embedding utilities
* `app/services/` – Document processing (text extraction, OCR, chunking)
* `app/routes/` – FastAPI routes for uploading and querying documents
* `app/ui/` – Streamlit user interface files
* `backend/data/` – Storage for uploaded files, FAISS index, and metadata

---

## Usage

* Upload PDF or image files through the UI or API endpoint
* Documents are chunked and indexed with their embeddings
* Search queries return the most similar document chunks with snippets
* Supports OCR extraction for scanned documents and images

---

## Customization

* Adjust embedding dimension and model in `app/core/db.py`
* Modify chunk size and overlap in `app/services/processing.py`
* Update upload folder path and FAISS index path in configuration

---

## Contributing

Contributions and suggestions are welcome! Feel free to open issues or submit pull requests.

---


```
