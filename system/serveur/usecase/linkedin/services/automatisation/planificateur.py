import httpx
import asyncio
import os
import logging
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace("/usecase/linkedin/services/automatisation", ""))


from data.database import supabase_client
from usecase.linkedin.query.check_start import check_start

logging.basicConfig(filename="planificateur.log", level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

supabase = supabase_client()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('SUPABASE_SERVICE_ROLE_KEY')}"
}

async def run():
    jobs = check_start()
    if jobs:
        for p in jobs:
            try:
                async with httpx.AsyncClient(timeout=None) as client:
                    response = await client.post(
                        "http://127.0.0.1:8001/backend/linkedin/start_chrome",
                        json={**p, "intitule": p.get("job_title", "")},
                        headers=headers
                    )
                logging.info(p)
                print(f"Status: {response.status_code}")
                print(f"Réponse: {response.text}")
            except Exception as e:
                print(e)

if __name__ == "__main__":
    asyncio.run(run())

