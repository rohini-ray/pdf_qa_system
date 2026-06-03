import streamlit as st
from pdf_loader import extract_text
from chunker import create_chunks
from query_system import PDFQA
import os

# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------
# Custom CSS
# ---------------------------------

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

h1 {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# Sidebar
# ---------------------------------

with st.sidebar:

    st.title("🤖 PDF AI Assistant")

    st.markdown("---")

    st.markdown("""
### Features

✅ Upload PDF

✅ Semantic Search

✅ AI Question Answering

✅ Phi-3 Powered

✅ FAISS Retrieval
""")

    st.markdown("---")

    st.success("Ready to analyze documents")

# ---------------------------------
# Main Header
# ---------------------------------

st.markdown("""
# 📚 PDF AI Assistant

Upload a PDF and ask questions from it instantly.
""")

st.markdown("---")

# ---------------------------------
# Session State
# ---------------------------------

if "qa" not in st.session_state:
    st.session_state.qa = None

if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------
# Upload PDF
# ---------------------------------

uploaded_pdf = st.file_uploader(
    "📄 Upload a PDF File",
    type=["pdf"]
)

# ---------------------------------
# Process PDF
# ---------------------------------

if uploaded_pdf is not None and not st.session_state.pdf_loaded:

    os.makedirs("data", exist_ok=True)

    pdf_path = "data/uploaded.pdf"

    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.getbuffer())

    with st.spinner("📖 Reading PDF..."):
        text = extract_text(pdf_path)

    with st.spinner("🧠 Creating Knowledge Base..."):

        chunks = create_chunks(text)

        qa = PDFQA()

        qa.create_index(chunks)

        st.session_state.qa = qa

    st.session_state.pdf_loaded = True

    st.success("✅ PDF Loaded Successfully!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Characters",
            len(text)
        )

    with col2:
        st.metric(
            "Chunks",
            len(chunks)
        )

    with col3:
        st.metric(
            "Status",
            "Ready"
        )

# ---------------------------------
# Chat Interface
# ---------------------------------

if st.session_state.pdf_loaded:

    st.markdown("## 💬 Ask Questions")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input(
        "Ask anything about your PDF..."
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

        import time

with st.chat_message("assistant"):

    with st.spinner("🤔 Thinking..."):

        start = time.time()

        answer = st.session_state.qa.ask(
            question
        )

        end = time.time()

        st.write(answer)

        st.caption(
            f"⏱ Response Time: {end-start:.2f} seconds"
        )

        print(
            f"Response Time: {end-start:.2f} seconds"
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

else:

    st.info(
        "👆 Upload a PDF to begin chatting with your document."
    )