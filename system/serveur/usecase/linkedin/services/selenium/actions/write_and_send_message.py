import time
import random

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def write_and_send_message(driver, btn_element):
    try:
        driver.execute_script("arguments[0].removeAttribute('disabled');", btn_element)
        time.sleep(random.uniform(7, 9))

        driver.execute_script("arguments[0].click();", btn_element)
        time.sleep(random.uniform(6, 9))

        time.sleep(random.uniform(5, 9))
        print("✅ Message envoyé")

        ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        print("✅ Message envoyé et fenêtre fermée")
    except Exception as e:
        print(f"❌ Erreur write_and_send_message: {e}")
        raise e