import os
from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import re
import shutil
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
import requests
import tempfile
from app.utils import file_parser, logic
from app.models.schema import QueryRequest, QueryResponse
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

security = HTTPBearer()
EXPECTED_TOKEN = os.getenv("AUTH_TOKEN")

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != EXPECTED_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")


def clean_answer(text: str) -> str:
    # Remove line breaks and excessive whitespace
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = re.sub(r'\s+', ' ', text).strip()

    # Optional: remove unrelated footer lines (adjust as needed)
    footer_keywords = [
        "National Insurance Company Limited",
        "IRDAI", "CIN", "CBD-81", "Page", "UIN"
    ]
    for keyword in footer_keywords:
        if keyword in text:
            text = text.split(keyword)[0].strip()

    return text


from urllib.parse import urlparse

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
def run_query(payload: QueryRequest,credentials: HTTPAuthorizationCredentials = Security(security)):
    verify_token(credentials)
    document = payload.documents

    # Check if the input is a URL
    parsed_url = urlparse(document)
    if parsed_url.scheme in ("http", "https"):
        try:
            response = requests.get(document)
            response.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Download error: {str(e)}")

        # Save the downloaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(response.content)
            temp.flush()
            text = file_parser.parse_pdf(temp.name)
    else:
        # Treat it as a local path
        if not Path(document).exists():
            raise HTTPException(status_code=404, detail="Local file not found")
        text = file_parser.parse_pdf(document)

    # Run your existing retrieval + cleaning logic
    answers = logic.retrieve_answers(text, payload.questions)
    cleaned_answers = [clean_answer(ans) for ans in answers]
    return QueryResponse(answers=cleaned_answers)
