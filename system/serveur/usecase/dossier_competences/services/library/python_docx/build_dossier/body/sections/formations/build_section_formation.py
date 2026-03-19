from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import RGBColor, Cm

from usecase.dossier_competences.services.library.python_docx.build_dossier.body.header_section.header_section import \
    header_section
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.formations.cells.left_cells import \
    left_cells
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.formations.cells.right_cells import \
    right_cells


def build_section_formation(doc, data):

    formations = data.get('Diplômes_Et_Formations_Antéchronologiques') or []

    if not formations or not formations[0].get('Diplôme'):
        return

    header_section(doc, "FORMATIONS/DIPLOMES")

    for diplome in data.get('Diplômes_Et_Formations_Antéchronologiques', []):
        table = doc.add_table(rows=1, cols=2)

        table.style = None
        cells = table.rows[0].cells
        table.columns[0].width = Cm(14)
        table.columns[1].width = Cm(3)

        for row in table.rows:
            row._tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit {nsdecls("w")} w:val="1"/>'))

        if diplome.get('Diplôme'):
            left_cells(cells, diplome)

        if diplome.get('Année'):
            right_cells(cells, diplome)