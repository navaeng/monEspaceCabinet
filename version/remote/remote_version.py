import os
import requests
import base64
RAW_VERSION_URL = "https://github.com/Ishak-devs/ERP/releases/latest"

def get_remote_version():
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
        
    }

    print(f"Fetching version from: {RAW_VERSION_URL}")
    
    r = requests.get(RAW_VERSION_URL, headers=headers)
    if r.status_code == 200:
        data = r.json()
        version = base64.b64decode(data["content"]).decode().strip()
        return version
    else:
        print(f"Erreur {r.status_code} lors de l'accès à la version distante.")
        return None