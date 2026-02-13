import time

from selenium.webdriver.common.by import By


def close_windows(driver):
    try:
        yield "On va nettoyer les fenêtres encore ouvertes..."
        print("On nettoie les fenêtres")
        time.sleep(6)

        close_buttons = driver.find_elements(
            By.CSS_SELECTOR,
            "button[data-control-name='close_messaging_bubble'], .msg-overlay-bubble-header__control--close",
        )
        print(f"nombre de boutons de fermeture trouvés : {len(close_buttons)}")

        for btn in close_buttons:
            print(f"Bouton de fermeture trouvé : {btn}")
            driver.execute_script("arguments[0].click();", btn)
    except Exception as e:
        print(f"Crash lors de la fermeture des fenêtres : {str(e)[:50]}")
