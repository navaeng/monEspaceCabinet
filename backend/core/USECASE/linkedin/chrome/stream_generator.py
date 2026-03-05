from fastapi.responses import StreamingResponse
from core.USECASE.linkedin.chrome.run_chrome import run_chrome
from core.query.linkedin.update_state_of_elements import update_state_of_elements


def stream_generator(body, config_db):
    try:
        print(f"🚀 Lancement Chrome pour {body.intitule}")
        for step in run_chrome(
            job_title=body.intitule,
            details=body.details,
            mode=body.mode,
            post=body.post or "",
            config_db=config_db,
            telephone=body.telephone or "",
            full_name=body.full_name or "",
            cabinet_name=config_db.get("cabinet_name") or "",
        ):
            print(f"{step}\n")
            yield f"{step}\n"
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Erreur lors de la prospection : {str(e)}")

    finally:
        update_state_of_elements()
        print("🔓 Session terminée")

    return StreamingResponse(stream_generator(body, config_db), media_type="text/plain")
