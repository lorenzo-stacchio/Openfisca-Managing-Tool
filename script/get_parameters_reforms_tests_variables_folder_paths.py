# -*- coding: utf-8 -*-
import os

def are_all_folders(dict_of_paths):
    for key in dict_of_paths:
        if not (os.path.isdir(dict_of_paths[key]) and os.path.exists(dict_of_paths[key])):
            return False
    return True


def get_all_paths(path_di_partenza):
    if os.path.isdir(path_di_partenza) and os.path.exists(path_di_partenza):
        print "You are in " + path_di_partenza
        #folder of the project
        project_folder = ""
        #I'm looking for the name
        for sub in os.listdir(path_di_partenza):
            # print sub
            if(sub.startswith("openfisca") and os.path.isdir(path_di_partenza + "\\" +sub)):
                project_folder = path_di_partenza + "\\" +sub
        if project_folder:
            # print "sono in project folder",project_folder
            dict_path = {}
            dict_path['initial_path'] = str(path_di_partenza)
            dict_path['inner_system_folder'] = str(project_folder)
            dict_path['reforms'] = str(project_folder + "/" + "reforms")
            dict_path['parameters'] =  str(project_folder + "/" + "parameters")
            dict_path['tests'] = str(project_folder + "/" + "tests")
            dict_path['variables'] = str(project_folder + "/" + "variables")

            if are_all_folders(dict_path):
                return dict_path
            else:
                return None
    elif not os.path.exists(path_di_partenza):
        print "Your path isn't correct"
    else: #!os.path.isdir(path_di_partenza)
        print "Your path isn't a directory"
