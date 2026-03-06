from datetime import time
from random import random

from selenium.webdriver.common.by import By

from core.USECASE.linkedin.loop.check_profiles_in_db import check_profiles_in_db
from core.query.linkedin.get_url_contactees import get_url_contactees


def find_profiles_links(driver):
    urls = []
    db_profiles_map = check_profiles_in_db()
    contacted_urls = get_url_contactees()

    try:
        yield "⏳ Chargement de la page des relations..."
        time.sleep(random.uniform(5, 7))
        yield "📡 Recherche des profils acceptés..."

        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/in/']")
        yield "✅ Profils trouvés dans le DOM"
        time.sleep(2)
        for link in links:
            url = link.get_attribute("href").split("?")[0]
            print(f"[DEBUG] Checking URL: {url}")
            print(f"[DEBUG] Already in urls: {url in urls}")
            print(f"[DEBUG] In db_profiles_map: {url in db_profiles_map}")
            print(f"[DEBUG] In contacted_urls: {url in contacted_urls}")
            if url not in urls and url in db_profiles_map and url not in contacted_urls:
                print(f"[DEBUG] Adding URL to process: {url}")
                urls.append(url)

        if len(urls) == 0:
            yield "⚠️ Aucun nouveau contact à ce moment"
            print("Aucun profil trouvé")
            pass

        yield f"✅ {len(urls)} profils trouvés (après filtre)..."
        print(
            f"{len(urls)} profils à traiter (base={len(db_profiles_map)}, déjà contactés={len(contacted_urls)})"
        )

    except Exception as e:
        print(f"Erreur lors de la récupération des liens : {e}")
        yield f"⚠️ Erreur: {str(e)[:60]}"
        pass

    return urls, db_profiles_map