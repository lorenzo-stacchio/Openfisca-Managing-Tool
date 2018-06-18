import os
import sys
import inspect
import datetime
import time
import importlib
from enum import Enum

# show the names in GUI
class TYPEOFVARIABLE(Enum):
    float = "Float type"
    bool = "Bool type"
    date = "Date type"
    Enum = "Enum type" # choose or write an enum
    int = "Integer type"
    str = "String type"


class TYPEOFSETINPUT(Enum):
    set_input_divide_by_period = "The 12 months are set equal to the 12th of the input value"
    set_input_dispatch_by_period = "The 12 months are set equal to input value"


class TYPEOFDEFINITIONPERIOD(Enum):
    month = "Monthly variable"
    year = "Year variable"
    eternity = "Eternal variable"

class Variable_To_Reform():

    def __init__(self, name = None, entity = None, type = None, reference = None, openfisca_tax_benefit_system_path = None,  formula = None, label = None, set_input = None, definition_period = None):
        self.__name__ = name
        self.__entity__ = entity
        self.__type__ = type
        self.__reference__ = reference
        self.__openfisca_tax_benefit_system_path__ = openfisca_tax_benefit_system_path
        self.__label__ = label
        self.__definition_period__ = definition_period
        self.__set_input__ = set_input
        self.__formula__ = formula

    def set_name(self, name):
        self.__name__ = name

    def set_type(self, type):
        accept_value = []
        for type_accepted in TYPEOFVARIABLE:
            accept_value.append(type_accepted.name)
        if type in accept_value:
            self.__type__ = type
        else:
            raise ValueError("The type choosen for the variable is not an openfisca type")

    def set_entity(self, entity):
        sys.path.append(self.__openfisca_tax_benefit_system_path__)
        entita = importlib.import_module('entita')
        self.entities = []
        for entity_real in entita.entities:
            self.entities.append(entity_real.__name__)
        if entity in self.entities:
            self.__entity__ = entity
        else:
            raise ValueError("The entity choosen doesn't exist in openfisca")
        self.__entity__ = entity

    def set_reference(self, reference):
        self.__reference__ = reference

    def set_formula(self, formula):
        self.__formula__ = formula

    def set_openfisca_tax_benefit_system_path(self, openfisca_tax_benefit_system_path):
        self.__openfisca_tax_benefit_system_path__ = openfisca_tax_benefit_system_path

    def set_label(self, label):
        self.__label__ = label

    def set_definition_period(self, definition_period):
        accept_value = []
        for type_accepted in TYPEOFDEFINITIONPERIOD:
            accept_value.append(type_accepted.name)
        if definition_period in accept_value:
            self.__definition_period__ = definition_period
        else:
            raise ValueError("The definition_period choosen for the variable is not an openfisca definition_period")

    def set_set_input(self, set_input):
        accept_value = []
        for type_accepted in TYPEOFSETINPUT:
            accept_value.append(type_accepted.name)
        if set_input in accept_value:
            self.__set_input__ = set_input
        else:
            raise ValueError("The set_input choosen for the variable is not an openfisca set_input")

    def __repr__(self):
        return "\n\nName: " + self.__name__ + "\nType: " + self.__type__ + "\nEntity: " + self.__entity__ + "\nDefinition period: " + self.__definition_period__ + "\nLabel: " + self.__label__ +  "\nSet_input: " + self.__set_input__ +  "\nReference: " + self.__reference__

class TYPEOFREFORMVARIABILE(Enum):
    update_variable = "Update an existing variable"
    add_variable = "Add a new variable"
    neutralize_variable = " Neutralize an existent variable"

class Variable_reform_manager():

    def __init__(self, variable_to_add = None, reform_name = None, path_to_save_reform = None):
        self.__variable_to_add__ = variable_to_add
        self.__reform_name__ = reform_name
        self.__path_to_save_reform__ = path_to_save_reform


    def set_variable_to_add(self, variable_to_add):
        if isinstance(variable_to_add, Variable_To_Reform):
            self.__variable_to_add__ = variable_to_add
        else:
            raise TypeError("The passed value is not a correct Variable")

    def do_reform(self, command):
        accept_value = []
        for type_accepted in TYPEOFREFORMVARIABILE:
            accept_value.append(type_accepted.name)
        if command in accept_value:
            # switch the command
            if command == TYPEOFREFORMVARIABILE.add_variable.name:
                self.__add_variable__()
            elif command == TYPEOFREFORMVARIABILE.update_variable.name:
                self.__update_variable__()
            elif command == TYPEOFREFORMVARIABILE.neutralize_variable.name:
                self.__neutralize_variable__()
        else:
            raise ValueError("The reform command is not acceptable")


    def __add_variable__(self):
        if self.__reform_name__ is None:
            self.__reform_name__ = "no_named_reform"
        # check the necessary fields, which are name, type, definition_period and entity
        if (self.__variable_to_add__.__name__ is None) or (self.__variable_to_add__.__entity__ is None) or (self.__variable_to_add__.__definition_period__ is None) or (self.__variable_to_add__.__entity__ is None):
            raise ValueError("You doesn't insert a necessary field")
        path_new_reform = self.__path_to_save_reform__ + "\\" + self.__reform_name__ + ".py"
        if os.path.exists(path_new_reform):
            os.remove(path_new_reform)
        with open(path_new_reform, 'a') as new_reform:
            new_reform.write("# -*- coding: utf-8 -*-") # to avoid erros
            new_reform.write("\nfrom openfisca_core.model_api import *\n\n")
            new_reform.write("\nfrom openfisca_core.model_api import *\n\n")

    def __update_variable__(self):
        print "SONO IN UP"


    def __neutralize_variable__(self):
        print "SONO IN NEUT"

v = Variable_To_Reform(openfisca_tax_benefit_system_path = 'C:\\Users\\Stach\\Desktop\\openfisca-italy\\openfisca_italy')
v.set_name("Prova")
v.set_type("float")
v.set_entity("Person")
v.set_definition_period("month")
v.set_set_input("set_input_divide_by_period")
manager = Variable_reform_manager(path_to_save_reform = 'C:\\Users\\Stach\\Desktop', variable_to_add = v )
manager.do_reform("add_variable")
