from datetime import timedelta, datetime
from random import random
from zoneinfo import ZoneInfo

from system.data import supabase_client


def update_new_date_to_start(job_id):

    maintenant = datetime.now(ZoneInfo("Europe/Paris"))
    demain = maintenant + timedelta(days=1)
    prochaine_heure = demain.replace(
        hour=random.randint(8, 19),
        minute=random.randint(0, 59),
    )
    supabase_client.table("prospection_settings").update(
        {
            "is_active": False,
            "hour_start": prochaine_heure.isoformat(),
        }
    ).eq("id", job_id).execute()