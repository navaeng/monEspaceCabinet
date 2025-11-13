import requests
import os
import sys

def make_update(download_url):
    try:
        dir = os.path.join(os.path.dirname(sys.executable), "temp")
        os.makedirs(dir, exist_ok=True)

        print("process ok ...")
        response = requests.get(download_url, stream=True)

        new_exe_app = os.path.join(dir, "nava_last_version.exe")

        with open(new_exe_app, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print('process ok step 2...')
        return new_exe_app

    except Exception as e:
        print(f"Download failed: {e}")
        return None