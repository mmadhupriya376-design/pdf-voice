import streamlit as st
from pypdf import PdfReader
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="Smart PDF App",
    page_icon="🔊"
)

st.title("📄 PDF to Voice Converter")
st.write("Upload a PDF file and listen to it as voice.")

uploaded_file = st.file_uploader(
    "📄 Upload your PDF",
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

        language = st.selectbox(
            "🌐 Select Language",
            [
                ("English", "en-IN"),
                ("Tamil", "ta-IN"),
                ("Hindi", "hi-IN")
            ]
        )

        language_name = language[0]
        language_code = language[1]

        if st.button("🔊 Convert to Voice"):

            safe_text = json.dumps(text)

            html_code = f"""
            <!DOCTYPE html>
            <html>
            <body>

            <button onclick="speakText()"
                    style="
                    font-size:18px;
                    padding:12px 25px;
                    cursor:pointer;
                    ">
                ▶️ Play Voice
            </button>

            <button onclick="stopVoice()"
                    style="
                    font-size:18px;
                    padding:12px 25px;
                    cursor:pointer;
                    margin-left:10px;
                    ">
                ⏹️ Stop
            </button>

            <script>

            const text = {safe_text};

            function speakText() {{

                window.speechSynthesis.cancel();

                const speech =
                    new SpeechSynthesisUtterance(text);

                speech.lang = "{language_code}";
                speech.rate = 0.9;
                speech.pitch = 1.0;
                speech.volume = 1.0;

                window.speechSynthesis.speak(speech);
            }}

            function stopVoice() {{

                window.speechSynthesis.cancel();

            }}

            </script>

            </body>
            </html>
            """

            st.success(
                "🎉 PDF converted to voice successfully!"
            )

            components.html(
                html_code,
                height=100
            )

    else:

        st.error(
            "❌ No readable text found in this PDF."
        )
