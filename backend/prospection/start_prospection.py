import os
import random
import re
import subprocess
import time
import urllib.parse

# from operator import call
import undetected_chromedriver as uc
from data.prompt.prospection.prompt_message_prospection import (
    prompt_message_prospection,
)
from pydantic import BaseModel
from selenium.webdriver.chrome.service import Service

# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from treatment.behavior.mouse import human_mouse_move

from data.call_groq import call_groq


class ProspectionRequest(BaseModel):
    intitule: str


def slow_type(element, text):
    for char in text:
        element.send_keys(char)

        time.sleep(random.uniform(0.1, 0.3))


def run_chrome(job_title: str, config_db):
    print(f"[DEBUG] Entrée dans run_chrome pour: {job_title}")
    uid = config_db.get("user_id")
    print(f"[DEBUG] User ID: {uid}")

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

    job_title = config_db.get("job_title")
    try:
        print("🤖 [DEBUG] Appel Groq pour le message...")
        instruction = prompt_message_prospection(job_title)
        message = call_groq(instruction)
        print(f"{message}")
        yield "On prépare un message..."

    except Exception as e:
        yield f"⚠️ Erreur IA : {str(e)[:50]}. Utilisation du message par défaut."
        message = "Bonjour"

    # os.system("pkill -9 chrome")
    os.system("taskkill /f /im chrome.exe /t >nul 2>&1")
    os.system("taskkill /f /im chromedriver.exe /t >nul 2>&1")
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

    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://www.linkedin.com/feed/")
        # time.sleep(120)
        yield "Accès à LinkedIn..."
        time.sleep(random.uniform(3, 6))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        yield "Chargement..."
        human_mouse_move(driver)
        time.sleep(random.uniform(2, 4))
    except Exception as e:
        print(f"Erreur lors du chargement de la page : {e}")
        # yield "Tentative d'accès échoué votre mot de passe à peut être été changé..."

    try:
        yield "🔍 Recherche..."
        time.sleep(random.uniform(8, 12))
        human_mouse_move(driver)

    except Exception as e:
        print(f"❌ Crash avant recherche : {str(e)[:50]}")
    try:
        time.sleep(random.uniform(8, 15))
        query_encoded = urllib.parse.quote(job_title)
        target_url = f"https://www.linkedin.com/search/results/people/?keywords={query_encoded}&origin=SWITCH_SEARCH_VERTICAL"
        driver.get(target_url)
        yield "Filtre personnes..."
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
            container = bouton.find_element(
                By.XPATH,
                "./ancestor::div[contains(@class, 'cf2a0fad') or @data-view-name='search-result-lockup-title']/../..",
            )
            print(f"Container text: {container.text}")
            infos_profil = container.text.lower()
            keyword_exclude = ["Nava", "Nava engineering"]

            if any(keyword in infos_profil for keyword in keyword_exclude):
                yield "Personne chez nava, on prospecte pas ce profil..."
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

    yield "--- Invitations terminées ---"

    try:
        from prospection.send_message import send_message

        for update in send_message(driver, job_title, message, config_db):
            yield update
    except Exception as e:
        print(f"Erreur passage messages : {e}")
