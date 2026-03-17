import json
import os
import time

from usecase.linkedin.chrome.mycookies.configs.config_cookie import config_cookie


def get_cookies(driver, uid):

    config_cookie(driver)

    cookie_path = f"usecase/linkedin/cookies/cookie_{uid}.json"
    if os.path.exists(cookie_path):
        with open(cookie_path, "r") as f:
            cookies = json.load(f)
            for cookie in cookies:
                if cookie.get("name") == "li_at":
                    driver.add_cookie(cookie)
                    time.sleep(1)
                    driver.refresh()
                    print("Session restaurée via cookie.")