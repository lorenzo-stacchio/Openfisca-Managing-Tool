import os
import shutil
import time
import sys
from subprocess import check_output

def download_and_install(path_to_save, project_name, github_link):
    current_path = os.getcwd()
    full_path = str(path_to_save + "\\"+ project_name)
    try:
        if os.path.exists(full_path):
            os.remove((full_path))
        os.chdir(str(path_to_save))
        check_output("git clone " + github_link, shell=True).decode()

        check_output("python -m pip install --upgrade pip", shell=True).decode()

        os.chdir(full_path)

        if project_name == 'openfisca-italy':
            check_output("git checkout Initizialize_open-fisca-italy", shell=True).decode()
        full_path = "\""+full_path+"\""
        check_output("pip install --editable " + full_path, shell=True).decode()
        os.chdir(current_path)
        return True
    except Exception as e:
        print e
        os.chdir(current_path)
        return False
