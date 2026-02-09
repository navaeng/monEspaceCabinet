import random
import time
import traceback

from data.prompt.prospection.prompt_check_ia_profile import (
    prompt_check_ia_profile,
)
from database import supabase_client
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from treatment.send_mail import send_mail
from uvicorn import config

# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait


def send_message(driver, job_title, message, offre, config_db):
    print("Début de l'envoi de messages directs...")
    yield f"Démarrage de l'envoi de messages directs pour {job_title}..."
    # links = driver.find_elements(
    #     By.XPATH,
    #     "//span[contains(@class, 'entity-result__title-line')]//a[contains(@href, '/in/')]",
    # )
    try:
        # time.sleep(random.uniform(2, 4))
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(random.uniform(5, 7))
        # links = driver.find_elements(
        #     By.XPATH,
        #     "//a[contains(@href, '/in/') and not(contains(@class, 'scale-down'))]",
        # )
        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/in/']")
        time.sleep(2)
        urls = []
        for link in links:
            url = link.get_attribute("href").split("?")[0]
            if url not in urls:
                urls.append(url)

        yield f"Nombre de profils trouvés : {len(urls)}"
        print(f"Nombre de profils trouvés : {len(urls)}")

    except Exception as e:
        print(f"Erreur lors de la récupération des liens : {e}")
        # yield f"Erreur lors de la récupération des liens : {e}"
        return

    for u, url in enumerate(urls, start=1):
        try:
            try:
                print(f"Traitement du profil {u}/{len(urls)}...")
                yield f"Traitement du profil {u}/{len(urls)}..."
                time.sleep(random.uniform(5, 8))

                # url = "https://www.linkedin.com/in/jouna%C3%AFd-ben-salah-601b77222/"
                # search_url = f"https://www.linkedin.com/search/results/people/?keywords={job_title}&origin=GLOBAL_SEARCH_CARD"
                driver.get(url)

                # for i, url in enumerate(urls, start=1):
                #     yield f"On accède au profil {i}/{len(urls)}..."
                #     time.sleep(random.uniform(5, 8))

                profile_main_content = driver.find_element(
                    By.TAG_NAME, "main"
                ).text.lower()
                content_lower = profile_main_content

                print(f"Contenu pour checker les candidats chez nava: {content_lower}")

                current_user_id = config_db.get("user_id")
                res = (
                    supabase_client.table("profiles")
                    .select("*, cabinets(nom)")
                    .eq("id", current_user_id)
                    .single()
                    .execute()
                )

                config_db = res.data
                cabinet_name = config_db.get("nom")
                print(f"Nom du cabinet: {cabinet_name}")

                print("On va vérifier si cette personne est chez nous...")
                yield "On va vérifier si cette personne est chez nous..."
                time.sleep(random.uniform(3, 5))

                if any(keyword in content_lower for keyword in cabinet_name):
                    yield "Candidat interne ou exclu, skip..."
                    print("Personne chez nous, on ne prospecte pas ce profil...")
                    continue

                ia_check, is_top, argument = prompt_check_ia_profile(
                    offre, profile_main_content
                )
                yield "On analyse son profil avec l'offre..."
                time.sleep(random.uniform(3, 5))

                if not ia_check:
                    print("Candidat non pertinent")
                    yield "Candidat non pertinent"
                    continue
                if is_top:
                    print("Candidat top, on envoie un mail")
                    send_mail(argument, url, config_db)
                    yield "Mail envoyé"
                # except Exception as e:
                #     print(f"Error checking profile content: {e}")

                time.sleep(random.uniform(6, 8))
            except Exception as e:
                traceback.print_exc()
                print(f"Détails : {e}")
                time.sleep(random.uniform(6, 9))
                yield "Traitement des profils impossibles"

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

            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", button
            )
            # button.click()
            driver.execute_script("arguments[0].click();", button)
            time.sleep(random.uniform(6, 8))

            # on cherche le champs de saisie et on tente le click
            try:
                xpath_input = "//div[@role='textbox' and contains(@class, 'msg-form__contenteditable')]"
                time.sleep(10)
                yield "On cherche le bouton..."
                message_box = driver.find_element(By.XPATH, xpath_input)
                message_box.click()
                time.sleep(random.uniform(4, 7))
                yield "Bouton trouvé..."
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
                continue
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
                continue
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

                try:
                    current_user_id = config_db.get("user_id")
                    print(f"User ID: {current_user_id}")
                    supabase_client.table("url_contactees").insert(
                        {"url": url, "user_id": current_user_id}
                    ).execute()
                except Exception as e:
                    print(f"Erreur: {e}")

            except Exception as e:
                traceback.print_exc()
                print(f"Détails : {e}")
                yield "❌ Échec à l'étape : Clic Envoi"
                time.sleep(random.uniform(6, 9))
                continue

        except Exception as e:
            print(e)
            continue

    # finally:
    #     config_id = config_db.get("id")
    #     if config_id:
    #         try:
    #             supabase_client.table("prospection_settings").update(
    #                 {"is_active": False}
    #             ).eq("id", config_id).execute()
    #             # yield f"✅ Session terminée {config_id}, fermeture navigateur.."
    #         except Exception as e:
    #             if "204" not in str(e) and "Missing response" not in str(e):
    #                 print(f"Erreur DB: {e}")
    #             else:
    #                 print(f"Log technique: {e}")
    if "driver" in locals():
        driver.quit()
        return
