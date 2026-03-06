import time

from data.database import supabase_client


def get_url_contactees(user_data):
    current_user_id = user_data.get("user_id")
    contacted_urls = set()
    try:
        res = (
            supabase_client.table("url_contactees")
            .select("url")
            .eq("user_id", current_user_id)
            .execute()
        )
        if res.data:
            contacted_urls = set(
                str(item.get("url") or "").split("?")[0]
                for item in res.data
                if item.get("url")
            )
        print(f"[DEBUG] {len(contacted_urls)} URLs déjà contactées en cache")
        print (f"[DEBUG] {len(contacted_urls)} Profils ont déjà été contactées...")
        time.sleep(3)
    except Exception as e:
        print(f"[WARN] Erreur récupération URLs contactées: {e}")

    return contacted_urls