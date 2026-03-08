import traceback

from usecase.dossier_competences.IA.analyse.analyse_data import analyse_data
from usecase.dossier_competences.services.documents.render.render_document import render_document

def generate_dossier(
    selected_file: str,
) -> dict:

    try:
        #EXTRACT
        all_data = analyse_data(file_path=selected_file)
        print(f"--- DEBUG ALL_DATA ---\n{all_data}\n----------------------")
        #BUILD
        data = all_data

        # RENDER
        file_stream = render_document(data)

        return {
            "success": True,
            "file_stream": file_stream
        }

    except Exception as e:
        error_msg = f"Erreur lors de la génération: {str(e)}\n{traceback.format_exc()}"
        print(f" {error_msg}")

        return {"success": False, "message": str(e), "error": error_msg}