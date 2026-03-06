import random
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from core.USECASE.linkedin.find_element.find_email_input import find_email_input
from core.USECASE.linkedin.find_element.find_password_input import find_password_input
from core.USECASE.linkedin.components.slow_type import slow_type


def login_linkedin(driver, user_data):

    try:
        email_user = user_data.get("linkedin_email")
        pass_user = user_data.get("linkedin_password")

        email_el = find_email_input(driver)
        pass_el = find_password_input(driver)

        email_el.clear()
        pass_el.clear()

        slow_type(email_el, email_user)
        time.sleep(random.uniform(2, 4))
        slow_type(pass_el, pass_user)
        time.sleep(random.uniform(2, 4))

        pass_el.send_keys(Keys.ENTER)

        if "feed" in driver.current_url:
            print("Connexion réussie, redirection vers feed OK")
            yield "Connexion réussie !"
        else:
            print(f"Redirection après login: {driver.current_url}")
            yield "Connexion en cours (vérification challenge ou captcha...)..."

    except Exception as e:
        print(f"CRASH BLOC LOGIN: {str(e)}")
        yield f"Erreur de connexion : {type(e).__name__}"
        raise e
