import traceback

from USECASE.dossier_competences.IA.analyse.analyse_data import analyse_data
from USECASE.dossier_competences.services.dossier.render.render_document import render_document

def generate_dossier(
    selected_file: str,
    output_path: str,
) -> dict:

    try:

        #EXTRACT
        all_data = analyse_data(file_path=selected_file)
        #BUILD
        data = all_data
        #RENDER
        render_document(data, output_path)

        return {
            "success": True,
        }

    except Exception as e:
        error_msg = f"Erreur lors de la génération: {str(e)}\n{traceback.format_exc()}"
        print(f" {error_msg}")

        return {"success": False, "message": str(e), "error": error_msg}