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



class Variable():

    def __init__(self, name = "", entity = None, type = None, reference = None, openfisca_tax_benefit_system_path = "", label = None, set_input = None, definition_period = datetime.datetime.now().year):
        self.__name__ = name
        self.__entity__ = entity
        self.__type__ = type
        self.__reference__ = reference
        self.__openfisca_tax_benefit_system_path__ = openfisca_tax_benefit_system_path
        self.__label__ = label
        self.__definition_period__ = definition_period
        self.__set_input__ = set_input


    def return_entites_openfisca(self): # use to show options
        sys.path.append(self.__openfisca_tax_benefit_system_path__)
        entita = importlib.import_module('entita')
        self.entities = []
        for entity in entita.entities:
            self.entities.append(entity)
        print self.entities

    def set_name(self, name):
        self.__name__ = name

    def set_type(self, type):
        accept_value = []
        for type_accepted in TYPEOFVARIABLE:
            accept_value.append(type_accepted.name)
        if type in accept_value:
            self.__type__ = type
        else:
            raise ValueError("The type defined for the variable is unacceptable")

    def set_entity(self, entity):
        self.__entity__ = entity

    def set_reference(self, reference):
        self.__reference__ = reference

    def set_openfisca_tax_benefit_system_path(self, openfisca_tax_benefit_system_path):
        self.__openfisca_tax_benefit_system_path__ = openfisca_tax_benefit_system_path

    def set_label(self, label):
        self.__label__ = label

    def set_definition_period(self, definition_period):
        self.__definition_period__ = definition_period

    def set_set_input(self, set_input):
        self.__set_input__ = set_input

    def __repr__(self):
        return "\n\nName: " + self.__name__ + "\nType: " + self.__type__ + "\nEntity: " + self.__entity__ + "\nDefinition period: " + self.__definition_period__

v = Variable(openfisca_tax_benefit_system_path = 'C:\\Users\\Stach\\Desktop\\openfisca-italy\\openfisca_italy')
v.return_entites_openfisca()
v.set_type("float")
