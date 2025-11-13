import requests
import os

def compare_version():
    print('compare')
    
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    headers = {
        "User-Agent": "Ishak-devs-ERP-Updater",
        "Accept": "application/vnd.github+json"
    }
    
    headers["Authorization"] = f"token {GITHUB_TOKEN}"
    remote_version = "https://api.github.com/repos/Ishak-devs/ERP/releases/latest"
    response = requests.get(remote_version, headers=headers)
    print("Response JSON:", response.json())
    print(response.status_code)
    latest_version = response.json()["tag_name"]
    print('remote_version:', remote_version)
    current_version = "v.1.0"

    #if latest_version > current_version:
        #download_url = response.json()["assets"][0]["browser_download_url"]
        #return True, download_url
    #return False, None