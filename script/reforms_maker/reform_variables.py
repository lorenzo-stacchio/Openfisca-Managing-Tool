import os
import sys
import inspect
import datetime
import time
import importlib
import json
import site
import re
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

    type_of_entity = None
    tax_benefit_system_module_class = None

    def __init__(self, name = None, entity = None, type = None, reference = None,  formula = None, label = None, set_input = None, definition_period = None):
        self.__name__ = name
        self.entity = entity
        self.__type__ = type
        self.__reference__ = reference
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
        entity_names = []
        self.entity = None
        for entity_name in Variable_To_Reform.type_of_entity:
            entity_names.append(entity)
        for entity_name in entity_names:
            if entity == entity_name:
                self.entity = entity
        if self.entity is None:
            raise ValueError("The entity choosen doesn't exist in openfisca")

    def set_reference(self, reference):
        self.__reference__ = reference

    def set_formula(self, formula):
        f = re.compile("def formula\(([a-zA-Z\, ]*)\)\:")
        if f.match(formula):
            self.__formula__ = formula
        else:
            raise ValueError("The text you insert is not a valid formula")

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


    @staticmethod
    def import_depending_on_system(tax_benefit_system_module_class, system_entity_module, system_all_entities_name):
        Variable_To_Reform.tax_benefit_system_module_class = tax_benefit_system_module_class()
        Variable_To_Reform.type_of_entity = getattr(system_entity_module,system_all_entities_name)


    def __repr__(self):
        return "\n\nName: " + self.__name__ + "\nType: " + self.__type__ + "\nEntity: " + self.entity + "\nDefinition period: " + self.__definition_period__ + "\nLabel: " + self.__label__ +  "\nSet_input: " + self.__set_input__ +  "\nReference: " + self.__reference__

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
        if self.__variable_to_add__ == None:
            raise ValueError("You have to choose a variable to do a reform")
        accept_value = []
        for type_accepted in TYPEOFREFORMVARIABILE:
            accept_value.append(type_accepted)
        if command in accept_value:
            # switch the command
            if command == TYPEOFREFORMVARIABILE.add_variable:
                self.__add_variable__()
            elif command == TYPEOFREFORMVARIABILE.update_variable:
                self.__update_variable__()
            elif command == TYPEOFREFORMVARIABILE.neutralize_variable:
                self.__neutralize_variable__()
        else:
            raise ValueError("The reform command is not acceptable")


    def __add_variable__(self):
        if self.__reform_name__ is None:
            self.__reform_name__ = "no_named_reform"
        # check the necessary fields, which are name, type, definition_period and entity
        if (self.__variable_to_add__.__name__ is None) or (self.__variable_to_add__.entity is None) or (self.__variable_to_add__.__definition_period__ is None) or (self.__variable_to_add__.entity is None):
            raise ValueError("You doesn't insert a necessary field")
        path_new_reform = self.__path_to_save_reform__ + "\\" + self.__reform_name__ + ".py"
        if os.path.exists(path_new_reform):
            os.remove(path_new_reform)
        with open(path_new_reform, 'a') as new_reform:
            new_reform.write("# -*- coding: utf-8 -*-") # to avoid erros
            new_reform.write("\nfrom openfisca_core.model_api import *")
            new_reform.write("\nfrom openfisca_core.model_api import *\n")
            # required fields
            new_reform.write("\nclass " + self.__variable_to_add__.__name__ + "(Variable):")
            new_reform.write("\n\tvalue_type = " + self.__variable_to_add__.__type__)
            new_reform.write("\n\tentity = " + self.__variable_to_add__.entity)
            new_reform.write("\n\tdefinition_period = " + self.__variable_to_add__.__definition_period__)
            # facultative fields
            if self.__variable_to_add__.__reference__:
                new_reform.write("\n\treference = " + self.__variable_to_add__.__reference__)

            if self.__variable_to_add__.__label__:
                new_reform.write("\n\tlabel = " + self.__variable_to_add__.__label__)

            if self.__variable_to_add__.__set_input__:
                new_reform.write("\n\tset_input = " + self.__variable_to_add__.__set_input__)

            if self.__variable_to_add__.__formula__:
                new_reform.write("\n\n\t" + self.__variable_to_add__.__formula__)
            # write reform
            new_reform.write("\n\n\nclass " + self.__reform_name__ + "(Reform):")
            new_reform.write("\n\tdef apply(self):\n\t\tself.add_variable(\'" + self.__variable_to_add__.__name__ + "\')")


    def __update_variable__(self):
        if self.__reform_name__ is None:
            self.__reform_name__ = "no_named_reform"

        if (self.__variable_to_add__.__name__ is None) or ((self.__variable_to_add__.__type__ is None) and (self.__variable_to_add__.entity is None) and (self.__variable_to_add__.__definition_period__ is None) and (self.__variable_to_add__.__set_input__ is None) and (self.__variable_to_add__.__label__ is None) and (self.__variable_to_add__.__reference__ is None) and (self.__variable_to_add__.__formula__ is None)):
            raise ValueError("You doesn't insert a necessary field")
        #check if variable exist
        all_variables = Variable_To_Reform.tax_benefit_system_module_class.get_variables()
        variable_exist = False

        for key,var in all_variables.iteritems():
            if self.__variable_to_add__.__name__ == key:
                variable_exist = True

        if variable_exist == False:
            raise ValueError("The variable you want update doesn't exist")

        path_new_reform = self.__path_to_save_reform__ + "\\" + self.__reform_name__ + ".py"

        if os.path.exists(path_new_reform):
            os.remove(path_new_reform)
        with open(path_new_reform, 'a') as new_reform:
            new_reform.write("# -*- coding: utf-8 -*-") # to avoid erros
            new_reform.write("\nfrom openfisca_core.model_api import *")
            new_reform.write("\nfrom openfisca_core.model_api import *\n")
            # facultative fields
            new_reform.write("\nclass " + self.__variable_to_add__.__name__ + "(Variable):")

            if self.__variable_to_add__.__type__:
                new_reform.write("\n\tvalue_type = " + self.__variable_to_add__.__type__)

            if self.__variable_to_add__.entity:
                new_reform.write("\n\tentity = " + self.__variable_to_add__.entity)

            if self.__variable_to_add__.__definition_period__:
                new_reform.write("\n\tdefinition_period = " + self.__variable_to_add__.__definition_period__)

            if self.__variable_to_add__.__reference__:
                new_reform.write("\n\treference = " + self.__variable_to_add__.__reference__)

            if self.__variable_to_add__.__label__:
                new_reform.write("\n\tlabel = " + self.__variable_to_add__.__label__)

            if self.__variable_to_add__.__set_input__:
                new_reform.write("\n\tset_input = " + self.__variable_to_add__.__set_input__)

            if self.__variable_to_add__.__formula__:
                new_reform.write("\n\n\t" + self.__variable_to_add__.__formula__)
            # write reform
            new_reform.write("\n\n\nclass " + self.__reform_name__ + "(Reform):")
            new_reform.write("\n\tdef apply(self):\n\t\tself.update_variable(\'" + self.__variable_to_add__.__name__ + "\')")


    def __neutralize_variable__(self):
        if self.__reform_name__ is None:
            self.__reform_name__ = "no_named_reform"

        if (self.__variable_to_add__.__name__ is None):
            raise ValueError("You doesn't insert a necessary field")

        #check if variable exist
        all_variables = Variable_To_Reform.tax_benefit_system_module_class.get_variables()
        variable_exist = False

        variable_exist = False

        for key,var in all_variables.iteritems():
            if self.__variable_to_add__.__name__ == key:
                variable_exist = True

        if variable_exist == False:
            raise ValueError("The variable you want neutralize doesn't exist")

        path_new_reform = self.__path_to_save_reform__ + "\\" + self.__reform_name__ + ".py"

        if os.path.exists(path_new_reform):
            os.remove(path_new_reform)
        with open(path_new_reform, 'a') as new_reform:
            new_reform.write("# -*- coding: utf-8 -*-") # to avoid erros
            new_reform.write("\nfrom openfisca_core.model_api import *")
            new_reform.write("\nfrom openfisca_core.model_api import *\n")
            # write reform
            new_reform.write("\n\n\nclass " + self.__reform_name__ + "(Reform):")
            new_reform.write("\n\tdef apply(self):\n\t\tself.neutralize_variable(\'" + self.__variable_to_add__.__name__ + "\')")


#with open('config_import.json') as f:
#    data_config = json.load(f)
#Variable_To_Reform.import_depending_on_system("openfisca_italy", data_config)
#v = Variable_To_Reform()
#v.set_name("RP62_periodo_2013")
#v.set_type("float")
#v.set_entity("person")
#v.set_definition_period("month")
#v.set_set_input("set_input_divide_by_period")
#v.set_formula("def formula(person, period, parameters):\n\t\treturn person('reddito_lavoro_dipendente_annuale', period) * parameters(period).tasse.aliquota_IRPEF")
#manager = Variable_reform_manager(path_to_save_reform = 'C:\\Users\\Lorenzo Stacchio\\Desktop', variable_to_add = v )
#manager.do_reform(TYPEOFREFORMVARIABILE.neutralize_variable)
