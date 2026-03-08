import streamlit as st
import requests
from gtts import gTTS
import os
import tempfile
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import subprocess
import base64
import time

# FFmpeg path
FFMPEG_PATH = r"C:\Users\sayal\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"
API_URL = "http://localhost:8000"

st.set_page_config(page_title="DRISHTI-AI", page_icon="👁️", layout="wide")

st.markdown("""
<style>
    body { background-color: #0e1117; }
    .title { font-size: 2.5em; font-weight: bold; text-align: center; color: #00d4ff; padding-top: 10px; }
    .subtitle { text-align: center; color: #aaaaaa; font-size: 1.1em; margin-bottom: 10px; }
    .mode-box { background-color: #1e2130; border: 2px solid #00d4ff; border-radius: 15px; padding: 20px; text-align: center; margin: 10px; }
    .mode-box h3 { color: #00d4ff; }
    .mode-box p { color: #aaaaaa; }
    .active-mode { background-color: #00d4ff22; border: 2px solid #00d4ff; border-radius: 15px; padding: 15px; text-align: center; margin: 10px 0; }
    .lecture-card { background-color: #1e2130; border-left: 4px solid #00d4ff; border-radius: 10px; padding: 15px; margin: 10px 0; }
    .progress-card { background-color: #1e2130; border-left: 4px solid #00ff88; border-radius: 10px; padding: 15px; margin: 10px 0; color: white; }
    .doubt-card { background-color: #1e2130; border-left: 4px solid #ff9900; border-radius: 10px; padding: 15px; margin: 10px 0; }
    .stButton button { border-radius: 50px; font-weight: bold; font-size: 1em; }
    .heard-box { background:#1e2130; border:1px solid #00d4ff44; border-radius:10px; padding:10px 16px; color:#00d4ff; font-size:1rem; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def play_audio(text: str):
    """Convert text to speech and autoplay — ONE call only per action."""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            path = f.name
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        # Use a unique id so the browser always treats it as a new audio element
        uid = str(int(time.time() * 1000))
        st.markdown(
            f'<audio id="a{uid}" autoplay>'
            f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
            f'</audio>',
            unsafe_allow_html=True
        )
        os.unlink(path)
    except Exception as e:
        st.warning(f"Audio error: {e}")

def audio_to_text(audio_bytes) -> str | None:
    recognizer = sr.Recognizer()
    webm_path = wav_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
            f.write(audio_bytes)
            webm_path = f.name
        wav_path = webm_path.replace(".webm", ".wav")
        subprocess.run(
            [FFMPEG_PATH, "-i", webm_path, "-ar", "16000", "-ac", "1",
             "-f", "wav", wav_path, "-y"],
            capture_output=True
        )
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language="en-IN")
    except:
        return None
    finally:
        for p in [webm_path, wav_path]:
            try:
                if p and os.path.exists(p): os.unlink(p)
            except: pass

def ask_ai(question: str) -> str:
    try:
        res = requests.post(f"{API_URL}/ask", json={"question": question, "speak_response": False})
        return res.json()["answer"]
    except:
        return "Sorry, I could not connect to the backend. Please make sure uvicorn is running."

def get_lecture(topic: str) -> str:
    try:
        res = requests.post(f"{API_URL}/lecture", json={"topic": topic})
        return res.json()["lecture_text"]
    except:
        return "Sorry, could not generate lecture. Please try again."

def fmt_time(seconds: int) -> str:
    m, s = seconds // 60, seconds % 60
    if m > 0: return f"{m} minutes and {s} seconds"
    return f"{s} seconds"

# ─── SESSION STATE ────────────────────────────────────────────────────────────

for k, v in {
    "welcomed": False,
    "welcome_audio_done": False,
    "mode": "home",
    "messages": [],
    "lectures_completed": [],
    "doubts_solved": 0,
    "total_time": 0,
    "session_start": time.time(),
    "current_lecture": None,
    # Rotating mic key — prevents Streamlit reusing the previous recording
    "mic_key_counter": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def next_mic_key() -> str:
    """Return a unique key for each new mic recording session."""
    st.session_state.mic_key_counter += 1
    return f"mic_{st.session_state.mic_key_counter}"

# ─── TITLE ───────────────────────────────────────────────────────────────────

st.markdown('<div class="title">👁️ DRISHTI-AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Voice-First AI Learning Platform</div>', unsafe_allow_html=True)

# ─── WELCOME SCREEN ──────────────────────────────────────────────────────────

if not st.session_state.welcomed:
    st.divider()
    st.markdown("""
    <div style='text-align:center; padding:30px;'>
        <h2 style='color:#00d4ff;'>👋 Welcome to DRISHTI-AI!</h2>
        <p style='color:#aaaaaa; font-size:1.15em;'>
            A voice-first learning platform built for visually impaired students.<br><br>
            🎤 <b style='color:#00d4ff;'>Say "Open Lectures"</b> → Browse and play chapter lectures<br>
            🤔 <b style='color:#00d4ff;'>Say "Solve My Doubt"</b> → Ask any question<br>
            📊 <b style='color:#00d4ff;'>Say "My Progress"</b> → Hear your learning stats<br><br>
            Everything works with just your voice!
        </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔊 Start DRISHTI-AI", use_container_width=True):
            st.session_state.welcomed = True
            st.session_state.session_start = time.time()
            st.rerun()
    st.stop()

# ─── WELCOME AUDIO (exactly once, no duplicate) ───────────────────────────────

if not st.session_state.welcome_audio_done:
    st.session_state.welcome_audio_done = True
    play_audio(
        "Hello! I am DRISHTI AI, your personal voice learning assistant. "
        "Say Open Lectures to start a chapter lecture. "
        "Say Solve My Doubt to ask any question. "
        "Say My Progress to hear your learning stats. "
        "Let us begin!"
    )

# ─── GLOBAL MIC ──────────────────────────────────────────────────────────────
# The mic key rotates every time we come back to this page after a recording,
# so Streamlit always shows a fresh recorder — no stale audio replaying.

st.divider()
st.markdown("### 🎤 Speak a Command or Question")

current_mic_key = f"mic_{st.session_state.mic_key_counter}"
audio = mic_recorder(
    start_prompt="🎤  Press to Speak",
    stop_prompt="⏹  Processing...",
    just_once=True,
    use_container_width=True,
    key=current_mic_key
)

if audio:
    # Immediately rotate key so the next rerun gets a fresh recorder
    st.session_state.mic_key_counter += 1

    with st.spinner("🔄 Recognising..."):
        command = audio_to_text(audio['bytes'])

    if command:
        command_lower = command.lower()
        st.markdown(f'<div class="heard-box">🗣️ You said: <b>{command}</b></div>',
                    unsafe_allow_html=True)

        # ── Navigation commands ──────────────────────────────
        if any(w in command_lower for w in [
            "open lecture", "lecture library", "start lecture",
            "play lecture", "open library", "lectures"
        ]):
            st.session_state.mode = "lecture"
            # Single audio — no double call
            play_audio("Opening lecture library. Say the chapter name to start.")
            st.rerun()

        elif any(w in command_lower for w in [
            "solve doubt", "doubt", "ask question",
            "i have a doubt", "solve my doubt", "question"
        ]):
            st.session_state.mode = "doubt"
            play_audio("Opening doubt solver. Speak your question.")
            st.rerun()

        elif any(w in command_lower for w in [
            "progress", "my progress", "how am i doing",
            "learning stats", "my stats", "report"
        ]):
            st.session_state.mode = "progress"
            st.rerun()

        elif any(w in command_lower for w in ["home", "go home", "main menu", "menu"]):
            st.session_state.mode = "home"
            play_audio("Going back to home screen.")
            st.rerun()

        # ── Context-aware: lecture mode → chapter name ───────
        elif st.session_state.mode == "lecture":
            st.session_state.current_lecture = command
            st.rerun()

        # ── Context-aware: doubt mode → question ─────────────
        elif st.session_state.mode == "doubt":
            with st.spinner("🤔 Solving your doubt..."):
                answer = ask_ai(command)
            st.session_state.messages.append({"role": "user", "content": command})
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.session_state.doubts_solved += 1
            play_audio(answer)   # single audio call
            st.rerun()

        else:
            # General question from home screen
            with st.spinner("🤔 Thinking..."):
                answer = ask_ai(command)
            play_audio(answer)   # single audio call
            st.info(f"💬 {answer}")

    else:
        play_audio("Sorry, I could not understand. Please try again.")
        st.error("❌ Could not understand. Please speak clearly and try again.")

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# HOME MODE
# ════════════════════════════════════════════════════════════════════════════

if st.session_state.mode == "home":
    st.markdown("## 🏠 What would you like to do?")
    st.markdown("*Say a command or click a button below*")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""<div class='mode-box'><h3>📚 Lecture Library</h3>
        <p>Listen to full chapter audio lectures from your syllabus</p></div>""",
                    unsafe_allow_html=True)
        if st.button("📚 Open Lectures", use_container_width=True, key="btn_lec"):
            st.session_state.mode = "lecture"
            play_audio("Opening lecture library.")
            st.rerun()

    with col2:
        st.markdown("""<div class='mode-box'><h3>🤔 Doubt Solver</h3>
        <p>Ask any question and get instant voice answers</p></div>""",
                    unsafe_allow_html=True)
        if st.button("🤔 Solve a Doubt", use_container_width=True, key="btn_dbt"):
            st.session_state.mode = "doubt"
            play_audio("Opening doubt solver.")
            st.rerun()

    with col3:
        st.markdown("""<div class='mode-box'><h3>📊 My Progress</h3>
        <p>Track your learning time, lectures and doubts solved</p></div>""",
                    unsafe_allow_html=True)
        if st.button("📊 View Progress", use_container_width=True, key="btn_prog"):
            st.session_state.mode = "progress"
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# LECTURE MODE
# ════════════════════════════════════════════════════════════════════════════

elif st.session_state.mode == "lecture":
    st.markdown("## 📚 Lecture Library")
    st.markdown('<div class="active-mode">🎤 <b>Say the chapter name — e.g. "Chapter 6" or "Haloalkanes"</b></div>',
                unsafe_allow_html=True)

    chapters = [
        ("⚗️", "Haloalkanes and Haloarenes"),
        ("🧬", "Biomolecules"),
        ("⚡", "Electrochemistry"),
        ("🌿", "Photosynthesis"),
        ("🔢", "Matrices and Determinants"),
        ("🧪", "Organic Chemistry"),
        ("🌊", "Wave Optics"),
        ("🧲", "Magnetism"),
        ("📐", "Trigonometry"),
        ("🌍", "Modern Indian History"),
        ("💧", "Chemical Bonding"),
        ("🔬", "Cell Biology"),
    ]

    st.markdown("### 📖 Available Chapters — click or say the name:")
    cols = st.columns(3)
    for i, (icon, chapter) in enumerate(chapters):
        with cols[i % 3]:
            if st.button(f"{icon} {chapter}", use_container_width=True, key=f"ch_{i}"):
                st.session_state.current_lecture = chapter
                st.rerun()

    # ── Generate lecture when topic is set ───────────────────
    if st.session_state.current_lecture:
        topic = st.session_state.current_lecture
        st.session_state.current_lecture = None   # clear immediately — prevents re-trigger

        st.markdown(f"""<div class='lecture-card'><h3>📖 Now Playing: {topic}</h3></div>""",
                    unsafe_allow_html=True)

        with st.spinner(f"🎙️ Generating lecture on {topic}..."):
            lecture_text = get_lecture(topic)

        st.markdown("#### 📄 Lecture Content:")
        st.write(lecture_text)

        if topic not in st.session_state.lectures_completed:
            st.session_state.lectures_completed.append(topic)

        # ✅ SINGLE audio call — no double voice
        play_audio(lecture_text)

        st.success("✅ Lecture complete! Say next chapter name or say Go Home.")

    if st.button("🏠 Back to Home", key="lec_home"):
        st.session_state.mode = "home"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# DOUBT MODE
# ════════════════════════════════════════════════════════════════════════════

elif st.session_state.mode == "doubt":
    st.markdown("## 🤔 Doubt Solver")
    st.markdown('<div class="active-mode">🎤 <b>Speak your question — I will answer it!</b></div>',
                unsafe_allow_html=True)

    if st.session_state.messages:
        st.markdown("### 💬 Questions & Answers")
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='doubt-card'>🙋 <b>Question:</b> {msg['content']}</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='lecture-card'>🤖 <b>Answer:</b> {msg['content']}</div>",
                            unsafe_allow_html=True)
    else:
        st.markdown("""<div style='text-align:center; color:#aaaaaa; padding:30px;'>
            <h3>No questions yet!</h3>
            <p>Press the mic button above and ask your first question.</p></div>""",
                    unsafe_allow_html=True)

    if st.button("🏠 Back to Home", key="dbt_home"):
        st.session_state.mode = "home"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# PROGRESS MODE
# ════════════════════════════════════════════════════════════════════════════

elif st.session_state.mode == "progress":
    st.markdown("## 📊 My Learning Progress")

    session_seconds = int(time.time() - st.session_state.session_start)
    total_seconds   = st.session_state.total_time + session_seconds
    lectures_done   = len(st.session_state.lectures_completed)
    doubts_done     = st.session_state.doubts_solved

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class='progress-card'>
            <h2 style='color:#00ff88;text-align:center;'>{fmt_time(total_seconds)}</h2>
            <p style='text-align:center;'>⏱️ Total Learning Time</p></div>""",
                    unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='progress-card'>
            <h2 style='color:#00d4ff;text-align:center;'>{lectures_done}</h2>
            <p style='text-align:center;'>📚 Lectures Completed</p></div>""",
                    unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='progress-card'>
            <h2 style='color:#ff9900;text-align:center;'>{doubts_done}</h2>
            <p style='text-align:center;'>🤔 Doubts Solved</p></div>""",
                    unsafe_allow_html=True)

    if st.session_state.lectures_completed:
        st.markdown("### ✅ Lectures Completed:")
        for i, lec in enumerate(st.session_state.lectures_completed, 1):
            st.markdown(f"**{i}.** 📖 {lec}")

    # ✅ SINGLE audio call for progress report
    progress_text = (
        f"Here is your learning progress. "
        f"You have spent {fmt_time(total_seconds)} learning today. "
        f"You completed {lectures_done} lectures and solved {doubts_done} doubts. "
    )
    if st.session_state.lectures_completed:
        progress_text += f"Chapters studied: {', '.join(st.session_state.lectures_completed)}. "
    progress_text += "Keep up the great work!"
    play_audio(progress_text)

    if st.button("🏠 Back to Home", key="prog_home"):
        st.session_state.total_time += session_seconds
        st.session_state.session_start = time.time()
        st.session_state.mode = "home"
        st.rerun()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

st.sidebar.markdown("## 👁️ DRISHTI-AI")
st.sidebar.markdown(f"**Mode:** `{st.session_state.mode.upper()}`")
st.sidebar.markdown(f"**Mic session:** `{st.session_state.mic_key_counter}`")
st.sidebar.divider()
st.sidebar.markdown("### 🎤 Voice Commands")
st.sidebar.markdown("""
- *"Open Lectures"*  
- *"Solve My Doubt"*  
- *"My Progress"*  
- *"Go Home"*  
- *(In lecture mode)* say chapter name  
- *(In doubt mode)* ask any question  
""")
st.sidebar.divider()
st.sidebar.markdown("### 📄 Syllabus Files")
if os.path.exists("syllabus/"):
    for f in os.listdir("syllabus/"):
        if f.endswith(".pdf"):
            st.sidebar.markdown(f"📄 {f}")
st.sidebar.divider()
if st.sidebar.button("🔄 Restart App"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()