from fastapi import FastAPI
from backend.app.api.routes import router as api_router
from backend.app.config import startup_db_client

app = FastAPI(
    title="Theme Identification Chatbot",
    description="Upload documents, query with NLP, and synthesize themes from responses.",
    version="1.0.0"
)

# MongoDB Connection Initialization
@app.on_event("startup")
def startup_event():
    startup_db_client()

# Register API Routes
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "🎉 Theme Identification Chatbot API is Live!"}
