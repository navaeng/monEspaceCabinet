import random
import time
import urllib.parse

from data.database import supabase_client
from selenium.webdriver.common.by import By


def request_connexion(job_title, driver, config_db):

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
