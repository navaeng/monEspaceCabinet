import os
import threading
import unicodedata
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, cast

from core.generate_dossier import generate_dossier_api, validate_cv_file
from database import supabase_client
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from postgrest.base_request_builder import APIResponse
from pydantic import BaseModel
from workflow.start_prospect_auto import start_prospect_auto


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=start_prospect_auto, daemon=True)
    thread.start()
    print("🔥 Serveur prêt, check Supabase au démarrage...")
    yield


app = FastAPI(title="Fillcloud API", version="1.0.0", lifespan=lifespan)
KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
prospection_lock = Lock()

# Configuration CORS pour autoriser le front React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  #
        "https://nava-eng.vercel.app",
        "https://fillcloud.vercel.app",
        "https://fillcloud-m938kynst-ishaks-projects-1e2e49cc.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


@app.get("/")
async def root():
    """Endpoint de test"""

    return {
        "message": "Fillcloud API is running",
        "status": "ok",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "generate": "/api/generate-dossier",
            "health": "/api/health",
        },
    }


@app.post("/api/generate-dossier")
async def generate_dossier(
    cv: UploadFile = File(..., description="Fichier CV (PDF ou DOCX)"),
    add_skills: bool = Form(..., description="Ajouter plus de compétences"),
    english_cv: bool = Form(False, description="CV en anglais"),
):
    print("Génération en cours")

    allowed_types = [  # allowlist
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
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

    temp_cv_path = None
    output_path = None

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clear_name = strip_accents(cv.filename).replace(" ", "_")
        temp_cv_path = UPLOAD_DIR / f"{timestamp}_{clear_name}"

        with open(temp_cv_path, "wb") as buffer:
            buffer.write(cv_content)

        print(f"✅ Fichier sauvegardé: {temp_cv_path}")

        if not validate_cv_file(str(temp_cv_path)):
            raise HTTPException(
                status_code=400, detail="Fichier CV invalide ou corrompu"
            )

        output_filename = f"dossier_{timestamp}_{clear_name.replace('.pdf', '').replace('.docx', '')}.docx"
        output_path = OUTPUT_DIR / output_filename

        print(f"🔄 Début de la génération...")
        result = generate_dossier_api(
            selected_file=str(temp_cv_path),
            output_path=str(output_path),
            add_skills=add_skills,
            english_cv=english_cv,
            progress_callback=lambda msg: print(f"   {msg}"),
        )

        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["message"])

        if not output_path.exists():
            raise HTTPException(
                status_code=500, detail="Le fichier n'a pas été généré correctement"
            )

        print(f"✅ Génération terminée: {output_path}")
        print(f"{'=' * 60}\n")

        return FileResponse(
            path=str(output_path),
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename={output_filename}",
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

    finally:
        if temp_cv_path and temp_cv_path.exists():
            try:
                os.remove(temp_cv_path)
                print(f"🗑️  Fichier temporaire supprimé: {temp_cv_path.name}")
            except Exception as e:
                print(f"⚠️  Erreur lors du nettoyage: {e}")  # delete cv


class ProspectionRequest(BaseModel):  # contrat
    intitule: str


@app.get("/backend/prospection/list")
async def get_prospection():
    try:
        res = (
            supabase_client.table("prospection_settings")
            .select("id, job_title, created_at, is_active")
            .order("created_at", desc=True)
            .execute()
        )
        return res.data if res.data else []
    except Exception as e:
        print(f"Erreur Supabase List: {e}")
        return []


@app.post("/backend/prospection/start_prospection")
async def start_prospection(
    request: ProspectionRequest, background_tasks: BackgroundTasks
):
    if not prospection_lock.acquire(blocking=False):
        return {"status": "error", "message": "Prospection déjà en cours"}
    try:
        from prospection.start_prospection import run_chrome

        SELECT_QUERY = f"*,profiles!inner(linkedin_email,linkedin_password:pgp_sym_decrypt(linkedin_password::bytea,'{KEY_SECRET}'))"

        if SELECT_QUERY:
            try:
                res = supabase_client.rpc(
                    "get_decrypted_settings",
                    {"job_title_input": request.intitule, "key_input": KEY_SECRET},
                ).execute()
                if not res or res.data is None:
                    return {
                        "status": "error",
                        "message": "Impossible de charger les données",
                    }
            except Exception as e:
                print(f"❌ ERREUR SUPABASE SELECT : {e}")
                prospection_lock.release()
                return {
                    "status": "error",
                    "message": f"Erreur base de données : {str(e)}",
                }
            try:
                supabase_client.table("prospection_settings").insert(
                    {
                        "job_title": request.intitule,
                        "query": request.intitule,
                        "is_active": True,
                        "user_id": "75578010-bb83-46b3-8b98-7851899d3b18",
                        "hour_start": datetime.now().astimezone().isoformat(),
                    }
                ).execute()
            except Exception as e:
                print(f"❌ ERREUR SUPABASE INSERT : {e}")

        response = cast(APIResponse, res)
        if res and hasattr(res, "data") and res.data:
            data_list = (
                cast(List[Dict[str, Any]], response.data) if response.data else []
            )
            data = data_list[0] if data_list else {}

            profile = data.get("profiles", {})
            config_db = {
                "id": data.get("id"),
                "linkedin_email": profile.get("linkedin_email"),
                "linkedin_password": profile.get("linkedin_password"),
                "job_title": request.intitule,
            }

            def wrapped_generator():
                try:
                    yield from run_chrome(request.intitule, config_db)
                finally:
                    prospection_lock.release()

            return StreamingResponse(wrapped_generator(), media_type="text/plain")

    except Exception as e:
        return {"status": "error", "message": str(e)}
        print(f"❌ ERREUR SUPABASE DERNIER EXCEPT : {e}")


@app.post("/start-async")
async def trigger_prospection(background_tasks: BackgroundTasks):
    from fastapi import BackgroundTasks

    background_tasks.add_task(start_prospect_auto)
    return {"status": "success", "message": "Prospection démarrée"}


@app.post("/start-async")
async def start_prospection_alone(background_tasks: BackgroundTasks):
    background_tasks.add_task(start_prospect_auto)
    return {"status": "success", "message": "Prospection démarrée"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000)  # config
