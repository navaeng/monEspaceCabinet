from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

POLICE = "Calibri (corps)"

def header_right(data, cell_droite):

    cell_droite.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    p1 = cell_droite.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(0)
    run1 = p1.add_run(data.get('Nom_prénom', ''))
    run1.font.name = POLICE
    run1.font.bold = True
    run1.font.size = Pt(17)
    run1.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

    p2 = cell_droite.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(0)
    run2 = p2.add_run(data.get('Poste', ''))
    run2.font.name = POLICE
    run2.font.size = Pt(14)
    run2.font.color.rgb = RGBColor(0x00, 0x20, 0x60)
    run2.font.bold = True

    p3 = cell_droite.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p3.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(0)
    run3 = p3.add_run(f"{data.get('Experience_totale', '')}")
    run3.font.name = POLICE
    run3.font.size = Pt(14)
    run3.font.color.rgb = RGBColor(0x00, 0x20, 0x60)