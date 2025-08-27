
import os
from PyPDF2 import PdfReader
import docx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_MODEL = "gpt-4o"

DOCUMENTS = {}



def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def store_document(doc_id, text):
    DOCUMENTS[doc_id] = text

def get_document(doc_id):
    return DOCUMENTS.get(doc_id)

def get_next_doc_id():
    return str(len(DOCUMENTS) + 1)

def get_openai_answer(document_text, question):
    prompt = f"""
    You are a helpful medical assistant. Use the following document content to answer questions:

    Document:
    {document_text[:6000]}

    Question: {question}
    """
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a knowledgeable medical assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
 
