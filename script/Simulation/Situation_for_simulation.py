import json
import imp


class Variable_for_simulation():
    __name__= None
    __entity__ = None
    __value__ = None

    def __init__(self, name = "", entity = None, value = None):
        self.__name__ = name
        self.__entity__ = entity
        self.__value__ = value

    def __repr__(self):
        print "\nName: " + self.__name__ + "\nEntity: " + self.__entity__ + "\nValue: " + self.__value__


class Entity():
    __name__= None
    __associated_variables__ = None

    def __init__(self, name = "" , associated_variables = []):
        self.__name__ = name
        self.__associated_variables__ = associated_variables

    def __repr__(self):
        print "\nName: " + self.__name__ + "\nNumber of variables: " + len(self.__associated_variables__)

    def set_associated_variables(self,associated_variables):
        self.__associated_variables__ = associated_variables


class Situation():
    __entities_with_variables__ = None
    __period__ = None

    def __init__(self,name = "" , entities_with_variables = [], period=None):
        self.__period__ = period
        self.__entities_with_variables__ = entities_with_variables

    def __repr__(self):
        print "\nName: " + self.__period__ + "\nNumber of variables: " + len(self.__entities_with_variables__)


class Simulation_generator():
    __path_to_openfisca_country__ = None

    def __init__(self, name = "" , path_to_openfisca_country = None):
        self.__path_to_openfisca_country__ = path_to_openfisca_country

    def generate_simulation(self):
        scenarios = imp.load_source('scenarios', self.__path_to_openfisca_country__)
        scenario = scenarios.Scenario()
        print type(scenario)


#MAIN
persona1 = Simulation_generator(path_to_openfisca_country = "C:\Users\Lorenzo Stacchio\Desktop\openfisca-italy\openfisca_italy" )
persona1.generate_simulation()
