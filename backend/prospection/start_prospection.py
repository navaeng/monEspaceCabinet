import os
import random
import re
import subprocess
import sys
import time
import urllib.parse
from typing import Optional

import undetected_chromedriver as uc
from database import supabase_client

# from httpx import post
from prospection.post_message import post_message
from pydantic import BaseModel
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from treatment.behavior.mouse import human_mouse_move

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ProspectionRequest(BaseModel):
    intitule: str
    details: Optional[str] = None
    offre: Optional[str] = None
    post: Optional[str] = None


def slow_type(element, text):

    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))


def run_chrome(
    job_title: str, details: str, mode: str, offre: str, post: str, config_db
):
    print("[DEBUG-STEP] Lancement chrome")

    if not post or post == "":
        post = config_db.get("post")

    print(f"[DEBUG] Offre : {offre}")
    print(f"[DEBUG] Entrée dans run_chrome pour: {job_title}")
    print(f"[DEBUG] Détails de la prospection : {details}")
    print(f"[DEBUG] Mode : {mode}")
    print(f"[DEBUG] Détails pour le post linkedin : {post}")
    print(f"CONFIG DB: {config_db}")

    uid = config_db.get("user_id")
    print(f"[DEBUG] User ID: {uid}")

    if not uid:
        print(
            "❌ ERREUR : Pas d'ID utilisateur, Chrome ne sait pas quel dossier ouvrir !"
        )
        return
    # print(f"🔍 [RUN_CHROME] job_title: {job_title}")
    # print(f"🔍 [RUN_CHROME] config_db: {config_db}")
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

    print(f"[DEBUG] Path profil: {profil_path}")
    options.add_argument(f"--user-data-dir={profil_path}")
    options.add_argument("--profile-directory=Default")
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disk-cache-size=1")
    options.add_argument("--media-cache-size=1")

    # job_title = config_db.get("query")
    # if job_title:
    #     print(f"Titre du poste: {job_title}")
    job_title = job_title or config_db.get("query")
    # if not job_title:
    #     job_title = config_db.get("job_title")
    #     print(f"Titre du poste: {job_title}")

    full_name = config_db.get("full_name")
    telephone = config_db.get("telephone")

    filtre_map = {
        "Personnes": "people",
        "Entreprises": "companies",
        "Offres": "offers",
        "Annonces": "ads",
    }

    segment = config_db.get("segment", "Personnes")
    segment = filtre_map.get(segment, "people")

    print(f"Segment: {segment}")

    print(f"Nom complet: {full_name}")
    print(f"Numéro de téléphone: {telephone}")

    KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
    print(f"KEY: {KEY_SECRET}")

    # chrome_service = Service(log_path="chromedriver.log")
    # lock_file = os.path.join(profil_path, "SingletonLock")
    # if os.path.exists(lock_file):
    #     try:
    #         os.remove(lock_file)
    #         print(f"✅ Lock supprimé pour le profil {uid}")
    #     except Exception as e:
    #         print(f"❌ Erreur lors de la suppression du lock : {e}")
    # # if os.path.exists("linkedin_profile_informations/SingletonLock"):
    # #     os.remove("linkedin_profile_informations/SingletonLock")
    v_chrome = int(
        next(
            re.finditer(
                r"\d+", subprocess.check_output(["google-chrome", "--version"]).decode()
            )
        ).group()
    )
    # time.sleep(random.randint(10, 30))
    # print("temps choisi : ", random.randint(10, 30))
    driver = uc.Chrome(
        options=options,
        # service=chrome_service,
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
            # print(f"DEBUG: Récupération pass pour UID: {uid}")
            # try:
            #     rpc_res = supabase_client.rpc(
            #         "get_decrypted_settings",
            #         {"job_title_input": job_title, "key_input": KEY_SECRET},
            #     ).execute()
            #     data = rpc_res.data
            #     print(f"DEBUG DATA BRUTE: {rpc_res.data}")
            #     if isinstance(data, list) and len(data) > 0:
            #         first_item = data[0]
            #         if isinstance(first_item, dict):
            #             pass_user = str(first_item.get("linkedin_password", ""))
            #         else:
            #             pass_user = ""
            #     else:
            #         pass_user = ""
            #     print(f"Mot de passe récupéré via RPC {pass_user}")
            # except Exception as e:
            #     print(f"❌ Erreur RPC password: {e}")
            #     yield "Erreur technique lors du décryptage du mot de passe."
            #     raise e

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
                time.sleep(7)
                # return
                driver.quit()
                return

            time.sleep(random.uniform(2, 4))

            # Saisie Password
            pass_user = config_db.get("linkedin_password", "")
            print(f"VALEUR REELLE password : '{pass_user}'")
            if pass_user:
                print(f"DEBUG: Saisie du mot de passe {pass_user}...")

                pass_input.click()
                slow_type(pass_input, pass_user)
                time.sleep(1)
            else:
                print("Mot de passe linkedin vide ")
                yield "Mot de passe linkedin vide ou incorrect."
                time.sleep(7)
                driver.quit()
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

    # except Exception as e:
    #     print(f"Erreur lors du chargement de la page : {e}")

    try:
        print("[DEBUG-STEP] Lancement post_message")

        yield from post_message(driver, post, config_db)
        time.sleep(5)
        print("[DEBUG-STEP] Lancement recherche personne")

        yield "🔍 Recherche..."

        for page in range(1, 2):
            time.sleep(random.uniform(8, 12))
            human_mouse_move(driver)
            print("accès a la recherche de personnes ")
            yield (f"Début de recherche, on va filtrer par {segment} à la page {page}")
            time.sleep(random.uniform(2, 4))

            try:
                print("Début de la recherche")
                time.sleep(random.uniform(8, 15))
                driver.refresh()
                query_encoded = urllib.parse.quote(str(job_title or "recrutement"))
                target_url = f"https://www.linkedin.com/search/results/{segment}/?keywords={query_encoded}&origin=SWITCH_SEARCH_VERTICAL&page={page}"
                driver.get(target_url)
                print(target_url)
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight/2);"
                )
                yield "Recherches de personnes..."
            except Exception as e:
                import traceback

                print(f"CRASH NAVIGATION : {e}")
                traceback.print_exc()
                continue

            time.sleep(random.uniform(4, 8))

            boutons_conx = driver.find_elements(
                By.XPATH,
                "//a[contains(@aria-label, 'Inviter') and contains(@aria-label, 'rejoindre votre réseau')]",
            )

            yield f" {len(boutons_conx)} personnes trouvés..."

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

                    yield f"On va vérifier si {cabinet_name} est mentionné dans son profil..."
                    print(
                        f"On va vérifier si la personne est chez nous {cabinet_name}..."
                    )

                    time.sleep(6)
                    if cabinet_name:
                        exclusions = [cabinet_name, cabinet_name.replace(" ", "")]

                        if any(excl in infos_profil for excl in exclusions):
                            yield f"Candidat de chez {cabinet_name}, skip..."
                            print(f"Interne ({cabinet_name}), on zappe.")
                            time.sleep(random.uniform(3, 5))
                            continue
                        else:
                            yield f"Pas de mention à {cabinet_name}..."

                    driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", bouton
                    )

                    time.sleep(random.uniform(2, 4))

                    driver.execute_script("arguments[0].click();", bouton)
                    yield f"[{i + 1}] Demande d'invitation..."

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
                            yield "On ne trouve pas le bouton Envoyer, on va actualiser la page, dans ce cas on actualise la page..."
                            driver.refresh()

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

            except Exception as e:
                if "204" not in str(e) and "Missing response" not in str(e):
                    print(f"Erreur DB: {e}")
                else:
                    print(f"Log technique: {e}")

    yield "--- Invitations terminées... ---"

    try:
        from prospection.send_message import send_message

        for update in send_message(
            driver, job_title, offre, mode, config_db, details, telephone, full_name
        ):
            yield update
    except Exception as e:
        print(f"Erreur passage messages : {e}")
