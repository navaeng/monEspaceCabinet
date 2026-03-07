from selenium.webdriver.common.by import By
def find_password_input(driver):
    try:
        pass_input = driver.find_element(
            By.CSS_SELECTOR,
            "input#password, input[name='session_password']",
        )
        print("Champ password trouvé")
        return pass_input
    except Exception as e:
        print("Champ password introuvable")
        raise e