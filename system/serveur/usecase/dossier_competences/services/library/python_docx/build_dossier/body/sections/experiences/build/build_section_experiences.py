from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from docx.shared import RGBColor, Cm
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.blue_line import blue_line
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.cellule_gauche import cellule_gauche
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.cellule_droite import cellule_droite
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.cellule_milieu import cellule_milieu
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.display_logiciels_outils import \
    display_logiciels_outils
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.display_poste import \
    display_poste
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.display_mission import display_mission
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.display_tasks import \
    display_tasks


def build_section_experiences(doc, data):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("EXPERIENCES PROFESIONELLES")
    run.font.color.rgb =  RGBColor(255, 255, 255)
    run.font.bold = True

    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="002060"/>')
    p._element.get_or_add_pPr().append(shd)
    p.paragraph_format.keep_with_next = True

    for exp in data.get('Expériences_Professionnelles', []):
        table = doc.add_table(rows=1, cols=3)
        table.style = None

        cellule_gauche(table, exp)
        cellule_milieu(table, exp)
        cellule_droite(table, exp)
        blue_line(table)

        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.keep_with_next = True

        if exp.get("Poste_Occupé"):
            display_poste(doc, exp)

        if exp.get('Résumé_concis_des_missions'):
            display_mission(doc, exp)

        if exp.get('Liste_Tâches'):
            display_tasks(doc, exp)

        if exp.get("Environnement_Technique"):
            display_logiciels_outils(doc, exp)

        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()
            cantSplit = OxmlElement('w:cantSplit')
            cantSplit.set(qn('w:val'), '1')
            trPr.append(cantSplit)