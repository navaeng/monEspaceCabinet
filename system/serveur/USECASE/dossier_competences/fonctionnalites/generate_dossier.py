import traceback
from USECASE.dossier_competences.data.dict.build_cv_data import build_cv_data
from USECASE.dossier_competences.data.extract_and_call_prompt import (
    extract_and_call_prompt,
)
from USECASE.dossier_competences.services.render_Document import render_Document

def generate_dossier(
    selected_file: str,
    output_path: str,
    add_skills: bool,
    english_cv: bool,
) -> dict:

    try:
        #EXTRACT
        all_data, data_skills_tools, data_infos, data_diplomes, data_experiences = extract_and_call_prompt(cv_file_path=selected_file, add_skills=add_skills, english_cv=english_cv)
        #BUILD
        data = build_cv_data(data_skills_tools, data_infos, data_diplomes, data_experiences, all_data)
        #RENDER
        render_Document(data, output_path)

        return {
            "success": True,
        }

    except Exception as e:
        error_msg = f"Erreur lors de la génération: {str(e)}\n{traceback.format_exc()}"
        print(f" {error_msg}")

        return {"success": False, "message": str(e), "error": error_msg}