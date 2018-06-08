import os
from enum import Enum
from dateutil.parser import parse as date_parser

class ParameterType(Enum):
    non_parametro = "The file doesn't contain a valid parameter"
    normal = "The parameter is a simple parameter"

class ParameterInterpeter():
    __parameter_path__ = None
    __parameter_type__ = ParameterType.non_parametro

    def __init__(self,parameter_path):
        self.__parameter_path__  = parameter_path


    def understand_type(self):
        count_values_word = 0
        with open(self.__parameter_path__,'r') as content_parameter:
            for line in content_parameter.readlines():
                if 'values' in line: #first control
                    count_values_word = count_values_word + 1
        if count_values_word == 1:
            self.__parameter_type__ = ParameterType.normal
            self.interpeter_normal_parameter()


    def interpeter_normal_parameter(self):
        dict_information = {}
        if (self.__parameter_type__ == ParameterType.normal ):
            with open(self.__parameter_path__,'r') as content_parameter:
                date_found = False
                date_founded = ""
                for line in content_parameter.readlines():
                    pieces = line.split(': ')
                    print 'primo pezzo ', pieces[0]
                    #print 'secondo pezzo ', pieces[1]
                    if ('description' in pieces) or ('reference' in pieces):
                        dict_information[pieces[0]] = pieces[1]
                    elif date_parser(pieces[0]):
                        date_found = True
                        date_founded = pieces[0]
                    elif date_found == True and pieces[0] == 'value':
                        dict_information[date_founded] = pieces[1]
        print dict_information

    def return_type(self):
        return self.__parameter_type__



# __main__
o = ParameterInterpeter('C:\\Users\\Lorenzo Stacchio\\Desktop\\openfisca-italy\\openfisca_italy\\parameters\\imposte\\IRPEF\\Quadro_LC\\limite_acconto_unico_LC2.yaml')
o.understand_type()
print o.return_type()
