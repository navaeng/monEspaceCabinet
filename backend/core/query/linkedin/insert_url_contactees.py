from core.query import config_db
from data.database import supabase_client


def insert_url_contactees(url):
    current_user_id = config_db.get("user_id")
    supabase_client.table("url_contactees").insert(
        {"url": url, "user_id": current_user_id}
    ).execute()