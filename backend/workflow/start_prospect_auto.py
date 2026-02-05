# import datetime
# import random
# import time
# from datetime import time as dt_time
import random
import time
from datetime import datetime, timedelta

# from threading import Lock
from typing import Any, cast

# import pytz
# import supabase
from database import supabase_client

# from typing_extensions import Sequence
from lock import prospection_lock
from prospection.start_prospection import run_chrome


def start_prospect_auto():
    supabase_client.table("prospection_settings").update({"is_active": False}).eq(
        "is_active", True
    ).execute()

    while True:
        try:
            maintenant = datetime.now().astimezone()
            # delai = random.randint(1, 55)
            res = (
                supabase_client.table("prospection_settings")
                .select("*")
                .eq("has_run_today", False)
                .lte("hour_start", maintenant.isoformat())
                .execute()
            )
            data = cast(list[dict[str, Any]], res.data or [])
            print(f"DEBUG - Nombre de jobs trouvés : {len(data)}")
            # prospection_lock = Lock()

            if prospection_lock.acquire(
                blocking=False
            ):  # Pour recuperer le verrou si il est pas pris
                try:
                    for job in data:
                        job_id = job.get("id")
                        title = str(job.get("job_title") or "")
                        details = str(job.get("job_details") or "")

                        if job_id and title:
                            print(f"Lancement : {title}")
                            supabase_client.table("prospection_settings").update(
                                {"is_active": True, "has_run_today": True}
                            ).eq("id", job_id).execute()
                            try:
                                list(run_chrome(title, details, job))
                            except Exception as e:
                                print(f"Erreur lors du lancement de {title}: {e}")

                            demain = maintenant + timedelta(days=1)
                            prochaine_heure = demain.replace(
                                hour=random.randint(8, 19), minute=random.randint(0, 59)
                            )
                            supabase_client.table("prospection_settings").update(
                                {
                                    "is_active": False,
                                    # "has_run_today": True,
                                    "hour_start": prochaine_heure.isoformat(),
                                }
                            ).eq("id", job_id).execute()
                finally:
                    prospection_lock.release()
        except Exception as e:
            print({e})
        time.sleep(60)
        print("Reload automatique pour verifier les prospect")


"""


def start_prospect_auto():
    h, m = random.randint(10, 14), random.randint(0, 59)
    target_time = dt_time(11, 35)
    print(f"Start... Prochain lancement prévu à : {target_time}")

    while True:
        tz_paris = pytz.timezone("Europe/Paris")
        now = datetime.datetime.now(tz_paris)

        res = supabase_client.table("prospection_settings").select("*").execute()

        data_list = res.data if isinstance(res.data, list) else []

        print(f"Data list: {data_list}")

        # if current_time >= target_time:
        #   print(f"[{now.strftime('%H:%M:%S')}] Lancement de la prospection...")

        for c in data_list:
            if not isinstance(c, dict):
                continue
            config: dict[str, Any] = c
            job_id = config["id"]
            job = config["job_title"]

            if not config.get("has_run_today", False):
                try:
                    supabase_client.table("prospection_settings").update(
                        {"is_active": True}
                    ).eq("id", job_id).execute()
                    print(f"Lancement pour : {job}")
                    for update in run_chrome(job, config):
                        print(f"Lancement pour : {job} {update}")

                    supabase_client.table("prospection_settings").update(
                        {"has_run_today": True}
                    ).eq("id", job_id).execute()

                    time.sleep(120)
                except Exception as e:
                    print(f"Erreur lors du lancement : {e}")

                finally:
                    supabase_client.table("prospection_settings").update(
                        {"is_active": False}
                    ).eq("id", job_id).execute()
                    print(f"Terminé : {job}")

        print("Tous les jobs sont terminés. En attente de demain.")
        time.sleep(3600)

        if now.hour == 0 and now.minute == 0:
            supabase_client.table("prospection_settings").update(
                {"has_run_today": False}
            ).neq("id", 0).execute()
            print(f"Reset fini. Nouvelle cible : {target_time}")
            time.sleep(60)

            h = random.randint(9, 11)
            m = random.randint(0, 59)
            target_time = dt_time(h, m)
            time.sleep(10)

"""
if __name__ == "__main__":
    start_prospect_auto()
