import os
import random
import re
import subprocess
import sys
import time
import urllib.parse

# from sqlite3.dbapi2 import Time
from typing import Optional

import undetected_chromedriver as uc

# import urllib.parse
# from operator import call
from data.prompt.prospection.prompt_message_prospection import (
    prompt_message_prospection,
)
from data.prompt.prospection.prompt_message_sourcing import (
    prompt_message_sourcing,
)
from database import supabase_client

# from data.supabase_client import supabase_client
from pydantic import BaseModel
from selenium.webdriver.chrome.service import Service

# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from treatment.behavior.mouse import human_mouse_move

from data.call_groq import call_groq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from locks import user_lock


class ProspectionRequest(BaseModel):
    intitule: str
    details: Optional[str] = None
    offre: Optional[str] = None
    # telephone: Optional[int] = None
    # full_name: Optional[str] = None


def slow_type(element, text):

    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))


def run_chrome(job_title: str, details: str, mode: str, offre, config_db):
    print(f"[DEBUG] Offre : {offre}")
    print(f"[DEBUG] Entrée dans run_chrome pour: {job_title}")
    print(f"[DEBUG] Détails de la prospection : {details}")
    # if not user_id:
    #     yield "❌ Erreur : ID utilisateur manquant"
    #     return
    uid = config_db.get("user_id")
    # offre = body.offre
    print(f"[DEBUG] User ID: {uid}")

    # tel_final = config_db.get("telephone") or ""
    # name_final = config_db.get("full_name") or ""

    if not uid:
        print(
            "❌ ERREUR : Pas d'ID utilisateur, Chrome ne sait pas quel dossier ouvrir !"
        )
        return
    print(f"🔍 [RUN_CHROME] job_title: {job_title}")
    print(f"🔍 [RUN_CHROME] config_db: {config_db}")
    print(f"🔍 [RUN_CHROME] Email: {config_db.get('linkedin_email')}")
    print(
        f"🔍 [RUN_CHROME] Password présent: {'OUI' if config_db.get('linkedin_password') else 'NON'}"
    )

    options = uc.ChromeOptions()
    profil_path = os.path.abspath(f"cookies/profile_{uid}")
    lock_file = os.path.join(profil_path, "SingletonLock")

    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
            print("lock supprimé avec succès")
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier de verrouillage : {e}")

    # profil_path = os.path.join(os.getcwd(), "linkedin_profile_informations")
    print(f"[DEBUG] Path profil: {profil_path}")
    options.add_argument(f"--user-data-dir={profil_path}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disk-cache-size=1")
    options.add_argument("--media-cache-size=1")

    job_title = config_db.get("query")

    print(f"🔍 [DEBUG] Valeur récupérée depuis 'query' : {job_title}")

    if not job_title:
        job_title = config_db.get("job_title")

    if not job_title:
        job_title = config_db.get("job_title")
        print(f"Titre du poste: {job_title}")

    # tel_final = data.get("telephone") or ""
    # name_final = data.get("full_name") or ""

    full_name = config_db.get("full_name")

    telephone = config_db.get("telephone")

    print(f"Nom complet: {full_name}")
    print(f"Numéro de téléphone: {telephone}")

    # telephone = config_db.get("telephone")
    # print("Numéro de téléphone:", telephone)

    # full_name = config_db.get("full_name")
    # print("Prénom:", full_name)

    KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
    print(f"KEY: {KEY_SECRET}")
    try:
        yield "Lancemenent..."
        print("🤖 [DEBUG] Appel Groq pour le message...")
        time.sleep(3)
        instruction = ""
        if mode == "prospection":
            instruction = prompt_message_prospection(
                job_title, details, telephone, full_name
            )
        elif mode == "sourcing":
            instruction = prompt_message_sourcing(
                job_title, details, telephone, full_name
            )
        message = call_groq(instruction)
        print(f"{message}")

        yield "Traitement des informations fournies..."

    except Exception as e:
        yield f"⚠️ Erreur IA : {str(e)[:50]}. Utilisation du message par défaut."
        message = "Bonjour"

    # os.system("pkill -9 chrome")
    # os.system("taskkill /f /im chrome.exe /t >nul 2>&1")
    # os.system("taskkill /f /im chromedriver.exe /t >nul 2>&1")
    #
    # subprocess.run(["pkill", "-9", "chrome"], stderr=subprocess.DEVNULL)
    # subprocess.run(["pkill", "-9", "chromedriver"], stderr=subprocess.DEVNULL)
    chrome_service = Service(log_path="chromedriver.log")
    lock_file = os.path.join(profil_path, "SingletonLock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
            print(f"✅ Lock supprimé pour le profil {uid}")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression du lock : {e}")
    # if os.path.exists("linkedin_profile_informations/SingletonLock"):
    #     os.remove("linkedin_profile_informations/SingletonLock")
    v_chrome = int(
        next(
            re.finditer(
                r"\d+", subprocess.check_output(["google-chrome", "--version"]).decode()
            )
        ).group()
    )
    time.sleep(random.randint(10, 30))
    print("temps choisi : ", random.randint(10, 30))
    driver = uc.Chrome(
        options=options,
        service=chrome_service,
        use_subprocess=True,
        version_main=v_chrome,
    )
    driver.maximize_window()
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        },
    )

    # wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://www.linkedin.com/feed/")
        # time.sleep(120)
        yield "Accès à LinkedIn..."
        time.sleep(random.uniform(3, 6))
        current_url = driver.current_url
        print("Current URL:", current_url)
        if "login" in driver.current_url or "uas" in driver.current_url:
            # from selenium.webdriver.common.action_chains import ActionChains

            # try:
            #     yield "Nous avons été redirigé vers la page de connexion..."
            #     time.sleep(random.uniform(3, 6))
            #     print("Page de connexion chargée")

            #     print("Page de login...")
            #     yield "Nous allons nous connecter..."
            #     print("Page de connexion chargée")
            #     wait = WebDriverWait(driver, 10)
            #     email_input = wait.until(
            #         EC.element_to_be_clickable((By.ID, "username"))
            #     )

            #     email_user = config_db.get("linkedin_email")

            #     rpc_res = supabase_client.rpc(
            #         "get_decrypted_password", {"user_id_param": uid}
            #     ).execute()
            #     pass_user = rpc_res.data

            #     pass_input = driver.find_element(By.ID, "password")

            #     email_input.clear()
            #     pass_input.clear()

            #     actions = ActionChains(driver)
            #     actions.move_to_element(email_input).click().perform()

            #     if email_user:
            #         slow_type(driver, email_user)
            #     else:
            #         print("Email non trouvé dans la configuration")
            #         yield (
            #             "Email linkedin non trouvé, vous devait le renseignez dans la section (modifier mes infos)"
            #         )
            #         time.sleep(6)
            #     # slow_type(driver, "kouicicontact@yahoo.com")

            #     time.sleep(random.uniform(3, 6))

            #     actions.move_to_element(pass_input).click().click().perform()
            #     if pass_user:
            #         slow_type(driver, pass_user)
            #     else:
            #         print("Email non trouvé dans la configuration")
            #         yield (
            #             "Mot de passe linkedin non trouvé, vous devait le renseignez dans la section (modifier mes infos)"
            #         )
            #         time.sleep(6)

            #     time.sleep(random.uniform(3, 6))
            #     yield "Connexion réussie..."

            # except Exception as e:
            #     print(f"Échec de la connexion{e}]...")
            #     raise
            #
            try:
                yield "Nous avons été redirigé vers la page de connexion..."
                print(f"DEBUG: URL actuelle avant login: {driver.current_url}")
                time.sleep(random.uniform(3, 6))

                print("DEBUG: Recherche du champ email (username)...")
                yield "Identification des champs..."

                try:
                    wait = WebDriverWait(driver, 15)
                    # Test de plusieurs sélecteurs car LinkedIn change souvent les IDs
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
                    yield "Erreur: Page de login LinkedIn non reconnue."
                    raise e

                # Récupération mot de passe
                print(f"DEBUG: Récupération pass pour UID: {uid}")
                try:
                    # rpc_res = supabase_client.rpc(
                    #     "get_decrypted_settings", {"user_id_param": uid}
                    # ).execute()
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
                        pass_user = str(data[0].get("linkedin_password", ""))
                    else:
                        pass_user = ""
                    print(
                        f"✅ Pass récupéré via RPC (longueur: {(pass_user) if pass_user else 0})"
                    )
                except Exception as e:
                    print(f"❌ Erreur RPC password: {e}")
                    yield "Erreur technique lors du décryptage du mot de passe."
                    raise e

                try:
                    pass_input = driver.find_element(
                        By.CSS_SELECTOR,
                        "input#password, input[name='session_password']",
                    )
                    print("✅ Champ password trouvé")
                except Exception as e:
                    print("❌ Champ password introuvable")
                    raise e

                email_input.clear()
                pass_input.clear()

                # Saisie Email
                email_user = config_db.get("linkedin_email")
                if email_user:
                    print(f"DEBUG: Saisie de l'email: {email_user}")
                    # actions = ActionChains(driver)
                    # actions.move_to_element(email_input).click().perform()
                    email_input.click()
                    slow_type(email_input, email_user)
                else:
                    print("❌ Email manquant dans config_db")
                    yield "Email linkedin non trouvé dans vos infos..."
                    return

                time.sleep(random.uniform(2, 4))

                # Saisie Password
                if pass_user:
                    print(f"DEBUG: Saisie du mot de passe {pass_user}...")
                    # actions.move_to_element(pass_input).click().perform()
                    # slow_type(driver, pass_user)
                    pass_input.click()
                    slow_type(pass_input, pass_user)
                    time.sleep(1)
                else:
                    print("❌ Mot de passe vide après RPC")
                    yield "Mot de passe linkedin vide ou incorrect."
                    return

                time.sleep(random.uniform(2, 4))

                print("DEBUG: Tentative de validation (Entrée)...")
                pass_input.send_keys(Keys.ENTER)

                yield "Vérification de la connexion..."
                time.sleep(5)

                if "feed" in driver.current_url:
                    print("✅ Connexion réussie, redirection vers feed OK")
                    yield "Connexion réussie !"
                else:
                    print(f"⚠️ Redirection après login: {driver.current_url}")
                    yield "Connexion en cours (vérification challenge ou captcha...)..."

            except Exception as e:
                print(f"💥 CRASH BLOC LOGIN: {str(e)}")
                yield f"Erreur de connexion : {type(e).__name__}"
                raise e

        human_mouse_move(driver)
        time.sleep(random.uniform(2, 4))
    except Exception as e:
        print(f"Erreur lors du chargement de la page : {e}")
        # yield "Tentative d'accès échoué votre mot de passe à peut être été changé..."

    try:
        yield "🔍 Recherche..."
        time.sleep(random.uniform(8, 12))
        human_mouse_move(driver)

        yield "On va nettoyer les fenêtres encore ouvertes..."
        print("On nettoie les fenêtres")
        time.sleep(6)

        try:
            close_buttons = driver.find_elements(
                By.CSS_SELECTOR,
                "button[data-control-name='close_messaging_bubble'], .msg-overlay-bubble-header__control--close",
            )
            print(f"Nombre de boutons de fermeture trouvés : {len(close_buttons)}")
            for btn in close_buttons:
                print(f"Bouton de fermeture trouvé : {btn}")
                driver.execute_script("arguments[0].click();", btn)
        except Exception as e:
            print(f"❌ Crash lors de la fermeture des fenêtres : {str(e)[:50]}")

    except Exception as e:
        print(f"❌ Crash avant recherche : {str(e)[:50]}")
    try:
        time.sleep(random.uniform(8, 15))
        query_encoded = urllib.parse.quote(job_title)
        # target_url = "https://www.linkedin.com/search/results/people/?keywords=nava%20&origin=FACETED_SEARCH&currentCompany=%5B%2286882974%22%5D"
        target_url = f"https://www.linkedin.com/search/results/people/?keywords={query_encoded}&origin=SWITCH_SEARCH_VERTICAL"
        driver.get(target_url)
        yield "On accède à la liste des personnes..."
    except Exception as e:
        print(f"{str(e)}")

    time.sleep(random.uniform(4, 8))

    boutons_conx = driver.find_elements(
        By.XPATH,
        "//a[contains(@aria-label, 'Inviter') and contains(@aria-label, 'rejoindre votre réseau')]",
    )

    yield f"✓ {len(boutons_conx)} personnes trouvés en première page..."

    for i, bouton in enumerate(boutons_conx):
        try:
            # container = bouton.find_element(
            #     By.XPATH,
            #     "./ancestor::div[contains(@class, 'cf2a0fad') or @data-view-name='search-result-lockup-title']/../..",
            # )
            container = bouton.find_element(
                By.XPATH, "./ancestor::div[@role='listitem'][1]"
            )
            print(f"Container text: {container.text}")

            infos_profil = container.text.lower().replace("\n", "").strip()

            current_user_id = config_db.get("user_id")
            res = (
                supabase_client.table("profiles")
                .select("*, cabinets(nom)")
                .eq("id", current_user_id)
                # .single()
                .execute()
            )
            print(f"Supabase response: {res}")

            # cabinet_data = res.data[0].get("cabinets") or {}
            cabinet_name = ""
            if res.data and len(res.data) > 0:
                first_row = res.data[0]
                if isinstance(first_row, dict):
                    cabinet_data = first_row.get("cabinets", {})
                    if isinstance(cabinet_data, dict):
                        cabinet_name = (
                            str(cabinet_data.get("nom") or "").lower().strip()
                        )
                        print(f"Cabinet name: {cabinet_name}")

                # cabinet_data = res.data[0].get("cabinets", {})
                # first_row = data[0]
                # cabinet_name = cabinet_data.get("nom", "").lower().strip()
                # print(f"Cabinet name: {cabinet_name}")

            yield "On va vérifier si la personne est chez nous..."
            print("On va vérifier si la personne est chez nous...")
            time.sleep(6)
            if cabinet_name:
                exclusions = [cabinet_name, cabinet_name.replace(" ", "")]

                if any(excl in infos_profil for excl in exclusions):
                    yield f"Candidat de chez {cabinet_name}, skip..."
                    print(f"Interne ({cabinet_name}), on zappe.")
                    time.sleep(random.uniform(3, 5))
                    continue

            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", bouton
            )

            time.sleep(random.uniform(2, 4))

            driver.execute_script("arguments[0].click();", bouton)
            yield f"[{i + 1}] Ouverture popup invitation"

            time.sleep(random.uniform(2, 4))

            try:
                time.sleep(5)
                script_final = """
                                                        function findButton() {
                                                            // 1. Check standard
                                                            let btn = document.querySelector('button[aria-label="Envoyer sans note"]');
                                                            if (btn) return btn;

                                                            // 2. Check dans le Shadow DOM (interop-outlet)
                                                            let host = document.querySelector('#interop-outlet');
                                                            if (host && host.shadowRoot) {
                                                                return host.shadowRoot.querySelector('button[aria-label="Envoyer sans note"]');
                                                            }

                                                            // 3. Check par texte si aria-label a sauté
                                                            return Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('sans note'));
                                                        }

                                                        let target = findButton();
                                                        if (target) {
                                                            target.click();
                                                            return true;
                                                        }
                                                        return false;
                                                        """

                success = driver.execute_script(script_final)
                if success:
                    yield "✅ Invitation envoyée !"
                else:
                    yield " Bouton introuvable même en recherche profonde."

                yield " Invitation envoyée avec succès !"
            except Exception as e:
                error_type = type(e).__name__
                yield f"Erreur précise [{error_type}] : {str(e)[:100]}"
        except Exception as e:
            yield f"  ⚠ Erreur bouton Envoyer : {e}"

        finally:
            config_id = config_db.get("id")
            if config_id:
                try:
                    supabase_client.table("prospection_settings").update(
                        {"is_active": False}
                    ).eq("id", config_id).execute()
                    # yield f"✅ Session terminée {config_id}, fermeture navigateur.."
                except Exception as e:
                    if "204" not in str(e) and "Missing response" not in str(e):
                        print(f"Erreur DB: {e}")
                    else:
                        print(f"Log technique: {e}")

    yield "--- Invitations terminées ---"

    try:
        from prospection.send_message import send_message

        for update in send_message(driver, job_title, message, offre, mode, config_db):
            yield update
    except Exception as e:
        print(f"Erreur passage messages : {e}")
