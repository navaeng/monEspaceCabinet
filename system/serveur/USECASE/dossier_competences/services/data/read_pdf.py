import fitz

from USECASE.dossier_competences.loops.extract_data.extract_ocr_text import extract_ocr_text
from USECASE.dossier_competences.loops.extract_data.extract_native_text import extract_native_text

def read_pdf(file_path):
    with fitz.open(file_path) as doc:
        text = extract_native_text(doc)
        if len(text.strip()) < 200:
            print("📸 PDF scanné détecté, lancement OCR...")
            text = "\n".join(extract_ocr_text(page) for page in doc)
    return text