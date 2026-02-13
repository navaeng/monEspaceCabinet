import os
import random
import re
import subprocess
import sys
import time

# import urllib.parse
from typing import Optional

# import undetected_chromedriver as uc
from database import supabase_client
from httpx import post
from linkedin.post_message import post_message
from linkedin.send_message import send_message
from login_linkedin import login_linkedin
from pydantic import BaseModel
from request_connexion import request_connexion
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from treatment.behavior.mouse import human_mouse_move

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ProspectionRequest(BaseModel):
    intitule: str
    details: Optional[str] = None
    offre: Optional[str] = None


def run_chrome(driver, job_title: str, details: str, mode: str, offre, config_db):

    config_chrome()

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

    # except Exception as e:
    #     print(f"Erreur lors du chargement de la page : {e}")

    try:
        yield from post_message(driver, post)
        time.sleep(5)
        yield from request_connexion(job_title, driver, config_db)
        yield from send_message(
            driver, job_title, offre, mode, config_db, details, telephone, full_name
        )

        # try:
        #     from linkedin.send_message import send_message

        #     for update in send_message(
        #         driver, job_title, offre, mode, config_db, details, telephone, full_name
        #     ):
        #         yield update
        # except Exception as e:
        #     print(f"Erreur passage messages : {e}")

        for page in range(1, 2):
            time.sleep(random.uniform(8, 12))
            human_mouse_move(driver)

            try:
                yield "On va nettoyer les fenêtres encore ouvertes..."
                print("On nettoie les fenêtres")
                time.sleep(6)

                close_buttons = driver.find_elements(
                    By.CSS_SELECTOR,
                    "button[data-control-name='close_messaging_bubble'], .msg-overlay-bubble-header__control--close",
                )
                print(f"nombre de boutons de fermeture trouvés : {len(close_buttons)}")

                for btn in close_buttons:
                    print(f"Bouton de fermeture trouvé : {btn}")
                    driver.execute_script("arguments[0].click();", btn)
            except Exception as e:
                print(f"Crash lors de la fermeture des fenêtres : {str(e)[:50]}")

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
