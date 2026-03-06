from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def find_email_input(driver):
    try:
        wait = WebDriverWait(driver, 15)
        email_input = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "input#username, input[name='session_key']",
                )
            )
        )
        print("✅ Champ email trouvé")
    except Exception as e:
        print(
            f"❌ Erreur: Impossible de trouver le champ email. URL: {driver.current_url}"
        )
        raise e