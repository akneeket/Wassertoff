import requests

# === Hardcoded Gemini API details ===
GOOGLE_API_KEY = "your_google_api_key_here"
GOOGLE_GEMINI_ENDPOINT = "https://your-vertex-ai-endpoint-url/v1/models/embedding-001:predict"

class GeminiEmbeddingClient:
    def __init__(self):
        self.api_key = GOOGLE_API_KEY
        self.endpoint = GOOGLE_GEMINI_ENDPOINT
        if not self.api_key or not self.endpoint:
            raise ValueError("Google API Key and Endpoint must be set.")

    def get_embedding(self, text: str):
        """
        Get embedding vector for input text using Google Gemini API.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "instances": [
                {"content": text}
            ]
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            embedding = result["predictions"][0]["embedding"]
            return embedding
        except Exception as e:
            print(f"Error fetching embedding from Gemini: {e}")
            return None
