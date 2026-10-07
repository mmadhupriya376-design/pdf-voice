 import streamlit as st
from pypdf import PdfReader
import edge_tts
import asyncio
import tempfile
import os

st.set_page_config(
    page_title="Smart PDF App",
    page_icon="🔊"
)

st.title("📄 PDF to Voice Converter")
st.write("Upload a PDF file and convert it into voice.")

uploaded_file = st.file_uploader(
    "Upload your PDF file",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("✅ PDF uploaded successfully!")

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    text = text.strip()

    if text:

        st.subheader("📖 Extracted Text")

        st.text_area(
            "PDF Text",
            text,
            height=250
        )

        voice = st.selectbox(
            "Select Voice",
            [
                "English",
                "Tamil",
                "Hindi"
            ]
        )

        if st.button("🔊 Convert to Voice"):

            with st.spinner("Converting to voice..."):

                try:

                    if voice == "English":
                        voice_name = "en-US-AriaNeural"

                    elif voice == "Tamil":
                        voice_name = "ta-IN-PallaviNeural"

                    else:
                        voice_name = "hi-IN-SwaraNeural"

                    output_file = tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".mp3"
                    )

                    output_path = output_file.name
                    output_file.close()

                    async def generate_audio():

                        communicate = edge_tts.Communicate(
                            text,
                            voice_name
                        )

                        await communicate.save(
                            output_path
                        )

                    asyncio.run(generate_audio())

                    st.success(
                        "🎉 PDF converted to voice successfully!"
                    )

                    with open(
                        output_path,
                        "rb"
                    ) as audio_file:

                        audio_data = audio_file.read()

                    st.audio(
                        audio_data,
                        format="audio/mp3"
                    )

                    st.download_button(
                        "⬇️ Download Voice",
                        audio_data,
                        file_name="pdf_voice.mp3",
                        mime="audio/mp3"
                    )

                    os.remove(output_path)

                except Exception as e:

                    st.error(
                        f"❌ Voice conversion failed: {e}"
                    )

    else:

        st.error(
            "❌ No readable text found in this PDF."
        )
