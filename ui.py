import streamlit as st
import requests

st.set_page_config(page_title="DRISHTI-AI", page_icon="👁️")

st.title("👁️ DRISHTI-AI")
st.subheader("Voice-First Learning Platform for Visually Impaired Students")

API_URL = "http://localhost:8000"

# Mode selection
mode = st.radio("Choose Input Mode:", ["Text Input", "Voice Input"])

if mode == "Text Input":
    question = st.text_input("Ask your question:")
    speak_out = st.checkbox("Speak the answer aloud", value=True)
    
    if st.button("Ask") and question:
        with st.spinner("Thinking..."):
            res = requests.post(f"{API_URL}/ask", json={
                "question": question,
                "speak_response": speak_out
            })
            answer = res.json()["answer"]
        st.success("Answer:")
        st.write(answer)

elif mode == "Voice Input":
    if st.button("🎤 Click and Speak"):
        with st.spinner("Listening and processing..."):
            res = requests.post(f"{API_URL}/voice-ask")
            data = res.json()
        
        st.info(f"**You asked:** {data.get('question')}")
        st.success(f"**Answer:** {data.get('answer')}")