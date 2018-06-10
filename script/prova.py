# -*- coding: utf-8 -*-
import os
from enum import Enum
from dateutil.parser import parse as date_parser
import datetime
import collections

class ParameterType(Enum):
    non_parametro = "The file doesn't contain a valid parameter"
    normal = "The parameter is a simple parameter"
    scale = "The parameter is a scale parameter"

class ParameterInterpeter():
    __parameter_path__ = None
    __parameter_name__ = None
    __parameter_type__ = ParameterType.non_parametro

    def __init__(self,parameter_path):
        self.__parameter_path__  = parameter_path
        self.__parameter_name__ = os.path.basename(parameter_path)

    def understand_type(self):
        count_values_word = 0
        count_brackets_word = 0
        with open(self.__parameter_path__,'r') as content_parameter:
            for line in content_parameter.readlines():
                if 'values' in line: #first control
                    count_values_word = count_values_word + 1
                elif 'brackets' in line: #first control
                    count_brackets_word = count_brackets_word + 1
        if count_values_word == 1:
            self.__parameter_type__ = ParameterType.normal
            dict = self.__interpeter_normal_parameter__()
            return dict
        elif count_brackets_word >=1:
            self.__parameter_type__ = ParameterType.scale
            self.__interpeter_scale_parameter__()

    #NORMAL PARAMETER
    def __interpeter_normal_parameter__(self):
        dict_information = {}
        if (self.__parameter_type__ == ParameterType.normal ):
            with open(self.__parameter_path__,'r') as content_parameter:
                date_found = False
                date_that_was_found = ""
                for line in content_parameter.readlines():
                    line = line.strip() #elimino spazi all'inizio e alla fine
                    #print line
                    pieces = line.split(': ')
                    # Caso speciale per i values and value
                    if not (pieces[0] == 'description') and not (pieces[0] == 'reference') and not (pieces[0] == 'unit'):
                        if len(pieces)==1:
                            pieces = [pieces[0].split(':')[0]] #ritorna intestazione riga
                        else:
                            pieces = [pieces[0].split(':')[0],pieces[1]] #ritorna intestazione riga + eventuale valore dopo i :
                    #print 'primo pezzo ', pieces[0]
                    #if len(pieces)>1: print 'secondo pezzo', pieces[1]
                    # date control
                    try: # cerco le date
                        if date_parser(pieces[0]):
                            #print 'data trovata', date_parser(pieces[0]).date()
                            date_found = True
                            date_that_was_found = date_parser(pieces[0]).date()
                    except:
                        pass
                        #inserisco description e reference
                    if (pieces[0] == 'description') or (pieces[0] == 'reference') or (pieces[0] == 'unit'):
                        dict_information[pieces[0]] = pieces[1]
                    # se ho trovato una data posso aggiungere il relativo valore
                    if date_found == True and (pieces[0] == 'value' or pieces[0] == 'expected'):
                        dict_information[date_that_was_found] = pieces[1]
                        date_found = False
        return dict_information


    def generate_RST_normal_parameter_view(self,dict_params_information):
        #print dict_params_information
        dict_values = {}
        #extracing the dates
        for k,v in dict_params_information.iteritems():
            if isinstance(k,datetime.date):
                dict_values[k] = v
        dict_values = collections.OrderedDict(sorted(dict_values.items()))
        #print collections.OrderedDict(sorted(dict_params_information.items()))
        #Describe parameters generating an RST file
        #path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\messages\\rst_da_visualizzare.txt"
        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\messages\\rst_da_visualizzare.txt"
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
            if 'description' in dict_params_information.keys():
                for n in range(1,1000):
                    rst.write('*')
                rst.write('\nDescription:' + "\n")
                for n in range(1,1000):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(dict_params_information['description'] + "\n\n")
            else:
                for n in range(1,1000):
                    rst.write('*')
                rst.write('\nDescription:' + "\n")
                for n in range(1,1000):
                    rst.write('*')
                rst.write("\n\n")
                rst.write("Not Specified" + "\n\n")
            # Reference is an optional field
            if 'reference' in dict_params_information.keys():
                for n in range(1,1000):
                    rst.write('*')
                rst.write('\nReference:' + "\n")
                for n in range(1,1000):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(dict_params_information['reference'] + "\n\n")
            else:
                for n in range(1,1000):
                    rst.write('*')
                rst.write('\nReference:' + "\n")
                for n in range(1,1000):
                    rst.write('*')
                rst.write("\n\n")
                rst.write("Not Specified" + "\n\n")
            # Reference is an optional field
            if 'unit' in dict_params_information.keys():
                for n in range(1,1000):
                    rst.write('*')
                rst.write('\nUnit:' + "\n")
                for n in range(1,1000):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(dict_params_information['unit'] + "\n\n")
            else:
                for n in range(1,1000):
                    rst.write('*')
                rst.write('\nUnit:' + "\n")
                for n in range(1,1000):
                    rst.write('*')
                rst.write("\n\n")
                rst.write("Not Specified" + "\n\n")
            #VALUES
            for n in range(1,1000):
                rst.write('*')
            rst.write('\nValues:' + "\n")
            for n in range(1,1000):
                rst.write('*')
            rst.write("\n")
            # writing the formatted the dates
            for k,v in dict_values.iteritems(): #key are the dates
                if k <= datetime.datetime.now().date(): # check if the value is future or not
                    rst.write("- Dal **" + k.strftime('%Y/%m/%d') + "** il parametro é valso **" + v + "**\n")
                else:
                    rst.write("- Dal **" + k.strftime('%Y/%m/%d') + "** si presume che il parametro varrà **" + v + "**\n")
            return path #return path of written file

    #SCALE PARAMETER
    def __interpeter_scale_parameter__(self):
        dict_information = {}
        dict_brackets = {}
        dict_rates_of_brackets = {}
        dict_date_values_threshold = {} # questo elemento non verrà utilizzato alla fine, serve come riempimento
        if (self.__parameter_type__ == ParameterType.scale):
            with open(self.__parameter_path__,'r') as content_parameter:
                date_found = False
                date_that_was_found = ""
                brackets_found = False
                number_brackets_found = 0
                rate_found = False
                number_rate_found = 0
                threshold_found = False
                for line in content_parameter.readlines():
                    line = line.strip() #elimino spazi all'inizio e alla fine
                    #print "Linea attuale", line
                    pieces = line.split(': ')
                    # Caso speciale per i rate,brackets and value
                    if not (pieces[0] == 'description') and not (pieces[0] == 'reference'):
                        if len(pieces)==1:
                            pieces = [pieces[0].split(':')[0]] #ritorna intestazione riga
                        else:
                            pieces = [pieces[0].split(':')[0],pieces[1]] #ritorna intestazione riga + eventuale valore dopo i :
                    #print "Stampo pieces",pieces
                    # define thing found
                    if pieces[0] == 'brackets':
                        # if we are in second cicle
                        rate_found = False
                        number_rate_found = 0
                        dict_rates_of_brackets = {}
                        #bracket init
                        brackets_found = True
                        number_brackets_found = number_brackets_found + 1
                        dict_brackets['brackets'+ str(number_brackets_found)] = "" #si inizializzer quando trovo una rata
                        # primo brackets
                        if number_brackets_found == 1:
                            dict_information['brackets'] = dict_brackets #inserisco il bind tra i dict
                    if pieces[0] == '- rate':
                        rate_found = True
                        # clear dates and threshold
                        dict_date_values_threshold = {}
                        date_found = False
                        date_that_was_found = ""
                        threshold_found = False
                        #logic
                        #print '\nrata trovata', rate_found
                        number_rate_found = number_rate_found + 1
                        #print '\nnumero rate trovata', number_rate_found
                        dict_rates_of_brackets ['rate'+str(number_rate_found)] = ""
                        if number_rate_found == 1: # first rate of a bracket
                            dict_brackets['brackets'+ str(number_brackets_found)] = dict_rates_of_brackets
                    # special case threshold
                    if pieces[0] == 'threshold':
                        threshold_found = True
                    # date control
                    try: # cerco le date
                        if date_parser(pieces[0]):
                            #print 'data trovata', date_parser(pieces[0]).date()
                            date_found = True
                            date_that_was_found = date_parser(pieces[0]).date()
                            if not date_that_was_found in dict_date_values_threshold.keys():
                                dict_date_values_threshold[date_that_was_found] = ''
                            if dict_rates_of_brackets['rate'+str(number_rate_found)] == "": #is empty
                                #print "\nsono qui\n"
                                dict_rates_of_brackets['rate'+str(number_rate_found)] = dict_date_values_threshold
                        #print " \n nel date parser ", dict_date_values_threshold
                    except:
                        pass
                    #inserisco description e reference
                    if (pieces[0] == 'description') or (pieces[0] == 'reference'):
                        dict_information[pieces[0]] = pieces[1]
                    # se ho trovato una data posso aggiungere il relativo valore
                    if date_found and rate_found and brackets_found and (pieces[0] == 'value'):
                        if threshold_found:
                            dict_date_values_threshold[date_that_was_found] = dict_date_values_threshold[date_that_was_found] + " - " + pieces[1]
                            print "dopo", dict_date_values_threshold[date_that_was_found]
                        else:
                            dict_date_values_threshold[date_that_was_found] = pieces[1]
                        #print " \n nel last section ", dict_date_values_threshold[date_that_was_found]
                        date_found = False
            print '\ndizionario padre: ', dict_information
            #print 'dizionario bracket: ', dict_brackets
            #print 'dizionario rate: ', dict_rates_of_brackets
            return dict_information

    def return_type(self):
        return self.__parameter_type__



# __main__
o = ParameterInterpeter('C:\\Users\\Lorenzo Stacchio\\Desktop\\openfisca-italy\\openfisca_italy\\parameters\\benefici\\boh.yaml')
dict = o.understand_type()
#print dict_information
#o.generate_RST_normal_parameter_view(dict)
#print o.return_type()
