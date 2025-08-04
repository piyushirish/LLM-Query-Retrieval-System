import fitz  # PyMuPDF
import docx
from email import message_from_string

def parse_pdf(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def parse_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_eml(path):
    with open(path, 'r') as f:
        msg = message_from_string(f.read())
    return msg.get_payload()