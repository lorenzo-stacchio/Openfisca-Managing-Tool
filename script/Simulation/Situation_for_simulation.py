import os
import sys
import inspect
import datetime
import time
import importlib
import re
from openfisca_italy import italy_taxbenefitsystem
from openfisca_italy.entita import Persona, Famiglia
from openfisca_italy import scenarios
from enum import Enum
from datetime import date
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

    def __init__(self, name = "", entity = None, type=None, set_input=None, definition_period = datetime.datetime.now().year):
        self.name = name
        self.entity = entity
        self.type = type
        self.definition_period = definition_period
        self.value = None
        self.set_input  = set_input


    def __repr__(self):
        return "\n\nName: " + self.name + "\nType: " + self.type + "\nEntity: " + self.entity + "\nDefinition period: " + self.definition_period

    def set_value(self,value):
        self.value = value


class Entity():

    def __init__(self, entity = None):
        if (entity is Persona) or (entity is Famiglia) : # assign variables to entity
            self.entity = entity
            self.entity_name = entity.label
        else:
            raise ValueError("The entity doesn't exist")

    def __repr__(self):
        return str("\nEntity name: " + self.entity + "\nNumber of variables: " + str(len(self.associated_variables)))

    def generate_associated_variable_filter(self, year = None, month = None, day = None):
        if year and not month and not day:
            if re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4:
                self.period_to_filter_variables = TYPEOFDEFINITIONPERIOD.year
            # i'll get however all the eternity variables
            else:
                raise ValueError("No valid date selected")
        elif year and month and not day:
            if re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4 and re.match(r'.*([1-12])', month) and len(month) == 2:
                self.period_to_filter_variables = TYPEOFDEFINITIONPERIOD.month
            # i'll get however all the eternity variables
            else:
                raise ValueError("No valid date selected")
        # i'll get however all the eternity variables
        else:
            raise ValueError("No valid date selected")
        # validates
        self.associated_variables = []
        tax_benefit_system = italy_taxbenefitsystem.ItalyTaxBenefitSystem()
        for key_variable, variables_content in tax_benefit_system.get_variables(entity = self.entity).iteritems():
            if (self.period_to_filter_variables.name == variables_content.definition_period) or (variables_content.definition_period == TYPEOFDEFINITIONPERIOD.eternity.name) or (variables_content.set_input):
                self.associated_variables.append(Variable(name = key_variable,type = variables_content.value_type.__name__, entity = variables_content.entity.__name__, definition_period = variables_content.definition_period))


    def generate_all_associated_variable(self):
        # validates
        self.associated_variables = []
        tax_benefit_system = italy_taxbenefitsystem.ItalyTaxBenefitSystem()
        for key_variable, variables_content in tax_benefit_system.get_variables(entity = self.entity).iteritems():
            self.associated_variables.append(Variable(name = key_variable,type = variables_content.value_type.__name__, entity = variables_content.entity.__name__, definition_period = variables_content.definition_period))


    def get_associated_variables(self):
        try:
            return {self.entity_name: self.associated_variables}
        except AttributeError:
            print "You have to generate the variables before getting their"


