import io

from docx import Document

from usecase.dossier_competences.services.library.python_docx.build_dossier.body.main.body_doc import body_doc
from usecase.dossier_competences.services.library.python_docx.build_dossier.header.main.header_doc import header_doc
from cloud.S3.get_logo import get_logo


def render_document(data):

    logo_path = get_logo()
    doc = Document()

    header_doc(doc, data, logo_path)
    body_doc(doc, data)

    file_stream = io.BytesIO()

    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream