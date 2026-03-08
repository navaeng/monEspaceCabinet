from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Pt, RGBColor

def build_section_langues(doc, data):
    p_titre = doc.add_paragraph()
    p_titre.alignment = 1  # Centre le titre
    run = p_titre.add_run("LANGUES")
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="002060"/>')
    p_titre._element.get_or_add_pPr().append(shd)

    for langue in data.get('Langues', []):
        p = doc.add_paragraph(style='List Bullet')
        run_l = p.add_run(f"{langue.get('langue')} : ")
        run_l.bold = True
        p.add_run(langue.get('niveau'))
        p.paragraph_format.space_after = Pt(2)