from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import RGBColor, Cm
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.blue_line import blue_line
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.cellule_gauche import cellule_gauche
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.celluledroite import cellule_droite
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.cellulemilieu import cellule_milieu
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.display_mission import display_mission
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.display_tasks import display_tasks

def build_section_experiences(doc, data):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    run = p.add_run("Expériences")
    run.font.color.rgb =  RGBColor(0x00, 0x20, 0x60)
    run.font.bold = True

    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="002060"/>')
    p._element.get_or_add_pPr().append(shd)

    for exp in data.get('Expériences', []):
        table = doc.add_table(rows=1, cols=3)
        table.columns[0].width = Cm(7)
        table.columns[1].width = Cm(4)
        table.columns[2].width = Cm(6)
        table.style = None

        cellule_gauche(table, exp)
        cellule_milieu(table, exp)
        cellule_droite(table, exp)
        blue_line(table)

        if exp.get('Mission'):
            display_mission(doc, exp)

        display_tasks(doc, exp)