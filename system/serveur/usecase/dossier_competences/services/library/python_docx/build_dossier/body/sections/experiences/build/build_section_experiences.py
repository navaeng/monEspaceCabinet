from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from docx.shared import RGBColor, Cm

from usecase.dossier_competences.services.library.python_docx.build_dossier.body.header_section.header_section import \
    header_section
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.tables.blue_line import blue_line
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.tables.cellule_gauche import cellule_gauche
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.tables.cellule_droite import cellule_droite
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.tables.cellule_milieu import cellule_milieu
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.logiciels_outils.display_logiciels_outils import \
    display_logiciels_outils
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.poste.display_poste import \
    display_poste
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.mission.display_mission import display_mission
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.tasks.display_tasks import \
    display_tasks


def build_section_experiences(doc, data):

    header_section(doc, "EXPERIENCES PROFESSIONNELLES")

    for exp in data.get('Expériences_Professionnelles_Antéchronologiques', []):
        table = doc.add_table(rows=1, cols=3)
        table.style = None
        table.columns[0].width = Cm(7.11)
        table.columns[1].width = Cm(3.39)
        table.columns[2].width = Cm(6.17)

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

        if exp.get('Résumé_mission'):
            display_mission(doc, exp)

        if exp.get('Liste_Tâches'):
            display_tasks(doc, exp)

        if exp.get("Logiciels_et_outils_utilisés"):
            display_logiciels_outils(doc, exp)

        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()
            cantSplit = OxmlElement('w:cantSplit')
            cantSplit.set(qn('w:val'), '1')
            trPr.append(cantSplit)