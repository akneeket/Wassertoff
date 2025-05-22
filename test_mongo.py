import streamlit as st
import requests
import os

API_URL = "http://localhost:8000/api"  # Adjust if your FastAPI backend runs on a different host/port

st.title("Document Upload & Search")

st.header("Upload Documents (PDF or images)")

uploaded_files = st.file_uploader(
    "Choose files", type=["pdf", "png", "jpg", "jpeg", "tiff", "bmp"], accept_multiple_files=True
)

if st.button("Upload"):
    if not uploaded_files:
        st.warning("Please upload at least one file.")
    else:
        with st.spinner("Uploading files..."):
            files_payload = []
            for f in uploaded_files:
                files_payload.append(
                    ("files", (f.name, f.read(), f.type))
                )
            try:
                response = requests.post(f"{API_URL}/upload", files=files_payload)
                response.raise_for_status()
                data = response.json()
                st.success(data.get("message", "Upload successful!"))
                for doc in data.get("documents", []):
                    st.write(f"- {doc['filename']} (ID: {doc['id']})")
            except Exception as e:
                st.error(f"Upload failed: {e}")

st.header("Search Documents")

query = st.text_input("Enter search query:")
top_k = st.number_input("Number of results to return:", min_value=1, max_value=20, value=5, step=1)

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        try:
            resp = requests.post(f"{API_URL}/query", json={"query": query, "top_k": top_k})
            resp.raise_for_status()
            results = resp.json().get("results", [])
            if not results:
                st.info("No similar documents found.")
            else:
                st.subheader("Search Results")
                for res in results:
                    st.markdown(f"**Filename:** {res['filename']}")
                    st.markdown(f"**Score:** {res['score']}")
                    st.markdown(f"**Snippet:** {res['snippet']}")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Search failed: {e}")
