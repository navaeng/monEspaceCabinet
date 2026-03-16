from fastapi import APIRouter
import subprocess, os

router_start_auto = APIRouter()

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("/usecase/linkedin/APIRouter", "")
CRON_TAG = "# lancement-automatique"

CRON_JOB = (
    f'*/1 * * * * cd "{PROJECT_DIR}" && '
    f'/usr/bin/python3 usecase/linkedin/services/automatisation/planificateur.py '
    f'2>> planificateur.log {CRON_TAG}'
)

@router_start_auto.on_event("startup")
async def root_start_auto():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current = result.stdout if result.returncode == 0 else ""

        filtered = "\n".join(line for line in current.splitlines() if CRON_TAG not in line)

        new_crontab = filtered + f"\n{CRON_JOB}\n"

        subprocess.run(["crontab", "-"], input=new_crontab, text=True, check=True)
        print("Cron enregistré")
    except Exception as e:
        print(e)