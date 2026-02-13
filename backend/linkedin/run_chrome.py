import os
import random
import sys
import time
from typing import Optional

from configurations.config_chrome import config_chrome
from database import supabase_client
from httpx import post
from linkedin.post_message import post_message
from linkedin.send_message import send_message
from login_linkedin import login_linkedin
from pydantic import BaseModel
from request_connexion import request_connexion
from selenium.webdriver.common.by import By
from treatment.behavior.mouse import human_mouse_move

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ProspectionRequest(BaseModel):
    intitule: str
    details: Optional[str] = None
    offre: Optional[str] = None


def run_chrome(
    driver,
    job_title: str,
    details: str,
    mode: str,
    offre,
    config_db,
    telephone,
    full_name,
):
    config_chrome(config_db)

    uid = config_db.get("user_id")
    print(f"[DEBUG] User ID: {uid}")
    print(f"[DEBUG] Offre : {offre}")
    print(f"[DEBUG] Entrée dans run_chrome pour: {job_title}")
    print(f"[DEBUG] Détails de la prospection : {details}")
    print(f"[DEBUG] Mode : {mode}")
    print(f"CONFIG DB: {config_db}")

    try:
        yield "Lancement..."
        time.sleep(random.uniform(3, 6))
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
        yield from post_message(driver, post)
        time.sleep(5)
        yield from request_connexion(job_title, driver, config_db)
        yield from send_message(
            driver, job_title, offre, mode, config_db, details, telephone, full_name
        )

        for page in range(1, 2):
            time.sleep(random.uniform(8, 12))
            human_mouse_move(driver)

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
