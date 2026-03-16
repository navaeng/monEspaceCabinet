import time
import random


def write_and_send_message(driver, btn_element):
    driver.execute_script(
        "arguments[0].removeAttribute('disabled');", btn_element
    )
    time.sleep(random.uniform(7, 9))

    driver.execute_script("arguments[0].click();", btn_element)
    time.sleep(random.uniform(6, 9))

    time.sleep(random.uniform(5, 9))