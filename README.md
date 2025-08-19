# Boo Logistics Voice Assistant 🚚🎤

Ứng dụng web cho phép:
- Thu âm giọng nói từ iPhone/máy tính
- Boo hiểu lệnh và trả lời bằng giọng nói
- Tạo báo cáo Excel (hiện tại demo: Doanh thu T6)

## Cách chạy trên Streamlit Cloud
1. Tạo repo GitHub (boo-logistics)
2. Upload các file này: `boo_voice_app.py`, `requirements.txt`, `README.md`
3. Vào https://share.streamlit.io/ → Deploy app
4. Thêm **Secrets** trong Streamlit Cloud:
```
[general]
OPENAI_API_KEY="sk-xxxxx"
```
5. Mở link public → test ngay trên iPhone
