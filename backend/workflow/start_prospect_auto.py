# import datetime
# import random
# import time
# from datetime import time as dt_time
import random
import threading
import time
from datetime import datetime, timedelta

# from threading import Lock
from typing import Any, cast

# import pytz
# import supabase
from database import supabase_client
from locks import user_lock

# from typing_extensions import Sequence
# from lock import prospection_lock
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
            time.sleep(60)
            # prospection_lock = Lock()

            # Pour recuperer le verrou si il est pas pris
            try:
                for job in data:
                    uid = job.get("user_id")
                    job_id = job.get("id")
                    title = str(job.get("job_title") or "")
                    details = str(job.get("job_details") or "")
                    mode = str(job.get("mode") or "")
                    offre = str(job.get("offre") or "")

                    if uid not in user_lock:
                        user_lock[uid] = threading.Lock()

                    if user_lock[uid].acquire(blocking=False):
                        try:
                            print(
                                f"DEBUG - Job ID : {job_id}, Title : {title}, Details : {details}"
                            )

                            if job_id and title:
                                print(f"Lancement : {title}")
                                supabase_client.table("prospection_settings").update(
                                    {"is_active": True, "has_run_today": True}
                                ).eq("id", job_id).execute()
                                try:
                                    for step in run_chrome(
                                        title, details, mode, offre, job
                                    ):
                                        print(f"LOG [{title}]: {step}")

                                except Exception as e:
                                    print(f"Erreur lors du lancement de {title}: {e}")
                                demain = maintenant + timedelta(days=1)
                                prochaine_heure = demain.replace(
                                    hour=random.randint(8, 19),
                                    minute=random.randint(0, 59),
                                )
                                supabase_client.table("prospection_settings").update(
                                    {
                                        "is_active": False,
                                        # "has_run_today": True,
                                        "hour_start": prochaine_heure.isoformat(),
                                    }
                                ).eq("id", job_id).execute()

                        finally:
                            user_lock[uid].release()
                        # except Exception as e:
                        #     print({e})
                        #     time.sleep(600)
                        #     print("Reload automatique pour verifier les prospect")
            except Exception as e:
                print({e})
                time.sleep(600)
                print("Reload automatique pour verifier les prospect")
        except Exception as e:
            print({e})
            time.sleep(600)
            print("Reload automatique pour verifier les prospect")

        # finally:
        #     # Libération du lock pour cet utilisateur
        #     user_lock[uid].release()


if __name__ == "__main__":
    start_prospect_auto()
