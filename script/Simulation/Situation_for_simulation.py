import os
import sys
import datetime
import importlib
import re
reload(sys)
sys.setdefaultencoding('utf8')
from enum import Enum
from dateutil.parser import parse
from glob import glob
from pydoc import locate

GRANDEZZA_STRINGHE_INTESTAZIONE = 1000

# show the names in GUI
class TYPEOFVARIABLE(Enum):
    """
    Type of variable
    """
    float = "Float type"
    bool = "Bool type"
    date = "Date type"
    Enum = "Enum type" # choose or write an enum
    int = "Integer type"
    str = "String type"


class TYPEOFSETINPUT(Enum):
    """
    Type of set input
    """
    set_input_divide_by_period = "The 12 months are set equal to the 12th of the input value"
    set_input_dispatch_by_period = "The 12 months are set equal to input value"


class TYPEOFDEFINITIONPERIOD(Enum):
    """
    Type of definition period
    """
    month = "Monthly variable"
    year = "Year variable"
    eternity = "Eternal variable"


class Variable():
    """
    Variable class
    """
    def __init__(self, name = "", entity = None, type=None, set_input=None, definition_period = datetime.datetime.now().year):
        """
        Constructor of Variable
        :param name: name of variable
        :param entity: entity
        :param type: type of variable
        :param set_input: type of set_input
        :param definition_period: period of variable
        """
        self.name = name
        self.entity = entity
        self.type = type
        self.definition_period = definition_period
        self.value = None
        self.set_input  = set_input


    def __repr__(self):
        """
        Representation of variable
        :return: string of variable
        """
        return "\n\nName: " + self.name + "\nType: " + self.type + "\nEntity: " + self.entity + "\nDefinition period: " + self.definition_period


    def set_value(self,value):
        """
        Change variable value
        :param value: new value
        """
        self.value = value


class Entity():
    """
    Class Entity
    """
    tax_benefit_system_module_class = None
    entity_module_all_entities = None

    def __init__(self, entity = None):
        """
        Constructor of Entity
        :param entity: ....
        """
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
        """
        ?????????????
        :param tax_benefit_system_module_class:
        :param entity_module_class:
        :param entity_module_all_entities:
        :return:
        """
        Entity.tax_benefit_system_module_class = tax_benefit_system_module_class()
        Entity.entity_module_all_entities = getattr(entity_module_class,entity_module_all_entities)

    def generate_associated_variable_filter(self, year = None, month = None, day = None):
        """
        Generate associated variable filter
        :param year: year of variable
        :param month: month of variable
        :param day: day of variable
        """
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
        """
        Generate all associated variable
        """
        # validates
        self.associated_variables = []
        for key_variable, variables_content in self.tax_benefit_system_module_class.get_variables(entity = self.entity).iteritems():
            self.associated_variables.append(Variable(name = key_variable,type = variables_content.value_type.__name__, entity = variables_content.entity.__name__, definition_period = variables_content.definition_period))


    def get_associated_variables(self):
        """
        Generate associated variable
        :return: dict with {entity_name: associated_variables}
        """
        try:
            return {self.entity_name: self.associated_variables}
        except AttributeError:
            print "You have to generate the variables before getting their"


class Reform():
    """
    Class Reform
    """
    tax_benefit_system_module_class = None
    reform_module = None


    def __init__(self):
        """
        Constructor of Reform class
        """
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
            key = key.replace("/", ".") # used to create a correct module path
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
        """
        Get all reform
        :return: list of all reform
        """
        list = []
        if self.reforms_file_dict == None:
            raise ValueError("You must init the reform!")
        for k,v in self.reforms_file_dict.iteritems():
            for reform in v:
                list.append(reform)
        return list


    def set_choose_reform(self, reform_name):
        """
        Set the choosen reform
        :param reform_name: new reform name
        """
        for k,v in self.reforms_file_dict.iteritems():
            if reform_name in v:
                self.choose_reform = {k : reform_name}
        if self.choose_reform is None:
            raise ValueError("You insert an invalid reform")


    def get_choose_reform(self):
        """
        Get the choosen reform
        :return: choosen reform
        """
        if self.choose_reform is None:
            raise TypeError("You have to set the reform to get it")
        else:
            return self.choose_reform


    @staticmethod
    def import_depending_on_system(tax_benefit_system_module_class, reform_module):
        """
        ??????????
        :param tax_benefit_system_module_class:
        :param reform_module:
        :return:
        """
        Reform.tax_benefit_system_module_class = tax_benefit_system_module_class()
        Reform.reform_module = reform_module


