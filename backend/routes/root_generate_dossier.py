from fastapi import UploadFile, HTTPException, Form, File, APIRouter
from starlette.responses import FileResponse

from core.USECASE.dossier_competences.generate_dossier import generate_dossier

router_start_generate_dossier = APIRouter()

@router_start_generate_dossier.post("/endpoint/generate-dossier")
async def root_generate_dossier(
    cv: UploadFile = File(..., description="Fichier CV (PDF ou DOCX)"),
    add_skills: bool = Form(..., description="Ajouter plus de compétences"),
    english_cv: bool = Form(False, description="CV en anglais"),
):
    temp_cv_path = None
    output_path = None

    allowed_types = [  # allowlist
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        # "application/msword",
    ]
    if cv.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Type de fichier non supporté: {cv.content_type}. Utilisez PDF ou DOCX.",
        )
    max_size = 10 * 1024 * 1024
    cv_content = await cv.read()
    if len(cv_content) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"Fichier trop volumineux ({len(cv_content) / 1024 / 1024:.2f} MB). Taille maximale: 10 MB",
        )

    try:
        result = generate_dossier(
            selected_file=str(temp_cv_path),
            output_path=str(output_path),
            add_skills=add_skills,
            english_cv=english_cv,
            progress_callback=lambda msg: print(f"   {msg}"),
        )
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["message"])
        if temp_cv_path and temp_cv_path.exists():
            raise HTTPException(
                status_code=500, detail="Le fichier n'a pas été généré correctement"
            )
        print(f"✅ Génération terminée: {output_path}")
        # print(f"{'=' * 60}\n")
        return FileResponse(
            path=str(output_path),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "X-Generation-Success": "true",
            },
        )  # keep file
    except HTTPException:
        raise
    except Exception as e:
        import traceback  # get error
        error_detail = traceback.format_exc()
        print(f"❌ ERREUR:\n{error_detail}")
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la génération du dossier: {str(e)}"
        )
