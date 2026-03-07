import os

from USECASE.dossier_competences.services.data.read_docx import read_docx
from USECASE.dossier_competences.services.data.read_pdf import read_pdf


def read_cv(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = read_pdf(file_path) if ext == ".pdf" else read_docx(file_path)
    print(f"✅ Extraction terminée : {len(text)} caractères trouvés.")
    return text