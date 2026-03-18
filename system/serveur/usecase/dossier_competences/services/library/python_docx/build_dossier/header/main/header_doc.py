from docx.shared import Cm, Pt
from usecase.dossier_competences.services.library.python_docx.build_dossier.header.left.header_left import header_left
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from usecase.dossier_competences.services.library.python_docx.build_dossier.header.right.header_right import \
    header_right

def header_doc(doc, data, logo_path):
    p = doc.sections[0].header.paragraphs[0]
    p.paragraph_format.tab_stops.add_tab_stop(Cm(17), WD_TAB_ALIGNMENT.RIGHT)

    header_left(logo_path, p)
    p.add_run("\t")
    header_right(doc, data, p)