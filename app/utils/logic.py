from langchain.vectorstores import FAISS
from app.utils.embedder import embedder, create_vector_store

def retrieve_answers(text, questions):
    chunks = text.split(". ")
    vector_store = create_vector_store(chunks)
    retriever = vector_store.as_retriever()

    answers = []
    for q in questions:
        docs = retriever.get_relevant_documents(q)
        matched_text = " ".join([doc.page_content for doc in docs])
        answers.append(matched_text.strip())
    return answers