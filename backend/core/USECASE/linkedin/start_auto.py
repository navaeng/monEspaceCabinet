import os
import threading
import time
from core.query.linkedin.check_start import check_start
from core.query.linkedin.get_job_and_email_password import get_job_and_email_password
from core.query.linkedin.update_has_run_today_true import update_has_run_today_true
from core.query.linkedin.update_is_active_false import update_is_active_false
from core.query.linkedin.update_new_date_to_start import update_new_date_to_start
from core.USECASE.linkedin.chrome.run_chrome import run_chrome
from core.USECASE.linkedin.components.locks import user_lock
from core.query.linkedin.get_job_title import get_job_title
from core.query import get_post_instruction
from core.query.user.get_user_informations import get_user_informations


def start_auto(cabinet_name=None, uid=None, post=None, title=None, job=None, job_id=None, details=None, config_db=None, mode=None,
               rpc_res=None):

    update_is_active_false(config_db)

    while True:
        try:
            check_start()
            try:

                KEY_SECRET = os.getenv("ENCRYPTION_SECRET")

                print(f"KEY: {KEY_SECRET}")
                print(f"cabinet_name: {cabinet_name}")

                get_job_title(title, KEY_SECRET)

                if post == "":
                    get_post_instruction(uid)

                    data_list = rpc_res.data

                if isinstance(data_list, list) and len(data_list) > 0:
                        get_user_informations(job)
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
                                update_has_run_today_true(job_id)

                                try:
                                    get_job_and_email_password(config_db, job)

                                    for step in run_chrome(
                                        title,
                                        details,
                                        mode,
                                        post,
                                        config_db,
                                    ):
                                        print(step)
                                    update_new_date_to_start(job_id)

                                except Exception as e:
                                    print(f"Erreur lors du lancement de {title}: {e}")

                        except Exception as e:
                            print(f"erreur lors du lancement de {title}: {e}")
                        finally:
                            user_lock[uid].release()
            except Exception as e:
                print(f"erreur lors du lancement de {title}: {e}")
        except Exception as e:
                print(f"{e}")
                time.sleep(15)
                print("Reload automatique pour verifier les jobs")

if __name__ == "__main__":
    start_auto()
