import os
from docxtpl import DocxTemplate

from USECASE.dossier_competences.jinja2.create_jinra_env import create_jinra_env
from USECASE.dossier_competences.services.fix_logiciels_outils import fix_logiciels_outils


def render_document(data, output_path):

    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ressources", "template_4.docx")

    doc = DocxTemplate(template_path)
    create_jinra_env(doc)

    fix_logiciels_outils(data)
    doc.render(data)
    doc.save(output_path)