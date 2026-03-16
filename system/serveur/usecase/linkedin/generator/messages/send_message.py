import random
import time
import traceback

from selenium.common import WebDriverException
from selenium.webdriver.common.by import By

from services.api_externes.groq.call_groq import call_groq
from usecase.linkedin.services.instructions.check_mode_and_get_instruction import check_mode_and_get_instruction
from usecase.linkedin.services.find_element.messages.find_profiles_links import find_profiles_links
from usecase.linkedin.services.find_element.messages.find_send_btn import find_send_btn
from usecase.linkedin.services.find_element.posts.get_textbox import get_textbox
from usecase.linkedin.services.selenium.actions.click_on_message import click_on_message
from usecase.linkedin.services.python_functions.slow_type import slow_type
from usecase.linkedin.services.selenium.actions.write_and_send_message import write_and_send_message
from usecase.linkedin.query.tables.url_contactees.insert.insert_url_contactees import insert_url_contactees
from usecase.linkedin.query.tables.cabinets.get.get_cabinets_name import get_cabinets_name as get_cabinets_name


def send_message(
    driver,
    job_title,
    user_data,
    details,
    telephone,
    full_name,
    candidatrecherche
):
    print("start messages directs...")
    yield f"Start envoi de messages pour {job_title}..."

    message = None
    urls, db_profiles_map = find_profiles_links(driver, user_data)

    for u, url in enumerate(urls, start=1):
        try:
            try:
                print(f"Traitement du profil {u}/{len(db_profiles_map)}...")
                yield f"lookig for profil {u}/{len(db_profiles_map)}..."
                time.sleep(random.uniform(5, 8))

                print(f"[DEBUG] Accès au profil: {url}")
                driver.set_page_load_timeout(
                    20
                )

                try:

                    driver.get(url)
                    print("[DEBUG] ✅ Page du profil chargée avec succès")
                except Exception as load_error:
                    print(
                        f"[DEBUG] ❌ Timeout/Erreur chargement page profil: {load_error}"
                    )
                    time.sleep(random.uniform(3, 5))
                    continue
                finally:
                    driver.set_page_load_timeout(
                        30
                    )

                print(f"✅ URL {url} non contactée (validée en cache)")
                yield "✅ Profil valide, traitement..."

                infos_profil = driver.find_element(By.TAG_NAME, "body").text.lower()
                print(f"infos_profil: {infos_profil}")

                result = get_cabinets_name(user_data)

                if result and len(result) == 2:
                    cabinet_name, exclusions = result
                else:
                    cabinet_name, exclusions = "Inconnu", []
                    print(f"[WARN] Données cabinet vides pour {user_data}")

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

                origin_mode = db_profiles_map.get(url, "")
                # if not origin_mode:
                #     print(f"⏭️ Profil {url} pas trouvé en base, skip...")
                #     yield "⏭️ Profil non trouvé en base, passage au suivant..."
                #     continue
                # print(f"origin mode: {origin_mode}")

                time.sleep(4)

                instruction = check_mode_and_get_instruction(origin_mode,     driver,
    job_title,
    details,
    telephone,
    full_name,
    candidatrecherche)
                message = call_groq(instruction)

                time.sleep(random.uniform(6, 8))
            except Exception as e:
                traceback.print_exc()
                print(f"Détails : {e}")
                time.sleep(random.uniform(6, 9))
                yield "Traitement des profils impossibles"

            try:
                print('click on message...')
                click_on_message(driver)
            except Exception as e:
                print(f"{e}")

            try:
                get_text_box = get_textbox(driver)
            except Exception as e:
                traceback.print_exc()
                print(f"Détails : {e}")
                time.sleep(random.uniform(6, 9))
                continue
            try:
                slow_type(get_text_box, message)
                yield "Saisie du message..."
                time.sleep(random.uniform(6, 9))
            except Exception as e:
                traceback.print_exc()
                print(f"Détails : {e}")
                time.sleep(random.uniform(6, 9))
                continue
            try:
                btn_element = find_send_btn(driver)
            except Exception as e:
                traceback.print_exc()
                print(f"Détails : {e}")
                time.sleep(random.uniform(6, 9))
                continue

            try:
                write_and_send_message(driver, btn_element)
                insert_url_contactees(url, user_data)

            except Exception as e:
                traceback.print_exc()
                print(f"Détails : {e}")
                time.sleep(random.uniform(6, 9))
                continue


        except WebDriverException as e:
            print(f"Error :\n{traceback.format_exc()}")
            continue