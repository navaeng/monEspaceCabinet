import json


def read_cookie(driver, user_data):

    cookies = driver.get_cookies()
    with open(f"usecase/linkedin/cookies/cookie_{user_data.get('id')}.json", "w") as file:
        json.dump(cookies, file)