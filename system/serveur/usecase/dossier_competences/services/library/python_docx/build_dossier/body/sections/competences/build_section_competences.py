from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Pt, Cm, RGBColor

from usecase.dossier_competences.services.library.python_docx.build_dossier.body.header_section.header_section import \
    header_section


def build_section_competences(doc, data):

    comps = data.get('15_Phrases_Percutantes_Compétences') or data.get('Compétences') or []
    comps = [c for c in comps if c and c.strip()]
    if not comps: return

    header_section(doc, "DOMAINES DE COMPETENCES")

    for comp in (data.get('15_Phrases_Percutantes_Compétences') or data.get('Compétences') or []):
        p_item = doc.add_paragraph(comp, style='List Bullet')

        for run in p_item.runs:
            run.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

        p_item.paragraph_format.left_indent = Cm(1)
        p_item.paragraph_format.space_after = Pt(3)