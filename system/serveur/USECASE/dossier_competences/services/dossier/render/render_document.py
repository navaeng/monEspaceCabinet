from docx import Document

from USECASE.dossier_competences.library.python_docx.header.header_doc import header_doc


def render_document(data, output_path, logo_path):
    doc = Document()
    header_doc(doc, data, logo_path)
    doc.save(output_path)