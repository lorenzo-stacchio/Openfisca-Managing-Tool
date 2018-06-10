# -*- coding: utf-8 -*-
import os
from enum import Enum
from dateutil.parser import parse as date_parser
import datetime
import collections


class Variable_for_writing():
    variable_name = None
    value_type = None
    entity = None
    definition_period = None
    label = None
    formula = None
    variables_involved_in_formula = None
    reference = None

    def __init__(self, variable_name = None, value_type = None, entity = None, definition_period = None, label = None, reference = None, formula = None, variables_involved_in_formula = None):
        # a file contains many variable, so i can't erase it when i generate an RST so i'll do when i create a variable
        if os.path.exists(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\messages\\rst_da_visualizzare.txt"):
            print "RIMOZIONE"
            os.remove(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\messages\\rst_da_visualizzare.txt")
        self.variable_name = variable_name
        self.value_type = value_type
        self.entity = entity
        self.definition_period = definition_period
        self.label = label
        self.formula = formula
        self.variables_involved_in_formula = variables_involved_in_formula
        self.reference = reference

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

    def set_variables_involved_in_formula(self,variables_involved_in_formula):
        self.variables_involved_in_formula = variables_involved_in_formula

    def set_reference(self,reference):
        self.reference = reference


    def generate_RST_variable(self):

        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\messages\\rst_da_visualizzare.txt"
        with open(path,'a') as rst:
            #variable name
            for n in range(1,1000):
                rst.write('#')
            rst.write("\n Variable: " + self.variable_name + "\n")
            for n in range(1,1000):
                rst.write('#')
            rst.write("\n\n")
            # properties
            for n in range(1,1000):
                rst.write('#')
            rst.write("\n Properties \n")
            for n in range(1,1000):
                rst.write('#')
            rst.write("\n")
            rst.write("\n" + "- Il tipo di questa variabile è: **" + self.value_type + "**\n")
            rst.write("\n" + "- L'entità a cui questa variabile appartiene è: **" + self.entity + "**\n")
            rst.write("\n" + "- Il periodo di definizione di questa varabile è: **" + self.definition_period + "**\n")

            if self.label:
                rst.write("\n" + "- La descrizione della varabile è: \n\n.. code-block:: rst\n\n " + self.label + "\n")
            else: rst.write("\n" + "- Nessuna descrizione inserita\n")

            if self.reference:
                rst.write("\n" + "- `Riferimento legislativo alla variabile`_ \n\n .. _A cool website:" + self.reference + "\n")
            else: rst.write("\n" + "- Nessun riferimento legislativo indicato\n")

            if self.formula:
                rst.write("\n" + "- La formula in codice è la seguente: \n\n.. code-block:: rst\n\n " + self.formula + "\n")
            else: rst.write("\n" + "- La variabile non possiede una formula\n\n")


class Variable_File_Interpeter():
    __variables_file_path__ = ""
    __variables__ = [] # will be an array

    def __init__(self,variable_path):
        self.__variable_path__ = variable_path

    def start_interpetration(self):
        formula_found = False
        current_variable_index = -1
        current_Variable = None
        with open(self.__variable_path__,'r') as content_variable:
            for line in content_variable.readlines():
                line =  line.strip()
                pieces = line.split('=')
                if 'class' in pieces[0] and '(Variable):' in pieces[0]:
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
                    for chs in ['u','\"']:
                        label = label.replace(chs,'')
                    current_Variable.set_label(label)#label could be written with unicode
                if 'definition_period' in pieces[0]:
                    current_Variable.set_definition_period(pieces[1].strip())
                if 'reference' in pieces[0]:
                    reference = pieces[1]
                    for chs in ['u','\"']:
                        reference = reference.replace(chs,'')
                    current_Variable.set_reference(reference.strip())



    def generate_RSTs_variables(self):
        print self.__variables__
        for var in self.__variables__:
            var.generate_RST_variable()

# TODO: QUANDO LEGGI LA FORMULA, DEVI FARE UNO STRIP E POI METTERE UNO SPAZIO ALL'INIZIO DI OGNI RIGA PERCHE' SENNO IL COMANDO PER RST NON FUNZIONA
# __main__

object = Variable_File_Interpeter('C:\\Users\\Stach\\Desktop\\aldo.txt')
object.start_interpetration()
object.generate_RSTs_variables()
#v = Variable_for_writing(value_type = 'float',entity = 'person',definition_period = 'MONTH', label = 'Individualized and monthly paid tax on salaries',formula = 'def formula(person, period, parameters): \n salary = person(salary, period)  \n return salary * parameters(period).taxes.salary.rate',variables_involved_in_formula='')
#v.generate_RST_variable()