class Situation(): # defined for one entity
    """
    Class Situation (one for entity)
    """
    def __init__(self, name_of_situation = "situazione_prova"):
        """
        Construction of Situation
        :param name_of_situation: name of situation
        """
        self.name_of_situation = name_of_situation
        self.choosen_input_variables = None
        self.choosen_output_variables = None
        self.period = None


    def __repr__(self):
        """
        String of situation
        :return:
        """
        return "\nSituation name: " + str(self.name_of_situation) + "\nSituation period: " + str(self.period) + "\nNumber of input variables: " + str(len(self.choosen_input_variables)) #+ "\nNumber of output variables: " + str(len(self.choosen_output_variables))


    def set_entity_choose(self, entity_choose):
        """
        Set choosen entity
        :param entity_choose: new entity
        """
        if isinstance(entity_choose, Entity):
                self.entity_choose = entity_choose
        else:
            raise TypeError("The object used is not an entity")

    def set_period(self,year = None, month = None, day = None):
        """
        Set period of situation
        :param year: year of situation
        :param month: month of situation
        :param day: day of situation
        """
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
        """
        Get period of situation
        :return: period
        """
        return self.period


    def get_choosen_input_variables(self):
        """
        Get choosen input variables
        :return: input variables
        """
        return self.choosen_input_variables


    def add_variable_to_choosen_input_variables(self, choosen_input_variable, value):
        """
        Add an input variable into a situation
        :param choosen_input_variable: new input variable
        :param value: value of variable
        """
        if self.choosen_input_variables is None:
            self.choosen_input_variables = {}
        variable_match = False
        for entity, associated_variables in self.entity_choose.get_associated_variables().iteritems():
            for variable in associated_variables:
                if str(variable.name) == choosen_input_variable:
                    if self.check_value_is_right_type(openfisca_system_variable=variable, value = value):
                        self.choosen_input_variables[choosen_input_variable] = value
                        variable_match = True
                    break
            if variable_match:
                break
        if not variable_match:
            raise TypeError("The variable you choose, is not defined for the entity or doesn't exist")



    def check_value_is_right_type(self, openfisca_system_variable ,value):
        """
        Check value of openfisca system variable
        :param openfisca_system_variable: variable
        :param value: value
        :return: true if is correct else false
        """
        for type_var in TYPEOFVARIABLE:
            print "openfisca tipo", openfisca_system_variable.type
            print "tipo variabile corrente", type_var.name
            print "Valore ", value
            print "tipo variabile corrente locate", locate(type_var.name)
            t = locate(type_var.name)

            # special case date
            if type_var.name == 'date' and self.is_date(value) and openfisca_system_variable.type == 'date':
                return True

            # special case int e float
            if not t is None:
                if ((t.__name__ == "float") or (t.__name__ == "int")):
                    if self.is_number(value):
                        if t(value) and t.__name__ == openfisca_system_variable.type:
                            return True
                else:
                    if t(value) and t.__name__ == openfisca_system_variable.type:
                        return True
        # if we are here the value is not valid
        raise TypeError("The value is not valid for the variable type")

    def is_date(self, string):
        """
        Check if is a date
        :param string: date string
        :return:
        """
        try:
            parse(string)
            return True
        except ValueError:
            return False

    def is_number(self, s):
        """
        Check if is a number
        :param s: string
        :return: true if is a number else false
        """
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False


    def remove_variable_from_choosen_input_variables(self, choosen_input_variable_to_remove):
        """
        Remove a variable from choosen input variables
        :param choosen_input_variable_to_remove: input vaiable to remove
        """
        if choosen_input_variable_to_remove is None:
            raise ValueError("You can't remove a None variable")
        if self.choosen_input_variables is None or self.choosen_input_variables == {}:
            raise ValueError("You can't remove an element from the input list if is empty")
        if choosen_input_variable_to_remove in self.choosen_input_variables:
            del self.choosen_input_variables[choosen_input_variable_to_remove]
        else:
            raise ValueError("The variable you want to remove, doesn't occur in the input variable list")


    def get_choosen_output_variables(self):
        """
        Get choosen output variables
        :return: choosen output variables
        """
        return self.choosen_output_variables


    def add_variable_to_choosen_output_variables(self, choosen_output_variable):
        """
        Add an output variable into a situation
        :param choosen_output_variable: new output variable
        """
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
        """
        Remove a variable from choosen output variables
        :param choosen_output_variable_to_remove: output variable to remove
        """
        if choosen_output_variable_to_remove is None:
            raise ValueError("You can't remove a None variable")
        if self.choosen_output_variables is None or self.choosen_output_variables == []:
            raise ValueError("You can't remove an element from the output list if is empty")
        if choosen_output_variable_to_remove in self.choosen_output_variables:
            self.choosen_output_variables.remove(choosen_output_variable_to_remove)
        else:
            raise ValueError("The variable you want to remove, doesn't occur in the output variable list")


