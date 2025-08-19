import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import pandas as pd
import openai

# 🚀 Config OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🎤 Boo Voice Assistant - Logistics")
st.write("Nói lệnh để Boo tạo báo cáo Doanh thu 📊")

uploaded_file = st.file_uploader("📂 Upload file dữ liệu Excel (DATA)", type=["xlsx"])

# Hàm tạo báo cáo doanh thu
def bao_cao_doanhthu(df, thang_filter="2025-06"):
    df_t = df[df["THÁNG"].astype(str).str.contains(thang_filter, na=False)].copy()
    report = df_t.groupby("TÊN KHÁCH HÀNG").agg({
        "Tổng VND": "sum"
    }).reset_index().rename(columns={"Tổng VND": "DOANH THU"})
    return report

# 1️⃣ Thu âm giọng nói
if st.button("🎙️ Thu âm"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("👉 Đang nghe...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio, language="vi-VN")
        st.success(f"Anh nói: {query}")
    except:
        st.error("❌ Không nhận diện được giọng nói.")
        query = ""

    if query:
        # 2️⃣ GPT xử lý câu hỏi (hiểu ngữ cảnh)
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": query}]
        )
        answer = response["choices"][0]["message"]["content"]
        st.write(f"🟢 Boo: {answer}")

        # 3️⃣ Đọc câu trả lời bằng giọng nói
        tts = gTTS(answer, lang="vi")
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        st.audio(audio_bytes, format="audio/mp3")

        # 4️⃣ Nếu có file dữ liệu thì xử lý báo cáo doanh thu
        if uploaded_file and "doanh thu" in query.lower():
            df = pd.read_excel(uploaded_file, sheet_name="DATA", header=1)
            report = bao_cao_doanhthu(df, thang_filter="2025-06")
            out_file = "Bao_cao_DoanhThu_T6.xlsx"
            report.to_excel(out_file, index=False)
            st.success("✅ Đã tạo báo cáo doanh thu T6")
            st.download_button("📥 Tải báo cáo Excel", data=open(out_file, "rb"), file_name=out_file)
