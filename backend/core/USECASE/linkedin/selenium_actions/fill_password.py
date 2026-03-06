from datetime import time
from core.USECASE.linkedin.components.slow_type import slow_type
from core.query.user.get_password import get_password

def fill_password(job_title, KEY_SECRET, find_password_input):
    get_password(job_title, KEY_SECRET)

    if find_password_input:
        print(f"DEBUG: Saisie du mot de passe {get_password}...")

        find_password_input.click()
        slow_type(get_password, get_password)
        time.sleep(1)
    else:
        print("Mot de passe vide après RPC")
        yield "Mot de passe linkedin vide ou incorrect."
        return