import os
import threading
import unicodedata
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

# from threading import Lock
from typing import Any, Dict, List, Optional, cast

from core.generate_dossier import generate_dossier_api, validate_cv_file
from database import supabase_client
from fastapi import (
    # BackgroundTasks,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from lock import prospection_lock
from locks import user_lock
from postgrest.base_request_builder import APIResponse
from prospection.start_prospection import run_chrome
from pydantic import BaseModel
from workflow.start_prospect_auto import start_prospect_auto


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        supabase_client.table("prospection_settings").update({"is_active": False}).neq(
            "id", -1
        ).execute()
        print("Supabase : Tous les statuts ont été réinitialisés.")
    except Exception as e:
        print(f"⚠️ Erreur reset démarrage: {e}")
    thread = threading.Thread(target=start_prospect_auto, daemon=True)
    thread.start()
    print("🔥 Serveur prêt, check Supabase au démarrage...")
    yield


app = FastAPI(title="Fillcloud API", version="1.0.0", lifespan=lifespan)
KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
print(f"KEY: {KEY_SECRET}")


# Configuration CORS pour autoriser le front React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    mode: str
    details: str
    offre: Optional[str]


@app.get("/backend/prospection/list")
async def get_prospection(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        print("❌ Authentification manquante")
        raise HTTPException(status_code=401)

    token = auth_header.replace("Bearer ", "")

    try:
        user_response = supabase_client.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Authentification invalide")
        # if not user_response.user:
        #     return []
        current_user_id = user_response.user.id
        print(f"👤 Utilisateur connecté: {current_user_id}")

        res = (
            supabase_client.table("prospection_settings")
            .select("id, job_title, created_at, is_active, hour_start")
            .eq("user_id", current_user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return res.data if res.data else []

    except Exception as e:
        print(f"Erreur Supabase List: {e}")
        return []


@app.post("/backend/prospection/start_prospection")
async def start_prospection(
    body: ProspectionRequest,
    # background_tasks: BackgroundTasks,
    request: Request,
):

    print("⏳ lancement...")

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        print("❌ Authentification manquante")
        return {"status": "error", "message": "Authentification manquante"}

    token = auth_header.replace("Bearer ", "")

    try:
        user_response = supabase_client.auth.get_user(token)
        print(f"User response: {user_response}")
        print(f"token:{token}")
        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Authentification invalide")
        current_user_id = user_response.user.id
        print(f"✅ Utilisateur authentifié : {current_user_id}")
    except Exception as e:
        print(f"Erreur Supabase User: {e}")
        return {"status": "error", "message": "Erreur lors de l'authentification"}

    if current_user_id not in user_lock:
        user_lock[current_user_id] = threading.Lock()

    supabase_client.table("prospection_settings").update({"is_active": False}).eq(
        "user_id", current_user_id
    ).execute()
    # supabase_client.table("prospection_settings").update({"is_active": False}).eq(
    #     "user_id", current_user_id
    # ).execute()
    print(f"DEBUG: Requête reçue pour {body.intitule}")
    if not user_lock[current_user_id].acquire(blocking=False):
        # print("❌ LOCK BLOQUÉ : Une autre instance tourne déjà")
        print(f"❌{current_user_id} vous avez déja un lancement en cours")
        return {"status": "error", "message": "Prospection déjà en cours"}

    try:
        print("🔒 LOCK ACQUIS")

        SELECT_QUERY = f"*,profiles!inner(linkedin_email,linkedin_password:pgp_sym_decrypt(linkedin_password::bytea,'{KEY_SECRET}'))"
        if SELECT_QUERY:
            try:
                print("🔒 insert db")
                supabase_client.table("prospection_settings").insert(
                    {
                        "job_title": body.intitule,
                        "query": body.intitule,
                        "is_active": True,
                        "details": body.details,
                        "offre": body.offre or "".replace("\x00", ""),
                        "user_id": current_user_id,
                        "hour_start": datetime.now().astimezone().isoformat(),
                    }
                ).execute()
            except Exception as e:
                print(f"❌ ERREUR SUPABASE INSERT : {e}")

            print("🔒 select db")
            print("⏳ Tentative d'appel RPC...")
            res = supabase_client.rpc(
                "get_decrypted_settings",
                {"job_title_input": body.intitule, "key_input": KEY_SECRET},
            ).execute()
            print(f"🔍 DEBUG - Données brutes RPC: {res.data}")
            print(f"🔍 DEBUG - Type de données: {type(res.data)}")

    except Exception as e:
        print(f"❌ ERREUR RPC : {e}")

        #             print("RPC terminée...")

        response = cast(APIResponse, res)
        if res and hasattr(res, "data") and res.data:
            data_list = (
                cast(List[Dict[str, Any]], response.data) if response.data else []
            )
            data = data_list[0] if data_list else {}
            print(f"🔍 DEBUG - Contenu de data: {data}")
            print(f"🔍 DEBUG - Clés disponibles: {data.keys() if data else 'VIDE'}")

            config_db = {
                "id": data.get("id"),
                "user_id": current_user_id,
                "linkedin_email": data.get("linkedin_email"),
                "linkedin_password": data.get("linkedin_password"),
                "job_title": body.intitule,
            }
            print(f"📧 Email récupéré: {config_db.get('linkedin_email')}")
            print(
                f"Password récupéré: {'OUI' if config_db.get('linkedin_password') else 'NON'}"
            )

            def stream_generator():
                try:
                    print(f"🚀 Lancement Chrome pour {body.intitule}")
                    for step in run_chrome(
                        body.intitule,
                        body.details,
                        body.mode,
                        body.offre,
                        config_db,
                    ):
                        yield f"{step}\n"
                except Exception as e:
                    import traceback

                    traceback.print_exc()
                    print(f"Erreur lors de la prospection : {str(e)}")
                    # yield f"❌ Erreur : {str(e)}\n"
                finally:
                    supabase_client.table("prospection_settings").update(
                        {"is_active": False}
                    ).not_.is_("id", "null").execute()
                    if prospection_lock.locked():
                        prospection_lock.release()
                    print("🔓 Session terminée")

            return StreamingResponse(stream_generator(), media_type="text/plain")

            # def run_in_background(job_title, config):
            #     print(f"🚀🚀🚀 BACKGROUND TASK STARTED pour {job_title}")
            #     print(f"🔍 Config reçue: {config}")
            #     try:
            #         for step in run_chrome(body.intitule, config):
            #             print(f"🤖 [DEBUG] Étape {step}")
            #     except Exception as e:
            #         print(f"💥 CRASH DANS LE BACKGROUND : {e}")
            #         return {
            #             "status": "error",
            #             "message": f"Erreur pendant l'exécution : {str(e)}",
            #         }
            #     finally:
            #         try:
            #             supabase_client.table("prospection_settings").update(
            #                 {"is_active": False}
            #             ).not_.is_("id", "null").execute()
            #             print("✅ DB: Statut réinitialisé à False")
            #         except Exception as e:
            #             print(f"❌ ERREUR SUPABASE UPDATE : {e}")
            #             pass
            #         if prospection_lock.locked():
            #             prospection_lock.release()
            #             print("🔓 LOCK LIBÉRÉ")

            # print(f"DEBUG CONFIG: {config_db}")
            # background_tasks.add_task(run_in_background, body.intitule, config_db)

            # return {"status": "success", "message": "Chrome va se lancer"}


# print(f"DEBUG CONFIG: {config_db}")
# background_tasks.add_task(
#     run_in_background, request.intitule, config_db
# )

#                 return {"status": "success", "message": "Chrome va se lancer"}

#             if not res or res.data is None:
#                 return {
#                     "status": "error",
#                     "message": "Impossible de charger les données",
#                 }
#     except Exception as e:
#         print(f"❌ ERREUR SUPABASE SELECT : {e}")
#         prospection_lock.release()
#         return {
#             "status": "error",
#             "message": f"Erreur base de données : {str(e)}",
#         }


# @app.post("/api/prospection/async-stream")
# async def start_prospection_stream(request: ProspectionRequest):
#     supabase_client.table("prospection_settings").update({"is_active": False}).not_.is_(
#         "id", "null"
#     ).execute()
#     try:
#         res = supabase_client.rpc(
#             "get_decrypted_settings",
#             {"job_title_input": request.intitule, "key_input": KEY_SECRET},
#         ).execute()

#         if not res.data:
#             return {"status": "error", "message": "Config introuvable"}
#             prospection_lock.release()
#         response = cast(APIResponse, res)

#         data_list = cast(List[Dict[str, Any]], response.data) if response.data else []
#         data = data_list[0] if data_list else {}

#         profile = data.get("profiles", {})
#         config_db = {
#             "id": data.get("id"),
#             "linkedin_email": profile.get("linkedin_email"),
#             "linkedin_password": profile.get("linkedin_password"),
#             "job_title": request.intitule,
#         }
#     except Exception as e:
#         return {"status": "error", "message": f"Erreur DB : {str(e)}"}

#     def wrapped_generator():
#         if not prospection_lock.acquire(blocking=False):
#             yield "⚠️ Déjà en cours"
#             return
#         try:
#             yield from run_chrome(request.intitule, config_db)
#         finally:
#             prospection_lock.release()

#     return StreamingResponse(wrapped_generator(), media_type="text/plain")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000)  # config
