from fastapi import HTTPException, UploadFile, File, APIRouter
from starlette.responses import FileResponse, StreamingResponse

from usecase.dossier_competences.services.documents.pont.read_save_doc import read_save_doc
router_start_generate_dossier = APIRouter()

@router_start_generate_dossier.post("/endpoint/generate_dossier")
async def root_generate_dossier(cv: UploadFile = File(...)):

    file_stream = await read_save_doc(await cv.read(), cv.filename)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.documents",
        headers={"Content-Disposition": f"attachment; filename=dossier_{cv.filename}.docx"}
    )