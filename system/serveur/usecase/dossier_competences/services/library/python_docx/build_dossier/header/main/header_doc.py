from docx.shared import Cm
from usecase.dossier_competences.services.library.python_docx.build_dossier.header.left.header_left import header_left

from usecase.dossier_competences.services.library.python_docx.build_dossier.header.right.header_right import \
    header_right

def header_doc(doc, data, logo_path):
    table = doc.sections[0].header.add_table(rows=1, cols=2, width=Cm(17))
    table.style = None
    doc.sections[0].left_margin = Cm(2)

    table.columns[0].width = Cm(6.44)
    table.columns[1].width = Cm(11.45)
    cells = table.rows[0].cells

    header_left(logo_path, cells[0])
    header_right(data, cells[1])