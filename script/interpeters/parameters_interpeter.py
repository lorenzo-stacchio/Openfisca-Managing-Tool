# -*- coding: utf-8 -*-
import os
from enum import Enum
from dateutil.parser import parse as date_parser
import datetime
import collections
GRANDEZZA_STRINGHE_INTESTAZIONE = 1000
PATH_RST_DOCUMENT = os.getcwd() + "\\messages\\rst_da_visualizzare.rst"

class ParameterType(Enum):
    non_parametro = "The file doesn't contain a valid parameter"
    normal = "The parameter is a simple parameter"
    scale = "The parameter is a scale parameter"

class NormalParameter():
    __description__ = None
    __reference__ = None
    __unit__ = None
    __dict_data_value__= None
    __parameter_name__ = None

    def __init__(self, parameter_name=None, description = None,reference = None, unit = None, dict_data_value=None):
        self.__description__ = description
        self.__reference__ = reference
        self.__dict_data_value__ = dict_data_value
        self.__unit__ = unit
        self.__parameter_name__ = parameter_name

    def __repr__(self):
        return "\nNome: " + str(self.__parameter_name__) + "\nDescrizione: " + str(self.__description__) + "\nReference: " + str(self.__reference__) + "\nUnit: " + str(self.__unit__) + "\nDict value: " + str(self.__dict_data_value__)

    def set_description(self,description):
        self.__description__ = description

    def set_parameter_name(self,parameter_name):
        self.__parameter_name__ = parameter_name

    def set_reference(self,reference):
        self.__reference__ = reference

    def set_unit(self,unit):
        self.__unit__ = unit

    def set_dict_data_value(self,dict_data_value):
        self.__dict_data_value__ = dict_data_value

    def set_element_to_dict_key(self,key,value):
        self.__dict_data_value__[key] =  value

    def generate_RST(self):
        ordined_dict = collections.OrderedDict(sorted(self.__dict_data_value__.items()))
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
            for k,v in ordined_dict.iteritems(): #key are the dates
                if k <= datetime.datetime.now().date(): # check if the value is future or not
                    rst.write("- Dal **" + k.strftime('%Y/%m/%d') + "** il parametro é valso **" + v.strip() + "**\n")
                else:
                    rst.write("- Dal **" + k.strftime('%Y/%m/%d') + "** si presume che il parametro varrà **" + v.strip() + "**\n")
            return PATH_RST_DOCUMENT #return path of written file


