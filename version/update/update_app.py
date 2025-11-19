def update_app(new_exe):
        import shutil, sys, subprocess, os
        current_exe = sys.executable    
        temp_exe = current_exe + ".new"   

        shutil.move(new_exe, temp_exe)

        updater_script = f"""
import shutil, time, sys, os, subprocess
time.sleep(1)  
shutil.move(r'{temp_exe}', r'{current_exe}')
subprocess.Popen([r'{current_exe}'])
"""
     
        print('update...')
        temp_updater = os.path.join(os.path.dirname(current_exe), "updater_temp.py")
        with open(temp_updater, "w") as f:
            f.write(updater_script)

        subprocess.Popen([sys.executable, temp_updater])

        sys.exit(0)