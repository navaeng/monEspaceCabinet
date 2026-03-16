from datetime import datetime
from zoneinfo import ZoneInfo
from data.database import supabase_client

def query_check_job():
    paris_tz = ZoneInfo("Europe/Paris")
    maintenant = datetime.now(paris_tz).isoformat()

    if supabase_client().table("prospection_settings").select("id").eq("is_active", True).execute().data:
        return []

    return supabase_client().table("prospection_settings") \
        .select("*") \
        .eq("has_run_today", False) \
        .lte("hour_start", maintenant) \
        .execute()