from datetime import time

from core.query import config_db
from core.query.linkedin.get_linkedin_contacts import get_linkedin_contacts


def check_profiles_in_db():
    db_profiles_map = {}
    current_user_id = config_db.get("user_id")
    contacts_res = get_linkedin_contacts(current_user_id)

    if contacts_res.data:
        try:
            for item in contacts_res.data:
                profile_url = str(item.get("profile_url") or "").split("?")[0]
                origin_mode = str(item.get("origin_mode") or "")
                if profile_url:
                    db_profiles_map[profile_url] = origin_mode
            print(
                f"[DEBUG] {len(db_profiles_map)} Profils trouvé depuis notre base de données"
            )
            yield f"[DEBUG] {len(db_profiles_map)} Profils trouvé depuis notre base de données..."
            time.sleep(3)
        except Exception as e:
            print(f"[WARN] Erreur {e}")

    return db_profiles_map