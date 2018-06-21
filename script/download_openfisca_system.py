import os
import shutil
import time
import sys
from subprocess import check_output

# TODO: message if directory exist yet
def download_and_install(path_to_save, project_name, github_link):
    current_path = os.getcwd()
    try:
        if os.path.exists(path_to_save + "\\"+ project_name):
            os.remove((path_to_save + "\\"+ project_name))
        os.chdir(path_to_save)
        check_output("git clone " + github_link, shell=True).decode()

        check_output("python -m pip install --upgrade pip", shell=True).decode()

        os.chdir(path_to_save + "\\"+ project_name)

        if project_name == 'openfisca-italy':
            check_output("git checkout Initizialize_open-fisca-italy", shell=True).decode()
        check_output("pip install --editable " + path_to_save + "\\"+ project_name, shell=True).decode()
        os.chdir(current_path)
        return True
    except Exception:
        os.chdir(current_path)
        return False
