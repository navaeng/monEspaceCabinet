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
        p = doc.add_paragraph()

        tab_xml = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:pos="10249"/></w:tabs>')
        p._element.get_or_add_pPr().append(tab_xml)

        run_dip = p.add_run(diplome.get('Diplôme', ''))
        run_dip.bold = True
        run_dip.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

        p.add_run('\t')

        run_date = p.add_run(str(diplome.get('Année', '')))
        run_date.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

        if diplome.get('École'):
            p_info = doc.add_paragraph()
            p_info.paragraph_format.left_indent = Cm(1.25)
            texte = diplome.get('École')
            if diplome.get('Lieu'):
                texte += f" - {diplome.get('Lieu')}"
            run_info = p_info.add_run(texte)
            run_info.font.color.rgb = RGBColor(0x00, 0x20, 0x60)