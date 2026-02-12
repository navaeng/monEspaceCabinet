import random
import time

from data.prompt.post_prompt import post_prompt
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.call_groq import call_groq


def post_message(driver, post):

    try:
        instruction = "Aide nous à généré un message pour Linkedin"
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

        # editor = wait.until(
        #     EC.presence_of_element_located(
        #         (By.CSS_SELECTOR, "div[role='textbox'], .ql-editor")
        #     )
        # )
        #
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
            yield "Messag reçu de la part du modèle.."
            time.sleep(5)

            for char in message_ia:
                actions.send_keys(char)
                actions.perform()
                time.sleep(random.uniform(0.10, 0.15))
                # print(f"Char sent: {char}")

            publish_xpath = "//button[contains(., 'Publier')]"
            publish_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, publish_xpath))
            )
            try:
                time.sleep(random.uniform(0.50, 0.90))
                driver.execute_script("arguments[0].click();", publish_btn)
                print("Message published")
                yield "Message publié..."
                time.sleep(5)

            except Exception as e:
                print(f"Erreur lors de la publication du message : {e}")

    except Exception as e:
        print(f"Erreur : {e}")
