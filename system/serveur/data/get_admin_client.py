import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

def get_admin_client():

    # base_dir = Path(__file__).resolve().parent.parent.parent
    # env_path = base_dir / ".env"
    #
    # if not env_path.exists():
    #     raise FileNotFoundError(f"Fichier .env introuvable ici : {env_path}")
    load_dotenv()

    url = os.environ.get("SUPABASE_URL", "")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

    return create_client(url, service_key)

admin_supabase = get_admin_client()