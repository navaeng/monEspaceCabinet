import random
import time
import traceback
from datetime import datetime

from data.prompt.post_prompt import post_prompt
from database import supabase_client
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing_extensions import Any

from data.call_groq import call_groq


def post_message(driver, post, config_db):

    yield "On va checker la derniere fois qu'on a posté..."
    print("On va checker la derniere fois qu'on a posté...")
    res = (
        supabase_client.table("prospection_settings")
        .select("created_at")
        .eq("id", config_db.get("id"))
        .execute()
    )

    data: Any = res.data
    if list(res.data) and len(res.data) > 0:
        row: dict = data[0]

        post_recent = (
            datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))
            - datetime.now()
        ).days < 2
        print(f"post_recent : {post_recent}")

        if post_recent:
            yield "On à poster récemment..."
            print("On a poster récemment...")

    print(data)

    full_name = config_db.get("full_name")
    telephone = config_db.get("telephone")
    cabinet_name = config_db.get("cabinet_name")
    print(
        "Infos pour post message:"
        f"Full Name: {full_name}, Telephone: {telephone}, Cabinet Name: {cabinet_name}"
    )

    try:
        # instruction = "Donne un message court en une phrase"
        prompt = post_prompt(post, full_name, telephone, cabinet_name)
        print(f"POST : {post}")

        message_ia = call_groq(prompt)
        print(f"Message généré : {message_ia}")

        # wait = WebDriverWait(driver, 30)
        time.sleep(random.uniform(5, 10))
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
            time.sleep(random.uniform(5, 10))
            editor.click()
            actions = ActionChains(driver)
            actions.move_to_element(editor)
            actions.click()
            actions.perform()

            print("Editor clicked")
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
                from script_element_xpath.post_button import post_button

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

            except Exception:
                print("❌ Bouton introuvable par le script JS")
                traceback.print_exc()
                print("------------------------")

    except Exception as e:
        print(f"Erreur : {e}")
