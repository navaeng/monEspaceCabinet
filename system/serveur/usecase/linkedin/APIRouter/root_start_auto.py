from fastapi import APIRouter
import subprocess, os

router_start_auto = APIRouter()

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("/usecase/linkedin/APIRouter", "")
CRON_TAG = "# lancement-automatique"
CRON_JOB = f"*/10 * * * * cd {PROJECT_DIR} && /usr/bin/python3 usecase/linkedin/services/automatisation/planificateur.py 2>> planificateur.log {CRON_TAG}"

@router_start_auto.on_event("startup")
async def root_start_auto():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current = result.stdout if result.returncode == 0 else ""
        if CRON_TAG in current:
            print("Cron déja enregistré")
            return
        subprocess.run(["crontab", "-"], input=current + f"\n{CRON_JOB}\n", text=True, check=True)
        print("Cron enregistré")
    except Exception as e:
        print(e)

