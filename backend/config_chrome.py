def config_chrome():

    print(f"[DEBUG] Offre : {offre}")
    print(f"[DEBUG] Entrée dans run_chrome pour: {job_title}")
    print(f"[DEBUG] Détails de la prospection : {details}")
    print(f"[DEBUG] Mode : {mode}")
    print(f"CONFIG DB: {config_db}")

    uid = config_db.get("user_id")
    print(f"[DEBUG] User ID: {uid}")

    if not uid:
        print(
            "❌ ERREUR : Pas d'ID utilisateur, Chrome ne sait pas quel dossier ouvrir !"
        )
        return
    # print(f"🔍 [RUN_CHROME] job_title: {job_title}")
    # print(f"🔍 [RUN_CHROME] config_db: {config_db}")
    print(f"🔍 [RUN_CHROME] Email: {config_db.get('linkedin_email')}")
    print(
        f"🔍 [RUN_CHROME] Password présent: {'OUI' if config_db.get('linkedin_password') else 'NON'}"
    )

    options = uc.ChromeOptions()
    profil_path = os.path.abspath(f"cookies/profile_{uid}")
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

    job_title = config_db.get("query")
    if job_title:
        print(f"Titre du poste: {job_title}")

    if not job_title:
        job_title = config_db.get("job_title")
        print(f"Titre du poste: {job_title}")

    full_name = config_db.get("full_name")
    telephone = config_db.get("telephone")

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
    time.sleep(random.randint(10, 30))
    print("temps choisi : ", random.randint(10, 30))
    driver = uc.Chrome(
        options=options,
        # service=chrome_service,
        use_subprocess=True,
        version_main=v_chrome,
    )
    driver.maximize_window()
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        },
    )
