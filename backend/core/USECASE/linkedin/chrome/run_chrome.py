import os
import random
import sys
import time
from typing import Optional

from data.database import supabase_client
from core.configurations.config_chrome import config_chrome
from core.USECASE.linkedin.login_linkedin import login_linkedin
from core.USECASE.linkedin.post_message import post_message
from core.USECASE.linkedin.request_connexion import request_connexion
from core.USECASE.linkedin.send_message import send_message
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ProspectionRequest(BaseModel):
    intitule: str
    details: Optional[str] = None
    offre: Optional[str] = None


def run_chrome(
    job_title: str,
    details: str,
    mode: str,
    offre,
    post,
    config_db,
    telephone,
    full_name: str = "",
    cabinet_name: str = "",
):

    uid = config_db.get("user_id")
    driver = config_chrome(config_db)
    current_url = ""

    print(f"[DEBUG] User ID: {uid}")
    print(f"[DEBUG] Offre : {offre}")
    print(f"[DEBUG] Entrée dans run_chrome pour: {job_title}")
    print(f"[DEBUG] Détails de la prospection : {details}")
    print(f"[DEBUG] Mode : {mode}")
    print(f"CONFIG DB: {config_db}")

    if driver is not None:
        try:
            yield "Lancement..."
            time.sleep(random.uniform(3, 6))
            yield "On tente l'accès à linkedin"

            driver.get("https://www.linkedin.com/feed/")
            yield "Accès à LinkedIn..."
            time.sleep(random.uniform(3, 6))
            current_url = driver.current_url
            print("Current URL:", current_url)

        except Exception as e:
            print(f"Erreur réseau : {e}")

        if "login" in driver.current_url or "uas" in driver.current_url:
            login_linkedin(driver, uid, job_title, supabase_client, config_db)

        try:
            yield from post_message(driver, post, config_db)
            time.sleep(5)
            yield from request_connexion(job_title, driver, config_db)
            yield from send_message(
                driver, job_title, offre, mode, config_db, details, telephone, full_name
            )

        finally:
            config_id = config_db.get("id")
            if config_id:
                try:
                    supabase_client.table("prospection_settings").update(
                        {"is_active": False}
                    ).eq("id", config_id).execute()

                except Exception as e:
                    if "204" not in str(e) and "Missing response" not in str(e):
                        print(f"Erreur DB: {e}")
                    else:
                        print(f"Log technique: {e}")

        yield "--- Invitations terminées, Nous avons envoyé {count} invitations ---"
