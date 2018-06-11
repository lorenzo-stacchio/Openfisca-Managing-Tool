# -*- coding: utf-8 -*-
import os
from enum import Enum
from dateutil.parser import parse as date_parser
import datetime
import collections
import re
import time

GRANDEZZA_STRINGHE_INTESTAZIONE = 1000

PATH_RST_DOCUMENT = os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), os.pardir)) + "\\messages\\rst_da_visualizzare.rst"

class TypeReformAction(Enum):
    add_variable = "Aggiunta variabile"
    modify_variable = "Modificata variabile esistente"
    add_parameter = "Aggiunto Parametro"
    modify_parameter = "Modificato parametro esistente"


class Reform_for_writing():
    __reform_name__ = None
    __reform_full_name__ = None
    __reference__ = None
    __reform_actions__ = [] # lista di n dict, ogni dict ha tipo azione e contenuto
    # dovrebbe essere un dict di azione e su cosa fa l'azione che però è al chiave della spiegazione
    modifier_function_dict = {}
    reformed_variables_dict = {}

    def __init__(self, reform_name = None, reform_full_name = None, reference = None, reform_actions = []):
        if os.path.exists(PATH_RST_DOCUMENT):
            os.remove(PATH_RST_DOCUMENT)
        self.__reform_name__ = reform_name
        self.__reference__ = reference
        self.__reform_actions__ = reform_actions
        self.__reform_full_name__ = reform_full_name

    def __repr__(self):
        return "\n" + str(self.__reform_name__) + "," + str(self.__reform_full_name__) + "," + str(self.__reference__) + "," +  str(self.__reform_actions__)

    def set_reform_name(self, reform_name):
        self.__reform_name__ = reform_name

    def set_reform_full_name(self, reform_full_name):
        self.__reform_full_name__ = reform_full_name

    def set_reference(self, reference):
        self.__reference__ = reference

    def set_reform_actions(self, reform_actions):
        self.__reform_actions__ = reform_actions

    def append_reform_action(self, reform_action):
        self.__reform_actions__.append(reform_action)

    def generate_RST_reform(self):
        with open(PATH_RST_DOCUMENT,'a') as rst:
            #reform name
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\nReform: " + self.__reform_name__ + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\n\n")
            # Full name
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\nFull name Reform\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\n\n" + self.__reform_full_name__.strip() + "\n\n")
            # Properties
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\nProperties: \n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\nReference \n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            # reference
            if self.__reference__:
                rst.write("\n" + self.__reference__ + "\n")
            else:
                rst.write("\nReference non specificata\n")
            rst.write("\nReform Actions \n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('*')
            # type of actions in reform
            count_actions = 0
            for action in self.__reform_actions__:
                rst.write("\n- Azione " + str(count_actions) +" : " + action + "\n")
                count_actions = count_actions + 1
            rst.write("\n\n")
        return PATH_RST_DOCUMENT


class Reform_File_Interpeter():
    __reforms_file_path__ = ""
    __reforms__ = [] # will be a list
    __file_is_a_reform__ = False

    def __init__(self,reform_path):
        self.__reforms_file_path__ = reform_path
        # check if the file passed contains a variable
        with open(self.__reforms_file_path__,'r') as content_reform:
            for line in content_reform.readlines():
                if 'class' in line and '(Reform):' in line:
                    self.__file_is_a_reform__ = True

    def start_interpetration(self):
        self.__reforms__ = []
        reform_apply_fun_found = False
        current_reform_index = -1
        current_reform = None
        with open(self.__reforms_file_path__,'r') as content_variable:
            for line in content_variable.readlines():
                line =  line.strip()
                if not line.startswith('#'):
                    #print "Linea attuale", line
                    if reform_apply_fun_found:
                        if 'class' in line and '(Reform):' in line:
                            reform_apply_fun_found = False
                        else:
                            if 'modify_parameters' in line:
                                current_reform.append_reform_action("Modifica o aggiunge dei parametri tramite la funzione")
                            elif 'update_variable' in line:
                                current_reform.append_reform_action("Aggiorna una variabile esistente")
                            elif 'add_variable' in line:
                                current_reform.append_reform_action("Aggiunge una nuova variabile")
                    pieces = line.split('=')
                    if 'class' in pieces[0] and '(Reform):' in pieces[0]:
                        reform_apply_fun_found = False
                        current_reform_index = current_reform_index + 1
                        reform_name = pieces[0]
                        for chs in ['class','(Reform):']:
                            reform_name = reform_name.replace(chs,'')
                        current_reform = Reform_for_writing(reform_name = reform_name)
                        current_reform.set_reform_actions(reform_actions=[])
                        #print "Dopo creazione", current_reform
                        self.__reforms__.append(current_reform)
                    if 'name' in pieces[0]:
                        full_name = pieces[1]
                        for chs in ['u"','\"']:
                            full_name = full_name.replace(chs,'')
                        current_reform.set_reform_full_name(full_name)
                    if 'def apply(self):' in pieces[0]:
                        reform_apply_fun_found = True
        print self.__reforms__

    def generate_RST_reforms(self):
        for reform in self.__reforms__:
            path = reform.generate_RST_reform()
        return path

    def file_is_a_reform(self):
        return self.__file_is_a_reform__

object = Reform_File_Interpeter('C:\\Users\\Stach\\Desktop\\openfisca-italy\\openfisca_italy\\reforms\\IRPEF\\Quadro_Determinazione_Imposta\\Quadro_RN\\RN5\\aliquota_irpef_minore_redditi_minori_15000.py')
#object = Reform_File_Interpeter('C:\\Users\\Stach\\Desktop\\aldo.txt')
object.file_is_a_reform()
object.start_interpetration()
object.generate_RST_reforms()
#object.start_interpetration()