class Situation(): # defined for one entity

    def __init__(self, name_of_situation = "situazione_prova"):
        self.name_of_situation = name_of_situation
        self.choosen_input_variables = None
        self.choosen_output_variables = None
        self.period = None


    def __repr__(self):
        return "\nSituation name: " + str(self.name_of_situation) + "\nSituation period: " + str(self.period) + "\nNumber of input variables: " + str(len(self.choosen_input_variables)) + "\nNumber of output variables: " + str(len(self.choosen_output_variables))

    def set_entity_choose(self, entity_choose):
        if isinstance(entity_choose, Entity):
            if not(entity_choose.entity is Persona) and not(entity_choose.entity is Famiglia):
                raise ValueError("One of the inserted entity doesn't exist")
            else:
                self.entity_choose = entity_choose
        else:
            raise TypeError("The object used is not an entity")

    def set_period(self,year = None, month = None, day = None):
        if year and not month and not day:
            if not (re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4):
                raise ValueError("No valid date selected")
            else:
                self.period = year
        elif year and month and not day:
            if not (re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4) or not(re.match(r'.*([1-12])', month) and len(month) == 2):
                raise ValueError("No valid date selected")
            else:
                self.period = year + "-" + month
        else:
            raise ValueError("No valid date selected")

    def get_period(self):
        return self.period


    def get_choosen_input_variables(self):
        return self.choosen_input_variables


    def add_variable_to_choosen_input_variables(self, choosen_input_variable, value):
        if self.choosen_input_variables is None:
            self.choosen_input_variables = {}
        variable_match = False
        for entity, associated_variables in self.entity_choose.get_associated_variables().iteritems():
            for variable in associated_variables:
                #print "Variable exist", variable.name
                #print "Variable choose", choosen_input_variable
                if str(variable.name) == choosen_input_variable:
                    self.choosen_input_variables[choosen_input_variable] = value
                    variable_match = True
                    break
            if variable_match:
                break
        if not variable_match:
            raise TypeError("The variable you choose, is not defined for the entity or doesn't exist")


    def get_choosen_output_variables(self):
        return self.choosen_output_variables


    def add_variable_to_choosen_output_variables(self, choosen_output_variable):
        if self.choosen_output_variables is None:
            self.choosen_output_variables = []
        variable_match = False
        for entity, associated_variables in self.entity_choose.get_associated_variables().iteritems():
            for variable in associated_variables:
                #print "Variable exist", variable.name
                #print "Variable choose", choosen_input_variable
                if str(variable.name) == choosen_output_variable:
                    self.choosen_output_variables.append(choosen_output_variable)
                    variable_match = True
                    break
            if variable_match:
                break
        if not variable_match:
            raise TypeError("The variable you choose, is not defined for the entity or doesn't exist")


class Simulation_generator(): #defined for Italy


    def __init__(self):
        self.situations = None #take n situations
        self.period = datetime.datetime.now().year
        self.results = None


    def init_profile(self, scenario, situation_period, entity_situation):
        scenario.init_single_entity(
            period = situation_period,
            parent1 = entity_situation
        )
        return scenario

    def set_period(self,year = None, month = None, day = None):
        if year and not month and not day:
            if not (re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4):
                raise ValueError("No valid date selected")
            else:
                self.period = year
        elif year and month and not day:
            if not (re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4) or not(re.match(r'.*([1-12])', month) and len(month) == 2):
                raise ValueError("No valid date selected")
            else:
                self.period = year + "-" + month
        else:
            raise ValueError("No valid date selected")


    def add_to_result(self, situation, name_of_variable_calculated, result):
        if self.results is None: # initialize if it is empty
            self.results = {}
        if not situation in self.results:
            self.results[situation] = {} #initialize inner dict
        self.results[situation][name_of_variable_calculated] = result


    def get_results(self):
        return self.results


    def add_situation_to_simulator(self, situation): # you can add situations with the same content
        if self.situations is None:
            self.situations = []
        if isinstance(situation, Situation):
            self.situations.append(situation)
        else:
            raise TypeError("The situation selected is not a valid situation")


    def generate_simulation(self):
        # import dinamically
        tax_benefit_system = italy_taxbenefitsystem.ItalyTaxBenefitSystem()
        if not (self.situations == []) and not (self.situations is None):
            for situation in self.situations:
                # RICORDA CHE DEVI FARE PRATICAMETE UNA SIMULAZIONE PER OGNI PERSONA, NEL SENSO CHE INIZIALIZZI TRE VOLTE LO SCENARIO E POI RUNNI per il problema dello scenario
                scenario = tax_benefit_system.new_scenario()
                scenario = self.init_profile(scenario = scenario, situation_period = situation.get_period(), entity_situation = situation.get_choosen_input_variables())
                simulation = scenario.new_simulation() # nuova simulazione per lo scenario normale
                for element in situation.get_choosen_output_variables():
                    self.add_to_result(situation = situation.name_of_situation, name_of_variable_calculated = element , result = simulation.calculate(element,self.period))
        else:
            raise ValueError("To trigger a simulation, at least a situation it's needed")

