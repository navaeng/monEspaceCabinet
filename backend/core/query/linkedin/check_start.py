from datetime import time
from typing import cast, Any
from core.USECASE.linkedin.loop.for_job_in_data import for_job_in_data
from core.USECASE.linkedin.components.locks import user_lock
from core.query.query_check_job import query_check_job


def check_start():

    res = query_check_job()

    print(f"CONTENU BRUT SUPABASE : {res.data}")
    data = cast(list[dict[str, Any]], res.data or [])
    print(f"DEBUG - Nombre de jobs trouvés : {len(data)}")
    if any (lock.locked() for lock in user_lock.values()):
                print('lock libéré on vérifie les prospections...')
    time.sleep(60)

    for_job_in_data(data)
