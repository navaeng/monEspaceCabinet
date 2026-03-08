from docx import Document

from USECASE.dossier_competences.services.library.python_docx.build_dossier.header.header_doc import header_doc
from cloud.S3.get_logo import get_logo


def render_document(data, output_path):
    logo_path = get_logo()
    doc = Document()
    header_doc(doc, data, logo_path)
    doc.save(output_path)