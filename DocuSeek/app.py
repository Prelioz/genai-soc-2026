from rag import ask_query, create_vector_db
import os
import shutil



if not os.path.exists("chroma_store"):

    pdf_path = input("Enter PDF path: ")
    
    if os.path.exists("chroma_store"):
     shutil.rmtree("chroma_store")

    create_vector_db(pdf_path)


while True:

    user_query = input("Ask a question (type 'exit' to quit): ")

    if user_query.lower() == "exit":
     break

    answer = ask_query(user_query)

    print(answer)
