import os
from docxtpl import DocxTemplate

from USECASE.dossier_competences.jinja2.create_jinra_env import create_jinra_env


def render_document(data, output_path):

    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..", "ressources", "template_4.docx")

    doc = DocxTemplate(template_path)
    create_jinra_env(doc)

    doc.render({"data": data})
    doc.save(output_path)