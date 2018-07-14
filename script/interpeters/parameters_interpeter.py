# -*- coding: utf-8 -*-
import os
from enum import Enum
from dateutil.parser import parse as date_parser
import datetime
import collections
import yaml
from script.interpeters.variables_file_interpeter import *
from script.interpeters.reforms_file_interpeter import *

# FONDAMENTALE, COSI PRENDI TUTTI I PARAMETRI ESISTENTI

GRANDEZZA_STRINGHE_INTESTAZIONE = 1000
PATH_RST_DOCUMENT = os.getcwd() + "/config_files/rst_file/rst_da_visualizzare.rst"

class ParameterType(Enum):
    """
    Type parameter enum
    """
    non_parametro = "The file doesn't contain a valid parameter"
    normal = "The parameter is a simple parameter"
    scale = "The parameter is a scale parameter"
    fancy_indexing = "The parameter is a fancy indexing parameter"

class NormalParameter():
    """
    Normal parameter class
    """
    __description__ = None
    __reference__ = None
    __unit__ = None
    __dict_data_value__= None
    __parameter_name__ = None

    def __init__(self, parameter_name=None, description = None, reference = None, unit = None, dict_data_value=None):
        """
        Costruction of normal parameter class
        :param parameter_name: name of normal parameter
        :param description: description of normal parameter
        :param reference: reference of normal parameter
        :param unit: unit of normal parameter
        :param dict_data_value: dict data value of normal parameter
        """
        self.__description__ = description
        self.__reference__ = reference
        self.__dict_data_value__ = dict_data_value
        self.__unit__ = unit
        self.__parameter_name__ = parameter_name

    def __repr__(self):
        """
        Representation of normal parameters
        :return: string of normal parameters
        """
        return "\nName: " + str(self.__parameter_name__) + "\nDescription: " + str(self.__description__) + "\nReference: " + str(self.__reference__) + "\nUnit: " + str(self.__unit__) + "\nDict value: " + str(self.__dict_data_value__)

    def set_description(self,description):
        """
        Set description normal parameter
        :param description: new description
        """
        self.__description__ = description

    def set_parameter_name(self,parameter_name):
        """
        Set normal parameter name
        :param parameter_name: new name
        """
        self.__parameter_name__ = parameter_name

    def set_reference(self,reference):
        """
        Set reference name
        :param reference: new reference
        """
        self.__reference__ = reference

    def set_unit(self,unit):
        """
        Set unit
        :param unit: new unit
        """
        self.__unit__ = unit

    def set_dict_data_value(self,dict_data_value):
        """
        Set dict data value
        :param dict_data_value: new dict data value
        """
        self.__dict_data_value__ = dict_data_value

    def set_element_to_dict_key(self,key,value):
        """
        Set element of dict data value
        :param key: input key
        :param value: new value
        """
        self.__dict_data_value__[key] =  value

    def string_RST(self):
        """
        Stringify in a RST document
        :return: string RST
        """
        string_RST = ""
        #parameter name
        for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
            string_RST = string_RST + ('#')
        string_RST = string_RST +("\nParameter: " + self.__parameter_name__ + "\n")
        for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
            string_RST = string_RST + ('#')
        string_RST = string_RST +("\n")
        # Description
        if self.__description__:
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +('\nDescription:' + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +("\n\n")
            string_RST = string_RST +(self.__description__ + "\n\n")
        else:
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +('\nDescription:' + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +("\n\n")
            string_RST = string_RST +("Not Specified" + "\n\n")
        # Reference is an optional field
        if self.__reference__:
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +('\nReference:' + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +("\n\n")
            string_RST = string_RST +(self.__reference__ + "\n\n")
        else:
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +('\nReference:' + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +("\n\n")
            string_RST = string_RST +("Not Specified" + "\n\n")
        # Reference is an optional field
        if self.__unit__:
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +('\nUnit:' + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +("\n\n")
            string_RST = string_RST +(self.__unit__ + "\n\n")
        else:
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +('\nUnit:' + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                string_RST = string_RST +('*')
            string_RST = string_RST +("\n\n")
            string_RST = string_RST +("Not Specified" + "\n\n")
        #VALUES
        for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
            string_RST = string_RST +('*')
        string_RST = string_RST +('\nValues:' + "\n")
        for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
            string_RST = string_RST +('*')
        string_RST = string_RST +("\n")
        # writing the formatted the dates
        for date,value_dict in self.__dict_data_value__.iteritems(): #key are the dates
            true_value = value_dict['value'] #is ever one element
            if date <= datetime.datetime.now().date(): # check if the value is future or not
                string_RST = string_RST +("- Dal **" + date.strftime('%Y/%m/%d') + "** il parametro é valso **" + str(true_value) + "**\n")
            else:
                string_RST = string_RST +("- Dal **" + date.strftime('%Y/%m/%d') + "** si presume che il parametro varrà **" + str(true_value) + "**\n")
        return string_RST


    def generate_RST(self):
        """
        Generate RST document
        :return: path rst document
        """
        if os.path.exists(PATH_RST_DOCUMENT):
            os.remove(PATH_RST_DOCUMENT)
        with open(PATH_RST_DOCUMENT,'a') as rst:
            #parameter name
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\nParameter: " + self.__parameter_name__ + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\n")
            # Description
            if self.__description__:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nDescription:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(self.__description__ + "\n\n")
            else:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nDescription:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write("Not Specified" + "\n\n")
            # Reference is an optional field
            if self.__reference__:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nReference:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(self.__reference__ + "\n\n")
            else:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nReference:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write("Not Specified" + "\n\n")
            # Reference is an optional field
            if self.__unit__:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nUnit:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(self.__unit__ + "\n\n")
            else:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nUnit:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write("Not Specified" + "\n\n")
            #VALUES
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('*')
            rst.write('\nValues:' + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('*')
            rst.write("\n")
            # writing the formatted the dates
            for date,value_dict in self.__dict_data_value__.iteritems(): #key are the dates
                true_value = value_dict['value'] #is ever one element
                date_to_compare = datetime.datetime(year=date_parser(date).date().year, month=date_parser(date).date().month, day=date_parser(date).date().day)
                if date_to_compare.date() <= datetime.datetime.now().date(): # check if the value is future or not
                    rst.write("- Dal **" + date_to_compare.date().strftime('%Y/%m/%d') + "** il parametro é valso **" + str(true_value) + "**\n")
                else:
                    rst.write("- Dal **" + date_to_compare.date().strftime('%Y/%m/%d') + "** si presume che il parametro varrà **" + str(true_value) + "**\n")
            return PATH_RST_DOCUMENT #return path of written file


class ScaleParameter():
    """
    Scale parameter class
    """
    __description__ = None
    __reference__ = None
    __brackets__ = None #dict
    __parameter_name__ = None

    def __init__(self, parameter_name=None,reference=None, description = None, brackets=None):
        """
        Constructor of Scale parameter
        :param parameter_name: name of scale parameter
        :param reference: reference of scale parameter
        :param description: description of scale parameter
        :param brackets: brackets of scale parameter
        """
        self.__description__ = description
        self.__reference__ = reference
        self.__brackets__ = brackets
        self.__parameter_name__ = parameter_name

    def __repr__(self):
        """
        Representation of Scale Parameter
        :return: string of scale parameter
        """
        return "\nName: " + str(self.__parameter_name__) + "\nDescription: " + str(self.__description__) + "\nReference: " + str(self.__reference__) + "\nBrackets: " + str(self.__brackets__)

    def set_description(self,description):
        """
        Set scale parameter description
        :param description: new description
        """
        self.__description__ = description

    def set_parameter_name(self,parameter_name):
        """
        Set scale parameter name
        :param parameter_name: new name
        """
        self.__parameter_name__ = parameter_name

    def set_reference(self,reference):
        """
        Set scale parameter reference
        :param reference: new reference
        """
        self.__reference__ = reference

    def set_brackets(self,brackets):
        """
        Set scale parameter brackets
        :param brackets: new brackets
        """
        self.__brackets__ = brackets

    def generate_RST(self):
        """
        Generate RST document
        :return: rst string
        """
        if os.path.exists(PATH_RST_DOCUMENT):
            os.remove(PATH_RST_DOCUMENT)
        with open(PATH_RST_DOCUMENT,'a') as rst:
            #parameter name
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\nParameter: " + self.__parameter_name__ + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\n")
            # Description
            if self.__description__:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nDescription:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(self.__description__ + "\n\n")
            else:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nDescription:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write("Not Specified" + "\n\n")
            # Reference is an optional field
            if self.__reference__:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nReference:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(self.__reference__ + "\n\n")
            else:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nReference:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write("Not Specified" + "\n\n")
            #Brackets
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('*')
            rst.write('\nBrackets:' + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('*')
            rst.write("\n\n")
            # Rates
            count_rate_for_view = 0
            formatted_dict = {}
            for element in self.__brackets__:
                count_rate_for_view = count_rate_for_view + 1
                formatted_dict[count_rate_for_view] = {}
                for key_name, dict_date in element.iteritems(): #inizialize
                    for date, value in dict_date.iteritems():
                        formatted_dict[count_rate_for_view][date] = {}
                for key_name, dict_date in element.iteritems(): #inizialize
                    if key_name == 'rate':
                        for date, value in dict_date.iteritems():
                            formatted_dict[count_rate_for_view][date]['rate'] = value['value']
                    elif key_name == 'threshold':
                        for date, value in dict_date.iteritems():
                            formatted_dict[count_rate_for_view][date]['threshold'] = value['value']
                # sort the values
                formatted_dict[count_rate_for_view] = collections.OrderedDict(sorted(formatted_dict[count_rate_for_view].items()))
            formatted_dict = collections.OrderedDict(sorted(formatted_dict.items()))
            #Dict formatted!
            for number_group_rates, date_dict in formatted_dict.iteritems():
                rst.write('\n\nBracket group'+ str(number_group_rates) + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('"')
                rst.write("\n\n")
                for date, values in date_dict.iteritems():
                    date_to_compare = datetime.datetime(year=date_parser(date).date().year,
                                                        month=date_parser(date).date().month,
                                                        day=date_parser(date).date().day)
                    # 1 value
                    if len(values)==1 and date_to_compare.date() < datetime.datetime.now().date():
                        if 'threshold' in values:
                            to_write = str('In **' + str(date) +'** it was defined the threshold for this rate as: **' + str(values['threshold']).strip()).strip() +'**\n\n'
                        else:
                            to_write = str('In **' + str(date) +'** it was defined the value for this rate as: **' + str(values['rate']).strip()).strip() +'**\n\n'
                        rst.write(to_write)
                    if len(values)==1 and date_to_compare.date() >= datetime.datetime.now().date():
                        if 'threshold' in values:
                            to_write = str('In **' + str(date) +'** it will be defined the threshold for this rate as: **' + str(values['threshold']).strip()).strip() +'**\n\n'
                        else:
                            to_write = str('In **' + str(date) +'** it will be defined the value for this rate as: **' + str(values['rate']).strip()).strip() +'**\n\n'
                        rst.write(to_write)
                    # 2 values
                    if len(values)==2 and date_to_compare.date() < datetime.datetime.now().date():
                        if 'threshold' in values:
                            to_write = str('In **' + str(date) +'** were defined both: \n - The threshold for this rate: **' + str(values['threshold']).strip() + '**; \n - The value for this rate: **'+ str(values['rate']).strip()).strip() +'**\n\n'
                        rst.write(to_write)
                    if len(values)==2 and date_to_compare.date() >= datetime.datetime.now().date():
                        if 'threshold' in values:
                            to_write = str('In **' + str(date) +'** will be defined both: \n - The threshold for this rate: **' + str(values['threshold']).strip() + ' **; \n - The value for this rate: **'+ str(values['rate']).strip()).strip() +'**\n\n'
                        rst.write(to_write)
            return PATH_RST_DOCUMENT


class FancyIndexingParamater():
    """
    Fancy indexing parameter class
    """
    __parameter_name__ = None
    __code_dict__ = None # contain key and normal parameter associated

    def __init__(self,parameter_name=None,values=None,code_dict= None):
        """
        Construction of fancy index parameter
        :param parameter_name: fancy index parameter name
        :param values: fancy index parameter values
        :param code_dict: fancy index parameter code dict
        """
        self.__parameter_name__  = parameter_name
        self.__code_dict__ = code_dict

    def set_code_dict(self,code_dict):
        """
        Set fancy index parameter dict
        :param code_dict: new code dict
        """
        self.__code_dict__ = code_dict

    def __repr__(self):
        """
        Representation of fancy index parameter
        :return:
        """
        return "\n\nParameter name: " + str(self.__parameter_name__) + "\nCode dict" + str(self.__code_dict__)

    def generate_RST(self):
        """
        Generate RST document
        :return: rst string
        """
        if os.path.exists(PATH_RST_DOCUMENT):
            os.remove(PATH_RST_DOCUMENT)
        with open(PATH_RST_DOCUMENT,'a') as rst:
            #parameter name
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\nParameter: " + self.__parameter_name__ + "\n")
            for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                rst.write('#')
            rst.write("\n")
            rst.write('\nIn this parameter it will be described the value of the various homogeneous parameters depending on the value of an external variable.\n\n')
            for key_lv1, value_lv1 in self.__code_dict__.iteritems():
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('#')
                rst.write("\nVariable_value: " + key_lv1 + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('#')
                for key_lv2, value_lv2 in value_lv1.iteritems():
                    rst.write("\n\n" + value_lv2.string_RST() + "\n")
        return PATH_RST_DOCUMENT


class ParameterInterpeter():
    """
    Parameter interpreter class
    """
    __actual_parameter__ = None

    def __init__(self,parameter_path):
        """
        Construction of Parameter interpreter
        :param parameter_path: path parameter
        """
        self.__parameter_path__  = parameter_path
        self.__parameter_name__ = os.path.basename(parameter_path)
        self.__parameter_type__ = ParameterType.non_parametro
        self.__yaml_file__ = yaml.load(file(parameter_path))


    def understand_type(self):
        """
        Unterstand type of parameter
        :return: parameter type
        """
        count_values_word = 0
        count_brackets_word = 0
        # first check
        for key_lv_1, value_lv_1 in self.__yaml_file__.iteritems():
            if key_lv_1 == 'values':
                count_values_word = count_values_word + 1
            elif key_lv_1 == 'brackets':
                count_brackets_word = count_brackets_word +1
        if count_values_word == 1: #simple parameter
            self.__parameter_type__ = ParameterType.normal
        elif count_brackets_word >=1: #bracket parameter
            self.__parameter_type__ = ParameterType.scale
        elif (self.__parameter_type__ == ParameterType.non_parametro) : # could be a fancy indexing
            key_value_dict = {}
            base_case_fancy = []
            for key_lv_1, value_lv_1 in self.__yaml_file__.iteritems():
                key_value_dict[key_lv_1] = []
                if base_case_fancy == []:
                    for key_lv_2, value_lv_2 in value_lv_1.iteritems():
                        key_value_dict[key_lv_1].append(key_lv_2)
                        base_case_fancy.append(key_lv_2)
                else:
                    for key_lv_2, value_lv_2 in value_lv_1.iteritems():
                        key_value_dict[key_lv_1].append(key_lv_2)
            valid_fancy_indexing = True
            for key, value in  key_value_dict.iteritems(): #check if it is a correct fancy indexing
                if not all(elem in base_case_fancy  for elem in value):
                    valid_fancy_indexing = False
            if valid_fancy_indexing: self.__parameter_type__ = ParameterType.fancy_indexing
        return self.__parameter_type__


    #NORMAL PARAMETER
    def __interpeter_normal_parameter__(self):
        """
        Interpreter of normal parameter
        """
        if (self.__parameter_type__ == ParameterType.normal):
            self.__actual_parameter__ = NormalParameter()
            self.__actual_parameter__.set_dict_data_value(self.__yaml_file__['values'])
            self.__actual_parameter__.set_parameter_name(os.path.basename(self.__parameter_path__))
            if 'description' in self.__yaml_file__:
                self.__actual_parameter__.set_description(self.__yaml_file__['description'].encode('utf-8').strip())
            if 'reference' in self.__yaml_file__:
                self.__actual_parameter__.set_reference(self.__yaml_file__['reference'].encode('utf-8').strip())
            if 'unit' in self.__yaml_file__:
                self.__actual_parameter__.set_unit(self.__yaml_file__['unit'].encode('utf-8').strip())


    #SCALE PARAMETER
    def __interpeter_scale_parameter__(self):
        """
        Interpreter of scale parameter
        """
        if (self.__parameter_type__ == ParameterType.scale):
            self.__actual_parameter__ = ScaleParameter()
            self.__actual_parameter__.set_brackets(self.__yaml_file__['brackets'])
            self.__actual_parameter__.set_parameter_name(os.path.basename(self.__parameter_path__))
            if 'description' in self.__yaml_file__:
                self.__actual_parameter__.set_description(self.__yaml_file__['description'].encode('utf-8').strip())
            if 'reference' in self.__yaml_file__:
                self.__actual_parameter__.set_reference(self.__yaml_file__['reference'].encode('utf-8').strip())
            if 'unit' in self.__yaml_file__:
                self.__actual_parameter__.set_unit(self.__yaml_file__['unit'].encode('utf-8').strip())


    def __interpeter_normal_parameter_for_fancy_indexing__(self, normal_yaml_parameter = None, parameter_name = None):
        """
        Interpreter of normal parameter for fancy indexing
        :param normal_yaml_parameter: normal yaml parameter
        :param parameter_name: parameter name
        :return: normal parameter
        """
        if normal_yaml_parameter:
            actual_normal = NormalParameter()
            actual_normal.set_dict_data_value(normal_yaml_parameter['values'])
            actual_normal.set_parameter_name(parameter_name)
            if 'description' in normal_yaml_parameter:
                actual_normal.set_description(normal_yaml_parameter['description'].encode('utf-8').strip())
            if 'reference' in normal_yaml_parameter:
                actual_normal.set_reference(normal_yaml_parameter['reference'].encode('utf-8').strip())
            if 'unit' in normal_yaml_parameter:
                actual_normal.set_unit(normal_yaml_parameter['unit'].encode('utf-8').strip())
            return actual_normal


    def __interpeter_fancy_indexing_parameter__(self):
        """
        Interpreter fancy indexing parameter
        """
        if (self.__parameter_type__ == ParameterType.fancy_indexing):
            self.__actual_parameter__ = FancyIndexingParamater(parameter_name = self.__parameter_name__)
            formatted_dict = {}
            # the fancy indexing is formed by many normal parameters
            for key_lv1, value_lv1 in self.__yaml_file__.iteritems():
                actual_inner_dict = {}
                for key_lv2, value_lv2 in value_lv1.iteritems():
                    actual_normal_parameter = self.__interpeter_normal_parameter_for_fancy_indexing__(normal_yaml_parameter = value_lv2, parameter_name = key_lv2)
                    actual_inner_dict[key_lv2] = actual_normal_parameter
                formatted_dict[key_lv1] = actual_inner_dict
            self.__actual_parameter__.set_code_dict(formatted_dict)


    def generate_RST_parameter(self):
        """
        Generate RST parameter
        :return: actual parameter rst document
        """
        if not (self.__parameter_type__ == ParameterType.non_parametro):
            return self.__actual_parameter__.generate_RST()


    def return_type(self):
        """
        Get parameter type
        :return: parameter type
        """
        return self.__parameter_type__