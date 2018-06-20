import os
import shutil
import time
import sys
from subprocess import check_output

# TODO: message if directory exist yet
def download_and_install(path_to_save, project_name, github_link):
    if os.path.exists(path_to_save + "\\"+ project_name):
        os.remove((path_to_save + "\\"+ project_name))
    os.chdir(path_to_save)
    check_output("git clone " + github_link, shell=True).decode()
    if project_name == 'openfisca-italy':
        os.chdir(path_to_save + "\\"+ project_name)
        check_output("git checkout Initizialize_open-fisca-italy", shell=True).decode()
