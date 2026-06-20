from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

def load_document(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print(len(documents))
    print(type(documents))
    print(documents[0])

  
    return documents

def create_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size = 500,
        chunk_overlap = 100,
        length_function=len,
    )

    chunks = splitter.split_documents(documents)

    print(type(chunks))
    print(len(chunks))
    print(type(chunks[0]))

    return chunks





