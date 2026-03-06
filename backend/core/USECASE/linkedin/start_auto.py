import os
import threading
import time

from core.USECASE.linkedin.classes.object_user_data import object_user_data
from core.query.linkedin.check_start import check_start
from core.query.linkedin.get_job_and_email_password import get_job_and_email_password
from core.query.linkedin.update_has_run_today_true import update_has_run_today_true
from core.query.linkedin.update_is_active_false import update_is_active_false
from core.query.linkedin.update_new_date_to_start import update_new_date_to_start
from core.USECASE.linkedin.chrome.run_chrome import run_chrome
from core.USECASE.linkedin.components.locks import user_lock


def start_auto(data, current_user_id, body):

    user_data = object_user_data(data, current_user_id, body)

    update_is_active_false(data, current_user_id, body)

    while True:
        try:
            check_start()
            try:
                job_id = data.get("id")
                title = data.get("job_title")
                details = data.get("details")
                mode = data.get("mode")
                post = data.get("post")
                job = data.get("job_title")
                uid = current_user_id

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
                                    get_job_and_email_password(user_data, job)

                                    for step in run_chrome(
                                        title,
                                        details,
                                        mode,
                                        post,
                                        user_data,
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
