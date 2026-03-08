from rag_engine import RAGEngine
from gtts import gTTS
import os
import tempfile

class LectureEngine:
    def __init__(self, rag: RAGEngine):
        self.rag = rag

    def generate_lecture(self, topic: str) -> tuple[str, str]:
        """Generate a lecture on a topic and return (lecture_text, audio_path)"""
        
        # Ask RAG to generate a structured lecture
        prompt = f"""
        Create a detailed audio lecture for visually impaired students on the topic: {topic}
        
        Structure the lecture as follows:
        1. Introduction - What is {topic}?
        2. Key Concepts - Main points students must know
        3. Examples - Real world examples
        4. Summary - Quick recap of what was covered
        
        Make it conversational, clear and easy to understand when heard as audio.
        Do not use bullet points or symbols. Write in full sentences only.
        Keep it detailed but under 500 words.
        """
        
        lecture_text = self.rag.ask(prompt)
        audio_path = self.text_to_audio(lecture_text, topic)
        
        return lecture_text, audio_path

    def text_to_audio(self, text: str, topic: str) -> str:
        """Convert lecture text to audio file and save it"""
        
        # Create lectures folder if not exists
        os.makedirs("lectures", exist_ok=True)
        
        # Clean topic name for filename
        safe_topic = "".join(c for c in topic if c.isalnum() or c == " ").strip()
        safe_topic = safe_topic.replace(" ", "_")[:50]
        audio_path = f"lectures/{safe_topic}.mp3"
        
        # Generate audio
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(audio_path)
        
        print(f"✅ Lecture saved: {audio_path}")
        return audio_path