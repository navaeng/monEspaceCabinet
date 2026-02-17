import os
import random
import threading
import time
from datetime import datetime, timedelta

# from threading import Lock
from typing import Any, cast

from database import supabase_client
from locks import user_lock
from prospection.start_prospection import run_chrome

# prospection_lock = Lock()


def start_prospect_auto():
    supabase_client.table("prospection_settings").update({"is_active": False}).eq(
        "is_active", True
    ).execute()

    while True:
        try:
            maintenant = datetime.now().astimezone()

            res = (
                supabase_client.table("prospection_settings")
                .select("*")
                .eq("has_run_today", False)
                .lte("hour_start", maintenant.isoformat())
                .execute()
            )

            print(f"CONTENU BRUT SUPABASE : {res.data}")
            data = cast(list[dict[str, Any]], res.data or [])
            print(f"DEBUG - Nombre de jobs trouvés : {len(data)}")
            time.sleep(60)

            # Pour recuperer le verrou si il est pas pris
            try:
                # get_post_instruction = None
                KEY_SECRET = os.getenv("ENCRYPTION_SECRET")
                print(f"KEY: {KEY_SECRET}")

                for job in data:
                    uid = job.get("user_id")
                    job_id = job.get("id")
                    title = str(job.get("job_title") or "")
                    details = str(job.get("details") or "")
                    mode = str(job.get("mode") or "")
                    offre = str(job.get("offre") or "")
                    post = str(job.get("post") or "")
                    config_db = job.get("config_db") or {}
                    cabinet_name = str(job.get("cabinet_name") or "")

                    print(f"cabinet_name: {cabinet_name}")

                    rpc_res = supabase_client.rpc(
                        "get_decrypted_settings",
                        {"job_title_input": title, "key_input": KEY_SECRET},
                    ).execute()

                    if post == "":
                        get_post_instruction = (
                            supabase_client.table("posts")
                            .select("instruction_post")
                            .eq("user_id", uid)
                            .limit(1)
                        ).execute()
                        post_data = get_post_instruction.data
                        if (
                            post_data
                            and isinstance(post_data, list)
                            and len(post_data) > 0
                        ):
                            first_item = post_data[0]
                            if isinstance(first_item, dict):
                                post = str(first_item.get("instruction_post") or "")
                        # if (
                        #     get_post_instruction
                        #     and get_post_instruction.data
                        #     and len(get_post_instruction.data) > 0
                        # ):
                        #     post = str(
                        #         get_post_instruction.data[0].get("instruction_post")
                        #         or ""
                        #     )
                    # data = rpc_res.data

                    # if rpc_res.data and len(rpc_res.data) > 0:
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
                                        offre,
                                        post,
                                        config_db,
                                        cabinet_name,
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
                time.sleep(15)
                print("Reload automatique pour verifier les prospect")
        except Exception as e:
            print({e})
            time.sleep(15)
            print("Reload automatique pour verifier les prospect")

        # finally:
        #     # Libération du lock pour cet utilisateur
        #     user_lock[uid].release()


if __name__ == "__main__":
    start_prospect_auto()