class ParameterInterpeter():
    __parameter_path__ = None
    __parameter_name__ = None
    __parameter_type__ = ParameterType.non_parametro
    __actual_parameter__ = None

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
        elif count_brackets_word >=1:
            self.__parameter_type__ = ParameterType.scale
        return self.__parameter_type__

    #NORMAL PARAMETER
    def __interpeter_normal_parameter__(self):
        if (self.__parameter_type__ == ParameterType.normal):
            self.__actual_parameter__ = NormalParameter()
            self.__actual_parameter__.set_dict_data_value({})
            self.__actual_parameter__.set_parameter_name(os.path.basename(self.__parameter_path__))
            with open(self.__parameter_path__,'r') as content_parameter:
                date_found = False
                date_that_was_found = ""
                for line in content_parameter.readlines():
                    line = line.strip() #elimino spazi all'inizio e alla fine
                    if '#' in line:
                        line = line[:line.find('#')]
                    pieces = line.split(': ')
                    # Caso speciale per i values and value
                    if not (pieces[0] == 'description') and not (pieces[0] == 'reference') and not (pieces[0] == 'unit'):
                        if len(pieces)==1:
                            pieces = [pieces[0].split(':')[0]] #ritorna intestazione riga
                        else:
                            pieces = [pieces[0].split(':')[0],pieces[1]] #ritorna intestazione riga + eventuale valore dopo i :
                    # date control
                    try: # cerco le date
                        if date_parser(pieces[0]):
                            #print 'data trovata', date_parser(pieces[0]).date()
                            date_found = True
                            date_that_was_found = date_parser(pieces[0]).date()
                    except:
                        pass
                        #inserisco description e reference
                    if (pieces[0] == 'description'):
                        self.__actual_parameter__.set_description(pieces[1])
                    elif (pieces[0] == 'reference'):
                        self.__actual_parameter__.set_reference(pieces[1])
                    elif (pieces[0] == 'unit'):
                        self.__actual_parameter__.set_unit(pieces[1])
                    # se ho trovato una data posso aggiungere il relativo valore
                    if date_found == True and (pieces[0] == 'value' or pieces[0] == 'expected'):
                        self.__actual_parameter__.set_element_to_dict_key(date_that_was_found,pieces[1])
                        date_found = False
        print "Stampo parametro normale ",self.__actual_parameter__

    def generate_RST_parameter(self):
        if not (self.__parameter_type__ == ParameterType.non_parametro):
            return self.__actual_parameter__.generate_RST()



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
                        else:
                            dict_date_values_threshold[date_that_was_found] = pieces[1]
                        #print " \n nel last section ", dict_date_values_threshold[date_that_was_found]
                        date_found = False
            #print '\ndizionario padre: ', dict_information
            #print 'dizionario bracket: ', dict_brackets
            #print 'dizionario rate: ', dict_rates_of_brackets
            #print '\ndizionario padre: ', dict_information
            return dict_information

    def generate_RST_scale_parameter_view(self,dict_params_information):
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
            if 'description' in dict_params_information.keys():
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nDescription:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(dict_params_information['description'] + "\n\n")
            else:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nDescription:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write("Not Specified" + "\n\n")
            # Reference is an optional field
            if 'reference' in dict_params_information.keys():
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nReference:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write(dict_params_information['reference'] + "\n\n")
            else:
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\nReference:' + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                rst.write("Not Specified" + "\n\n")
            #Brackets
            for key_brackets_father,value_dict_brackets in dict_params_information['brackets'].iteritems():
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write('\n'+ key_brackets_father + "\n")
                for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                    rst.write('*')
                rst.write("\n\n")
                ordered_value_dict_brackets = collections.OrderedDict(sorted(value_dict_brackets.items()))
                # per ogni gruppo di scaglioni, abbiamo n rate
                for key_rate_number, value_rate_threshold in ordered_value_dict_brackets.iteritems():
                    rst.write('\n'+ key_rate_number + "\n")
                    for n in range(1,GRANDEZZA_STRINGHE_INTESTAZIONE):
                        rst.write('"')
                    rst.write("\n\n")
                    ordered_value_rate_content = collections.OrderedDict(sorted(value_rate_threshold.items()))
                    # per ogni rata abbiamo valori e soglie per le quali valgono questi valori
                    for data_valore_soglia, valore_soglia in ordered_value_rate_content.iteritems():
                        # il valore soglia va splittato con _, il primo numero è il valore mentre il secondo è la soglia definita per lo stesso
                        values_threshold_splitted = valore_soglia.split('-')
                        stringa_solo_valore = stringa_valore_soglia = ""
                        if data_valore_soglia < datetime.datetime.now().date():
                            stringa_solo_valore = " è stato definito il valore di questa rata che è pari a: "
                            stringa_valore_soglia = " sono stati definiti:"
                        else:
                            stringa_solo_valore = " ci si aspetta che il valore di questa rata sarà pari a: "
                            stringa_valore_soglia = " ci si aspetta che verranno definiti:"
                        if len(values_threshold_splitted)==1:
                            to_write = str('Nel **' + str(data_valore_soglia) +'** ' + stringa_solo_valore + '**' + values_threshold_splitted[0]).strip() +'**\n\n'
                            rst.write(to_write)
                        if len(values_threshold_splitted)==2:
                            to_write = str('Nel **' + str(data_valore_soglia) + "**" + stringa_valore_soglia +'\n - Il valore di questa rata che è pari a: **' + values_threshold_splitted[0].strip() + "**;\n - La soglia da superare per fare in modo che questa rata valga che è pari a **" + values_threshold_splitted[1].strip() + "**\n\n")
                            rst.write(to_write)
            return PATH_RST_DOCUMENT #return path of written file



    def return_type(self):
        return self.__parameter_type__



# __main__
#o = ParameterInterpeter('C:\\Users\\Lorenzo Stacchio\\Desktop\\openfisca-italy\\openfisca_italy\\parameters\\imposte\\IRPEF\\Quadro_LC\\limite_acconto_unico_LC2.yaml')
#dict = o.understand_type()
#print dict_information
#o.generate_RST_normal_parameter_view(dict)
#print o.return_type()
