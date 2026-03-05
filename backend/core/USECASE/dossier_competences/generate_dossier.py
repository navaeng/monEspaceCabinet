import traceback
from pathlib import Path

from data.extract_and_call_prompt import (
    extract_and_call_prompt,
)
from docxtpl import DocxTemplate
from core.USECASE.dossier_competences.jinja2 import create_jinra_env
from core.json.replace_json_element.replace_empersand import replace_ampersand
from core.json.replace_json_element.replace_level_language import (
    replace_level_language,
)
from core.ressources_path import ressources_path

from core.fix_logiciels_outils import fix_logiciels_outils


def generate_dossier(
    selected_file: str,
    output_path: str,
    add_skills: bool,
    english_cv: bool,
    progress_callback=None,
) -> dict:

    try:
        # Appeler la version API de extract_and_call_prompt
        all_data, data_skills_tools, data_infos, data_diplomes, data_experiences = (
            extract_and_call_prompt(
                cv_file_path=selected_file,
                add_skills=add_skills,
                english_cv=english_cv,
                progress_callback=progress_callback,
            )
        )

        data = {
            "cv_texte_propre": all_data,
            **(data_skills_tools or {}),
            **(data_infos or {}),
            **(data_diplomes or {}),
            **(data_experiences or {}),
        }

        if not data:
            raise ValueError("Les données du CV n'ont pas pu être extraites.")

        # Charger le template Word
        template_path = ressources_path("ressources/template_4.docx")
        doc = DocxTemplate(template_path)

        # Créer l'environnement Jinja
        create_jinra_env(doc)

        # Appliquer les transformations
        data = replace_ampersand(data)
        data = replace_level_language(data)

        if not isinstance(data, dict):
            raise ValueError(f"Erreur: data n'est pas un dict (type={type(data)})")

        # Rendre le template avec les données
        fix_logiciels_outils(data)
        doc.render(data)

        # Sauvegarder
        doc.save(output_path)

        return {
            "success": True,
            "message": "Dossier généré avec succès",
            "output_path": output_path,
        }

    except Exception as e:
        error_msg = f"Erreur lors de la génération: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_msg}")

        return {"success": False, "message": str(e), "error": error_msg}


def validate_cv_file(file_path: str) -> bool:
    path = Path(file_path)

    if not path.exists():
        return False

    valid_extensions = [".pdf", ".doc", ".docx"]
    return path.suffix.lower() in valid_extensions
