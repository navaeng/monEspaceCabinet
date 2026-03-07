import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

base_dir = Path(__file__).resolve().parent.parent.parent
env_path = base_dir / ".env"

if not env_path.exists():
    raise FileNotFoundError(f"Fichier .env introuvable ici : {env_path}")
load_dotenv(dotenv_path=env_path)

print(f"environnement : {env_path}")

url = os.environ.get("SUPABASE_URL", "")
key = os.environ.get("SUPABASE_ANON_KEY", "")

print(f"url: {url}, key: {key}")
supabase_client = create_client(url, key)
supabase_client.postgrest.timeout = 60