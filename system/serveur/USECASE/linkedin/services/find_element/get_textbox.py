import traceback
from datetime import time
from random import random

from selenium.webdriver.common.by import By


def get_textbox(driver):
        xpath_input = "//div[@role='textbox' and contains(@class, 'msg-form__contenteditable')]"
        time.sleep(10)
        yield "On cherche le bouton..."
        message_box = driver.find_element(By.XPATH, xpath_input)
        message_box.click()
        time.sleep(random.uniform(4, 7))
        yield "Bouton trouvé..."

        return message_box