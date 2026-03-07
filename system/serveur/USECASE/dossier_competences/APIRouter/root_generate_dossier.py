from fastapi import HTTPException, UploadFile, File, Form, APIRouter
from starlette.responses import FileResponse

from USECASE.dossier_competences.services.cv.process_cv_to_dossier import process_cv_to_dossier

router_start_generate_dossier = APIRouter()

@router_start_generate_dossier.post("/endpoint/generate_dossier")
async def root_generate_dossier(cv: UploadFile = File(...), add_skills: bool = Form(...),
                                english_cv: bool = Form(False)):

    output_path = await process_cv_to_dossier(await cv.read(), cv.filename, add_skills, english_cv)

    if not output_path:
        raise HTTPException(status_code=500, detail="error.")

    return FileResponse(path=str(output_path),
                        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")