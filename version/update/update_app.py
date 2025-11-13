import shutil
import sys
import subprocess
import os


def update_app(download_url, GITHUB_TOKEN=None):
    from version.download.downloader import download_new_version
    new_exe = download_new_version(download_url, GITHUB_TOKEN)

    if new_exe:
        current_exe = sys.executable    
        temp_exe = current_exe + ".new"   

        shutil.move(new_exe, temp_exe)

        updater_script = f"""
import shutil, time, sys, os
time.sleep(1)  
shutil.move(r'{temp_exe}', r'{current_exe}')
subprocess.Popen([r'{current_exe}'])
"""
     
    temp_updater = os.path.join(os.path.dirname(current_exe), "updater_temp.py")
    with open(temp_updater, "w") as f:
        f.write(updater_script)

    subprocess.Popen([sys.executable, temp_updater])
    sys.exit(0)