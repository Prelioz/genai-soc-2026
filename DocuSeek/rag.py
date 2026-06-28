from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from embeddings import embedding_model
from LLM import generate_response


def load_document(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    return documents


def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        length_function=len,
    )

    chunks = splitter.split_documents(documents)

    return chunks


def create_vector_db(pdf_path):
    documents = load_document(pdf_path)
    chunks = create_chunks(documents)

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="chroma_store",
    )


def load_vector_db():
    db = Chroma(
        persist_directory="chroma_store",
        embedding_function=embedding_model,
    )

    return db


def ask_query(user_query):
    db = load_vector_db()

    docs = db.similarity_search(user_query, k=7)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
Answer the question only using the context below.

If the answer cannot be found in the context, reply:
"I couldn't find that information in the provided document."

Context:
{context}

Question:
{user_query}

Answer:
"""

    return generate_response(prompt)