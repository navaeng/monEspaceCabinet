import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def post_message(driver, post):

    try:
        post_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//p[contains(text(), 'Commencer un post')]")
            )
        )
        post_input.click()
        time.sleep(random.uniform(3, 5))
        print("Message ouvert")
    except Exception as e:
        print(f"Erreur lors de l'ouverture du message : {e}")
