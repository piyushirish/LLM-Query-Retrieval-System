from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    documents: str  # Blob URL or path
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]