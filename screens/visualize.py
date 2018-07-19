# -*- coding: utf-8 -*-
import kivy
import json
import os
import sys
import datetime
from functools import partial
kivy.require("1.10.0")
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.image import Image as kivyImage
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.utils import get_color_from_hex
from kivy.graphics import Rectangle, Color
from kivy.uix.progressbar import ProgressBar
from kivy.config import Config
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from kivy.uix.textinput import TextInput
from script.get_parameters_reforms_tests_variables_folder_paths import *
from script.interpeters.variables_file_interpeter import *
from script.interpeters.parameters_interpeter import *
from script.interpeters.reforms_file_interpeter import *
from script.download_openfisca_system import download_and_install as download_and_install_openfisca
from script.download_openfisca_system import check_package_is_installed
from script.download_openfisca_system import install_country_package
from script.Simulation.Situation_for_simulation import *
from script.reforms_maker.reform_variables import *
from folder_screen_widgets.personalized_widget import *
import common_modules

class VisualizeSystemScreen(Screen):

    def __init__(self, **kwargs):
        super(VisualizeSystemScreen, self).__init__(**kwargs)

    def ricevi_inizializza_path(self,*args):
        path = self.manager.get_screen('init').PATH_OPENFISCA
        self.dict_path = get_all_paths(path)
        self.PATH_OPENFISCA = self.dict_path['inner_system_folder']
        with open('./config_files/config_import.json') as f:
            data_config = json.load(f)
        Variable_File_Interpeter.import_depending_on_system(tax_benefit_system_module_class = common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS) #static method
        Reform_File_Interpeter.import_depending_on_system(tax_benefit_system_module_class = common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS) #static method
        # entity of situation for simulator
        Entity.import_depending_on_system(tax_benefit_system_module_class = common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS, entity_module_class = common_modules.ENTITY_MODULE_CLASS,entity_module_all_entities = common_modules.ENTITY_MODULE_CLASS_ALL_ENTITIES)
        if not(common_modules.REFORM_MODULE is None):
            Reform.import_depending_on_system(tax_benefit_system_module_class = common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS, reform_module = common_modules.REFORM_MODULE)
        Simulation_generator.import_depending_on_system(tax_benefit_system_module_class = common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS)
        Variable_To_Reform.import_depending_on_system(tax_benefit_system_module_class = common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS, system_entity_module = common_modules.ENTITY_MODULE_CLASS, system_all_entities_name = common_modules.ENTITY_MODULE_CLASS_ALL_ENTITIES)

        os.chdir(os.getcwd())
        # personalize rst rendere colors
        property_dict_viewer = {"paragraph":"202020ff", "link": "33AAFFff", "background": "ffffffff", "bullet" : "000000ff", "title": "971640ff"}
        dict_viewer_set = [self.ids.document_variables_viewer, self.ids.document_parameters_viewer, self.ids.document_reforms_viewer]
        for viewer in dict_viewer_set:
            for key_property,value_property in property_dict_viewer.iteritems():
                viewer.colors[key_property] = value_property
        viewer.underline_color = "971640ff"

    def show_variables(self):
        self.ids.visualize_file_chooser_variables.path = self.dict_path['variables']
        self.ids.current_path_variables.text = self.ids.visualize_file_chooser_variables.path
        self.do_layout()

    def show_parameters(self):
        self.ids.visualize_file_chooser_parameters.path = self.dict_path['parameters']
        self.ids.current_path_parameters.text = self.ids.visualize_file_chooser_parameters.path
        self.do_layout()

    def show_reforms(self):
        self.ids.visualize_file_chooser_reforms.path = self.dict_path['reforms']
        self.ids.current_path_reforms.text = self.ids.visualize_file_chooser_reforms.path
        self.do_layout();

    def file_allowed(self, directory, filename):
        filename, file_extension = os.path.splitext(filename)
        return ((file_extension in ['.py', '.yaml'] and not (os.path.basename(filename) == '__init__')) or (
            os.path.isdir(os.path.join(directory, filename))))


    def __check_path__(self, path_file_scelto):
        path_file_scelto = str(os.path.normpath(path_file_scelto))
        path_variable = str(os.path.normpath(self.dict_path['variables']))
        path_reforms = str(os.path.normpath(self.dict_path['reforms']))
        path_parameter = str(os.path.normpath(self.dict_path['parameters']))
        if (path_variable in path_file_scelto) or (path_parameter in path_file_scelto) or (
                path_reforms in path_file_scelto):
            return True
        else:
            self.ids.visualize_file_chooser_variables.path = self.dict_path['variables']
            self.ids.visualize_file_chooser_parameters.path = self.dict_path['parameters']
            self.ids.visualize_file_chooser_reforms.path = self.dict_path['reforms']
            self.ids.document_variables_viewer.source = "config_files/rst_file/file_not_allowed.rst"
            self.ids.document_parameters_viewer.source = "config_files/rst_file/file_not_allowed.rst"
            self.ids.document_reforms_viewer.source = "config_files/rst_file/file_not_allowed.rst"
            return False


    def selected_file(self, *args):
        # clear document viewer
        self.ids.document_variables_viewer.source = ""
        self.ids.document_parameters_viewer.source = ""
        self.ids.document_reforms_viewer.source = ""
        try:
            path_file_scelto = args[1][0]
            if self.__check_path__(path_file_scelto):
                filename, file_extension = os.path.splitext(path_file_scelto)
                path_rst = path_file_scelto # default
                # the file could be a parameter or a variable
                if file_extension == '.yaml':
                    parameter_interpeter = ParameterInterpeter(path_file_scelto)
                    if (parameter_interpeter.understand_type() == ParameterType.normal):
                        parameter_interpeter.__interpeter_normal_parameter__()
                        path_rst = parameter_interpeter.generate_RST_parameter()
                    elif (parameter_interpeter.understand_type() == ParameterType.scale):
                        parameter_interpeter.__interpeter_scale_parameter__()
                        path_rst = parameter_interpeter.generate_RST_parameter()
                    elif (parameter_interpeter.understand_type() == ParameterType.fancy_indexing):
                        parameter_interpeter.__interpeter_fancy_indexing_parameter__()
                        path_rst = parameter_interpeter.generate_RST_parameter()
                    self.ids.document_variables_viewer.source = path_rst
                    self.ids.document_parameters_viewer.source = path_rst
                    self.ids.document_reforms_viewer.source = path_rst
                elif file_extension == '.py':
                    variable_interpeter = Variable_File_Interpeter(path_file_scelto)
                    reform_interpeter = Reform_File_Interpeter(path_file_scelto)
                    if (variable_interpeter.file_is_a_variable() and not (reform_interpeter.file_is_a_reform())):
                        variable_interpeter.start_interpetration()
                        path_rst = variable_interpeter.generate_RSTs_variables()
                    elif (reform_interpeter.file_is_a_reform()):
                        reform_interpeter.start_interpetration_reforms()
                        path_rst = reform_interpeter.generate_RST_reforms()
                    self.ids.document_variables_viewer.source = path_rst
                    self.ids.document_parameters_viewer.source = path_rst
                    self.ids.document_reforms_viewer.source = path_rst
                else: # file for which the interpretation is not defined yet
                    self.ids.document_variables_viewer.source = path_file_scelto
                    self.ids.document_parameters_viewer.source = path_file_scelto
                    self.ids.document_reforms_viewer.source = path_file_scelto
                # update current path
                self.ids.current_path_variables.text = self.ids.visualize_file_chooser_variables.path
                self.ids.current_path_parameters.text = self.ids.visualize_file_chooser_parameters.path
                self.ids.current_path_reforms.text = self.ids.visualize_file_chooser_reforms.path
        except Exception as e:
            self.popup_error_run_simulation = ErrorPopUp()
            self.popup_error_run_simulation.ids.label_error.text = str(e)
            self.popup_error_run_simulation.open()

    def go_to_home(self):
        if self.manager.current == 'visualize_system':
            self.manager.current = 'home'
