import random
import time
import traceback

from data.prompt.post_prompt import post_prompt
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.call_groq import call_groq


def post_message(driver, post, config_db):

    full_name = config_db.get("full_name")
    telephone = config_db.get("telephone")
    cabinet_name = config_db.get("cabinet_name")
    print(
        "Infos pour post message:"
        f"Full Name: {full_name}, Telephone: {telephone}, Cabinet Name: {cabinet_name}"
    )

    try:
<<<<<<< HEAD:backend/linkedin/post_message.py
        instruction = "Donne un message court en une phrase"
        prompt = post_prompt(instruction)
=======
        # instruction = "Donne un message court en une phrase"
        prompt = post_prompt(post, full_name, telephone, cabinet_name)
        print(f"POST : {post}")

>>>>>>> clean_code:backend/prospection/post_message.py
        message_ia = call_groq(prompt)
        print(f"Message généré : {message_ia}")

        wait = WebDriverWait(driver, 30)
        post_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//p[contains(text(), 'Commencer un post')]")
            )
        )
        post_input.click()
        time.sleep(random.uniform(3, 5))
        print("Message ouvert")

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

<<<<<<< HEAD:backend/linkedin/post_message.py
                time.sleep(1)
                button_post.click()
                print("Message publié")
=======
                driver.execute_script(post_button())
                # if resultat == "BOUTON_CLIQUE":
                print("✅ Message publié !")
                yield "✅ Post publié..."
                time.sleep(random.uniform(5, 10))
                # else:
                #     if (
                #         len(driver.find_elements(By.CSS_SELECTOR, "div[role='dialog']"))
                #         == 0
                #     ):
                #         print("✅ Le post semble être parti tout seul !")
>>>>>>> clean_code:backend/prospection/post_message.py

            except Exception:
                print("❌ Bouton introuvable par le script JS")
                traceback.print_exc()
                print("------------------------")

    except Exception as e:
        print(f"Erreur : {e}")
