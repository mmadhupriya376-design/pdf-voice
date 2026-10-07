import streamlit as st
from pypdf import PdfReader
import edge_tts
import asyncio
import os
import tempfile

st.set_page_config(
    page_title="Smart PDF App",
    page_icon="🔊"
)

st.title("📄 PDF to Voice Converter")
st.write("Upload a PDF file and convert its text into voice.")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

language = st.selectbox(
    "Select Language",
    [
        ("English", "en-US-AriaNeural"),
        ("Tamil", "ta-IN-PallaviNeural"),
        ("Hindi", "hi-IN-SwaraNeural")
    ],
    format_func=lambda x: x[0]
)

def split_text(text, size=3000):
    return [
        text[i:i + size]
        for i in range(0, len(text), size)
    ]

async def create_audio(text, voice, output_file):

    chunks = split_text(text)

    with open(output_file, "wb") as final_audio:

        for i, chunk in enumerate(chunks):

            temp_file = os.path.join(
                tempfile.gettempdir(),
                f"voice_part_{i}.mp3"
            )

            communicate = edge_tts.Communicate(
                chunk,
                voice
            )

            await communicate.save(temp_file)

            with open(temp_file, "rb") as part:
                final_audio.write(part.read())

            os.remove(temp_file)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    text = text.strip()

    st.text_area(
        "Text Preview",
        text[:1000],
        height=200
    )

    if st.button("🔊 Convert to Voice"):

        if not text:
            st.error(
                "No readable text found in this PDF."
            )

        else:

            with st.spinner(
                "Converting PDF to voice..."
            ):

                try:

                    audio_file = os.path.join(
                        tempfile.gettempdir(),
                        "converted_audio.mp3"
                    )

                    asyncio.run(
                        create_audio(
                            text,
                            language[1],
                            audio_file
                        )
                    )

                    st.success(
                        "✅ PDF converted to voice successfully!"
                    )

                    with open(
                        audio_file,
                        "rb"
                    ) as audio:

                        audio_data = audio.read()

                    st.audio(
                        audio_data,
                        format="audio/mp3"
                    )

                    st.download_button(
                        "⬇️ Download Audio",
                        audio_data,
                        file_name="converted_audio.mp3",
                        mime="audio/mp3"
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )
