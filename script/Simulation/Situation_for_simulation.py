import os
import sys
import inspect
import datetime
import time
import importlib
import re
import site
reload(sys)
sys.setdefaultencoding('utf8')
from enum import Enum
from datetime import date
from glob import glob

GRANDEZZA_STRINGHE_INTESTAZIONE = 1000

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

    tax_benefit_system_module_class = None
    entity_module_all_entities = None

    def __init__(self, entity = None):
        if Entity.tax_benefit_system_module_class is None or Entity.entity_module_all_entities is None:
            raise ValueError("You must import the system before you can create entity")
        print self.entity_module_all_entities
        if entity in self.entity_module_all_entities: # assign variables to entity
            self.entity = entity
            self.entity_name = entity.label
        else:
            raise ValueError("The entity doesn't exist")

    def __repr__(self):
        return str("\nEntity name: " + self.entity + "\nNumber of variables: " + str(len(self.associated_variables)))


    @staticmethod
    def import_depending_on_system(tax_benefit_system_module_class,entity_module_class,  entity_module_all_entities):
        Entity.tax_benefit_system_module_class = tax_benefit_system_module_class()
        Entity.entity_module_all_entities = getattr(entity_module_class,entity_module_all_entities)

    def generate_associated_variable_filter(self, year = None, month = None, day = None):
        if year and not month and not day:
            if re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4:
                self.period_to_filter_variables = TYPEOFDEFINITIONPERIOD.year
            # i'll get however all the eternity variables
            else:
                raise ValueError("No valid date selected")
        elif year and month and not day:
            if re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4 and re.match(r'.*([01-12])', month) and (len(month) == 2):
                self.period_to_filter_variables = TYPEOFDEFINITIONPERIOD.month
            # i'll get however all the eternity variables
            else:
                raise ValueError("No valid date selected")
        elif year and month and day:
            if re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4 and re.match(r'.*([01-12])', month) and (len(month) == 2) and re.match(r'.*([01-31])', day) and (len(day) == 2):
                self.period_to_filter_variables = TYPEOFDEFINITIONPERIOD.month
            else:
                raise ValueError("No valid date selected")
        else:
            raise ValueError("No valid date selected")
        # validates
        self.associated_variables = []
        for key_variable, variables_content in self.tax_benefit_system_module_class.get_variables(entity = self.entity).iteritems():
            if (self.period_to_filter_variables.name == variables_content.definition_period) or (variables_content.definition_period == TYPEOFDEFINITIONPERIOD.eternity.name) or (variables_content.set_input):
                self.associated_variables.append(Variable(name = key_variable,type = variables_content.value_type.__name__, entity = variables_content.entity.__name__, definition_period = variables_content.definition_period))


    def generate_all_associated_variable(self):
        # validates
        self.associated_variables = []
        for key_variable, variables_content in self.tax_benefit_system_module_class.get_variables(entity = self.entity).iteritems():
            self.associated_variables.append(Variable(name = key_variable,type = variables_content.value_type.__name__, entity = variables_content.entity.__name__, definition_period = variables_content.definition_period))


    def get_associated_variables(self):
        try:
            return {self.entity_name: self.associated_variables}
        except AttributeError:
            print "You have to generate the variables before getting their"


class Reform():
    tax_benefit_system_module_class = None
    reform_module = None


    def __init__(self):
        if self.tax_benefit_system_module_class is None or self.reform_module is None:
            raise ValueError("You must import the system and add the reform path, before you can create a reform")
        self.choose_reform = None # reform used for simulation
        self.reforms_file_dict = {} # dict that contains module name of the reform and reforms within it
        self.reform_module_name = self.reform_module.__name__ #reform name module
        self.reform_folder_name = os.path.basename(self.reform_module.__path__[0]) #basepath of reform module path
        files_in_reform_path = [y for x in os.walk(self.reform_module.__path__[0]) for y in glob(os.path.join(x[0], '*.py')) if not os.path.basename(y) == "__init__.py" ]
        for file in files_in_reform_path:
            # create a key that will be used to import the reform
            start_index = re.search(self.reform_folder_name, str(file)).start()
            key = str(file)[(start_index + len(self.reform_folder_name) + 1):]
            key = key.replace("\\", ".") # used to create a correct module path
            key = key.replace(".py", "") # erase the extension
            self.reforms_file_dict[key] = []
            with open(file, 'r') as f_r:
                for line in f_r.readlines():
                    line =  line.strip()
                    if '#' in line:
                        line = line[:line.find('#')]
                    if line:
                        if 'class' in line and '(Reform):' in line:
                            reform_name = line
                            for chs in ['class','(Reform):', ' ']:
                                reform_name = reform_name.replace(chs,'')
                            self.reforms_file_dict[key].append(reform_name)


    def get_reform_list(self):
        list = []
        if self.reforms_file_dict == None:
            raise ValueError("You must init the reform!")
        for k,v in self.reforms_file_dict.iteritems():
            for reform in v:
                list.append(reform)
        return list


    def set_choose_reform(self, reform_name):
        for k,v in self.reforms_file_dict.iteritems():
            if reform_name in v:
                self.choose_reform = {k : reform_name}
        if self.choose_reform is None:
            raise ValueError("You insert an invalid reform")


    def get_choose_reform(self):
        if self.choose_reform is None:
            raise TypeError("You have to set the reform to get it")
        else:
            return self.choose_reform


    @staticmethod
    def import_depending_on_system(tax_benefit_system_module_class, reform_module):
        Reform.tax_benefit_system_module_class = tax_benefit_system_module_class()
        Reform.reform_module = reform_module


