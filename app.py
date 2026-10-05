import streamlit as st
from pypdf import PdfReader
from gtts import gTTS
import io

st.set_page_config(page_title="PDF to Voice Converter", page_icon="🔊")
st.title("🔊 PDF to Voice Converter")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

language = st.selectbox(
    "Select Language",
    options=[("English", "en"), ("Tamil", "ta"), ("Hindi", "hi")],
    format_func=lambda x: x[0],
)

def split_text(text, size=3000):
    return [text[i:i + size] for i in range(0, len(text), size)]

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = " ".join(p.extract_text() or "" for p in reader.pages).strip()

    st.text_area("Text preview", text[:1000], height=200)

    if st.button("Convert to Voice 🎙️"):
        if not text:
            st.error("No readable text found. Scanned PDF-ah irukkalaam.")
        else:
            with st.spinner("Converting..."):
                try:
                    buffer = io.BytesIO()
                    for chunk in split_text(text):
                        gTTS(text=chunk, lang=language[1]).write_to_fp(buffer)
                    audio_bytes = buffer.getvalue()

                    st.success("Done! 🎉")
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(
                        "Download Audio",
                        audio_bytes,
                        file_name="converted_audio.mp3",
                        mime="audio/mp3",
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