# main
path = 'C:\\Users\\Stach\\Desktop\\openfisca-italy\\openfisca_italy'
person = Entity(entity = Persona)
person.generate_associated_variable_filter(year = '2017')

situation_IRPEF_1 = Situation(name_of_situation = "IRPEF1_2017")
situation_IRPEF_1.set_entity_choose(person)
situation_IRPEF_1.set_period(year = '2017')
# input variables
situation_IRPEF_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN1_reddito_complessivo', value = 25000)
situation_IRPEF_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN2_deduzione_abitazione_principale', value = 2000)
situation_IRPEF_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN3_oneri_deducibili_totali', value = 1500)
situation_IRPEF_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN22_totale_detrazioni_imposta', value = 2000)
situation_IRPEF_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN25_totale_altre_detrazioni_crediti_imposta', value = 1000)
# output
situation_IRPEF_1.add_variable_to_choosen_output_variables(choosen_output_variable = 'RN4_reddito_imponibile')
situation_IRPEF_1.add_variable_to_choosen_output_variables(choosen_output_variable = 'RN5_irpef_lorda')
situation_IRPEF_1.add_variable_to_choosen_output_variables(choosen_output_variable = 'RN26_irpef_netta')
print "IRPEF",  situation_IRPEF_1


situation_IRPEF_2 = Situation(name_of_situation = "IRPEF2_2017")
situation_IRPEF_2.set_entity_choose(person)
situation_IRPEF_2.set_period(year = '2017')
# input variables
situation_IRPEF_2.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN1_reddito_complessivo', value = 15000)
situation_IRPEF_2.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN2_deduzione_abitazione_principale', value = 1000)
situation_IRPEF_2.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN3_oneri_deducibili_totali', value = 1000)
situation_IRPEF_2.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN22_totale_detrazioni_imposta', value = 500)
situation_IRPEF_2.add_variable_to_choosen_input_variables(choosen_input_variable = 'RN25_totale_altre_detrazioni_crediti_imposta', value = 400)
# output
situation_IRPEF_2.add_variable_to_choosen_output_variables(choosen_output_variable = 'RN4_reddito_imponibile')
situation_IRPEF_2.add_variable_to_choosen_output_variables(choosen_output_variable = 'RN5_irpef_lorda')
situation_IRPEF_2.add_variable_to_choosen_output_variables(choosen_output_variable = 'RN26_irpef_netta')
print "IRPEF",  situation_IRPEF_2
#print id(situation_IRPEF_1)
#situation_IMU_1 = Situation(name_of_situation = "IMU_2017")
#situation_IMU_1.set_period(year = '2017' , month ='01')
#situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'valore_immobile_non_rivalutato', value = 10000)
#situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'is_immobile_prima_casa', value = False)
#situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'immobile_categoria_catastale', value = 'A5')
#situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'percentuale_possesso', value = 100)
#situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'mesi_di_possesso', value = 12)
#situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'aliquota_imu', value = 7.6)
#situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'is_interesse_storico_artistico', value = True)
# outpu
#situation_IMU_1.add_variable_to_choosen_output_variables(choosen_output_variable = 'imposta_imu')
#situation_IMU_1.add_variable_to_choosen_output_variables(choosen_output_variable = 'detrazioni_imu')
#situation_IMU_1.add_variable_to_choosen_output_variables(choosen_output_variable = 'importo_imu')
#print "IMU",  situation_IMU_1
#print id(situation_IMU_1)
simulation_IRPEF = Simulation_generator()
simulation_IRPEF.set_period('2017')
simulation_IRPEF.add_situation_to_simulator(situation_IRPEF_1)
simulation_IRPEF.add_situation_to_simulator(situation_IRPEF_2)
simulation_IRPEF.generate_simulation()
print simulation_IRPEF.get_results()
#simulation_IMU = Simulation_generator(situations = [situation_IMU_1], period='2017-01')
#simulation_IMU.generate_simulation()
#simulation_IMU.get_results()
