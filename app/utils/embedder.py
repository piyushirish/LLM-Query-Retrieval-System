from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from app.core.config import GOOGLE_API_KEY

embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

def create_vector_store(chunks):
    return FAISS.from_texts(chunks, embedder)