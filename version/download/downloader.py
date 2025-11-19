import requests
import os, sys


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def download_new_version(download_url, GITHUB_TOKEN):
    
    try:
        temps_dir = os.path.join(os.path.dirname(sys.executable), "temp")
        os.makedirs(temps_dir, exist_ok=True)

        headers = {
                    "Authorization": f"token {GITHUB_TOKEN}",
                    "User-Agent": "Ishak-devs-ERP-Updater",
                    "Accept": "application/octet-stream"
                   } 
        response = requests.get(download_url, stream=True, headers=headers)
        response.raise_for_status()

        new_exe_app = os.path.join(temps_dir, "nava_last_version.exe")

        with open(new_exe_app, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(response.status_code)
        print(response.headers["Content-Type"])
        return new_exe_app

    except Exception as e:
        print(f"Download failed: {e}")
        return None
