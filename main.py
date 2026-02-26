from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine import RAGEngine
from speech import speak

app = FastAPI()
rag = RAGEngine()  # Loads syllabus on startup

class QueryRequest(BaseModel):
    question: str
    speak_response: bool = False

@app.get("/")
def root():
    return {"message": "DRISHTI-AI is running"}

@app.post("/ask")
def ask_question(req: QueryRequest):
    answer = rag.ask(req.question)
    
    if req.speak_response:
        speak(answer)
    
    return {
        "question": req.question,
        "answer": answer
    }

@app.post("/voice-ask")
def voice_ask():
    """Full voice pipeline: mic → STT → RAG → TTS"""
    from speech import listen_from_mic
    
    question = listen_from_mic()
    if not question:
        return {"error": "Could not capture voice"}
    
    answer = rag.ask(question)
    speak(answer)
    
    return {"question": question, "answer": answer}