from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import RGBColor, Pt, Cm

def build_section_competences(doc, data):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("DOMAINES DE COMPETENCES")
    RGBColor(255, 255, 255)
    run.font.bold = True


    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="002060"/>')
    p._element.get_or_add_pPr().append(shd)
    p.paragraph_format.keep_with_next = True

    for comp in data.get('competences', []):
        p_item = doc.add_paragraph(comp, style='List Bullet')
        p_item.paragraph_format.keep_together = True
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.left_indent = Pt(20)