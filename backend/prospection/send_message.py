import random
import time
import traceback

from database import supabase_client
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from backend.data.prompt.prospection.prompt_check_ia_profile import (
    prompt_check_ia_profile,
)

# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait


def send_message(driver, job_title, message, config_db):
    yield f"Démarrage de l'envoi de messages directs pour {job_title}..."
    try:
        try:
            time.sleep(random.uniform(5, 8))

            search_url = "https://www.linkedin.com/in/jouna%C3%AFd-ben-salah-601b77222/"
            # search_url = f"https://www.linkedin.com/search/results/people/?keywords={job_title}&origin=GLOBAL_SEARCH_CARD"
            driver.get(search_url)
            yield "On accède aux profils pour envoyer des messages..."
            time.sleep(random.uniform(6, 8))
        except Exception as e:
            traceback.print_exc()
            print(f"Détails : {e}")
            time.sleep(random.uniform(6, 9))
            yield "Erreur au premier try"

        # buton message
        # button = driver.find_element(
        #     By.XPATH,
        #     "//a[contains(@href, '/messaging/compose')]//span[contains(text(), 'Message')]",
        # )
        # driver.execute_script("window.scrollTo(0, 500);")
        # button = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located(
        #         (
        #             By.XPATH,
        #             "//a[contains(@href, '/messaging/compose') and contains(., 'Message')]",
        #         )
        #     )
        # )
        # time.sleep(10)
        # yield "bouton de message trouvé..."
        # driver.execute_script("arguments[0].click();", button)

        try:
            profile_main_content = driver.find_element(By.TAG_NAME, "main").text.lower()
            content_lower = profile_main_content.lower()

            print(content_lower)

            keyword_exclude = ["nava engineering", "navaengineering"]
            if any(keyword in content_lower for keyword in keyword_exclude):
                yield "Candidat interne ou exclu, skip..."
                print("Personne chez nava, on prospecte pas ce profil...")
                return

            ia_check = prompt_check_ia_profile(job_title, profile_main_content)
            if not ia_check:
                yield "Candidat non pertinent"
                return
        except Exception as e:
            print(f"Error checking profile content: {e}")

        button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@href, 'messaging/compose')]//*[contains(text(), 'Message')] | //button[contains(., 'Message')]",
                )
            )
        )
        # container = button.find_element(
        #     By.XPATH, "./ancestor::div[@role='listitem'][1]"
        # )
        # print(f"Container text: {container.text}")
        # infos_profil = container.text.lower().replace("\n", "").strip()
        # keyword_exclude = ["nava engineering", "navaengineering"]

        # if any(keyword in infos_profil for keyword in keyword_exclude):
        #     yield "Personne chez nava, on prospecte pas ce profil..."
        #     print("Personne chez nava, on prospecte pas ce profil...")
        #     return

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        # button.click()
        driver.execute_script("arguments[0].click();", button)
        time.sleep(random.uniform(6, 8))

        # on cherche le champs de saisie et on tente le click
        try:
            xpath_input = "//div[@role='textbox' and contains(@class, 'msg-form__contenteditable')]"
            time.sleep(10)
            yield "On cherche l'input..."
            message_box = driver.find_element(By.XPATH, xpath_input)
            message_box.click()
            time.sleep(random.uniform(4, 7))
            yield "Input trouvé..."
        except Exception as e:
            traceback.print_exc()
            print(f"Détails : {e}")
            yield "❌ Échec à l'étape : Recherche Input"
            time.sleep(random.uniform(6, 9))
            return
            # on ecris le message
        try:

            def slow_type(element, text):
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.1))

            # message_box.send_keys(message)
            slow_type(message_box, message)
            yield "Saisie du message..."
            time.sleep(random.uniform(6, 9))
        except Exception as e:
            traceback.print_exc()
            print(f"Détails : {e}")
            yield "❌ Échec à l'étape : Saisie du message"
            time.sleep(random.uniform(6, 9))
            return
            # on cherche le bouton
        try:
            send_btn = (
                "//button[contains(@class, 'msg-form__send-btn') or @type='submit']"
            )
            btn_element = driver.find_element(By.XPATH, send_btn)
        except Exception as e:
            traceback.print_exc()
            print(f"Détails : {e}")
            yield "❌ Échec à l'étape : localisation bouton"
            time.sleep(random.uniform(6, 9))
            return
            # on tente le click
        try:
            driver.execute_script(
                "arguments[0].removeAttribute('disabled');", btn_element
            )
            time.sleep(random.uniform(7, 9))
            yield "Envoi du message..."
            driver.execute_script("arguments[0].click();", btn_element)
            time.sleep(random.uniform(6, 9))
            yield "✅ Message envoyé !"
            time.sleep(random.uniform(5, 9))
        except Exception as e:
            traceback.print_exc()
            print(f"Détails : {e}")
            yield "❌ Échec à l'étape : Clic Envoi"
            time.sleep(random.uniform(6, 9))
            return

    except Exception as e:
        print(e)
        return

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
        if "driver" in locals():
            driver.quit()
            return
