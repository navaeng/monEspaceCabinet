from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import RGBColor, Pt, Cm

def build_section_outils(doc, data):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("OUTILS")
    run.font.color.rgb =  RGBColor(255, 255, 255)
    run.font.bold = True

    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="002060"/>')

    p._element.get_or_add_pPr().append(shd)
    p.paragraph_format.keep_with_next = True

    for categorie in data.get('Logiciels_par_titre', []):
        print(categorie)
        titre = categorie.get('titre', '')
        logiciels_outils = categorie.get('logiciels_outils', [])

        if titre and logiciels_outils:
            p = doc.add_paragraph()

            run_t = p.add_run(f"{titre.upper()} : ")
            run_t.bold = True

            p.add_run(", ".join(logiciels_outils))

            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True