# -*- coding: utf-8 -*-
import os
from enum import Enum
from dateutil.parser import parse as date_parser
import datetime
import collections
import re
import time

GRANDEZZA_STRINGHE_INTESTAZIONE = 1000
PATH_RST_DOCUMENT = os.getcwd() + "\\messages\\rst_da_visualizzare.rst"

class Variable_for_writing():
    variable_name = None
    value_type = None
    entity = None
    definition_period = None
    label = None
    formula = None
    reference = None
    set_input = None

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

    def set_entity(self,entity):
        self.entity = entity

    def set_definition_period(self,definition_period):
        self.definition_period = definition_period

    def set_label(self,label):
        self.label = label

    def set_value_type(self,value_type):
        self.value_type = value_type

    def set_formula(self,formula):
        self.formula = formula

    def get_formula(self):
        return self.formula

    def set_variables_involved_in_formula(self,variables_involved_in_formula):
        self.variables_involved_in_formula = variables_involved_in_formula

    def set_set_input(self,set_input):
        self.set_input = set_input


    def set_reference(self,reference):
        self.reference = reference


    def generate_RST_variable(self):
        with open(PATH_RST_DOCUMENT,'a') as rst:
            #variable name
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\n Variable: " + self.variable_name + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\n\n")
            # properties
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\n Properties \n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\n")
            rst.write("\n" + "- Il tipo di questa variabile è: **" + self.value_type + "**\n")
            rst.write("\n" + "- L'entità a cui questa variabile appartiene è: **" + self.entity + "**\n")
            rst.write("\n" + "- Il periodo di definizione di questa varabile è: **" + self.definition_period + "**\n")
            if self.set_input:
                rst.write("\n" + "- Il set_input di questa variabile vale: **" + self.set_input + "**\n")
            else: rst.write("\n" + "- Nessun set_input inserito\n")
            if self.label:
                rst.write("\n" + "- La descrizione della varabile è: \n\n.. code-block:: rst\n\n " + self.label + "\n")
            else: rst.write("\n" + "- Nessuna descrizione inserita\n")
            if self.reference:
                #rst.write("\n" + "- `Riferimento legislativo alla variabile`_\n\n   .. _Riferimento legislativo alla variabile: " + self.reference + "\n")
                #rst.write("\n" + "- `Riferimento legislativo alla variabile`__ \n\n   .. _link"+self.variable_name.strip()+": " + self.reference + "\n\n   __ link"+self.variable_name+"_" + "\n")
                rst.write("\n" + "- `Riferimento legislativo alla variabile <" + self.reference.strip() + ">`__" + "\n")
            else: rst.write("\n" + "- Nessun riferimento legislativo indicato\n")
            if self.formula:
                rst.write("\n" + "- La formula in codice è la seguente: \n\n.. code-block:: rst\n\n " + self.formula + "\n")
            else: rst.write("\n" + "- La variabile non possiede una formula\n\n")
        return PATH_RST_DOCUMENT


class Variable_File_Interpeter():
    __variables_file_path__ = ""
    __variables__ = [] # will be a list
    __file_is_a_variable__ = False

    def __init__(self,variable_path):
        self.__variable_path__ = variable_path
        # check if the file passed contains a variable
        with open(self.__variable_path__,'r') as content_variable:
            for line in content_variable.readlines():
                if 'class' in line and '(Variable):' in line:
                    self.__file_is_a_variable__ = True

    def file_is_a_variable(self):
        return self.__file_is_a_variable__

    def start_interpetration(self):
        self.__variables__ = []
        formula_found = False
        current_variable_index = -1
        current_Variable = None
        with open(self.__variable_path__,'r') as content_variable:
            for line in content_variable.readlines():
                line =  line.strip()
                if not line.startswith('#'):
                    # if found a formula, we don't have to split the line
                    if formula_found:
                        if 'class' in line and '(Variable):' in line:
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
                        current_Variable = Variable_for_writing(variable_name = variable_name)
                        self.__variables__.append(current_Variable)
                    if 'value_type' in pieces[0]:
                        current_Variable.set_value_type(pieces[1].strip())
                    if 'entity' in pieces[0]:
                        current_Variable.set_entity(pieces[1].strip())
                    if 'label' in pieces[0]:
                        label = pieces[1]
                        for chs in ['u"','\"']:
                            label = label.replace(chs,'')
                        current_Variable.set_label(label)#label could be written with unicode
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

# __main__

#object = Variable_File_Interpeter('C:\\Users\\Stach\\Desktop\\openfisca-italy\\openfisca_italy\\parameters\\benefici\\indennita_alloggio.yaml')
#object = Variable_File_Interpeter('C:\\Users\\Stach\\Desktop\\aldo.rst')
#object.start_interpetration()
#if object.file_is_a_variable():
#    object.generate_RSTs_variables()
#else:
#    print "Not a variable"
