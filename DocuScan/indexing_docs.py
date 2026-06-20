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

  
    return documents