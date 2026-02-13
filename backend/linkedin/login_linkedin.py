import os
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from treatment.slow_type import slow_type


def login_linkedin(driver, uid, job_title, supabase_client, config_db):
    KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
    try:
        yield "Nous avons été redirigé vers la page de connexion..."
        print(f"URL : {driver.current_url}")
        time.sleep(random.uniform(3, 6))

        print("DEBUG: Recherche du champ email (username)...")
        yield "Identification des champs..."

        try:
            wait = WebDriverWait(driver, 15)
            email_input = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "input#username, input[name='session_key']",
                    )
                )
            )
            print("✅ Champ email trouvé")
        except Exception as e:
            print(
                f"❌ Erreur: Impossible de trouver le champ email. URL: {driver.current_url}"
            )
            raise e

        # Récupération mot de passe
        print(f"DEBUG: Récupération pass pour UID: {uid}")
        try:
            rpc_res = supabase_client.rpc(
                "get_decrypted_settings",
                {"job_title_input": job_title, "key_input": KEY_SECRET},
            ).execute()
            data = rpc_res.data
            print(f"DEBUG DATA BRUTE: {rpc_res.data}")
            if isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                if isinstance(first_item, dict):
                    pass_user = str(first_item.get("linkedin_password", ""))
                else:
                    pass_user = ""
            else:
                pass_user = ""
            print(f"Mot de passe récupéré via RPC {pass_user}")
        except Exception as e:
            print(f"❌ Erreur RPC password: {e}")
            yield "Erreur technique lors du décryptage du mot de passe."
            raise e

        try:
            pass_input = driver.find_element(
                By.CSS_SELECTOR,
                "input#password, input[name='session_password']",
            )
            print("Champ password trouvé")
        except Exception as e:
            print("Champ password introuvable")
            raise e

        email_input.clear()
        pass_input.clear()

        # Saisie Email
        email_user = config_db.get("linkedin_email")
        if email_user:
            print(f"DEBUG: Saisie de l'email: {email_user}")
            email_input.click()
            slow_type(email_input, email_user)
        else:
            print("Email manquant dans config_db")
            yield "Email linkedin non trouvé dans vos infos..."
            return

        time.sleep(random.uniform(2, 4))

        # Saisie Password
        if pass_user:
            print(f"DEBUG: Saisie du mot de passe {pass_user}...")

            pass_input.click()
            slow_type(pass_input, pass_user)
            time.sleep(1)
        else:
            print("Mot de passe vide après RPC")
            yield "Mot de passe linkedin vide ou incorrect."
            return

        time.sleep(random.uniform(2, 4))

        print("DEBUG: Tentative de validation..")
        pass_input.send_keys(Keys.ENTER)
        # wait = WebDriverWait(driver, 20)
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
