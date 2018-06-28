# -*- coding: utf-8 -*-
import os
import json
from enum import Enum
from dateutil.parser import parse as date_parser
import datetime
import collections
import re
import time
import importlib
import inspect
import sys
import site
reload(sys)
sys.setdefaultencoding('utf8')

GRANDEZZA_STRINGHE_INTESTAZIONE = 1000
PATH_RST_DOCUMENT = os.getcwd() + "\\messages\\rst_da_visualizzare.rst"


class Variable_for_writing():
    __RST_string__ = None

    def __init__(self, variable_name = None, value_type = None, entity = None, definition_period = None, set_input = None, label = None, reference = None, formula = None, variables_involved_in_formula = None):
        if os.path.exists(PATH_RST_DOCUMENT):
            os.remove(PATH_RST_DOCUMENT)
        # a file contains many variable, so i can't erase it when i generate an RST so i'll do when i create a variable
        self.variable_name = variable_name
        self.value_type = value_type
        self.entity = entity
        self.definition_period = definition_period
        self.label = label
        self.formula = formula
        self.variables_involved_in_formula = variables_involved_in_formula
        self.reference = reference
        self.set_input = set_input

    def __repr__(self):
        return "\n" + str(self.variable_name) + "," + str(self.value_type) + "," +  str(self.entity) + "," +  str(self.definition_period) + "," +  str(self.label) + "," +  str(self.formula) + "," +  str(self.variables_involved_in_formula) + "," +  str(self.reference)

    def set_variable_name(self,variable_name):
        self.variable_name = variable_name

    def get_variable_name(self):
        return self.variable_name

    def set_entity(self,entity):
        self.entity = entity

    def get_entity(self):
        return self.entity

    def set_definition_period(self,definition_period):
        self.definition_period = definition_period

    def get_definition_period(self):
        return self.definition_period

    def set_label(self,label):
        self.label = label

    def get_label(self):
        return self.label

    def set_value_type(self,value_type):
        self.value_type = value_type

    def get_value_type(self):
        return self.value_type

    def set_formula(self,formula):
        self.formula = formula

    def get_formula(self):
        return self.formula

    def set_variables_involved_in_formula(self,variables_involved_in_formula):
        self.variables_involved_in_formula = variables_involved_in_formula

    def set_set_input(self,set_input):
        self.set_input = set_input

    def get_set_input(self):
        return self.set_input

    def set_reference(self,reference):
        self.reference = reference

    def get_reference(self):
        return self.reference

    def RST_string(self):
        return self.__RST_string__

    def generate_RST_string_variable(self): #used for reforms reading, so i'll put some more if necessary
        self.__RST_string__ = ""
        for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
            self.__RST_string__= self.__RST_string__ + '#'
        self.__RST_string__= self.__RST_string__ + "\n Variable: " + self.variable_name + "\n"
        for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
            self.__RST_string__= self.__RST_string__ + '#'
        self.__RST_string__= self.__RST_string__ + "\n\n"
        # Properties check
        for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
            self.__RST_string__= self.__RST_string__ + "#"
        self.__RST_string__= self.__RST_string__ + "\n Properties \n"
        for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
            self.__RST_string__= self.__RST_string__ + "#"
        self.__RST_string__= self.__RST_string__ + "\n"

        if self.value_type:
            self.__RST_string__= self.__RST_string__ + "\n" + "Il ``tipo`` di questa variabile è: **" + self.value_type + "**\n"
        else: self.__RST_string__= self.__RST_string__ + "\n" + "``Tipo`` non ridefinito\n"

        if self.entity:
            self.__RST_string__= self.__RST_string__ +"\n" + "L'``entità`` a cui questa variabile appartiene è: **" + self.entity + "**\n"
        else:
            self.__RST_string__= self.__RST_string__ +"\n" + "``Entità`` non ridefinita\n"

        if self.definition_period:
            self.__RST_string__= self.__RST_string__ + "\n" + "Il ``periodo`` di definizione di questa varabile è: **" + self.definition_period + "**\n"
        else:
            self.__RST_string__= self.__RST_string__ + "\n" + "``Periodo`` di definizione non ridefinito\n"

        if self.set_input:
            self.__RST_string__= self.__RST_string__ + "\n" + "Il ``set_input`` di questa variabile vale: **" + self.set_input + "**\n"
        else:
            self.__RST_string__= self.__RST_string__ + "\n" + "Nessun ``set_input`` inserito\n"

        if self.label:
            self.__RST_string__= self.__RST_string__ + "\n" + "La ``descrizione`` della varabile è: \n\n.. code-block:: rst\n\n " + self.label + "\n"
        else:
            self.__RST_string__= self.__RST_string__ + "\n" + "Nessuna ``descrizione`` inserita\n"

        if self.reference:
            self.__RST_string__= self.__RST_string__ + "\n" + "`Riferimento legislativo alla variabile <" + self.reference.strip() + ">`__" + "\n"
        else:
            self.__RST_string__= self.__RST_string__ + "\n" + "Nessun ``riferimento legislativo`` indicato\n"

        if self.formula:
            self.__RST_string__= self.__RST_string__ + "\n" + "La ``formula`` in codice è la seguente: \n\n.. code:: python\n\n " + self.formula + "\n"
        else:
            self.__RST_string__= self.__RST_string__ + "\n" + "La variabile non possiede una ``formula``\n\n"
        return self.__RST_string__


    def generate_RST_variable(self):
        # This method will generate an RST file and meanwhile, generate the corrispective in string
        with open(PATH_RST_DOCUMENT,'a') as rst:
            #variable name
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\nVariable: " + self.variable_name + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\n\n")
            # properties
            rst.write("\nProperties \n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('=')
            rst.write("\n")
            if self.value_type:
                rst.write("\n" + "Il ``tipo`` di questa variabile è: ``" + self.value_type + "``\n")
            else:
                rst.write("\n" + "``Tipo`` non definito\n")

            if self.entity:
                rst.write("\n" + "L'``entità`` a cui questa variabile appartiene è: ``" + self.entity + "``\n")
            else:
                rst.write("\n" + "``Entità`` non definita\n")

            if self.definition_period:
                rst.write("\n" + "Il ``periodo`` di definizione di questa varabile è: ``" + self.definition_period + "``\n")
            else:
                rst.write("\n" + "``Periodo`` di definizione non definito\n")

            if self.set_input:
                rst.write("\n" + "Il ``set_input`` di questa variabile vale: ``" + str(self.set_input) + "``\n")
            else:
                rst.write("\n" + "Nessun ``set_input`` inserito\n")

            if self.label:
                rst.write("\n" + "La ``descrizione`` della varabile è: \n\n.. code-block:: rst\n\n " + self.label + "\n")
            else:
                rst.write("\n" + "Nessuna ``descrizione`` inserita\n")

            if self.reference:
                rst.write("\n" + "`Riferimento legislativo alla variabile <" + self.reference.strip() + ">`__" + "\n")
            else:
                rst.write("\n" + "Nessun ``riferimento legislativo`` indicato\n")

            if self.formula:
                rst.write("\n" + "La ``formula`` in codice è la seguente: \n\n.. code:: python \n\n\n " + self.formula + "\n")
            else:
                rst.write("\n" + "La variabile non possiede una ``formula``\n\n")
        return PATH_RST_DOCUMENT


class Variable_File_Interpeter():
    __variables__ = [] # will be a list
    __file_is_a_variable__ = None
    tax_benefit_system_module_class = None

    def __init__(self,variable_path):
        self.__variable_path__ = variable_path
        if Variable_File_Interpeter.tax_benefit_system_module_class is None:
            raise ValueError("You must import the system to create a variable interpeter")
        # check if the file passed contains a variable
        with open(self.__variable_path__,'r') as content_variable:
            for line in content_variable.readlines():
                if 'class' in line and '(Variable):' in line:
                    self.__file_is_a_variable__ = True

    def get_variables(self):
        return self.__variables__

    def file_is_a_variable(self):
        return self.__file_is_a_variable__

    @staticmethod
    def import_depending_on_system(tax_benefit_system_module_class):
        Variable_File_Interpeter.tax_benefit_system_module_class = tax_benefit_system_module_class()

    def start_interpetration(self):
        self.__variables__ = []
        with open(self.__variable_path__,'r') as content_variable:
            for line in content_variable.readlines():
                line =  line.strip()
                if '#' in line:
                    line = line[:line.find('#')]
                if line: # found only the name of the variable
                    if 'class' in line and '(Variable):' in line: # variable found
                        variable_name = line
                        for chs in ['class','(Variable):']:
                            variable_name = variable_name.replace(chs,'')
                        current_Variable = Variable_for_writing(variable_name = variable_name.strip())
                        self.__variables__.append(current_Variable)
        variables = self.tax_benefit_system_module_class.get_variables()
        for k,v in variables.iteritems():
            for element in self.__variables__:
                if k == element.get_variable_name():
                    element.set_value_type(v.value_type.__name__)
                    element.set_entity(v.entity.__name__)
                    if v.label:
                        element.set_label(v.label.encode("utf-8"))
                    element.set_definition_period(v.definition_period)
                    if v.reference:
                        element.set_reference(v.reference[0])
                    if v.set_input :
                        element.set_set_input(v.set_input.__name__)
                    if not (v.is_input_variable()):
                        lines = inspect.getsource(v.get_formula())  # get formula if the variable if exist
                        element.set_formula(lines)

    def __interpretation_variable_for_reform__(self):
        self.__variables__ = []
        formula_found = False
        current_variable_index = -1
        current_Variable = None
        with open(self.__variable_path__,'r') as content_variable:
            for line in content_variable.readlines():
                line =  line.strip()
                if '#' in line:
                    line = line[:line.find('#')]
                if line:
                    if formula_found:
                        if ('class' in line and '(Variable):' in line) or ('class' in line and '(Reform):' in line):
                            formula_found = False
                        else:
                            current_Variable.set_formula(current_Variable.get_formula() + "\n   "+ line)
                    pieces = line.split('=')
                    if 'class' in pieces[0] and '(Variable):' in pieces[0]:
                        formula_found = False
                        current_variable_index = current_variable_index + 1
                        variable_name = pieces[0]
                        for chs in ['class','(Variable):']:
                            variable_name = variable_name.replace(chs,'')
                        current_Variable = Variable_for_writing(variable_name = variable_name.strip())
                        self.__variables__.append(current_Variable)
                    if 'value_type' in pieces[0]:
                        current_Variable.set_value_type(pieces[1].strip())
                    if 'entity' in pieces[0]:
                        current_Variable.set_entity(pieces[1].strip())
                    if 'label' in pieces[0]:
                        label = pieces[1]
                        for chs in ['u"','\"']:
                            label = label.replace(chs,'')
                        current_Variable.set_label(label.strip())#label could be written with unicode
                    if 'definition_period' in pieces[0]:
                        current_Variable.set_definition_period(pieces[1].strip())
                    if 'set_input' in pieces[0]:
                        current_Variable.set_set_input(pieces[1].strip())
                    if 'reference' in pieces[0]:
                        reference = pieces[1]
                        for chs in ['\"']:
                            reference = reference.replace(chs,'')
                        reference = re.search("(?P<url>https?://[^\s]+)", reference).group("url")
                        current_Variable.set_reference(reference.strip())
                    if 'formula' in pieces[0]:
                        formula_found = True
                        current_Variable.set_formula(' ' + pieces[0].strip())


    def generate_RSTs_variables(self):
        #print self.__variables__
        for var in self.__variables__:
            path = var.generate_RST_variable() # the path is always the same
        return path
