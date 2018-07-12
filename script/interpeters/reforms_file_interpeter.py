# -*- coding: utf-8 -*-
import os
from enum import Enum
from dateutil.parser import parse as date_parser
import datetime
import collections
import re
import time
import importlib
import sys
import site
reload(sys)
sys.setdefaultencoding('utf8')
from variables_file_interpeter import *

GRANDEZZA_STRINGHE_INTESTAZIONE = 1000

PATH_RST_DOCUMENT = os.getcwd() + "/messages/rst_da_visualizzare.rst"

class TypeReformAction(Enum):
    add_variable = "Aggiunta variabile"
    modify_variable = "Modificata variabile esistente"
    add_parameter = "Aggiunto Parametro"
    modify_parameter = "Modificato parametro esistente"


class Reform_for_writing():

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
            # reform actions
            rst.write("\nReform Actions \n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('*')
            # type of actions in reform
            count_actions = 0
            for action in self.__reform_actions__: # action is ever a dict of one
                for k,v in action.iteritems():
                    rst.write("\n\n- **Action " + str(count_actions + 1) +"** : " + v + "\n")
                    count_actions = count_actions + 1
            rst.write("\n\n")
        return PATH_RST_DOCUMENT


class Reform_File_Interpeter():
    __reforms__ = [] # will be a list
    tax_benefit_system_module_class = None

    def __init__(self,reform_path):
        self.__reforms_file_path__ = reform_path
        self.__file_is_a_reform__ = False
        if Reform_File_Interpeter.tax_benefit_system_module_class  is None:
            raise ValueError("You must import the system to create a reform interpeter")
        # check if the file passed contains a variable
        with open(self.__reforms_file_path__,'r') as content_reform:
            for line in content_reform.readlines():
                if 'class' in line and '(Reform):' in line:
                    self.__file_is_a_reform__ = True

    @staticmethod
    def import_depending_on_system(tax_benefit_system_module_class):
        Reform_File_Interpeter.tax_benefit_system_module_class = tax_benefit_system_module_class()


    def __find_and_bind_variables__(self):
        for reform in self.__reforms__:
            for action in reform.get_reform_actions():
                for key,value in action.iteritems():
                    if not (value == 'modify_parameters'):
                        if value == 'neutralize_variable':
                            for k_var, val_var in Reform_File_Interpeter.tax_benefit_system_module_class.get_variables().iteritems():
                                if key==k_var:
                                    variable = Variable_for_writing()
                                    variable.set_variable_name(key)
                                    variable.set_value_type(val_var.value_type.__name__)
                                    variable.set_entity(val_var.entity.__name__)
                                    if val_var.label:
                                        variable.set_label(val_var.label.encode("utf-8"))
                                    variable.set_definition_period(val_var.definition_period)
                                    if val_var.reference:
                                        variable.set_reference(val_var.reference[0])
                                    if val_var.set_input :
                                        variable.set_set_input(val_var.set_input.__name__)
                                    if not (val_var.is_input_variable()):
                                        lines = inspect.getsource(val_var.get_formula())  # get formula if the variable if exist
                                        variable.set_formula(lines)
                                    action[key] = action[key] + "\n\n" + variable.generate_RST_string_variable()
                        elif value == 'add_variable':
                            var_interpeter = Variable_File_Interpeter(self.__reforms_file_path__)
                            var_interpeter.__interpretation_variable_for_reform__()
                            variables_in_reform = var_interpeter.get_variables()
                            for variable in variables_in_reform:
                                if key == str(variable.get_variable_name()):
                                    action[key] = action[key] + "\n\n" + variable.generate_RST_string_variable()
                        elif value == 'update_variable':
                            var_interpeter = Variable_File_Interpeter(self.__reforms_file_path__)
                            var_interpeter.__interpretation_variable_for_reform__()
                            variables_in_reform = var_interpeter.get_variables()
                            var_interpeter.start_interpetration() #get the existing variable
                            variables_updated_if_exist = var_interpeter.get_variables()
                            for variable_in_reform,variable_in_system in zip(variables_in_reform,variables_updated_if_exist):
                                if key == variable_in_reform.get_variable_name():
                                    variable_X = Variable_for_writing(variable_name = key)
                                    if not (variable_in_reform.get_value_type() == None):
                                        variable_X.set_value_type(variable_in_reform.get_value_type())
                                    else:
                                        variable_X.set_value_type(variable_in_system.get_value_type())
                                    if not (variable_in_reform.get_entity() == None):
                                        variable_X.set_entity(variable_in_reform.get_entity())
                                    else:
                                        variable_X.set_entity(variable_in_system.get_entity())

                                    if not (variable_in_reform.get_definition_period() == None):
                                        variable_X.set_definition_period(variable_in_reform.get_definition_period())
                                    else:
                                        variable_X.set_definition_period(variable_in_system.get_definition_period())

                                    if not (variable_in_reform.get_label() == None):
                                        variable_X.set_label(variable_in_reform.get_label())
                                    else:
                                        variable_X.set_label(variable_in_system.get_label())

                                    if not (variable_in_reform.get_formula() == None):
                                        variable_X.set_formula(variable_in_reform.get_formula())
                                    else:
                                        variable_X.set_formula(variable_in_system.get_formula())

                                    if not (variable_in_reform.get_reference() == None):
                                        variable_X.set_reference(variable_in_reform.get_reference())
                                    else:
                                        variable_X.set_reference(variable_in_system.get_reference())

                                    if not (variable_in_reform.get_set_input() == None):
                                        variable_X.set_set_input(variable_in_reform.get_set_input())
                                    else:
                                        variable_X.set_set_input(variable_in_system.get_set_input())
                                    action[key] = action[key] + "\n\n" + variable_X.generate_RST_string_variable()


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
                        modifier_function_dict[name] = "\n\n .. code:: python \n\n  " + line

        for reform in self.__reforms__:
            for action in reform.get_reform_actions():
                for key,value in action.iteritems():
                    if(value == 'modify_parameters'):
                        for name,value_name in modifier_function_dict.iteritems():
                            if key==name:
                                action[key] = action[key] + value_name

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
                    if reform_apply_fun_found:
                        if 'class' in line and '(Reform):' in line:
                            reform_apply_fun_found = False
                        else:
                            dict_action = {}
                            if 'modify_parameters' in line:
                                # example of code line self.modify_parameters(modifier_function = modifica_scaglioni_IRPEF), i suppose that all lines will be like this
                                line = line.split('=')[1]
                                line = (line[:line.find(')')].strip()).replace("self.","")
                                dict_action[line] = "modify_parameters"
                                current_reform.append_reform_action(dict_action)
                            elif 'update_variable' in line:
                                # example of code line self.update_variable(income_tax)
                                line = (line [(line.find('(') + 1):line.find(')')].strip()).replace("self.","") # start is inclusive, instead end is exclusive
                                # erase '' from line
                                line = line.replace("\'", "")
                                dict_action[line] = "update_variable"
                                current_reform.append_reform_action(dict_action)
                            elif 'add_variable' in line:
                                # example of code line self.add_variable(income_tax)
                                line = (line[(line.find('(') + 1):line.find(')')].strip()).replace("self.","")
                                line = line.replace("\'", "")
                                dict_action[line] = "add_variable"
                                current_reform.append_reform_action(dict_action)
                            elif 'neutralize_variable' in line:
                                # example of code line self.add_variable(income_tax)
                                line = (line[(line.find('(\'') + 2):line.find('\')')].strip()).replace("self.","")
                                line = line.replace("\'", "")
                                dict_action[line] = "neutralize_variable"
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
                        self.__reforms__.append(current_reform)
                    elif 'name ' in pieces[0] and reform_found == True:
                        full_name = pieces[1]
                        for chs in ['u"','\"']:
                            full_name = full_name.replace(chs,'')
                        current_reform.set_reform_full_name(full_name)
                    elif 'def apply(self):' in pieces[0]:
                        reform_found = False # set to false because the function is the last part
                        reform_apply_fun_found = True
        self.__find_and_bind_variables__()
        self.__find_and_bind_modifier_func__()


    def generate_RST_reforms(self):
        for reform in self.__reforms__:
            path = reform.generate_RST_reform()
        return path

    def file_is_a_reform(self):
        return self.__file_is_a_reform__
