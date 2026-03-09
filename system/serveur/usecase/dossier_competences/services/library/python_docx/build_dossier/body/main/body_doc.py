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
    print(data.keys())
    build_section_competences(doc, data)
    build_section_outils(doc, data)
    build_section_secteurs_activites(doc, data)
    build_section_formation(doc, data)
    build_section_langues(doc, data)
    build_section_experiences(doc, data)