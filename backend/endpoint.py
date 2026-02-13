import os
import threading
import unicodedata
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, cast

import uvicorn
from core.generate_dossier import generate_dossier_api
from database import supabase_client
from fastapi import (
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from linkedin.run_chrome import run_chrome
from linkedin.start_prospect_auto import start_prospect_auto
from locks import user_lock
from postgrest.base_request_builder import APIResponse
from pydantic import BaseModel


@asynccontextmanager
async def thread_(app: FastAPI):
    thread = threading.Thread(target=start_prospect_auto, daemon=True)
    thread.start()
    print("Lancement de thread pour les lancements automatique...")
    yield


app = FastAPI(title="API workCabinet", version="1.0.0", lifespan=thread_)
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


def delete_accents(s):  # on evite d'avoir des acccents
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


@app.get("/")
async def root():
    """Endpoint principal"""

    return {
        "message": "L'application tourne !",
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

    allowed_types = [  # allowlist
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
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
        result = generate_dossier_api(
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


class ProspectionRequest(BaseModel):  # contrat
    intitule: str
    mode: str
    details: str
    telephone: str
    full_name: str
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
        current_user_id = user_response.user.id
        print(f"👤 Utilisateur connecté : {current_user_id}")

        res = (
            supabase_client.table("prospection_settings")
            .select("id, job_title, created_at, is_active, hour_start")
            .eq("user_id", current_user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return res.data if res.data else []

    except Exception as e:
        print(f"Erreur Supabase: {e}")
        return []


@app.post("/backend/linkedin/start_chrome")
async def start_chrome(
    body: ProspectionRequest,
    request: Request,
):
    print("lancement...")
    res = None

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        print("Authentification manquante")
        return {"status": "error", "message": "Authentification manquante"}

    token = auth_header.replace("Bearer ", "")

    try:
        user_response = supabase_client.auth.get_user(token)

        print(f"User response: {user_response}")
        print(f"token:{token}")

        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Authentification invalide")
        current_user_id = user_response.user.id
        print(f"Utilisateur authentifié : {current_user_id}")
    except Exception as e:
        print(f"Erreur Supabase User: {e}")
        return {"status": "error", "message": "Erreur lors de l'authentification"}

    supabase_client.table("prospection_settings").update({"is_active": False}).not_.is_(
        "id", "null"
    ).execute()

    print(f"Requête supabase reçue pour {body.intitule}")
    if not user_lock[current_user_id].acquire(blocking=False):
        # print("❌ LOCK BLOQUÉ : Une autre instance tourne déjà")
        print(f"❌{current_user_id} vous avez déja un lancement en cours")
        return {"status": "error", "message": "Prospection déjà en cours"}

    try:
        print("LOCK ACQUIS")
        print("On lance la requête")

        SELECT_QUERY = f"*,profiles!inner(linkedin_email,linkedin_password:pgp_sym_decrypt(linkedin_password::bytea,'{KEY_SECRET}'))"
        if SELECT_QUERY:
            try:
                print("insert db...")
                import random

                prochaine_heure = (
                    datetime.now().astimezone() + timedelta(days=1)
                ).replace(
                    hour=random.randint(8, 19),
                    minute=random.randint(0, 59),
                )

                supabase_client.table("prospection_settings").insert(
                    {
                        "job_title": body.intitule,
                        "query": body.intitule,
                        "is_active": True,
                        "details": body.details,
                        "offre": body.offre or "".replace("\x00", ""),
                        "user_id": current_user_id,
                        # "telephone": body.telephone or "",
                        # "full_name": body.full_name or "",
                        "hour_start": prochaine_heure.isoformat(),
                    }
                ).execute()
            except Exception as e:
                print(f" ERREUR SUPABASE INSERT : {e}")

            print("⏳ Tentative d'appel RPC...")
            res = supabase_client.rpc(
                "get_decrypted_settings",
                {"job_title_input": body.intitule, "key_input": KEY_SECRET},
            ).execute()

            print(f"🔍 DEBUG - Données brutes RPC: {res.data}")
            print(f"🔍 DEBUG - Type de données: {type(res.data)}")

            print("RPC terminée...")

            response = cast(APIResponse, res)
            if res and hasattr(res, "data") and res.data:
                data_list = (
                    cast(List[Dict[str, Any]], response.data) if response.data else []
                )
                data = data_list[0] if data_list else {}
                data["user_id"] = current_user_id
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
                            driver=None,
                            job_title=body.intitule,
                            details=body.details,
                            mode=body.mode,
                            offre=body.offre or "",
                            config_db=config_db,
                            telephone=body.telephone or "",
                            full_name=body.full_name or "",
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
                        if user_lock[current_user_id].locked():
                            user_lock[current_user_id].release()

                        print("🔓 Session terminée")

                return StreamingResponse(stream_generator(), media_type="text/plain")

            if not res or res.data is None:
                return {
                    "status": "error",
                    "message": "Impossible de charger les données",
                }
    except Exception as e:
        print(f"❌ ERREUR RPC : {e}")

    # config_db = {}

    # if res and hasattr(res, "data") and res.data:
    #     response = cast(APIResponse, res)
    #     data_list = cast(List[Dict[str, Any]], response.data) if response.data else []
    #     data = data_list[0] if data_list else {}
    #     print(f"Contenu de data: {data}")

    #     config_db = {
    #         "id": data.get("id"),
    #         "user_id": current_user_id,
    #         "linkedin_email": data.get("linkedin_email"),
    #         "linkedin_password": data.get("linkedin_password"),
    #         "job_title": body.intitule,
    #         "telephone": data.get("telephone"),
    #         "full_name": data.get("full_name"),
    #         "email": data.get("email"),
    #     }
    #     print(f"📧 Email linkedin récupéré: {config_db.get('linkedin_email')}")
    #     print(f"📧 Email récupéré: {config_db.get('email')}")
    #     print(
    #         f"Password récupéré: {'OUI' if config_db.get('linkedin_password') else 'NON'}"
    #     )

    # def stream_generator():
    #     try:
    #         print(f"DEBUG: type de config_db est {type(config_db)}")
    #         print(f"Lancement Chrome pour {body.intitule}")
    #         for step in run_chrome(
    #             driver=None,
    #             job_title=body.intitule,
    #             details=body.details,
    #             mode=body.mode,
    #             offre=body.offre or "",
    #             config_db=config_db,
    #             telephone=body.telephone,
    #             full_name=body.full_name,
    #         ):
    #             yield f"{step}\n"
    #     except Exception as e:
    #         import traceback

    #         traceback.print_exc()
    #         print(f"Erreur lors de la prospection : {str(e)}")

    #     finally:
    #         supabase_client.table("prospection_settings").update(
    #             {"is_active": False}
    #         ).not_.is_("id", "null").execute()

    #         if user_lock[current_user_id].locked():
    #             user_lock[current_user_id].release()
    #         print("Session terminée")

    # return StreamingResponse(stream_generator(), media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8001)  # config
