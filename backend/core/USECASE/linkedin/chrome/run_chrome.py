import os
import random
import sys
import time

from core.query.linkedin.update_is_active_false import update_is_active_false
from data.database import supabase_client
from core.configurations.config_chrome import config_chrome
from core.USECASE.linkedin.login_linkedin import login_linkedin
from core.USECASE.linkedin.post_message import post_message
from core.USECASE.linkedin.request_connexion import request_connexion
from core.USECASE.linkedin.send_message import send_message

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_chrome(
    job_title: str,
    details: str,
    mode: str,
    post,
    user_data,
):

    uid = user_data.get("user_id")
    driver = config_chrome(user_data)

    print(f"[DEBUG] User ID: {uid}")
    print(f"[DEBUG] Entrée dans run_chrome pour: {job_title}")
    print(f"[DEBUG] Détails de la prospection : {details}")
    print(f"[DEBUG] Mode : {mode}")
    print(f"CONFIG DB: {user_data}")

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
            login_linkedin(driver, uid, job_title, supabase_client, user_data)

        try:
            yield from post_message(driver, post, user_data)
            time.sleep(5)
            yield from request_connexion(job_title, driver, user_data)
            yield from send_message(
                driver, job_title
            )

        finally:
            update_is_active_false()

        yield "--- Invitations terminées, Nous avons envoyé {count} invitations ---"
