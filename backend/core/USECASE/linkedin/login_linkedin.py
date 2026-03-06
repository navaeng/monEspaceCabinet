import os
import random
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC, wait

from core.USECASE.linkedin.find_element.find_email_input import find_email_input
from core.USECASE.linkedin.find_element.find_password_input import find_password_input
from core.USECASE.linkedin.selenium_actions.fill_email import fill_email
from core.USECASE.linkedin.selenium_actions.fill_password import fill_password
from core.USECASE.linkedin.components.slow_type import slow_type


def login_linkedin(driver, uid, job_title, supabase_client, config_db):
    KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
    try:
        yield "Nous avons été redirigé vers la page de connexion..."
        print(f"URL : {driver.current_url}")
        time.sleep(random.uniform(3, 6))

        print("DEBUG: Recherche du champ email (username)...")
        yield "Identification des champs..."

        find_email_input(driver)
        find_password_input(driver)

        find_email_input.clear()
        find_password_input.clear()

        fill_email(find_email_input, slow_type)
        time.sleep(random.uniform(3, 6))
        fill_password(job_title, KEY_SECRET, find_password_input)

        time.sleep(random.uniform(2, 4))

        print("DEBUG: Tentative de validation..")
        find_password_input.send_keys(Keys.ENTER)
        wait.until(EC.url_contains("feed"))

        yield "Vérification de la connexion..."
        time.sleep(5)

        if "feed" in driver.current_url:
            print("Connexion réussie, redirection vers feed OK")
            yield "Connexion réussie !"
        else:
            print(f"Redirection après login: {driver.current_url}")
            yield "Connexion en cours (vérification challenge ou captcha...)..."

    except Exception as e:
        print(f"CRASH BLOC LOGIN: {str(e)}")
        yield f"Erreur de connexion : {type(e).__name__}"
        raise e
