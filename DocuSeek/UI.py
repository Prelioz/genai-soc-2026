import streamlit as st
import tempfile
import shutil
import os
import types

from rag import create_vector_db, ask_query

# 1. Page Config
st.set_page_config(
    page_title="DocuSeek",
    page_icon="📄",
    layout="centered"
)

# 2. Inject Conceptual Sketch CSS
st.markdown("""
<style>
/* Import hand-drawn and monospace fonts */
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

/* Paper Background for the app & hide top header */
.stApp {
    background-color: #f5f1e8;
    background-image: none;
}
[data-testid="stHeader"] {
    background-color: transparent !important;
}


html, body {
    font-family: 'Space Mono', monospace;
    font-size: 18px;
    color: #2e2e2e;
}

.stMarkdown,
.stTextInput,
.stButton,
.stAlert,
label,
p {
    font-family: 'Space Mono', monospace !important;
    color: #2e2e2e !important;
}
            
/* Hand-drawn Headers */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Architects Daughter', cursive !important;
    color: #2e2e2e !important;
}

h1 {
    border-bottom: 2px dashed #4a6b8a;
    display: inline-block;
    padding-bottom: 5px;
    margin-bottom: 10px;
    transform: rotate(-1deg);
}

h3 {
    border-bottom: 2px dotted #b5494b;
    display: inline-block;
    transform: rotate(0.5deg);
}

/* Target the main content block to create the sketched card */
.block-container {
    background: #f5f1e8;
    /* Irregular hand-drawn looking border */
    border-radius: 255px 15px 225px 15px/15px 225px 15px 255px; 
    border: 2px solid #2e2e2e;
    /* Hard flat shadow */
    box-shadow: 6px 6px 0px #2e2e2e;
    padding: 3rem !important;
    margin-top: 3rem !important;
    margin-bottom: 3rem !important;
    transform: rotate(-0.3deg);
}

/* Clean Sketched Text Input */
.stTextInput [data-baseweb="base-input"] {
    background-color: #f5f1e8 !important;
    border: 2px solid #2e2e2e !important;
    border-radius: 10px 15px 12px 18px !important;
    box-shadow: 3px 3px 0px #2e2e2e !important;
}
.stTextInput [data-baseweb="input"] {
    background-color: transparent !important;
    border: none !important;
}
.stTextInput input {
    color: #2e2e2e !important;
    caret-color: #000000 !important;
    font-family: 'Space Mono', monospace !important;
    background-color: transparent !important;
    -webkit-text-fill-color: #2e2e2e !important;
}
.stTextInput input::placeholder {
    color: rgba(46, 46, 46, 0.6) !important;
    font-family: 'Architects Daughter', cursive !important;
}

/* --- FIX: Unified Sketched Buttons (Apply to Main Buttons AND Browse Files Button) --- */
.stButton > button,
[data-testid="stFileUploadDropzone"] button {
    background-color: #f5f1e8 !important;
    border: 2px solid #2e2e2e !important;
    border-radius: 12px 18px 14px 20px !important;
    color: #2e2e2e !important;
    font-family: 'Architects Daughter', cursive !important;
    font-size: 1.1rem !important;
    font-weight: bold !important;
    box-shadow: 4px 4px 0px #4a6b8a !important; 
    transition: all 0.2s ease !important;
    transform: rotate(-0.5deg) !important;
    position: relative; 
    z-index: 10;
}

.stButton > button:hover,
[data-testid="stFileUploadDropzone"] button:hover {
    transform: translate(2px, 2px) rotate(-0.5deg) !important;
    box-shadow: 2px 2px 0px #4a6b8a !important;
}

/* Streamlit 1.58 uploader */
[data-testid="stFileUploader"] > div,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] [data-testid="stFileUploadDropzone"]{
    background: #f5f1e8 !important;
    border: 2px dashed #2e2e2e !important;
    border-radius: 18px !important;
}

/* Every nested container */
[data-testid="stFileUploader"] *{
    background: transparent !important;
    color:#2e2e2e !important;
}

/* Upload icon */
[data-testid="stFileUploader"] svg{
    fill:#2e2e2e !important;
}

/* Style the Dropzone Box */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed #2e2e2e !important;
    border-radius: 20px 15px 25px 10px !important;
    padding: 2rem !important;
}

/* Explicitly style just the layout text, NOT the hidden file input */
[data-testid="stFileUploadDropzone"] p,
[data-testid="stFileUploadDropzone"] small {
    color: #2e2e2e !important;
}

[data-testid="stFileUploadDropzone"] svg {
    fill: #2e2e2e !important;
}

/* --- FIX: Uploaded File Info Card --- */
[data-testid="stUploadedFile"] {
    border: 2px solid #2e2e2e !important;
    border-radius: 10px 15px 12px 18px !important;
    margin-top: 15px !important;
    padding: 4px !important;
}

/* Force dark text for the file name and size */
[data-testid="stUploadedFile"] span,
[data-testid="stUploadedFile"] small,
[data-testid="stUploadedFile"] p {
    color: #2e2e2e !important;
}

/* Fix the file and close icons */
[data-testid="stUploadedFile"] svg {
    fill: #2e2e2e !important;
    stroke: #2e2e2e !important;
}

/* Reset the specific "X" Remove button so it doesn't look like a giant bordered button 
   but still give it the same translation animation */
[data-testid="stUploadedFile"] button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stUploadedFile"] button:hover {
    transform: translate(2px, 2px) rotate(-0.5deg) !important;
    box-shadow: none !important;
}


/* Sketched Alert Boxes (Success, Info, Warning) */
[data-testid="stAlert"] {
    background-color: #f5f1e8 !important;
    border: 2px solid #2e2e2e !important;
    border-radius: 255px 15px 225px 15px/15px 225px 15px 255px !important;
    box-shadow: 4px 4px 0px #2e2e2e !important;
    color: #2e2e2e !important;
    transform: rotate(0.2deg);
}
[data-testid="stAlert"] * {
    color: #2e2e2e !important;
}

/* Hand-drawn divider */
hr {
    border-top: 2px dashed #2e2e2e !important;
    background: transparent !important;
    margin: 30px 0 !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# 3. Main UI Application
st.title("DocuSeek")
st.markdown("### Turn Documents into Answers")

# Upload Section
with st.container():
    uploaded_file = st.file_uploader("Drop your PDF here", type="pdf")

    if uploaded_file is not None:
        if st.button("Process PDF", use_container_width=True):

            # Delete previous vector database
            if os.path.exists("chroma_store"):
                shutil.rmtree("chroma_store")

            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                pdf_path = temp_file.name

            with st.spinner("Analyzing and indexing your document..."):
                create_vector_db(pdf_path)

            os.remove(pdf_path)
            st.success("Document processed successfully! You can now start asking questions.")


# 4. Chat/Query Section
# Ask questions only after processing
if os.path.exists("chroma_store"):
    
    st.markdown("---")
    st.markdown("### Ask DocuSeek")
    
    question = st.text_input(
        "What would you like to know?", 
        placeholder="Summarise the document"
    )

    if st.button("Ask Question", type="primary"):
        if question.strip():
            with st.spinner("Searching through document..."):
                
                # Retrieve the answer (might be a string or a generator)
                raw_answer = ask_query(question)
                
                # Convert generator to string if necessary
                if isinstance(raw_answer, types.GeneratorType):
                    answer = "".join(raw_answer)
                else:
                    answer = str(raw_answer)

            st.markdown("#### Answer")
            st.info(answer) 
        else:
            st.warning("Please enter a question to ask.")