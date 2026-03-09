from docx.shared import Cm, Pt
from usecase.dossier_competences.services.library.python_docx.build_dossier.header.left.header_left import header_left

from usecase.dossier_competences.services.library.python_docx.build_dossier.header.right.header_right import \
    header_right

def header_doc(doc, data, logo_path):
    table = doc.sections[0].header.add_table(rows=1, cols=2, width=Cm(17))
    p = doc.sections[0].header.add_paragraph()
    p.paragraph_format.space_after = Pt(6)

    table.columns[0].width = Cm(3)
    table.columns[1].width = Cm(14)

    cells = table.rows[0].cells

    header_left(logo_path, cells[0])
    header_right(data, cells[1])