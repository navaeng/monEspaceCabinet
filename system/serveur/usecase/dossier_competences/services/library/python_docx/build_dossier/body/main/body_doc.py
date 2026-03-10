from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.competences.build_section_competences import \
    build_section_competences
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.experiences.build.build_section_experiences import \
    build_section_experiences
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.formations.build_section_formation import \
    build_section_formation
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.langues.build_section_langues import \
    build_section_langues
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.outils.build_section_outils import \
    build_section_outils
from usecase.dossier_competences.services.library.python_docx.build_dossier.body.sections.secteurs_activites.build_section_secteurs_activites import \
    build_section_secteurs_activites

def body_doc(doc, data):
    if 'Compétences_Clefs' in data:
        build_section_competences(doc, data)

    if 'Logiciels_Et_Outils' in data:
        build_section_outils(doc, data)

    if 'Secteurs_Activités' in data:
        build_section_secteurs_activites(doc, data)

    if 'Diplômes_Et_Formations' in data:
        build_section_formation(doc, data)

    if 'Langues_Étrangères' in data:
        build_section_langues(doc, data)

    if 'Expériences_Professionnelles' in data:
        build_section_experiences(doc, data)