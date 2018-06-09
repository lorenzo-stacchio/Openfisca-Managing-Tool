# -*- coding: utf-8 -*-
import os
from enum import Enum
from dateutil.parser import parse as date_parser
import datetime
import collections

class ParameterType(Enum):
    non_parametro = "The file doesn't contain a valid parameter"
    normal = "The parameter is a simple parameter"

class ParameterInterpeter():
    __parameter_path__ = None
    __parameter_name__ = None
    __parameter_type__ = ParameterType.non_parametro

    def __init__(self,parameter_path):
        self.__parameter_path__  = parameter_path
        self.__parameter_name__ = os.path.basename(parameter_path)

    def understand_type(self):
        count_values_word = 0
        with open(self.__parameter_path__,'r') as content_parameter:
            for line in content_parameter.readlines():
                if 'values' in line: #first control
                    count_values_word = count_values_word + 1
        if count_values_word == 1:
            self.__parameter_type__ = ParameterType.normal
            dict = self.__interpeter_normal_parameter__()
            return dict


    def __interpeter_normal_parameter__(self):
        dict_information = {}
        if (self.__parameter_type__ == ParameterType.normal ):
            with open(self.__parameter_path__,'r') as content_parameter:
                date_found = False
                date_founded = ""
                for line in content_parameter.readlines():
                    line = line.strip() #elimino spazi all'inizio e alla fine
                    pieces = line.split(': ')
                    # Caso speciale per i values and value
                    if not (pieces[0] == 'description') and not (pieces[0] == 'reference'):
                        if len(pieces)==1:
                            pieces = [pieces[0].split(':')[0]] #ritorna intestazione riga
                        else:
                            pieces = [pieces[0].split(':')[0],pieces[1]] #ritorna intestazione riga + eventuale valore dopo i :
                    #print 'primo pezzo ', pieces[0]
                    #if len(pieces)>1: print 'secondo pezzo', pieces[1]
                    # date control
                    try: # cerco le date
                        #print date_parser(pieces[0])
                        if date_parser(pieces[0]):
                            #print 'data trovata'
                            date_found = True
                            date_founded = date_parser(pieces[0]).date()
                    except:
                        pass
                        #inserisco description e reference
                    if (pieces[0] == 'description') or (pieces[0] == 'reference'):
                        dict_information[pieces[0]] = pieces[1]
                    # se ho trovato una data posso aggiungere il relativo valore
                    if date_found == True and pieces[0] == 'value':
                        dict_information[date_founded] = pieces[1]
                        date_found = False
        return dict_information


    def generate_RST_normal_parameter_view(self,dict_params_information):
        print dict_params_information
        dict_values = {}
        #extracing the dates
        for k,v in dict_params_information.iteritems():
            if isinstance(k,datetime.date):
                dict_values[k] = v
        dict_values = collections.OrderedDict(sorted(dict_values.items()))
        #print collections.OrderedDict(sorted(dict_params_information.items()))
        #Describe parameters generating an RST file
        #path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\messages\\rst_da_visualizzare.txt"
        path = os.getcwd() + "\\messages\\rst_da_visualizzare.txt"
        if os.path.exists(path):
            os.remove(path)
        with open(path,'a') as rst:
            #parameter name
            for n in range(1,1000):
                rst.write('#')
            rst.write("\n" + self.__parameter_name__ + "\n")
            for n in range(1,1000):
                rst.write('#')
            rst.write("\n")
            # Description
            for n in range(1,1000):
                rst.write('*')
            rst.write('\nDescription:' + "\n")
            for n in range(1,1000):
                rst.write('*')
            rst.write("\n\n")
            rst.write(dict_params_information['description'] + "\n\n")
            # Reference is an optional field
            if 'reference' in dict_params_information.keys():
                for n in range(1,1000):
                    rst.write('*')
                rst.write('\nReference:' + "\n")
                for n in range(1,1000):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(dict_params_information['reference'] + "\n\n")
            #VALUES
            for n in range(1,1000):
                rst.write('*')
            rst.write('\nValues:' + "\n")
            for n in range(1,1000):
                rst.write('*')
            rst.write("\n")
            # writing the formatted the dates
            for k,v in dict_values.iteritems():
                rst.write("- Dal **" + k.strftime('%Y/%m/%d') + "** il parametro é valso **" + v + "**\n")
            return path #return path of written file

    def return_type(self):
        return self.__parameter_type__



# __main__
o = ParameterInterpeter('C:\\Users\\Lorenzo Stacchio\\Desktop\\openfisca-italy\\openfisca_italy\\parameters\\imposte\\IRPEF\\Quadro_LC\\limite_acconto_unico_LC2.yaml')
dict = o.understand_type()
#print dict_information
o.generate_RST_normal_parameter_view(dict)
#print o.return_type()
