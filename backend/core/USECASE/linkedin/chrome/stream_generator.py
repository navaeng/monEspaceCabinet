from core.USECASE.linkedin.chrome.run_chrome import run_chrome
from core.query.linkedin.update_is_active_false import update_is_active_false


def stream_generator(body, user_data):
    try:
        print(f"🚀 Lancement Chrome pour {body.intitule}")
        for step in run_chrome(
            job_title=body.intitule,
            details=body.details,
            mode=body.mode,
            post=body.post or "",
            user_data=user_data,
        ):
            print(f"{step}\n")
            yield f"{step}\n"
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Erreur lors de la prospection : {str(e)}")

    finally:

        update_is_active_false(user_data)
        print("🔓 Session terminée")
