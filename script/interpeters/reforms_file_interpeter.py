# -*- coding: utf-8 -*-
import os
from enum import Enum
from dateutil.parser import parse as date_parser
import datetime
import collections
import re
import time
from variables_file_interpeter import *


GRANDEZZA_STRINGHE_INTESTAZIONE = 1000

#PATH_RST_DOCUMENT = os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), os.pardir)) + "\\messages\\rst_da_visualizzare.rst"
PATH_RST_DOCUMENT = os.getcwd() + "\\messages\\rst_da_visualizzare.rst"

class TypeReformAction(Enum):
    add_variable = "Aggiunta variabile"
    modify_variable = "Modificata variabile esistente"
    add_parameter = "Aggiunto Parametro"
    modify_parameter = "Modificato parametro esistente"


class Reform_for_writing():
    #each reform coul contain variables and modifier functions
    __reform_name__ = None
    __reform_full_name__ = None
    __reference__ = None
    __reform_actions__ = []
    __variables_used__ = {}  # dict key = name, value = RST string
    #__modifier_functions__ = []

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

    def get_reform_actions(self):
        return self.__reform_actions__

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
            rst.write("\nFull name or description\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            if self.__reform_full_name__:
                rst.write("\n\n" + self.__reform_full_name__.strip() + "\n\n")
            else:
                rst.write("\n\nUndefined full name\n\n")
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
            for action in self.__reform_actions__: # action is ever a dict of one
                for k,v in action.iteritems():
                    rst.write("\n- Azione " + str(count_actions) +" : " + v + "\n")
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


    def __find_and_bind_variables__(self):
        var_interpeter = Variable_File_Interpeter(self.__reforms_file_path__)
        var_interpeter.start_interpetration()
        variables = var_interpeter.get_variables()
        #print "Quante variabili?", len(variables)
        for reform in self.__reforms__:
            for action in reform.get_reform_actions():
                for key,value in action.iteritems():
                    # get the actions
                    for var in variables:
                        if key==var.get_variable_name():
                            action[key] = action[key] + var.generate_RST_string_variable()


    def __find_and_bind_modifier_func__(self):
        modifier_function_found = False
        modifier_function_dict = {}
        with open(self.__reforms_file_path__,'r') as content_variable:
            for line in content_variable.readlines():
                line =  line.strip()
                if '#' in line:
                    line = line[:line.find('#')]
                if line:
                    if ('(Reform):' in line) or ('(Variable):' in line) or ('class'in line) or ('def'in line):
                        modifier_function_found = False
                    if modifier_function_found == True:
                        modifier_function_dict[name] = modifier_function_dict[name] + "\n  " + line
                    if ('def' in line) and ('parameters' in line) and ('(' in line) and (')' in line) and (':' in line) and not('formula' in line): # is almost a modifier function
                        modifier_function_found = True
                        name = (line[:line.find('(')].replace("def","")).strip()
                        #print "Name of modifier function:", name
                        modifier_function_dict[name] = "\n .. code:: python \n\n  " + line
            #print "Dict", modifier_function_dict

        for reform in self.__reforms__:
            for action in reform.get_reform_actions():
                for key,value in action.iteritems():
                    #print "key", key
                    #print "value", value
                    # get the actions
                    for name,value_name in modifier_function_dict.iteritems():
                        print "name", name
                        if key==name:
                            action[key] = action[key] + value_name
        #for reform in self.__reforms__:
            #print "Riforme", reform.get_reform_actions()

    def start_interpetration_reforms(self):
        self.__reforms__ = []
        reform_apply_fun_found = False
        current_reform_index = -1
        current_reform = None
        reform_found = False
        # Find Reform
        with open(self.__reforms_file_path__,'r') as content_variable:
            for line in content_variable.readlines():
                line =  line.strip()
                if '#' in line:
                    line = line[:line.find('#')]
                if line:
                    #print "Linea attuale", line
                    if reform_apply_fun_found:
                        if 'class' in line and '(Reform):' in line:
                            reform_apply_fun_found = False
                        else:
                            dict_action = {}
                            if 'modify_parameters' in line:
                                # example of code line self.modify_parameters(modifier_function = modifica_scaglioni_IRPEF), i suppose that all lines will be like this
                                line = line.split('=')[1]
                                line = (line[:line.find(')')].strip()).replace("self.","")
                                dict_action[line] = "Modifica o aggiunge dei parametri tramite la seguente funzione: \n\n"
                                current_reform.append_reform_action(dict_action)
                            elif 'update_variable' in line:
                                # example of code line self.update_variable(income_tax)
                                line = (line [(line.find('(') + 1):line.find(')')].strip()).replace("self.","") # start is inclusive, instead end is exclusive
                                dict_action[line] = "Aggiorna la variabile esistente " + line + " rendendola:\n\n"
                                current_reform.append_reform_action(dict_action)
                            elif 'add_variable' in line:
                                # example of code line self.add_variable(income_tax)
                                line = (line[(line.find('(') + 1):line.find(')')].strip()).replace("self.","")
                                dict_action[line] = "Aggiunge al sistema la seguente variabile: \n\n"
                                current_reform.append_reform_action(dict_action)
                    pieces = line.split('=')
                    if 'class' in pieces[0] and '(Reform):' in pieces[0]:
                        reform_found = True
                        reform_apply_fun_found = False
                        current_reform_index = current_reform_index + 1
                        reform_name = pieces[0]
                        for chs in ['class','(Reform):']:
                            reform_name = reform_name.replace(chs,'')
                        current_reform = Reform_for_writing(reform_name = reform_name)
                        current_reform.set_reform_actions(reform_actions=[])
                        #print "Dopo creazione", current_reform
                        self.__reforms__.append(current_reform)
                    elif 'name ' in pieces[0] and reform_found == True:
                        full_name = pieces[1]
                        for chs in ['u"','\"']:
                            full_name = full_name.replace(chs,'')
                        current_reform.set_reform_full_name(full_name)
                    elif 'def apply(self):' in pieces[0]:
                        reform_found = False # set to false because the function is the last part
                        reform_apply_fun_found = True
        #print "\nSTAMPO LE RIFORME",self.__reforms__
        #print self.__reforms__
        self.__find_and_bind_variables__()
        self.__find_and_bind_modifier_func__()


    def generate_RST_reforms(self):
        for reform in self.__reforms__:
            path = reform.generate_RST_reform()
        return path

    def file_is_a_reform(self):
        return self.__file_is_a_reform__

#object = Reform_File_Interpeter('C:\\Users\\Stach\\Desktop\\openfisca-italy\\openfisca_italy\\reforms\\IRPEF\\Quadro_Determinazione_Imposta\\Quadro_RN\\RN5\\aliquota_irpef_minore_redditi_minori_15000.py')
#object = Reform_File_Interpeter('C:\\Users\\Stach\\Desktop\\rodino.txt')
#object = Reform_File_Interpeter('C:\\Users\\Stach\\Desktop\\openfisca-italy\\openfisca_italy\\reforms\\IRPEF\\Quadro_Determinazione_Imposta\\Quadro_RN\\RN6\\riforma_detrazioni_per_figli_a_carico.py')
#object.file_is_a_reform()
#object.start_interpetration_reforms()
#object.generate_RST_reforms()
#object.start_interpetration()
