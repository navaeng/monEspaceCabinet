import random
import time
import traceback
from datetime import datetime, timezone

from data.database import supabase_client
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing_extensions import Any


def post_message(driver, post, config_db, message_ia=None):

    yield "On va checker la derniere fois qu'on a posté..."
    print("On va checker la derniere fois qu'on a posté...")

    res = (
        supabase_client.table("posts")
        .select("id, last_posted_at")
        .eq("user_id", config_db.get("user_id"))
        # .neq("id", config_db.get("id"))
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    print(f"resultat de la requete sur la table posts: {res}")

    data: Any = res.data

    if list(res.data) and len(res.data) > 0:
        row: dict = data[0]

        print(f"data : {data}")
        now = datetime.now(timezone.utc)

        last_post = datetime.fromisoformat(
            row["last_posted_at"].replace("+00", "+00:00")
        )
        print(f"last_post: {last_post}")

        row_id = row["id"]
        print(f"row_id: {row_id}")

        # delta = now - last_post
        delta = now.replace(tzinfo=None) - last_post.replace(tzinfo=None)
        post_recent = delta.days < 2

        if message_ia:
            driver.execute_script("arguments[0].focus();", editor)
            time.sleep(5)
            editor.click()
            actions = ActionChains(driver)
            actions.move_to_element(editor)
            actions.click()
            actions.perform()

            print("Editor clicked")
            yield "Message reçu de la part du modèle..."
            time.sleep(2)
            yield "✍️ Écriture du message en cours..."

            print("[DEBUG-STEP] Lancement post message")
            for char in message_ia:
                # time.sleep(3)
                actions.send_keys(char)
                actions.perform()
                time.sleep(random.uniform(0.14, 0.22))
            time.sleep(2)

            try:
                wait = WebDriverWait(driver, 10)
                # xpath_button_post = "//button//span[contains(text(), 'Publier')]/.."
                xpath_button_post = "//button[.//span[contains(text(), 'Publier')]]"
                button_post = wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath_button_post))
                )

                js_find_editor = """
                                        function findDeep(sel, root = document) {
                                            let n = root.querySelector(sel);
                                            if (n) return n;
                                            let all = root.querySelectorAll('*');
                                            for (let e of all) {
                                                if (e.shadowRoot) {
                                                    let res = findDeep(sel, e.shadowRoot);
                                                    if (res) return res;
                                                }
                                            }
                                            return null;
                                        }
                                        return findDeep("div[contenteditable='true'], div[role='textbox'], .ql-editor");
                                        """

                editor = driver.execute_script(js_find_editor)
                print("Editor found")

                if message_ia:
                    driver.execute_script("arguments[0].focus();", editor)
                    time.sleep(random.uniform(5, 10))
                    editor.click()
                    actions = ActionChains(driver)
                    actions.move_to_element(editor)
                    actions.click()
                    actions.perform()

                    print("Editor clicked")
                    yield "Nous avons pas posté depuis un moment..."
                    yield "Nous allons saisir un post..."
                    time.sleep(random.uniform(5, 10))
                    yield "✍️ Écriture du message en cours..."

                    print("[DEBUG-STEP] Lancement post message")
                    for char in message_ia:
                        # time.sleep(3)
                        actions.send_keys(char)
                        actions.perform()
                        time.sleep(random.uniform(0.25, 0.35))
                    time.sleep(random.uniform(5, 10))

                    try:
                        time.sleep(random.uniform(5, 10))

                        print("✅ Message publié !")
                        yield "✅ Post publié..."
                        time.sleep(random.uniform(5, 10))

                        try:
                            print(
                                "tentative de mise à jour de la date de dernière publication"
                            )

                            supabase_client.table("posts").update(
                                {"last_posted_at": datetime.now().isoformat()}
                            ).eq("id", row_id).execute()

                            print("✅ Date de dernière publication mise à jour")

                        except Exception as e:
                            print(
                                f"❌ Erreur lors de la mise à jour de la date de dernière publication : {e}"
                            )

                    except Exception:
                        print("❌ Bouton introuvable par le script JS")
                        traceback.print_exc()
                        print("------------------------")

            except Exception as e:
                print(f"Erreur : {e}")
