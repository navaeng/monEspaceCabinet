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


async def run():
    jobs = check_start()
    if jobs:
        for p in jobs:
            headers = {
                "Content-Type": "application/json",
                "X-Internal-Secret": os.getenv("INTERNAL_SECRET"),
                "X-User-Id": p.get("user_id")
            }
            payload = {
                **p,
                "intitule": p.get("job_title", ""),
                "segment": p.get("segment", ""),
                "post": p.get("post", ""),
                "candidatrecherche": p.get("candidatrecherche") or "",
            }
            print(f"Payload envoyé : {payload}")
            try:
                async with httpx.AsyncClient(timeout=None) as client:
                    response = await client.post(

                        "http://127.0.0.1:8001/backend/linkedin/start_chrome",

                        json=payload,
                        headers=headers
                    )

                if response.status_code != 200:
                    logging.error(f"422 détail: {response.text}")

                logging.info(p)
                print(f"Status: {response.status_code}")
                print(f"Réponse: {response.text}")
            except Exception as e:
                print(e)

if __name__ == "__main__":
    asyncio.run(run())

