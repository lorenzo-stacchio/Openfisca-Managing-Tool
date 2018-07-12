import os
import sys
import inspect
import datetime
import time
import importlib
import json
import site
from glob import glob
import re
from enum import Enum
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) # get father directory
from script.interpeters import parameters_interpeter


class Parameter_reform_manager():

    def __init__(self, system_parameter_path = None):
        if system_parameter_path is None:
            raise ValueError("You must insert the path in which parameters files are based")
        self.system_parameter_path = system_parameter_path
        self.actual_parameters = None
        self.dict_path_parameter_name = None
        # list all parameters
        self.dict_normal_parameters = {}
        self.dict_scale_parameters = {}
        self.dict_fancy_indexing_parameters = {}
        self.fill_dict_type_parameters()

    def set_type_of_parameter_to_reform(self, type_of_parameter_to_reform):
        self.type_of_parameter_to_reform = type_of_parameter_to_reform


    def set_system_parameter_path(self, system_parameter_path):
        self.system_parameter_path = system_parameter_path


    def fill_dict_type_parameters(self):
        if self.system_parameter_path is None:
            raise ValueError("You have to set the path in which parameters files are based")

        if self.dict_path_parameter_name is None:
            self.dict_path_parameter_name = {}
        # get all the parameters file
        result = [y for x in os.walk(self.system_parameter_path) for y in glob(os.path.join(x[0], '*.yaml'))]
        for path_parameter in result:
            filename, ext = os.path.splitext(os.path.basename(path_parameter))
            self.dict_path_parameter_name[os.path.basename(filename)] = path_parameter

        if self.dict_path_parameter_name == {}:
            raise TypeError("The path doesn't contain a valid parameter")

        # start filling
        parameter_interpeter = None
        for parameter_name, parameter_path in self.dict_path_parameter_name.iteritems():
            parameter_interpeter = parameters_interpeter.ParameterInterpeter(parameter_path = parameter_path)
            parameter_interpeter.understand_type()
            # if normal parameter
            if parameter_interpeter.__parameter_type__ is parameters_interpeter.ParameterType.normal:
                parameter_interpeter.__interpeter_normal_parameter__()
                self.dict_normal_parameters[parameter_name] =  parameter_interpeter.__actual_parameter__
            # if scale parameter
            elif parameter_interpeter.__parameter_type__ is parameters_interpeter.ParameterType.scale:
                parameter_interpeter.__interpeter_scale_parameter__()
                self.dict_scale_parameters[parameter_name] =  parameter_interpeter.__actual_parameter__
            # if fancy indexing parameter
            elif parameter_interpeter.__parameter_type__ is parameters_interpeter.ParameterType.fancy_indexing:
                    parameter_interpeter.__interpeter_fancy_indexing_parameter__()
                    self.dict_fancy_indexing_parameters[parameter_name] =  parameter_interpeter.__actual_parameter__


    def get_parameters_of_the_choosen_type(self, type_of_parameter):
        if self.system_parameter_path is None:
            raise ValueError("You have to set the path in which parameters files are based")

        if self.dict_path_parameter_name is None:
            raise ValueError("You have to fill the parameter name dict before getting the parameters")

        if not isinstance(type_of_parameter, parameters_interpeter.ParameterType):
            raise TypeError("The parameter type you choose, doesn't exist")

        if type_of_parameter is parameters_interpeter.ParameterType.normal:
            return self.dict_normal_parameters
        elif type_of_parameter is parameters_interpeter.ParameterType.scale:
            return self.dict_scale_parameters
        elif type_of_parameter is parameters_interpeter.ParameterType.fancy_indexing:
            return self.dict_fancy_indexing_parameters



