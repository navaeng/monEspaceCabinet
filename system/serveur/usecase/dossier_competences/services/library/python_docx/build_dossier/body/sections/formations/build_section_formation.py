from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Pt, RGBColor


def build_section_formation(doc, data):
    p_titre = doc.add_paragraph()
    p_titre.alignment = 1  # Centré
    run_titre = p_titre.add_run("FORMATIONS")
    run_titre.font.bold = True
    run_titre.font.color.rgb = RGBColor(255, 255, 255)
    p_titre._element.get_or_add_pPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="002060"/>'))

    for diplome in data.get('Diplômes', []):
        p = doc.add_paragraph()
        run = p.add_run(f"{diplome.get('Année')} : {diplome.get('Diplôme')}")
        run.bold = False
        p.add_run(f"\n{diplome.get('École')} - {diplome.get('Lieu')}")
        p.paragraph_format.space_after = Pt(8)