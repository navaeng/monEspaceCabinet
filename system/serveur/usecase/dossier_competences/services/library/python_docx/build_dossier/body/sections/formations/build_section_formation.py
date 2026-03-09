from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import RGBColor, Cm

from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.formations.cells.left_cells import \
    left_cells
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.formations.cells.right_cells import \
    right_cells


def build_section_formation(doc, data):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    run = p.add_run("FORMATIONS")
    run.font.color.rgb = RGBColor(0x00, 0x20, 0x60)
    run.font.bold = True
    p._element.get_or_add_pPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="002060"/>'))

    for diplome in data.get('Diplômes', []):
        table = doc.add_table(rows=1, cols=2)
        table.style = None
        cells = table.rows[0].cells
        table.columns[0].width = Cm(14)
        table.columns[1].width = Cm(3)

        left_cells(cells, diplome)
        right_cells(cells, diplome)