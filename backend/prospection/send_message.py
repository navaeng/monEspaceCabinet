import random
import time
import traceback
from selenium.webdriver.common.keys import Keys
# from core.send_mail import send_mail
from data.prompt.prospection.prompt_message_prospection import (
    prompt_message_prospection,
)
from data.prompt.prospection.prompt_message_sourcing import (
    prompt_message_sourcing,
)
from database import supabase_client
from prospection.script_js.bouton_close_discussion import close_discussion
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from data.call_groq import call_groq


def send_message(
    driver,
    job_title,
    mode,
    config_db,
    details,
    telephone,
    full_name,
    candidatrecherche,
):
    print("Début de l'envoi de messages directs...")
    yield f"Démarrage envoi de messages pour {job_title}..."

    urls = []  # Initialiser urls avant le try
    button = None
    current_user_id = config_db.get("user_id")

    # Autoriser uniquement les profils presents en base linkedin_contacts
    db_profiles_map = {}
    try:
        contacts_res = (
            supabase_client.table("linkedin_contacts")
            .select("profile_url, origin_mode")
            .eq("user_id", current_user_id)
            .execute()
        )
        if contacts_res.data:
            for item in contacts_res.data:
                profile_url = str(item.get("profile_url") or "").split("?")[0]
                origin_mode = str(item.get("origin_mode") or "")
                if profile_url:
                    db_profiles_map[profile_url] = origin_mode
        print(
            f"[DEBUG] {len(db_profiles_map)} Profils trouvé depuis notre base de données"
        )
        yield f"[DEBUG] {len(db_profiles_map)} Profils trouvé depuis notre base de données..."
        time.sleep(3)
    except Exception as e:
        print(f"[WARN] Erreur récupération linkedin_contacts: {e}")

    # ✅ FIX OPTIMISATION: Récupérer les URLs contactées UNE SEULE FOIS
    contacted_urls = set()
    try:
        res = (
            supabase_client.table("url_contactees")
            .select("url")
            .eq("user_id", current_user_id)
            .execute()
        )
        if res.data:
            contacted_urls = set(
                str(item.get("url") or "").split("?")[0]
                for item in res.data
                if item.get("url")
            )
        print(f"[DEBUG] {len(contacted_urls)} URLs déjà contactées en cache")
        yield (f"[DEBUG] {len(contacted_urls)} Profils ont déjà été contactées...")
        time.sleep(3)
    except Exception as e:
        print(f"[WARN] Erreur récupération URLs contactées: {e}")

    try:
        # time.sleep(random.uniform(2, 4))
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        yield "⏳ Chargement de la page des acceptations..."
        time.sleep(random.uniform(5, 7))
        yield "📡 Recherche des profils acceptés..."
        # links = driver.find_elements(
        #     By.XPATH,
        #     "//a[contains(@href, '/in/') and not(contains(@class, 'scale-down'))]",
        # )
        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/in/']")
        yield "✅ Profils trouvés dans le DOM"
        time.sleep(2)
        for link in links:
            url = link.get_attribute("href").split("?")[0]
            print(f"[DEBUG] Checking URL: {url}")
            print(f"[DEBUG] Already in urls: {url in urls}")
            print(f"[DEBUG] In db_profiles_map: {url in db_profiles_map}")
            print(f"[DEBUG] In contacted_urls: {url in contacted_urls}")
            if url not in urls and url in db_profiles_map and url not in contacted_urls:
                print(f"[DEBUG] Adding URL to process: {url}")
                urls.append(url)

        if len(urls) == 0:
            yield "⚠️ Aucun nouveau contact à ce moment"
            print("Aucun profil trouvé")
            pass

        yield f"✅ {len(urls)} profils trouvés (après filtre)..."
        print(
            f"{len(urls)} profils à traiter (base={len(db_profiles_map)}, déjà contactés={len(contacted_urls)})"
        )

    except Exception as e:
        print(f"Erreur lors de la récupération des liens : {e}")
        yield f"⚠️ Erreur: {str(e)[:60]}"
        pass

    previous_message = []
    print (f"{previous_message}")
    for u, url in enumerate(urls, start=1):


        try:
            try:
                print(f"Traitement du profil {u}/{len(urls)}...")
                yield f"Traitement du profil {u}/{len(urls)}..."
                time.sleep(random.uniform(5, 8))

                # url = "https://www.linkedin.com/in/jouna%C3%AFd-ben-salah-601b77222/"
                # search_url = f"https://www.linkedin.com/search/results/people/?keywords={job_title}&origin=GLOBAL_SEARCH_CARD"

                # ✅ CORRECTION BUG: Ajout timeout pour éviter blocage indéfini
                print(f"[DEBUG] Accès au profil: {url}")
                driver.set_page_load_timeout(
                    20
                )  # Timeout de 20 secondes max pour charger la page
                try:
                    driver.get(url)
                    print("[DEBUG] ✅ Page du profil chargée avec succès")
                except Exception as load_error:
                    print(
                        f"[DEBUG] ❌ Timeout/Erreur chargement page profil: {load_error}"
                    )
                    yield "⚠️ Page profil n'a pas pu charger. Passage au suivant..."
                    time.sleep(random.uniform(3, 5))
                    continue
                finally:
                    driver.set_page_load_timeout(
                        30
                    )  # Réinitialiser au timeout par défaut

                # ✅ FIX OPTIMISATION: Vérification DB déjà faite au début (contacted_urls)
                print(f"✅ URL {url} non contactée (validée en cache)")
                yield "✅ Profil valide, traitement..."

                # ✅ CORRECTION BUG: Gestion du cas où <main> n'existe pas
                try:
                    print("[DEBUG] Recherche de l'élément <main>...")
                    profile_main_content = driver.find_element(
                        By.TAG_NAME, "main"
                    ).text.lower()
                    content_lower = profile_main_content
                    print("[DEBUG] ✅ Élément <main> trouvé")
                except Exception as main_error:
                    print(f"[DEBUG] ⚠️ Élément <main> introuvable: {main_error}")
                    print("[DEBUG] Utilisation du body entier comme fallback")
                    try:
                        content_lower = driver.find_element(
                            By.TAG_NAME, "body"
                        ).text.lower()
                    except:
                        print("[DEBUG] ❌ Impossible de récupérer le contenu du profil")
                        yield "⚠️ Impossible de lire le contenu du profil. Passage au suivant..."
                        time.sleep(random.uniform(3, 5))
                        continue

                print(f"Contenu pour checker les candidats : {content_lower[:200]}...")

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

                    # if mode == "sourcing":
                    #     ia_check, is_top, argument = prompt_sourcing(candidatrecherche)
                    #     yield "On analyse son profil avec l'offre..."
                    #     print(
                    #         f"ia_check: {ia_check}, is_top: {is_top}, argument: {argument}"
                    #     )

                    # if not ia_check:
                    #     print("Candidat non pertinent")
                    #     yield "Candidat non pertinent"
                    #     continue
                    # else:
                    #     yield "Ce candidat semble être pertinent pour l'offre..."
                    #     time.sleep(random.uniform(3, 5))
                    #     print("Candidat pertinent...")

                    # if is_top:
                    #     print("Candidat top, on envoie un mail...")
                    #     send_mail(argument, url, config_db)
                    #     yield "Mail envoyé"
                    #     # continue
                    #     #

                origin_mode = db_profiles_map.get(url, "")
                if not origin_mode:
                    print(f"⏭️ Profil {url} pas trouvé en base, skip...")
                    yield "⏭️ Profil non trouvé en base, passage au suivant..."
                    continue
                print(f"origin mode: {origin_mode}")

                time.sleep(4)
                yield "🤖 Appel du modèle pour générer un message..."
                print("🤖 [DEBUG] Appel Groq pour le message...")
                time.sleep(random.uniform(6, 8))
                instruction = ""

                if origin_mode == "prospection":
                    instruction = prompt_message_prospection(
                        job_title, details, telephone, full_name, previous_message
                    )
                elif origin_mode == "sourcing":
                    instruction = prompt_message_sourcing(
                        job_title, details, telephone, full_name, candidatrecherche, previous_message
                    )

                message = call_groq(instruction)
                previous_message.append(message)
                print(f"message ajouté a previous: {message}")
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

            # ✅ CORRECTION BUG: Ajout try-except pour éviter le blocage silencieux
            try:
                print("[DEBUG] Recherche du bouton 'Message' sur le profil...")
                yield "🔍 Recherche du bouton de message..."

                try:
                    button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//*[contains(@href, 'messaging/compose')]//*[contains(text(), 'Message')] | //button[contains(., 'Message')]",
                            )
                        )
                    )
                    print("[DEBUG] ✅ Bouton 'Message' trouvé après attente")
                except Exception as timeout_error:
                    print(
                        f"[DEBUG] ⚠️ Timeout attente bouton 'Message': {timeout_error}"
                    )
                    print(f"[DEBUG] URL actuelle: {driver.current_url}")

                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", button
                )
                print("[DEBUG] Clic sur le bouton 'Message'...")
                driver.execute_script("arguments[0].click();", button)
                yield "✅ Bouton 'Message' cliqué..."
                print("Boutton de message cliqué")
                time.sleep(random.uniform(6, 8))

            except Exception as e:
                print(
                    f"[DEBUG] ❌ Erreur lors de la gestion du bouton Message: {type(e).__name__}: {e}"
                )
                traceback.print_exc()
                yield f"❌ Erreur lors du clic sur Message: {str(e)[:80]}"
                time.sleep(random.uniform(3, 5))
                continue

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
                # yield "❌ Échec à l'étape : Recherche Input"
                time.sleep(random.uniform(6, 9))
                # yield "On a rencontré un soucis lors de la recherche du bouton d'envoi, rien de grave on continue avec d'autres profils..."
                continue
                # on ecris le message
            try:

                def slow_type(element, text):
                    for char in text:
                        element.send_keys(char)
                        time.sleep(random.uniform(0.15, 0.25))

                # message_box.send_keys(message)
                slow_type(message_box, message)
                yield "Saisie du message..."
                time.sleep(random.uniform(6, 9))
            except Exception as e:
                traceback.print_exc()
                print(f"Détails : {e}")
                yield "❌ Échec à l'étape : Saisie du message"
                time.sleep(random.uniform(6, 9))
                # yield "On a rencontré un soucis au moment de saisir le message, rien de grave on continue avec d'autres profils..."
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
                # yield "On a rencontré un soucis au moment de localiser le bouton d'envoi, rien de grave on continue avec d'autres profils..."
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
                # ✅ current_user_id déjà disponible depuis le début
                print(f"User ID: {current_user_id}")
                supabase_client.table("url_contactees").insert(
                    {"url": url, "user_id": current_user_id}
                ).execute()

            except Exception as e:
                traceback.print_exc()
                print(f"Détails : {e}")
                yield "❌ Échec à l'étape : Clic Envoi"
                time.sleep(random.uniform(6, 9))
                # yield "On a rencontré un soucis lors de l'envoi du message, rien de grave on continue avec d'autres profils..."
                continue

            try:
                print("On va tenter de fermer la fenêtre")
                yield "On va fermer la fenêtre de discussion..."
                time.sleep(4)
                # close_xpath = "//*[@data-test-icon='close-small']/ancestor::button"

                # close_btn = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.XPATH, close_xpath))
                # )

                # driver.execute_script("arguments[0].click();", close_btn)
                # time.sleep(random.uniform(5, 10))
                #
                try:
                    print('tentative close discussion')
                    time.sleep(5)

                    # result = close_discussion(driver)
                    driver.switch_to.active_element.send_keys(Keys.ESCAPE)

                    time.sleep(5)
                    print('fenetre fermée...')
                    # print(f"resultat close discussion {result}")
                except Exception as e:

                    # driver.find_element(By.CSS_SELECTOR, "button[data-control-name='close_messaging_shell']").click()
                    print(f"erreur {e}")
                time.sleep(6)
                print("la fenêtre de discussion a été fermée.")
                yield "Fenêtre fermée... On passe au profil suivant"
                time.sleep(random.uniform(5, 10))

            except Exception as e:
                print(f"Erreur lors de la fermeture des fenêtres : {e}")
                print(f"Erreur bouton close :\n{traceback.format_exc()}")

        except Exception as e:
            print(f"Erreur : {e}")
            print(f"Erreur :\n{traceback.format_exc()}")
            continue

        finally:
            print("bloc finally")
            print("Fin de la boucle principale dans send_message. Tous les profils ont été traités.")
