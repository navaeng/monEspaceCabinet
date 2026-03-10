from usecase.dossier_competences.json.templates.competences.competences_template import competences_template
from usecase.dossier_competences.json.templates.experiences.experiences_template import experiences_template
from usecase.dossier_competences.json.templates.formations.formation_template import formation_template
from usecase.dossier_competences.json.templates.identite.identite_template import identite_template
from usecase.dossier_competences.json.templates.outils.outils_template import outils_template

def config_ia():

    config = [
        ("google/gemini-3.1-flash-lite-preview", identite_template()),
        ("nousresearch/hermes-4-405b", outils_template()),
        ("meta-llama/llama-3.1-70b-instruct", competences_template()),
        ("nousresearch/hermes-4-405b", formation_template()),
        ("nousresearch/hermes-4-405b", experiences_template()),
    ]
    return config


