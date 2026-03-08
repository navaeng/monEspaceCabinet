from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL

POLICE = "Arial"
COULEUR_PRINCIPALE = RGBColor(0x1B, 0x4A, 0x8A)
COULEUR_GRIS = RGBColor(0x77, 0x77, 0x77)

def header_doc(doc, data, logo_path):
    section = doc.sections[0]
    header = section.header

    table = header.add_table(rows=1, cols=2, width=Cm(17))
    table.columns[0].width = Cm(5)
    table.columns[1].width = Cm(12)

