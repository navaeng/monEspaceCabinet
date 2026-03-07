import os
import random
import sys
import time

from USECASE.linkedin.generator.request_connexion import request_connexion
from USECASE.linkedin.generator.send_message import send_message
from USECASE.linkedin.configurations.config_chrome import config_chrome
from USECASE.linkedin.generator.login_linkedin import login_linkedin
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
    print(f"user data: {user_data}")

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

            if "login" in driver.current_url:
                yield "Connexion nécessaire..."
                yield from login_linkedin(driver, user_data)

            yield from request_connexion(driver, job_title, user_data)
            yield from send_message(driver, job_title, user_data)

        except Exception as e:
            print(f"Erreur réseau : {e}")



        yield "--- Invitations terminées, Nous avons envoyé {count} invitations ---"
