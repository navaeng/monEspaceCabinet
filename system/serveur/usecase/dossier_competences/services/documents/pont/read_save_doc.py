import os
from pathlib import Path
from usecase.dossier_competences.traitement.generate_dossier import generate_dossier

async def read_save_doc(cv_content: bytes, filename: str):
    temp_path = Path(f"/tmp/temp_{filename}")

    

    with open(temp_path, "wb") as f:
        f.write(cv_content)

    result = generate_dossier(str(temp_path))

    if temp_path.exists():
        os.remove(temp_path)

    return result.get("file_stream") if result.get("success") else None