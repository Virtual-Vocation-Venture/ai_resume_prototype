import fitz  # PyMuPDF for PDF extraction

def extract_text_from_pdf(pdf_file):
    """Extracts text from the given PDF file."""
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
