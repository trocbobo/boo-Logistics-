import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

# 🔑 API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Boo Logistics Voice", page_icon="🎤", layout="wide")

st.title("🎤 Trợ lý Boo Logistics")
st.write("Upload file giọng nói (.wav, .mp3) để Boo tạo báo cáo 📊")

# 🎤 Upload file audio
uploaded_audio = st.file_uploader("👉 Chọn file giọng nói (.wav, .mp3)", type=["wav", "mp3"])

query = ""
if uploaded_audio:
    recognizer = sr.Recognizer()
    with sr.AudioFile(uploaded_audio) as source:
        audio = recognizer.record(source)
    try:
        query = recognizer.recognize_google(audio, language="vi-VN")
        st.success(f"Anh nói: {query}")
    except:
        st.error("❌ Không nhận diện được giọng nói.")
        query = ""

# 📝 Xử lý yêu cầu
if query:
    with st.spinner("⏳ Boo đang xử lý..."):
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là Trợ lý Boo, chuyên báo cáo logistics."},
                {"role": "user", "content": query}
            ]
        )
        answer = response.choices[0].message.content
        st.write("### 📊 Kết quả báo cáo")
        st.write(answer)

        # 🎧 Xuất ra file mp3 để nghe
        tts = gTTS(answer, lang="vi")
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmpfile.name)
        st.audio(tmpfile.name, format="audio/mp3")