class Situation(): # defined for one entity

    def __init__(self, name_of_situation = "situazione_prova"):
        self.name_of_situation = name_of_situation
        self.choosen_input_variables = None
        self.choosen_output_variables = None
        self.period = None


    def __repr__(self):
        return "\nSituation name: " + str(self.name_of_situation) + "\nSituation period: " + str(self.period) + "\nNumber of input variables: " + str(len(self.choosen_input_variables)) #+ "\nNumber of output variables: " + str(len(self.choosen_output_variables))


    def set_entity_choose(self, entity_choose):
        if isinstance(entity_choose, Entity):
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
            if not (re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4) or not(re.match(r'.*([01-12])', month) and (len(month) == 2 or len(month) == 1)):
                raise ValueError("No valid date selected")
            else:
                self.period = year + "-" + month
        elif year and month and day:
            if re.match(r'.*([1-3][0-9]{3})', year) and len(year) == 4 and re.match(r'.*([01-12])', month) and (len(month) == 2) and re.match(r'.*([01-31])', day) and (len(day) == 2):
                self.period_to_filter_variables = TYPEOFDEFINITIONPERIOD.month
            else:
                self.period = year + "-" + month + "-" + day
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
                if str(variable.name) == choosen_input_variable:
                    self.choosen_input_variables[choosen_input_variable] = value
                    variable_match = True
                    break
            if variable_match:
                break
        if not variable_match:
            raise TypeError("The variable you choose, is not defined for the entity or doesn't exist")


    def remove_variable_from_choosen_input_variables(self, choosen_input_variable_to_remove):
        if choosen_input_variable_to_remove is None:
            raise ValueError("You can't remove a None variable")
        if self.choosen_input_variables is None or self.choosen_input_variables == {}:
            raise ValueError("You can't remove an element from the input list if is empty")
        if choosen_input_variable_to_remove in self.choosen_input_variables:
            del self.choosen_input_variables[choosen_input_variable_to_remove]
        else:
            raise ValueError("The variable you want to remove, doesn't occur in the input variable list")


    def get_choosen_output_variables(self):
        return self.choosen_output_variables


    def add_variable_to_choosen_output_variables(self, choosen_output_variable):
        if self.choosen_output_variables is None:
            self.choosen_output_variables = []
        variable_match = False
        for entity, associated_variables in self.entity_choose.get_associated_variables().iteritems():
            for variable in associated_variables:
                if str(variable.name) == choosen_output_variable:
                    self.choosen_output_variables.append(choosen_output_variable)
                    variable_match = True
                    break
            if variable_match:
                break
        if not variable_match:
            raise TypeError("The variable you choose, is not defined for the entity or doesn't exist")


    def remove_variable_from_choosen_output_variables(self, choosen_output_variable_to_remove):
        if choosen_output_variable_to_remove is None:
            raise ValueError("You can't remove a None variable")
        if self.choosen_output_variables is None or self.choosen_output_variables == []:
            raise ValueError("You can't remove an element from the output list if is empty")
        if choosen_output_variable_to_remove in self.choosen_output_variables:
            self.choosen_output_variables.remove(choosen_output_variable_to_remove)
        else:
            raise ValueError("The variable you want to remove, doesn't occur in the output variable list")


