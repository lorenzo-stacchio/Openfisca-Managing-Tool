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
        print self.period_to_filter_variables
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

    def __init__(self, name_of_situation = None , entity_choose = None, choosen_input_variables = None, choosen_output_variables = None, period = None):
        self.name_of_situation = name_of_situation
        self.period = period
        self.entity_choose = entity_choose
        self.choosen_input_variables= choosen_input_variables
        self.choosen_output_variables = choosen_output_variables

    def __repr__(self):
        return "\nSituation name: " + str(self.name_of_situation) + "\nSituation period: " + str(self.period) + "\nNumber of input variables: " + str(len(self.choosen_input_variables)) + "\nNumber of output variables: " + str(len(self.choosen_output_variables))

    def set_entity_choose(self, entity_choose):
        for element in entity_choose: # we want a list
            if not(element is Persona) and not(element is Famiglia):
                raise ValueError("One of the inserted entity doesn't exist")
        self.entity_choose = entity_choose # if we are here all it's ok

    # getters and setters
    def set_period(self,period):
        self.period = period

    def get_period(self):
        return self.period

    # TODO: controlla se le variabili messe in input esistono
    def set_choosen_input_variables(self,choosen_input_variables):
        if self.choosen_input_variables is None:
            self.choosen_input_variables = {}
        self.choosen_input_variables = choosen_input_variables

    def get_choosen_input_variables(self):
        return self.choosen_input_variables

    def add_variable_to_choosen_input_variables(self,choosen_input_variable,value):
        if self.choosen_input_variables is None:
            self.choosen_input_variables = {}
        self.choosen_input_variables[choosen_input_variable] = value

    def set_choosen_output_variables(self,choosen_output_variables):
        if self.choosen_output_variables is None:
            self.choosen_output_variables = []
        self.choosen_output_variables = choosen_output_variables

    def get_choosen_output_variables(self):
        return self.choosen_output_variables

    def add_variable_to_choosen_output_variables(self,choosen_output_variable):
        if self.choosen_output_variables is None:
            self.choosen_output_variables = []
        self.choosen_output_variables.append(choosen_output_variable)


class Simulation_generator(): #defined for Italy

    def __init__(self, situations = None, results = None, period = datetime.datetime.now().year):
        self.situations = situations #take n situations
        self.period = period
        self.results = results


    def init_profile(self, scenario, entity_situation):
        #print "Situation: ", entity_situation
        scenario.init_single_entity(
            period = self.period,
            parent1 = entity_situation
        )
        return scenario

    def add_to_result(self,result):
        if self.results is None:
            self.results = []
        self.results.append(result)

    def get_results(self):
        return self.results

    def generate_simulation(self):
        # import dinamically
        tax_benefit_system = italy_taxbenefitsystem.ItalyTaxBenefitSystem()
        for situation in self.situations:
            # RICORDA CHE DEVI FARE PRATICAMETE UNA SIMULAZIONE PER OGNI PERSONA, NEL SENSO CHE INIZIALIZZI TRE VOLTE LO SCENARIO E POI RUNNI per il problema dello scenario
            scenario = tax_benefit_system.new_scenario()
            scenario = self.init_profile(scenario = scenario, entity_situation = situation.get_choosen_input_variables())
            simulation = scenario.new_simulation() # nuova simulazione per lo scenario normale
            for element in situation.get_choosen_output_variables():
                self.add_to_result(simulation.calculate(element,self.period))
# main
path = 'C:\\Users\\Stach\\Desktop\\openfisca-italy\\openfisca_italy'
situation_IRPEF_1 = Situation(name_of_situation = "IRPEF_2017", period = '2017')
person = Entity(entity = Persona) # LOAD PERSONA
person.generate_associated_variable_filter(year = '2017' , month ='01' )
#person.generate_associated_variable_filter(year = '2017')
print person.get_associated_variables()
#print "*************************PERSON***********************************"
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
print id(situation_IRPEF_1)
situation_IMU_1 = Situation(name_of_situation = "IMU_2017", period = '2017-01')
situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'valore_immobile_non_rivalutato', value = 10000)
situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'is_immobile_prima_casa', value = False)
situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'immobile_categoria_catastale', value = 'A5')
situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'percentuale_possesso', value = 100)
situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'mesi_di_possesso', value = 12)
situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'aliquota_imu', value = 7.6)
situation_IMU_1.add_variable_to_choosen_input_variables(choosen_input_variable = 'is_interesse_storico_artistico', value = True)
# outpu
situation_IMU_1.add_variable_to_choosen_output_variables(choosen_output_variable = 'imposta_imu')
situation_IMU_1.add_variable_to_choosen_output_variables(choosen_output_variable = 'detrazioni_imu')
situation_IMU_1.add_variable_to_choosen_output_variables(choosen_output_variable = 'importo_imu')
print "IMU",  situation_IMU_1
print id(situation_IMU_1)

simulation_IRPEF = Simulation_generator(situations = [situation_IRPEF_1], period='2017')
simulation_IRPEF.generate_simulation()
print simulation_IRPEF.get_results()
simulation_IMU = Simulation_generator(situations = [situation_IMU_1], period='2017-01')
simulation_IMU.generate_simulation()
simulation_IMU.get_results()
