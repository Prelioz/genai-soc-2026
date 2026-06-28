import streamlit as st
import tempfile
import shutil
import os

from rag import create_vector_db, ask_query

st.set_page_config(
    page_title="DocuSeek",
    page_icon="📄",
    layout="centered"
)

st.title("📄 DocuSeek")
st.caption("Chat with your PDF using Retrieval-Augmented Generation (RAG)")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type="pdf"
)

if uploaded_file is not None:

    if st.button("Process PDF"):

        # Delete previous vector database
        if os.path.exists("chroma_store"):
            shutil.rmtree("chroma_store")

        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            pdf_path = temp_file.name

        with st.spinner("Processing PDF..."):
            create_vector_db(pdf_path)

        os.remove(pdf_path)

        st.success("✅ PDF processed successfully!")

# Ask questions only after processing
if os.path.exists("chroma_store"):

    st.divider()

    question = st.text_input("Ask a question")

    if st.button("Ask"):

        if question.strip():

            with st.spinner("Generating answer..."):
                answer = ask_query(question)

            st.subheader("Answer")
            st.write(answer)

        else:
            st.warning("Please enter a question.")