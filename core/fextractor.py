#PyMuPDF (fitz) to open the PDF, For each page extracting plain text.

import fitz  # PyMuPDF - pdf parser
from pathlib import Path

def extract_resume_text(pdf_path: Path) -> str:  #takes the path to a resume pdf and returns a single string containing all texts
    try:
        text = []
        with fitz.open(pdf_path) as doc:
            for page in doc: #loops through all pages and extracts text
                text.append(page.get_text("text"))
        return "\n".join(text) # Combine text from all pages to a big string
    except Exception:
        return ""
