import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / "front" / ".env"

load_dotenv(dotenv_path=env_path)

url = os.environ.get("SUPABASE_URL", "")
key = os.environ.get("SUPABASE_ANON_KEY", "")

supabase_client = create_client(url, key)
supabase_client.postgrest.timeout = 60
