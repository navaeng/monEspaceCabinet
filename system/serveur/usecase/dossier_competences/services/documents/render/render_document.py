import io

from docx import Document
from docx.shared import Cm

from usecase.dossier_competences.services.library.python_docx.build_dossier.body.main.body_doc import body_doc
from usecase.dossier_competences.services.library.python_docx.build_dossier.footer.main.footer_doc import footer_doc
from usecase.dossier_competences.services.library.python_docx.build_dossier.header.main.header_doc import header_doc
from cloud.S3.get_logo import get_logo
from usecase.dossier_competences.services.library.python_docx.build_dossier.marge.add_marge import add_marge


def render_document(data):

    logo_path = get_logo()
    doc = Document()
    doc.sections[0].left_margin = Cm(2)

    add_marge(doc)

    header_doc(doc, data, logo_path)
    body_doc(doc, data)
    footer_doc(doc, data)

    file_stream = io.BytesIO()

    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream