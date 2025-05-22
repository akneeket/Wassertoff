from app.core.embedding import GeminiEmbeddingClient

client = GeminiEmbeddingClient()

def get_embedding(text: str) -> list:
    """
    Wrapper around GeminiEmbeddingClient to match route expectations.
    """
    embedding = client.get_embedding(text)
    if embedding is None:
        raise ValueError("Failed to retrieve embedding.")
    return embedding
