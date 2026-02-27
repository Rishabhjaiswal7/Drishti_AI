import streamlit as st
import requests
from gtts import gTTS
import os
import tempfile
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment
from pydub import AudioSegment
import pydub.utils

FFMPEG_PATH = r"C:\Users\sayal\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\Users\sayal\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffprobe.exe"

AudioSegment.converter = FFMPEG_PATH
AudioSegment.ffmpeg = FFMPEG_PATH
AudioSegment.ffprobe = FFPROBE_PATH
# FFmpeg path
AudioSegment.converter = r"C:\Users\sayal\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="DRISHTI-AI",
    page_icon="👁️",
    layout="centered"
)

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .title { 
        font-size: 3em; 
        font-weight: bold; 
        text-align: center;
        color: #00d4ff;
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 2em;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">👁️ DRISHTI-AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Voice-First Learning Platform for Visually Impaired Students</div>', unsafe_allow_html=True)
st.divider()

# Sidebar
speak_out = st.sidebar.checkbox("🔊 Speak answers aloud", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown("### How to use")
st.sidebar.markdown("""
1. Click **Start Recording**
2. Ask your question
3. Click **Stop Recording**
4. Wait for the answer
5. Answer will be spoken aloud!
""")
st.sidebar.markdown("---")
st.sidebar.markdown("### About DRISHTI-AI")
st.sidebar.markdown("An AI-powered learning platform designed for visually impaired students!")

def speak_answer(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            temp_path = f.name
            tts.save(temp_path)
        os.system(f"start {temp_path}")
    except Exception as e:
        st.warning(f"Could not play audio: {e}")

def audio_to_text(audio_bytes):
    recognizer = sr.Recognizer()
    webm_path = None
    wav_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
            f.write(audio_bytes)
            webm_path = f.name

        wav_path = webm_path.replace(".webm", ".wav")

        import subprocess
        subprocess.run([
            FFMPEG_PATH,
            "-i", webm_path,
            "-ar", "16000",
            "-ac", "1",
            "-f", "wav",
            wav_path,
            "-y"
        ], capture_output=True)

        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="en-IN")
        return text

    except sr.UnknownValueError:
        st.error("Could not understand. Speak clearly and try again!")
        return None
    except sr.RequestError as e:
        st.error(f"Speech service error: {e}")
        return None
    except Exception as e:
        st.error(f"Audio error: {e}")
        return None
    finally:
        try:
            if webm_path and os.path.exists(webm_path):
                os.unlink(webm_path)
            if wav_path and os.path.exists(wav_path):
                os.unlink(wav_path)
        except:
            pass
        
# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

st.divider()

# Input tabs
tab1, tab2 = st.tabs(["🎤 Voice Input", "💬 Text Input"])

# VOICE INPUT TAB
with tab1:
    st.markdown("### 🎤 Speak your question")
    st.markdown("Click **Start** → Ask question → Click **Stop**")

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        just_once=True,
        use_container_width=True,
        key="mic"
    )

    if audio:
        st.info("🔄 Processing your voice...")
        question = audio_to_text(audio['bytes'])

        if question:
            st.success(f"**You asked:** {question}")

            with st.chat_message("user"):
                st.write(question)
            st.session_state.messages.append({"role": "user", "content": question})

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        res = requests.post(f"{API_URL}/ask", json={
                            "question": question,
                            "speak_response": False
                        })
                        answer = res.json()["answer"]
                    except:
                        answer = "Sorry, could not connect to backend."
                st.write(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})

            if speak_out:
                speak_answer(answer)
        else:
            st.error("❌ Could not understand. Please try again!")

# TEXT INPUT TAB
with tab2:
    st.markdown("### 💬 Type your question")
    question_text = st.chat_input("Ask your question here...")

    if question_text:
        with st.chat_message("user"):
            st.write(question_text)
        st.session_state.messages.append({"role": "user", "content": question_text})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(f"{API_URL}/ask", json={
                        "question": question_text,
                        "speak_response": False
                    })
                    answer = res.json()["answer"]
                except:
                    answer = "Sorry, could not connect to backend."
            st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

        if speak_out:
            speak_answer(answer)