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


def post_message(driver, post):

    try:
        instruction = "Donne un message court en une phrase"
        prompt = post_prompt(instruction)
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

                time.sleep(1)
                button_post.click()
                print("Message publié")

            except Exception:
                traceback.print_exc()
                print("------------------------")

    except Exception as e:
        print(f"Erreur : {e}")
