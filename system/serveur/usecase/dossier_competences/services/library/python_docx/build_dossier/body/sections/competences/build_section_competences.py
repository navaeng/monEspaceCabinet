from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import RGBColor, Pt, Cm

from usecase.dossier_competences.services.library.python_docx.build_dossier.body.header_section.header_section import \
    header_section


def build_section_competences(doc, data):

    comps = data.get('15_Phrases_Percutantes_Compétences') or data.get('Compétences') or []
    comps = [c for c in comps if c and c.strip()]
    if not comps: return

    header_section(doc, "DOMAINES DE COMPETENCES")

    for comp in (data.get('15_Phrases_Percutantes_Compétences') or data.get('Compétences') or []):
        p_item = doc.add_paragraph(comp, style='List Bullet')
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.left_indent = Pt(20)