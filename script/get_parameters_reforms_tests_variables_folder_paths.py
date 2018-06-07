# -*- coding: utf-8 -*-
import os

def are_all_folders( dict_of_paths ):
    for key in dict_of_paths:
        if not (os.path.isdir(dict_of_paths[key]) and os.path.exists(dict_of_paths[key])):
            return False
    return True


def get_all_paths(path_di_partenza):
    reforms_path = ""
    parameters_path = ""
    tests_path = ""
    variables_path = ""
    if os.path.isdir(path_di_partenza) and os.path.exists(path_di_partenza):
        print "You are in " + path_di_partenza
        os.chdir(path_di_partenza)
        #folder of the project
        project_folder = ""
        #I'm looking for the name
        for sub in os.listdir(path_di_partenza):
            if(sub.startswith("openfisca") and os.path.isdir(sub)):
                project_folder = sub
        os.chdir(project_folder)
        project_absolute_path = path_di_partenza + "/" + project_folder
        print "You are in " + project_absolute_path

        dict_path = {}


        dict_path['initial_path'] = str(path_di_partenza)
        dict_path['reforms'] = str(project_absolute_path + "/" + "reforms")
        dict_path['parameters'] =  str(project_absolute_path + "/" + "parameters")
        dict_path['tests'] = str(project_absolute_path + "/" + "tests")
        dict_path['variables'] = str(project_absolute_path + "/" + "variables")

        if are_all_folders(dict_path):
            return dict_path
        else:
            return None
    elif not os.path.exists(path_di_partenza):
        print "Your path isn't correct"
    else: #!os.path.isdir(path_di_partenza)
        print "Your path isn't a directory"


#Execute
#dict_of_paths = get_all_paths("C:/Users/Corrado/Desktop/openfisca-italy/")

#Show all
#for key in dict_of_paths :
    #print "Chiave: "+key
    #print "Valore: "+dict_of_paths[key]
    #print ""