class Simulation_generator(): #defined for Italy
    tax_benefit_system_module_class = None

    def __init__(self):
        if Simulation_generator.tax_benefit_system_module_class is None:
            raise ValueError("You must import the system before you can create simulator")
        self.situations = None #take n situations
        self.period = datetime.datetime.now().year
        self.results = None
        self.reform = None


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


    def set_reform(self, reform):
        if not isinstance(reform, Reform):
            raise TypeError("The object you passed is not a valid reform")
        elif reform is None:
            raise ValueError("A non empty reform is required")
        else:
            self.reform = reform


    def add_to_result(self, situation, name_of_variable_calculated, result):
        if self.results is None: # initialize if it is empty
            self.results = {}
        if not situation in self.results:
            self.results[situation] = {} #initialize inner dict
        self.results[situation][name_of_variable_calculated] = result


    def __repr__(self):
        return "\nNumber of situations: " + str(len(self.situations)) + "\nPeriod: " + str(self.period)


    def get_results(self):
        if not(self.results is None):
            return self.results
        else:
            raise TypeError("You must do a simulation to get the results")


    def add_situation_to_simulator(self, situation): # you can add situations with the same content
        if self.situations is None:
            self.situations = []
        if isinstance(situation, Situation):
            self.situations.append(situation)
        else:
            raise TypeError("The situation selected is not a valid situation")


    def generate_simulation(self):
        if not (self.situations == []) and not (self.situations is None):
            # import reform if it used
            if not (self.reform is None):
                module_reform_name = ""
                self.reform_class_name = "" #self because it's used in other method
                for module_adding_name, reform_class in self.reform.get_choose_reform().iteritems():
                    module_reform_name = module_adding_name
                    self.reform_class_name = reform_class
                current_reform_module = importlib.import_module(self.reform.reform_module_name + "." + module_reform_name)
                current_reform_module_class = getattr(current_reform_module,self.reform_class_name)
                print current_reform_module
                print current_reform_module_class
            # start simulation
            for situation in self.situations:
                # RICORDA CHE DEVI FARE PRATICAMETE UNA SIMULAZIONE PER OGNI PERSONA, NEL SENSO CHE INIZIALIZZI TRE VOLTE LO SCENARIO E POI RUNNI per il problema dello scenario
                scenario = self.tax_benefit_system_module_class.new_scenario()
                print type(self.tax_benefit_system_module_class)
                scenario = self.init_profile(scenario = scenario, situation_period = situation.get_period(), entity_situation = situation.get_choosen_input_variables())
                simulation = scenario.new_simulation() # nuova simulazione per lo scenario normale
                for element in situation.get_choosen_output_variables():
                    self.add_to_result(situation = situation.name_of_situation, name_of_variable_calculated = element , result = simulation.calculate(element,self.period))
                if not (self.reform is None):
                    reformed_system = current_reform_module_class(self.tax_benefit_system_module_class)
                    print type(current_reform_module_class)
                    reformed_scenario = reformed_system.new_scenario()
                    reformed_scenario = self.init_profile(scenario = reformed_scenario, situation_period = situation.get_period(), entity_situation = situation.get_choosen_input_variables())
                    reformed_simulation = reformed_scenario.new_simulation() # nuova simulazione per lo scenario normale
                    for element in situation.get_choosen_output_variables():
                        print reformed_simulation.calculate(element,self.period)
                        self.add_to_result(situation = (situation.name_of_situation + " applying " + self.reform_class_name), name_of_variable_calculated = element , result = reformed_simulation.calculate(element,self.period))
            print self.get_results()
        else:
            raise ValueError("To trigger a simulation, at least a situation it's needed")


    def generate_rst_strings_document_after_simulation(self):
        strings_RST = []
        for situation in self.situations:
            string_RST= ""
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST= string_RST + '#'
            string_RST = string_RST + str("\nSituation: " + situation.name_of_situation + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST= string_RST + '#'
            string_RST= string_RST + '\n\n'
            #input variables
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST= string_RST + '#'
            string_RST = string_RST + str("\nInput variables: \n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST= string_RST + '#'
            for k,v in situation.get_choosen_input_variables().iteritems():
                string_RST = string_RST + "\n- " + k + " with value: " + v + "\n"
            string_RST= string_RST + '\n'
            #output variables
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST + '#'
            string_RST = string_RST + str("\nOutput calculated variables: \n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST + '#'
            for out_v in situation.get_choosen_output_variables():
                results = self.results
                string_RST = string_RST + "\n- " + out_v + " with value: " + str(results[situation.name_of_situation][out_v]) +"\n"
            if not (self.reform is None):
                for out_v in situation.get_choosen_output_variables():
                    results = self.results
                    string_RST = string_RST + "\n- " + out_v + " calculated with the reform "+ self.reform_class_name + " assume: " + str(results[situation.name_of_situation + " applying " + self.reform_class_name][out_v]) +"\n"
            strings_RST.append(string_RST)
        return strings_RST



    @staticmethod
    def import_depending_on_system(tax_benefit_system_module_class):
        Simulation_generator.tax_benefit_system_module_class = tax_benefit_system_module_class()
