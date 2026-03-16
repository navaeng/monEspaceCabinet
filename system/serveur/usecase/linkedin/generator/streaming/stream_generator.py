from usecase.linkedin.chrome.run.run_chrome import run_chrome
from usecase.linkedin.query.tables.prospection_settings.update.update_has_run_today_true import update_has_run_today_true
from usecase.linkedin.query.tables.prospection_settings.update.update_is_active_false import update_is_active_false
from usecase.linkedin.query.tables.prospection_settings.update.update_is_active_true import update_is_active_true
from usecase.linkedin.services.python_functions.generate_next_hour import generate_next_hour


def stream_generator(body, user_data):
    try:
        print(f"🚀 Lancement Chrome pour {body.intitule}")
        update_is_active_true(user_data)
        for step in run_chrome(
            job_title=body.intitule,
            details=body.details,
            mode=body.mode,
            user_data=user_data,
            telephone=body.telephone,
            full_name=body.full_name,
            candidatrecherche=body.candidatrecherche,
        ):
            print(f"{step}\n")
            yield f"{step}\n"
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Erreur lors de la prospection : {str(e)}")

    finally:
        update_is_active_false(user_data)
        update_has_run_today_true()

        print("🔓 Session terminée")