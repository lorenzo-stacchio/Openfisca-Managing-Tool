import os
import sys
import inspect
import datetime
import time
import importlib

class Variable():
    __name__= None
    __entity__ = None
    __value__ = None
    __type__ = None
    __definition_period__ = None

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
    __name__= None
    __associated_variables__ = []
    __types_of_entity__ = []
    __openfisca_tax_benefit_system_path__ = None

    def __init__(self, name = "", openfisca_tax_benefit_system_path = None):
        self.__associated_variables__ = []
        self.__openfisca_tax_benefit_system_path__ = openfisca_tax_benefit_system_path
        # import dinamically
        sys.path.append(self.__openfisca_tax_benefit_system_path__)
        italy_taxbenefitsystem = importlib.import_module('italy_taxbenefitsystem')
        scenarios = importlib.import_module('scenarios')
        entita = importlib.import_module('entita')
        tax_benefit_system = italy_taxbenefitsystem.ItalyTaxBenefitSystem()
        for entity in entita.entities: # entities in the openfisca_ssytem
            self.__types_of_entity__.append(entity.__name__)
        if (name in self.__types_of_entity__): # assign variables to entity
            self.__name__ = name
            for key_variable, variables_content in tax_benefit_system.get_variables().iteritems():
                #print name == variables_content.entity.__name__
                if name == variables_content.entity.__name__:
                    self.__associated_variables__.append(Variable(name = key_variable,type = variables_content.value_type.__name__, entity = variables_content.entity.__name__, definition_period = variables_content.definition_period))
        else:
            raise ValueError('Entity selected doesn\'t exist')

    def __repr__(self):
        return str("\nName: " + self.__name__ + "\nNumber of variables: " + str(len(self.__associated_variables__)))

    def get_associated_variables(self):
        return self.__associated_variables__


class Situation():
    __entities_choosen__ = None
    __period__ = None
    __choosen_input_variables__ = None
    __choosen_output_variables__ = None
    __name_of_situation__ = None

    def __init__(self,name_of_situation = "" , entities_choosen = [], choosen_input_variables = {}, choosen_output_variables = [], period = datetime.datetime.now().year):
        self.__name_of_situation__ = name_of_situation
        self.__period__ = period
        self.__entities_choosen__ = entities_choosen
        self.__choosen_input_variables__ = choosen_input_variables
        self.__choosen_output_variables__ = choosen_output_variables

    def __repr__(self):
        return "\nSituation name: " + str(self.__name_of_situation__) + "\nSituation period: " + str(self.__period__) + "\nNumber of input variables: " + str(len(self.__choosen_input_variables__)) + "\nNumber of output variables: " + str(len(self.__choosen_output_variables__))

    def set_entities_choosen(self,entities_choosen):
        self.__entities_choosen__ = entities_choosen

    # getters and setters
    def set_period(self,period):
        self.__period__ = period

    def get_period(self):
        return self.__period__

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
    __situation__ = None
    __openfisca_tax_benefit_system_path__ = None
    __period__ = None

    def __init__(self, situation = None, openfisca_tax_benefit_system_path = None, period = datetime.datetime.now().year):
        self.__situation__ = situation
        self.__openfisca_tax_benefit_system_path__ = openfisca_tax_benefit_system_path
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
        sys.path.append(self.__openfisca_tax_benefit_system_path__)
        italy_taxbenefitsystem = importlib.import_module('italy_taxbenefitsystem')
        scenarios = importlib.import_module('scenarios')
        entita = importlib.import_module('entita')
        tax_benefit_system = italy_taxbenefitsystem.ItalyTaxBenefitSystem()
        # RICORDA CHE DEVI FARE PRATICAMETE UNA SIMULAZIONE PER OGNI PERSONA, NEL SENSO CHE INIZIALIZZI TRE VOLTE LO SCENARIO E POI RUNNI per il problema dello scenario
        scenario = tax_benefit_system.new_scenario()
        print "\n\nSCENARIO BEFORE INIT", scenario
        #scenario = self.init_profile(scenario = scenario, entity_situation = self.__situation__.get_choosen_input_variables())
        print "\n\nSCENARIO IN SIMULATION", scenario
        simulation = scenario.new_simulation() # nuova simulazione per lo scenario normale
        print "\n\nSIMULATION", simulation, "\n\n"
        for element in self.__situation__.get_choosen_input_variables():
            print simulation.calculate(element,self.__period__)

# main
path = 'C:\\Users\\Stach\\Desktop\\openfisca-italy\\openfisca_italy'
situation = Situation(name_of_situation = "IRPEF_2017", period = '2017')
print "INIZIO SITUAZIONE",  situation
person = Entity(name = 'Person' , openfisca_tax_benefit_system_path = path)
print "AGGIUNTA PERSONA", person
#print "*************************PERSON***********************************"
list_person_variables =  person.get_associated_variables()
situation.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN4_reddito_imponibile', value = 10000)
situation.add_variable_to_choosen_output_variables(choosen_output_variable = 'RN5_irpef_lorda')
print "FINE SITUAZIONE",  situation
simulation = Simulation_generator(situation = situation, openfisca_tax_benefit_system_path = path, period='2017')
simulation.generate_simulation()
