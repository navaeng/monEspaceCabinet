import os
from pathlib import Path
from USECASE.dossier_competences.fonctionnalites.generate_dossier import generate_dossier

async def process_cv_to_dossier(cv_content: bytes, filename: str):
    temp_path = Path(f"temp_{filename}")
    output_path = Path(f"dossier_{filename}.docx")

    with open(temp_path, "wb") as f:
        f.write(cv_content)

    result = generate_dossier(str(temp_path), str(output_path))

    if temp_path.exists():
        os.remove(temp_path)

    return output_path if result.get("success") else None