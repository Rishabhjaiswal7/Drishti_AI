from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_engine import RAGEngine
from lecture_engine import LectureEngine
import os

app = FastAPI(title="DRISHTI-AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount lectures folder so frontend can access audio files
os.makedirs("lectures", exist_ok=True)
app.mount("/lectures", StaticFiles(directory="lectures"), name="lectures")

print("🚀 Starting DRISHTI-AI...")
rag = RAGEngine()
lecture_engine = LectureEngine(rag)

class QueryRequest(BaseModel):
    question: str
    speak_response: bool = False

class LectureRequest(BaseModel):
    topic: str

@app.get("/")
def root():
    return {"status": "running", "message": "DRISHTI-AI is active"}

@app.post("/ask")
def ask_question(req: QueryRequest):
    answer = rag.ask(req.question)
    return {"question": req.question, "answer": answer, "status": "success"}

@app.post("/lecture")
def get_lecture(req: LectureRequest):
    """Generate and return a lecture on a topic"""
    print(f"📖 Generating lecture on: {req.topic}")
    lecture_text, audio_path = lecture_engine.generate_lecture(req.topic)
    
    # Return audio URL that frontend can play
    audio_url = f"http://localhost:8000/lectures/{os.path.basename(audio_path)}"
    
    return {
        "topic": req.topic,
        "lecture_text": lecture_text,
        "audio_url": audio_url,
        "status": "success"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}