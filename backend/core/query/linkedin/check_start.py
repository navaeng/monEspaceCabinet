from datetime import datetime, time
from zoneinfo import ZoneInfo
from typing import cast, Any
from loop.for_job_in_data import for_job_in_data
from core.USECASE.linkedin.locks import user_lock
from data.database import supabase_client


def check_start():
            paris_tz = ZoneInfo("Europe/Paris")
            maintenant = datetime.now(paris_tz).isoformat()

            res = supabase_client.table("prospection_settings")\
                .select("*")\
                .eq("has_run_today", False)\
                .lte("hour_start", maintenant)\
                .execute()

            print(f"CONTENU BRUT SUPABASE : {res.data}")
            data = cast(list[dict[str, Any]], res.data or [])
            print(f"DEBUG - Nombre de jobs trouvés : {len(data)}")
            if any (lock.locked() for lock in user_lock.values()):
                print('lock libéré on vérifie les prospections...')
                time.sleep(60)

            for_job_in_data()
