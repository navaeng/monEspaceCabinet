import json
import os
import random
import sys
import time

import requests

from usecase.linkedin.generator.connexions.request_connexion import request_connexion
from usecase.linkedin.generator.messages.send_message import send_message
from usecase.linkedin.chrome.configurations.config_chrome import config_chrome
from usecase.linkedin.generator.login.login_linkedin import login_linkedin
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_chrome(
    job_title: str,
    details: str,
    mode: str,
    user_data,
    post: str
):

    uid = user_data.get("user_id")
    id = user_data.get("id")
    driver = config_chrome(user_data)


    print(f"[DEBUG] JOB ID: {id}")
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
            print(requests.get("https://ipapi.co/json/").json())

            driver.get("https://www.linkedin.com/feed/")
            cookie_path = f"usecase/linkedin/cookies/cookie_{uid}.json"

            if os.path.exists(cookie_path):
                with open(cookie_path, "r") as f:
                    li_at = json.load(f)
                driver.add_cookie(li_at)
                driver.refresh()
                yield "Session restaurée via cookie."
            else:
                yield "Pas de session active, tentative de connexion..."
                yield from login_linkedin(driver, user_data, uid)

            yield from request_connexion(driver, job_title, user_data)
            yield from send_message(driver, job_title, user_data)

        except Exception as e:
            print(f"Erreur réseau : {e}")


        finally:
            driver.quit()

        yield "--- Invitations terminées, Nous avons envoyé {count} invitations ---"
