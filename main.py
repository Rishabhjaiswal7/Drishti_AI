from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import RAGEngine

app = FastAPI(title="DRISHTI-AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load RAG on startup
print("🚀 Starting DRISHTI-AI...")
rag = RAGEngine()

class QueryRequest(BaseModel):
    question: str
    speak_response: bool = False

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "DRISHTI-AI is active",
        "version": "1.0"
    }

@app.post("/ask")
def ask_question(req: QueryRequest):
    answer = rag.ask(req.question)
    return {
        "question": req.question,
        "answer": answer,
        "status": "success"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}