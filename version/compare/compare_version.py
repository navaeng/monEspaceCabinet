import requests
import os

def compare_version():
    print('compare version...')
    
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
    current_version = "v1.1.2"

    if latest_version > current_version:
        
        assets = response.json()["assets"]
        print(f"Available assets: {assets}")
        download_url = response.json()["assets"][0]["url"]

        download_headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/octet-stream"
        }

        print(f'Download URL: {download_url, download_headers }')
        from version.download.downloader import download_new_version
        new_exe = download_new_version(download_url, GITHUB_TOKEN)
        if new_exe:
            from version.update.update_app import update_app
            update_app(new_exe)
            
        return True, download_url
    return False, None

