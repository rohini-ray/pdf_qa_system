import streamlit as st
import os
import time

from src.pdf_loader import extract_text
from src.chunker import create_chunks
from src.query_system import PDFQA


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.title("🤖 PDF AI Assistant")

    st.markdown("---")

    st.markdown("""
### Features

✅ PDF Upload

✅ Semantic Search

✅ Fast Retrieval

✅ Local AI

✅ RAG Pipeline
""")

    st.markdown("---")

    st.success("Ready")

# -----------------------------
# SESSION STATE
# -----------------------------

if "qa" not in st.session_state:
    st.session_state.qa = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

# -----------------------------
# HEADER
# -----------------------------

st.title("📚 PDF AI Assistant")

st.write(
    "Upload a PDF and ask questions instantly."
)

# -----------------------------
# PDF UPLOAD
# -----------------------------

uploaded_pdf = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# -----------------------------
# PROCESS PDF ONLY ONCE
# -----------------------------

if uploaded_pdf is not None and not st.session_state.pdf_processed:

    os.makedirs("data", exist_ok=True)

    pdf_path = "data/uploaded.pdf"

    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.getbuffer())

    with st.spinner("📖 Reading PDF..."):

        text = extract_text(pdf_path)

    with st.spinner("🧠 Creating Index..."):

        chunks = create_chunks(
            text,
            chunk_size=1500
        )

        qa = PDFQA()

        qa.create_index(chunks)

        st.session_state.qa = qa

    st.session_state.pdf_processed = True

    st.success("✅ PDF Ready")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Characters",
        len(text)
    )

    col2.metric(
        "Chunks",
        len(chunks)
    )

    col3.metric(
        "Status",
        "Ready"
    )

# -----------------------------
# CHAT AREA
# -----------------------------

if st.session_state.pdf_processed:

    st.markdown("## 💬 Chat")

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input(
        "Ask a question about your PDF..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("🤔 Thinking..."):

                start = time.time()

                answer = st.session_state.qa.ask(
                    question
                )

                response_time = (
                    time.time() - start
                )

                st.write(answer)

                st.caption(
                    f"⏱ {response_time:.2f} sec"
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

else:

    st.info(
        "👆 Upload a PDF to begin."
    )