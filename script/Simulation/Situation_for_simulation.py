import os
import sys
import inspect
import datetime
import time
import importlib
from openfisca_italy import italy_taxbenefitsystem
from openfisca_italy.entita import Persona, Famiglia
from openfisca_italy import scenarios
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

## TODO: FAI IL CHECK DEI TIPI


class Variable():

    def __init__(self, name = "", entity = None, type=None, definition_period = datetime.datetime.now().year):
        self.__name__ = name
        self.__entity__ = entity
        self.__type__ = type
        self.__definition_period__ = definition_period
        self.__value__ = None


    def __repr__(self):
        return "\n\nName: " + self.__name__ + "\nType: " + self.__type__ + "\nEntity: " + self.__entity__ + "\nDefinition period: " + self.__definition_period__

    def set_value(self,value):
        self.__value__ = value


class Entity():

    def __init__(self, entity = None):
        self.__associated_variables__ = []
        tax_benefit_system = italy_taxbenefitsystem.ItalyTaxBenefitSystem()
        if (entity is Persona) or (entity is Famiglia) : # assign variables to entity
            self.__entity__ = entity.__name__
            for key_variable, variables_content in tax_benefit_system.get_variables(entity = self.__entity__ ).iteritems():
                self.__associated_variables__.append(Variable(name = key_variable,type = variables_content.value_type.__name__, entity = variables_content.entity.__name__, definition_period = variables_content.definition_period))
        else:
            raise ValueError('Entity selected doesn\'t exist')

    def __repr__(self):
        return str("\nEntity name: " + self.__entity__ + "\nNumber of variables: " + str(len(self.__associated_variables__)))

    def get_associated_variables(self):
        return self.__associated_variables__


class Situation():

    def __init__(self,name_of_situation = "" , entities_choosen = [], choosen_input_variables = {}, choosen_output_variables = [], period = datetime.datetime.now().year):
        self.__name_of_situation__ = name_of_situation
        self.__period__ = period
        self.__entities_choosen__ = entities_choosen
        self.__choosen_input_variables__ = choosen_input_variables
        self.__choosen_output_variables__ = choosen_output_variables

    def __repr__(self):
        return "\nSituation name: " + str(self.__name_of_situation__) + "\nSituation period: " + str(self.__period__) + "\nNumber of input variables: " + str(len(self.__choosen_input_variables__)) + "\nNumber of output variables: " + str(len(self.__choosen_output_variables__))

    def set_entities_choosen(self, entities_choosen):
        for element in entities_choosen: # we want a list
            if not(element is Persona) and not(element is Famiglia):
                raise ValueError("One of the inserted entity doesn't exist")
        self.__entities_choosen__ = entities_choosen # if we are here all it's ok

    # getters and setters
    def set_period(self,period):
        self.__period__ = period

    def get_period(self):
        return self.__period__

    # TODO: controlla se le variabili messe in input esistono
    def set_choosen_input_variables(self,choosen_input_variables):
        self.__choosen_input_variables__ = choosen_input_variables

    def get_choosen_input_variables(self):
        return self.__choosen_input_variables__

    def add_variable_to_choosen_input_variables(self,choosen_input_variable,value):
        self.__choosen_input_variables__[choosen_input_variable] = value

    def set_choosen_output_variables(self,choosen_output_variables):
        self.__choosen_output_variables__ = choosen_output_variables

    def get_choosen_output_variables(self):
        return self.__choosen_output_variables__

    def add_variable_to_choosen_output_variables(self,choosen_output_variable):
        self.__choosen_output_variables__.append(choosen_output_variable)


class Simulation_generator(): #defined for Italy

    def __init__(self, situation = None, period = datetime.datetime.now().year):
        self.__situation__ = situation
        self.__period__ = period


    def init_profile(self, scenario, entity_situation):
        #print "Situation: ", entity_situation
        scenario.init_single_entity(
            period = self.__period__,
            parent1 = entity_situation
        )
        return scenario


    def generate_simulation(self):
        # import dinamically
        tax_benefit_system = italy_taxbenefitsystem.ItalyTaxBenefitSystem()
        # RICORDA CHE DEVI FARE PRATICAMETE UNA SIMULAZIONE PER OGNI PERSONA, NEL SENSO CHE INIZIALIZZI TRE VOLTE LO SCENARIO E POI RUNNI per il problema dello scenario
        scenario = tax_benefit_system.new_scenario()
        scenario = self.init_profile(scenario = scenario, entity_situation = self.__situation__.get_choosen_input_variables())
        simulation = scenario.new_simulation() # nuova simulazione per lo scenario normale
        for element in self.__situation__.get_choosen_output_variables():
            print "Risultato simulazione", simulation.calculate(element,self.__period__)

# main
path = 'C:\\Users\\Stach\\Desktop\\openfisca-italy\\openfisca_italy'
situation = Situation(name_of_situation = "IRPEF_2017", period = '2017')
print "INIZIO SITUAZIONE",  situation
person = Entity(entity = Persona )
print "AGGIUNTA PERSONA", person
#print "*************************PERSON***********************************"
#list_person_variables =  person.get_associated_variables()
situation.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN4_reddito_imponibile', value = 10000)
situation.add_variable_to_choosen_output_variables(choosen_output_variable = 'RN5_irpef_lorda')
print "FINE SITUAZIONE",  situation
simulation = Simulation_generator(situation = situation, period='2017')
simulation.generate_simulation()
