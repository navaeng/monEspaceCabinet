import time
from random import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait


def click_on_message(driver):
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