from selenium.webdriver.common.by import By


def find_buttons_conx(driver):
    boutons_conx = driver.find_elements(
        By.XPATH,
        "//a[contains(@aria-label, 'Inviter') and contains(@aria-label, 'rejoindre votre réseau')]",
    )
    return boutons_conx


