from selenium.webdriver.common.by import By


def find_send_btn(driver):
    send_btn = (
        "//button[contains(@class, 'msg-form__send-btn') or @type='submit']"
    )
    btn_element = driver.find_element(By.XPATH, send_btn)

    return btn_element