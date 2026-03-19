from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import RGBColor, Pt, Cm

from usecase.dossier_competences.services.library.python_docx.build_dossier.body.header_section.header_section import \
    header_section


def build_section_secteurs_activites(doc, data):

    secteurs = data.get('Secteurs_Activités_Entreprises_Travaillés') or []
    if not secteurs:
        return

    header_section(doc, "SECTEURS ACTIVITES")

    for secteur in data.get('Secteurs_Activités_Entreprises_Travaillés', []):
        p_item = doc.add_paragraph(secteur, style='List Bullet')
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.left_indent = Pt(20)
        p_item.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

        print(secteur)