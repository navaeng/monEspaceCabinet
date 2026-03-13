def config_cookie(driver):
    driver.get("https://www.linkedin.com")

    driver.add_cookie({
        "name": "lang",
        "value": "v=2&lang=fr-fr",
        "domain": ".linkedin.com",
        "path": "/",
    })