class Simulation_generator(): #defined for Italy
    """
    Simulation generator Class
    """
    tax_benefit_system_module_class = None

    def __init__(self):
        """
        Construction of Simulation Generator
        """
        if Simulation_generator.tax_benefit_system_module_class is None:
            raise ValueError("You must import the system before you can create simulator")
        self.situations = None #take n situations
        self.period = datetime.datetime.now().year
        self.results = None
        self.reform = None


    def init_profile(self, scenario, situation_period, entity_situation):
        """
        Inizialize profile of simulation generator
        :param scenario: input scenario
        :param situation_period: input situation period
        :param entity_situation: entity situation
        :return: scenario
        """
        scenario.init_single_entity(
            period = situation_period,
            parent1 = entity_situation
        )
        return scenario


    def set_period(self,year = None, month = None, day = None):
        """
        Set period simulation generator
        :param year: new year
        :param month: new month
        :param day: new day
        """
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
        """
        Set reform
        :param reform: new reform
        """
        if not isinstance(reform, Reform):
            raise TypeError("The object you passed is not a valid reform")
        elif reform is None:
            raise ValueError("A non empty reform is required")
        else:
            self.reform = reform


    def add_to_result(self, situation, name_of_variable_calculated, result):
        """
        ??????
        :param situation:
        :param name_of_variable_calculated:
        :param result:
        :return:
        """
        if self.results is None: # initialize if it is empty
            self.results = {}
        if not situation in self.results:
            self.results[situation] = {} #initialize inner dict
        self.results[situation][name_of_variable_calculated] = result


    def __repr__(self):
        """
        Representation of situation generator
        :return: string of summary situations
        """
        return "\nNumber of situations: " + str(len(self.situations)) + "\nPeriod: " + str(self.period)


    def get_results(self):
        """
        Get results of situation
        :return: results
        """
        if not(self.results is None):
            return self.results
        else:
            raise TypeError("You must do a simulation to get the results")


    def add_situation_to_simulator(self, situation): # you can add situations with the same content
        """
        Add situation to simulator
        :param situation: situation to insert
        """
        if self.situations is None:
            self.situations = []
        if isinstance(situation, Situation):
            self.situations.append(situation)
        else:
            raise TypeError("The situation selected is not a valid situation")


    def generate_simulation(self):
        """
        Generate simulation
        """
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
        """
        Generate rst after simulation
        :return: rst string
        """
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
        """
        Import class of tax benefit system
        :param tax_benefit_system_module_class: input class
        """
        Simulation_generator.tax_benefit_system_module_class = tax_benefit_system_module_class()
