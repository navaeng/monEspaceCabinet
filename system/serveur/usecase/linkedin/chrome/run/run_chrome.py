import os
import random
import sys
import time

from usecase.linkedin.chrome.mycookies.get_cookies import get_cookies
from usecase.linkedin.generator.connexions.request_connexion import request_connexion
from usecase.linkedin.generator.messages.send_message import send_message
from usecase.linkedin.chrome.configurations.config_chrome import config_chrome
from usecase.linkedin.generator.login.login_linkedin import login_linkedin

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_chrome(
    job_title: str,
    details: str,
    mode: str,
    user_data,
    telephone,
    full_name,
    candidatrecherche,
):

    uid = user_data.get("user_id")
    driver, vdisplay = config_chrome(user_data, uid)

    if driver is not None:
        try:
            yield "Start..."
            time.sleep(random.uniform(3, 6))

            get_cookies(driver, uid)
            driver.get("https://www.linkedin.com/feed/")

            yield "Go LinkedIn..."
            time.sleep(random.uniform(3, 6))
            current_url = driver.current_url

            if "login" in driver.current_url:
                yield from login_linkedin(driver, user_data)

            yield from request_connexion(driver, job_title, user_data)
            yield from send_message(driver, job_title, user_data, details, telephone, full_name, candidatrecherche)

        except Exception as e:
            print(f"Error : {e}")

        finally:
            driver.quit()
            vdisplay.stop()