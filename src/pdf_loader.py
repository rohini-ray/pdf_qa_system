from pypdf import PdfReader

def extract_text(pdf_path):
    """
    Extracts plain text from all pages of a PDF file.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text
