import streamlit as st

from pdf_loader import extract_text
from chunker import create_chunks
from query_system import PDFQA

st.title("PDF Question Answering System")

uploaded_pdf = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_pdf:

    with open(
        "data/uploaded.pdf",
        "wb"
    ) as f:

        f.write(
            uploaded_pdf.getbuffer()
        )

    text = extract_text(
        "data/uploaded.pdf"
    )

    chunks = create_chunks(text)

    if "qa" not in st.session_state:

        qa = PDFQA()

        qa.create_index(
            chunks
        )

        st.session_state.qa = qa

    question = st.text_input(
        "Ask a Question"
    )

    if question:

        answer = (
            st.session_state.qa.ask(
                question
            )
        )

        st.write("### Answer")

        st.write(answer)