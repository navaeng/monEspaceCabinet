import os
import re
import subprocess
import traceback

import selenium
from selenium.common.exceptions import WebDriverException
import undetected_chromedriver as uc
from xvfbwrapper import Xvfb

def config_chrome(user_data, uid):

    print(f"🔍 [CONFIG] Email: {user_data.get('linkedin_email')}")
    print(
        f"🔍 [CONFIG] Password présent: {'OUI' if user_data.get('linkedin_password') else 'NON'}"
    )

    vdisplay = Xvfb(width=1920, height=1080, colordepth=24)
    # vdisplay.start()

    options = uc.ChromeOptions()

    options.add_argument("--profile-directory=Default")
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disk-cache-size=1")
    options.add_argument("--media-cache-size=1")

    job_title = user_data.get("query")
    if job_title:
        print(f"Titre du poste: {job_title}")

    if not job_title:
        job_title = user_data.get("job_title")
        print(f"Titre du poste: {job_title}")

    full_name = user_data.get("full_name")
    telephone = user_data.get("telephone")

    print(f"Nom complet: {full_name}")
    print(f"Numéro de téléphone: {telephone}")

    key_secret = os.getenv("ENCRYPTION_SECRET")
    print(f"KEY: {key_secret}")

    v_chrome = int(
        next(
            re.finditer(
                r"\d+", subprocess.check_output(["google-chrome", "--version"]).decode()
            )
        ).group()
    )

    try:
        print('Nous lançons chrome...')
        driver = uc.Chrome(
            options=options,
            use_subprocess=True,
            version_main=v_chrome,
        )


    except (selenium.common.exceptions.WebDriverException, RuntimeError) as e:
        print(f"❌ Erreur lancement Chrome : {traceback.format_exc()}")
        return None
    print('fin de lancement chrome')

    return driver, vdisplay
