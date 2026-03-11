from datetime import datetime
from zoneinfo import ZoneInfo

from system.serveur.data.database import supabase_client


def query_check_job():
    paris_tz = ZoneInfo("Europe/Paris")
    maintenant = datetime.now(paris_tz).isoformat()

    all_active_jobs = supabase_client().table("prospection_settings") \
        .select("*") \
        .eq("has_run_today", False) \
        .lte("hour_start", maintenant) \
        .execute()

    return all_active_jobs