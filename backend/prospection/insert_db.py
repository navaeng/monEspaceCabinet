from database import supabase_client
from selenium.webdriver.common.by import By


def insert_db(container, mode, config_db):
    profile_url = next(
        (
            h.split("?")[0]
            for a in container.find_elements(By.CSS_SELECTOR, "a[href*='/in/']")
            if (h := a.get_attribute("href"))
        ),
        None,
    )
    full_name = container.text.split("\n")[0] if container.text else None
    if profile_url:
        supabase_client.table("linkedin_contacts").insert(
            {
                "user_id": config_db.get("user_id"),
                "profile_url": profile_url,
                "full_name": full_name,
                "origin_mode": mode,
                "status": "en attente",
            }
        ).execute()
