import random
import time
import traceback

from data.prompt.prospection.prompt_check_ia_profile import (
    prompt_check_ia_profile,
)
from data.prompt.prospection.prompt_message_prospection import (
    prompt_message_prospection,
)
from data.prompt.prospection.prompt_message_sourcing import (
    prompt_message_sourcing,
)
from database import supabase_client
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from treatment.send_mail import send_mail

from data.call_groq import call_groq


def send_message(
    driver, job_title, offre, mode, config_db, details, telephone, full_name
):
    print("Début de l'envoi de messages directs...")
    print(f"Mode dans send message : {mode}")
    yield f"Démarrage envoi de messages pour {job_title}... en mode {mode}"
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

        yield f"{len(urls)} profils trouvés..."
        print(f"{len(urls)} profils trouvés")

    except Exception as e:
        print(f"Erreur lors de la récupération des liens : {e}")
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
                current_user_id = config_db.get("user_id")
                print(f"current_user_id: {current_user_id}")

                yield "On va vérifier si le profil à été contacté récemment..."
                print("On va vérifier si le profil à été contacté récemment...")
                time.sleep(random.uniform(5, 8))
                check_contact = (
                    supabase_client.table("url_contactees")
                    .select("id")
                    .eq("url", url)
                    .eq("user_id", current_user_id)
                    .execute()
                )
                print(f"check_contact: {check_contact}")

                if check_contact.data:
                    yield f"⏭️ Déjà contacté ({url}), skip..."
                    print("Déjà dans la base, on passe au suivant.")
                    time.sleep(random.uniform(5, 8))
                    continue
                yield "Pas encore contacté..."

                profile_main_content = driver.find_element(
                    By.TAG_NAME, "main"
                ).text.lower()
                content_lower = profile_main_content

                print(f"Contenu pour checker les candidats : {content_lower}")

                current_user_id = config_db.get("user_id")
                res = (
                    supabase_client.table("profiles")
                    .select("*, cabinets(nom)")
                    .eq("id", current_user_id)
                    .execute()
                )

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

                yield f"On va vérifier si le profil mentionne {cabinet_name}..."
                print("On va vérifier si la personne est chez nous...")
                time.sleep(6)

                infos_profil = driver.find_element(By.TAG_NAME, "body").text.lower()
                print(f"infos_profil: {infos_profil}")

                if cabinet_name:
                    exclusions = [cabinet_name, cabinet_name.replace(" ", "")]
                    print(f"Exclusions: {exclusions}")

                    if any(excl in infos_profil for excl in exclusions):
                        yield f"Candidat de chez {cabinet_name}, skip..."
                        print(f"Interne ({cabinet_name}), on zappe.")
                        time.sleep(random.uniform(3, 5))
                        continue
                    else:
                        print(
                            f"Pas de spécifications au cabinet {cabinet_name} dans son profil..."
                        )
                        yield f"Pas de spécifications au cabinet {cabinet_name} dans son profil..."

                if mode == "sourcing":
                    ia_check, is_top, argument = prompt_check_ia_profile(
                        offre, profile_main_content
                    )
                    yield "On analyse son profil avec l'offre..."
                    print(
                        f"ia_check: {ia_check}, is_top: {is_top}, argument: {argument}"
                    )

                    time.sleep(random.uniform(3, 5))

                    if not ia_check:
                        print("Candidat non pertinent")
                        yield "Candidat non pertinent"
                        continue
                    else:
                        yield "Ce candidat semble être pertinent pour l'offre..."
                        time.sleep(random.uniform(3, 5))
                        print("Candidat pertinent...")

                    if is_top:
                        print("Candidat top, on envoie un mail...")
                        send_mail(argument, url, config_db)
                        yield "Mail envoyé"
                        # continue
                        #

                yield "🤖 Appel du modèle pour générer un message..."
                print("🤖 [DEBUG] Appel Groq pour le message...")
                time.sleep(random.uniform(6, 8))
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
                yield "Message reçu..."

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
                message = ""

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

                # is_still_here = driver.find_elements(By.XPATH, xpath_input)

                # if not is_still_here:
                current_user_id = config_db.get("user_id")
                print(f"User ID: {current_user_id}")
                supabase_client.table("url_contactees").insert(
                    {"url": url, "user_id": current_user_id}
                ).execute()

            except Exception as e:
                traceback.print_exc()
                print(f"Détails : {e}")
                yield "❌ Échec à l'étape : Clic Envoi"
                time.sleep(random.uniform(6, 9))
                continue

        except Exception as e:
            print(e)
            continue

    if "driver" in locals():
        driver.quit()
        return
