import random
import time
import json
from selenium.webdriver.common.keys import Keys
from usecase.linkedin.services.find_element.login.find_email_input import find_email_input
from usecase.linkedin.services.find_element.login.find_password_input import find_password_input
from usecase.linkedin.services.python_functions.slow_type import slow_type


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
            print("Connexion success, redirection vers feed OK")

            cookies = driver.get_cookies()
            with open(f"usecase/linkedin/cookies/cookies_{user_data.get('id')}.json", "w") as file:
                json.dump(cookies, file)
            yield "Connexion success !"
        else:
            print(f"Redirection après login: {driver.current_url}")

    except Exception as e:
        print(f"CRASH BLOC LOGIN: {str(e)}")
        yield f"Error de connexion : {type(e).__name__}"
        raise e
