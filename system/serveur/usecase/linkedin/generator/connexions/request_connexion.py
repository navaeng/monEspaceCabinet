import random
import time
import urllib.parse

from selenium.webdriver.common.by import By

from usecase.linkedin.query.tables.linkedin_contactees.insert.insert_linkedin_contacts import insert_linkedin_contacts
from usecase.linkedin.script_JS.buttons.find_button_envoyer_sans_note import find_button_envoyer_sans_note
from usecase.linkedin.query.tables.cabinets.get.get_cabinets_name import get_cabinets_name
from usecase.linkedin.services.find_element.connexions.find_buttons_conx import find_buttons_conx
from usecase.linkedin.services.find_element.connexions.get_container_info import get_container_info


# from usecase.linkedin.services.find_element.connexions.find_buttons_conx import find_buttons_conx
# from usecase.linkedin.services.find_element.connexions.get_container_info import get_container_info


def request_connexion(driver, job_title, user_data):

    for page in range(1, 3):
        try:
            time.sleep(random.uniform(8, 15))
            query_encoded = urllib.parse.quote(job_title)
            target_url = (f"https://www.linkedin.com/search/results/people/?keywords={query_encoded}"
                          f"&origin=SWITCH_SEARCH_VERTICAL&page={page}")
            driver.get(target_url)
            driver.add_cookie({"name": "lang", "value": "v=2&lang=fr-fr", "domain": ".linkedin.com", "path": "/"})
            driver.refresh()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            yield "Searching..."
        except Exception as e:
            print(f"{str(e)}")

        time.sleep(random.uniform(4, 8))


        boutons_conx = find_buttons_conx(driver)
        yield f" {len(boutons_conx)} users finding..."

        for i, bouton in enumerate(boutons_conx):
            try:

                infos_profiles, container = get_container_info(bouton)
                cabinet_name = get_cabinets_name(user_data)

                yield f"check profile..."
                print(f"On va vérifier si la personne est chez nous ...")

                time.sleep(6)
                if cabinet_name:
                    exclusions = [cabinet_name, cabinet_name.replace(" ", "")]

                    if any(excl in infos_profiles for excl in exclusions):
                        yield f"user from {cabinet_name}, skip..."
                        print(f"user from ({cabinet_name}), skip.")
                        time.sleep(random.uniform(3, 5))
                        continue
                    else:
                        yield f"Pas de mention à {cabinet_name}..."

                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", bouton
                )

                time.sleep(random.uniform(2, 4))

                driver.execute_script("arguments[0].click();", bouton)

                yield f"[{i + 1}] invitations..."

                time.sleep(random.uniform(2, 4))

                success = find_button_envoyer_sans_note(driver)
                if success:
                    yield "✅ Invitation sent !"
                    insert_linkedin_contacts(container, user_data)
                else:
                    print('bouton non trouvé')

                yield " Invitation sent !"
            except Exception as e:
                print (f"  ⚠ Error bouton Envoyer : {e}")
