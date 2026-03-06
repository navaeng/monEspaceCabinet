import random
import time
import urllib.parse

from core.USECASE.linkedin.script_JS.find_button_envoyer_sans_note import find_button_envoyer_sans_note
from core.query.cabinets.get_cabinets_name import get_cabinets_name
from selenium.webdriver.common.by import By


def request_connexion(driver, job_title, user_data):

    for page in range(1, 2):
        try:
            time.sleep(random.uniform(8, 15))
            query_encoded = urllib.parse.quote(job_title)
            target_url = f"https://www.linkedin.com/search/results/people/?keywords={query_encoded}&origin=SWITCH_SEARCH_VERTICAL&page={page}"
            driver.get(target_url)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            yield "Recherches de personnes..."
        except Exception as e:
            print(f"{str(e)}")

        time.sleep(random.uniform(4, 8))

        boutons_conx = driver.find_elements(
            By.XPATH,
            "//a[contains(@aria-label, 'Inviter') and contains(@aria-label, 'rejoindre votre réseau')]",
        )

        yield f" {len(boutons_conx)} personnes trouvés..."

        for i, bouton in enumerate(boutons_conx):
            try:
                container = bouton.find_element(
                    By.XPATH, "./ancestor::div[@role='listitem'][1]"
                )
                print(f"Container text: {container.text}")

                infos_profil = container.text.lower().replace("\n", "").strip()

                cabinet_name = get_cabinets_name(user_data)

                yield f"On va vérifier si {cabinet_name} est mentionné dans son profil..."
                print(f"On va vérifier si la personne est chez nous {cabinet_name}...")

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

                success = find_button_envoyer_sans_note(driver)
                if success:
                    yield "✅ Invitation envoyée !"
                else:
                    yield "Bouton introuvable."

                yield " Invitation envoyée avec succès !"
            except Exception as e:
                yield f"  ⚠ Erreur bouton Envoyer : {e}"
