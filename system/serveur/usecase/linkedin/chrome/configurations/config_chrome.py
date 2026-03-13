import os
import re
import subprocess
import traceback

import undetected_chromedriver as uc


def config_chrome(user_data):
    uid = user_data.get("user_id")
    print(f"[DEBUG] User ID: {uid}")

    if not uid:
        print(
            "❌ ERREUR : Pas d'ID utilisateur, Chrome ne sait pas quel documents ouvrir !"
        )
        return

    print(f"🔍 [CONFIG] Email: {user_data.get('linkedin_email')}")
    print(
        f"🔍 [CONFIG] Password présent: {'OUI' if user_data.get('linkedin_password') else 'NON'}"
    )

    options = uc.ChromeOptions()
    profil_path = os.path.abspath(f"usecase/linkedin/cookies/profile_{uid}")
    lock_file = os.path.join(profil_path, "SingletonLock")

    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
            print("lock supprimé avec succès")
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier de verrouillage : {e}")

    print(f"[DEBUG] Path profil: {profil_path}")
    options.add_argument(f"--user-data-dir={profil_path}")
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

    KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
    print(f"KEY: {KEY_SECRET}")

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

    except Exception as e:
        print(f"❌ Erreur lancement Chrome : {traceback.format_exc()}")  # Affiche toute la pile d'erreurs
        return None
    print('fin de lancement chrome')

    return driver
