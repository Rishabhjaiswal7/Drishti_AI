import speech_recognition as sr
from gtts import gTTS
import os
import tempfile

def listen_from_mic() -> str:
    """Capture voice and convert to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=10)
    
    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Speech service unavailable"

def speak(text: str):
    """Convert text to speech and play it"""
    tts = gTTS(text=text, lang='en', slow=False)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        os.system(f"mpg321 {f.name}")  # Linux
        # For Windows use: os.system(f"start {f.name}")
        # For Mac use: os.system(f"afplay {f.name}")