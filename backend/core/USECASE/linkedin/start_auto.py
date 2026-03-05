import os
import random
import threading
import time
from datetime import timedelta
from core.query.linkedin.check_start import check_start
from data.database import supabase_client
from core.USECASE.linkedin.chrome.run_chrome import run_chrome
from core.USECASE.linkedin.locks import user_lock
from core.query.linkedin.get_job_title import get_job_title
from core.query import get_post_instruction

def start_auto(cabinet_name=None, uid=None, post=None, title=None, job=None, job_id=None, details=None, config_db=None, mode=None,
               maintenant=None, rpc_res=None):
    supabase_client.table("prospection_settings").update({"is_active": False}).eq(
        "is_active", True
    ).execute()

    while True:
        try:

            check_start()

            try:
                # get_post_instruction = None
                KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
                print(f"KEY: {KEY_SECRET}")

                print(f"cabinet_name: {cabinet_name}")

                get_job_title(title, KEY_SECRET)

                if post == "":
                    get_post_instruction(uid)

                    data_list = rpc_res.data

                if isinstance(data_list, list) and len(data_list) > 0:
                        decrypted_data = data_list[0]
                        if isinstance(decrypted_data, dict):
                            print("DEBUG - Settings linkedin successfully")
                            job["linkedin_email"] = decrypted_data.get("linkedin_email")
                            job["linkedin_password"] = decrypted_data.get(
                                "linkedin_password"
                            )
                            job["full_name"] = decrypted_data.get("full_name")
                            job["telephone"] = decrypted_data.get("telephone")

                            print(f"linkedin_email: {job['linkedin_email']}")
                            print(f"linkedin_password: {job['linkedin_password']}")
                            print(f"full_name: {job['full_name']}")
                            print(f"telephone: {job['telephone']}")
                        else:
                            print("DEBUG - Invalid settings format")
                else:
                    print("DEBUG - No settings linkedin found")

                    print(
                        f"DEBUG - Job ID : {job_id}, Title : {title}, Details : {details}"
                    )

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
                                    if not isinstance(config_db, dict):
                                        config_db = {}
                                    config_db = {
                                        **job,
                                        **(
                                            config_db
                                            if isinstance(config_db, dict)
                                            else {}
                                        ),
                                    }

                                    for step in run_chrome(
                                        title,
                                        details,
                                        mode,
                                        # candidatrecherche,
                                        post,
                                        config_db,
                                        # cabinet_name,
                                    ):
                                        print(step)

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
                        except Exception as e:
                            print(f"erreur lors du lancement de {title}: {e}")
                        finally:
                            user_lock[uid].release()
            except Exception as e:
                print(f"erreur lors du lancement de {title}: {e}")
        except Exception as e:
                print(f"{e}")
                time.sleep(15)
                print("Reload automatique pour verifier les prospect")

if __name__ == "__main__":
    start_auto()
