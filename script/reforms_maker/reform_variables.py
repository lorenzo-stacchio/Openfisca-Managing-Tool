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
    no_set_input_period = "There's no set_input_period"
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
        if   Variable_To_Reform.tax_benefit_system_module_class is None or   Variable_To_Reform.type_of_entity is None:
            raise ValueError("You must import the system to create a variable to reform")
        self.__name__ = name
        self.entity = entity
        self.__type__ = type
        self.__reference__ = "\"" + str(reference) + "\""
        self.__label__ = "\"" + str(label) + "\""
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
        if not(formula is None or formula==""):
            f = re.compile("def formula\(([a-zA-Z\, ]*)\)\:")
            if f.match(formula):
                self.__formula__ = formula
            else:
                raise ValueError("The text you insert is not a valid formula")
        else:
            self.__formula__ = formula

    def set_label(self, label):
        self.__label__ = label

    def set_definition_period(self, definition_period):
        accept_value = []
        for type_accepted in TYPEOFDEFINITIONPERIOD:
            accept_value.append(type_accepted.name)
        if definition_period in accept_value:
            if definition_period is TYPEOFSETINPUT.no_set_input_period:
                self.__definition_period__ = None
            else:
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

    def __init__(self, variable = None, reform_name = None, path_to_save_reform = None, reform_full_description = None):
        if isinstance(variable, Variable_To_Reform):
            self.__variable__ = variable
        else:
            raise TypeError("The passed value is not a correct Variable")
        if not (reform_name == None):
            self.__reform_name__ = reform_name.replace(" ", "_")
        else:
            self.__reform_name__ = reform_name

        self.__path_to_save_reform__ = path_to_save_reform
        self.__reform_full_description__ = "\"" + str(reform_full_description) + "\""

    def set_description(self,reform_full_description):
        self.__reform_full_description__ = "\"" + reform_full_description + "\""

    def set_variable(self, variable):
        if isinstance(variable, Variable_To_Reform):
            self.__variable__ = variable
        else:
            raise TypeError("The passed value is not a correct Variable")

    def do_reform(self, command):
        if self.__variable__ == None:
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
            self.__reform_name__ = "add_" + self.__variable__.__name__
        # check the necessary fields, which are name, type, definition_period and entity
        if (self.__variable__.__name__ is None) or (self.__variable__.entity is None) or (self.__variable__.__definition_period__ is None) or (self.__variable__.entity is None):
            raise ValueError("You doesn't insert a necessary field")

        all_variables = Variable_To_Reform.tax_benefit_system_module_class.get_variables()
        variable_exist = False

        for key,var in all_variables.iteritems():
            if self.__variable__.__name__ == key:
                variable_exist = True

        if variable_exist == True:
            raise ValueError("The variable you want update already exist please update it!")

        path_new_reform = self.__path_to_save_reform__ + "\\" + self.__reform_name__ + ".py"
        if os.path.exists(path_new_reform):
            os.remove(path_new_reform)
        with open(path_new_reform, 'a') as new_reform:
            new_reform.write("# -*- coding: utf-8 -*-") # to avoid erros
            new_reform.write("\nfrom openfisca_core.model_api import *")
            new_reform.write("\nfrom openfisca_core.model_api import *\n")
            # required fields
            new_reform.write("\nclass " + self.__variable__.__name__ + "(Variable):")
            new_reform.write("\n\tvalue_type = " + self.__variable__.__type__)
            new_reform.write("\n\tentity = " + self.__variable__.entity)
            new_reform.write("\n\tdefinition_period = " + self.__variable__.__definition_period__)
            # facultative fields
            if self.__variable__.__reference__:
                new_reform.write("\n\treference = " + self.__variable__.__reference__)

            if self.__variable__.__label__:
                new_reform.write("\n\tlabel = " + self.__variable__.__label__)

            if self.__variable__.__set_input__:
                new_reform.write("\n\tset_input = " + self.__variable__.__set_input__)

            if self.__variable__.__formula__:
                new_reform.write("\n\n\t" + self.__variable__.__formula__)
            # write reform
            new_reform.write("\n\n\nclass " + self.__reform_name__ + "(Reform):")
            if not(self.__reform_full_description__ is None):
                new_reform.write("\n\tname = " + self.__reform_full_description__)
            new_reform.write("\n\tdef apply(self):\n\t\tself.add_variable(\'" + self.__variable__.__name__ + "\')")


    def __update_variable__(self):
        if self.__reform_name__ is None:
            self.__reform_name__ = "update_" + self.__variable__.__name__

        #check if variable exist
        all_variables = Variable_To_Reform.tax_benefit_system_module_class.get_variables()
        variable_exist = False
        variable_to_update = None
        for key,var in all_variables.iteritems():
            if self.__variable__.__name__ == key:
                variable_exist = True
                variable_to_update = var
                break
        if variable_exist == False:
            raise ValueError("The variable you want update doesn't exist")

        path_new_reform = self.__path_to_save_reform__ + "\\" + str(self.__reform_name__) + ".py"
        if os.path.exists(path_new_reform):
            os.remove(path_new_reform)
        # check if at least one field is changed
        at_least_one_field_is_changed = False
        variable_elements_to_check =  [self.__variable__.__type__, self.__variable__.entity,
        self.__variable__.__definition_period__]
        system_variable_elements_to_check = [variable_to_update.value_type.__name__, variable_to_update.entity.__name__,
                                             variable_to_update.definition_period]
        if not(variable_to_update.reference == None):
            variable_elements_to_check.append(self.__variable__.__reference__)
            system_variable_elements_to_check.append(variable_to_update.reference[0])
        if not(variable_to_update.label == None):
            variable_elements_to_check.append(self.__variable__.__label__)
            system_variable_elements_to_check.append(variable_to_update.label)
        if not(variable_to_update.set_input == None):
            variable_elements_to_check.append(self.__variable__.__set_input__)
            system_variable_elements_to_check.append(str(variable_to_update.set_input.__name__ ))

        for var_to_check, sys_var in zip(variable_elements_to_check, system_variable_elements_to_check):
            if not(var_to_check == sys_var) and not(var_to_check==None):
                at_least_one_field_is_changed = True

        if self.__variable__.__formula__ and not variable_to_update.is_input_variable():
            # formula analysis
            if "\n" in inspect.getsource(variable_to_update.get_formula()): # if there is more than one line
                lines = inspect.getsource(variable_to_update.get_formula()).split("\n")
                formatted_lines = []
                for line in lines:
                    if line:
                        formatted_lines.append(line.strip())
            system_variable_formula = formatted_lines
            if "\n" in self.__variable__.__formula__:
                lines = self.__variable__.__formula__.split("\n")
                formatted_lines = []
                for line in lines:
                    if line:
                        formatted_lines.append(line.strip())
            current_formula = formatted_lines
            print system_variable_formula, len(system_variable_formula)
            print current_formula, len (current_formula)
            for sys_var_row, curr_var_row in zip(system_variable_formula,current_formula):
                if not(sys_var_row == curr_var_row):
                    at_least_one_field_is_changed = True

        elif self.__variable__.__formula__ and  variable_to_update.is_input_variable():
            at_least_one_field_is_changed = True

        if not at_least_one_field_is_changed:
            raise ValueError("You must change something to update the variable!!")

        # Start writing the formula
        with open(path_new_reform, 'a') as new_reform:
            new_reform.write("# -*- coding: utf-8 -*-") # to avoid erros
            new_reform.write("\nfrom openfisca_core.model_api import *")
            new_reform.write("\nfrom openfisca_core.model_api import *\n")
            # facultative fields
            new_reform.write("\nclass " + self.__variable__.__name__ + "(Variable):")
            # facultative fields
            variable_elements_to_write = [self.__variable__.__type__, self.__variable__.entity,
                                          self.__variable__.__definition_period__,self.__variable__.__reference__,
                                          self.__variable__.__label__,self.__variable__.__set_input__]
            system_variable_elements_to_compare = [variable_to_update.value_type.__name__,
                                                 variable_to_update.entity.__name__,
                                                 variable_to_update.definition_period]
            if not (variable_to_update.reference == None):
                system_variable_elements_to_check.append(variable_to_update.reference[0])
            else:
                system_variable_elements_to_check.append(None)
            if not (variable_to_update.label == None):
                system_variable_elements_to_check.append(variable_to_update.label)
            else:
                system_variable_elements_to_check.append(None)
            if not (variable_to_update.set_input == None):
                system_variable_elements_to_check.append(str(variable_to_update.set_input.__name__))
            else:
                system_variable_elements_to_check.append(None)

            string_to_write = ["\n\tvalue_type = ", "\n\tentity = ", "\n\tdefinition_period = ", "\n\treference = ", "\n\tlabel = "
                               , "\n\tset_input = "]

            for var_to_check, sys_var, curr_str in zip(variable_elements_to_write, system_variable_elements_to_compare, string_to_write):
               if var_to_check and not (var_to_check == sys_var):
                   new_reform.write(curr_str + var_to_check)

            # special case formula
            if (self.__variable__.__formula__ and variable_to_update.is_input_variable()) or (self.__variable__.__formula__ and not(self.__variable__.__formula__ == current_formula)):
                # formula analysis
                formula = self.__variable__.__formula__  # get formula if the variable if exist
                new_reform.write("\n")
                current_formula = ""
                if "\n" in formula: # if there is more than one line
                    lines = formula.split("\n")
                    formatted_lines = []
                    final_formatted_lines = []
                    for line in lines:
                        formatted_lines.append(line.strip())
                    final_formatted_lines.append(formatted_lines[0])
                    for line in formatted_lines[1:]: #except the first line
                        final_formatted_lines.append("\t" + line)
                    for line in final_formatted_lines:
                        new_reform.write("\n\t" + line)
            # write reform
            new_reform.write("\n\nclass " + self.__reform_name__ + "(Reform):")
            if not(self.__reform_full_description__ is None):
                new_reform.write("\n\tname = " + self.__reform_full_description__)
            new_reform.write("\n\tdef apply(self):\n\t\tself.update_variable(\'" + self.__variable__.__name__ + "\')")


    def __neutralize_variable__(self):
        if self.__reform_name__ is None:
            self.__reform_name__ = "neutralize_" + self.__variable__.__name__

        if (self.__variable__.__name__ is None):
            raise ValueError("You doesn't insert a necessary field")

        #check if variable exist
        all_variables = Variable_To_Reform.tax_benefit_system_module_class.get_variables()
        variable_exist = False

        variable_exist = False

        for key,var in all_variables.iteritems():
            if self.__variable__.__name__ == key:
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
            if not(self.__reform_full_description__ is None):
                new_reform.write("\n\tname = " + self.__reform_full_description__)
            new_reform.write("\n\tdef apply(self):\n\t\tself.neutralize_variable(\'" + self.__variable__.__name__ + "\')")
