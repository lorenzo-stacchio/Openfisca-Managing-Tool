
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

class ExecuteSimulationScreen(Screen):

    def __init__(self, **kwargs):
        super(ExecuteSimulationScreen, self).__init__(**kwargs)

    def run_simulation(self,reform=None):
        # situations
        situations =  self.manager.get_screen('make_simulation').situations
        period =  str(self.manager.get_screen('choose_entity').period).split("-")
        simulation_generator = Simulation_generator()
        if len(period) == 1:
            simulation_generator.set_period(year = period[0])
        elif len(period) == 2:
            simulation_generator.set_period(year = period[0],month = period[1])
        elif len(period) == 3:
            simulation_generator.set_period(year = period[0],month = period[1],day = period[2])
        # get notes to visualize results
        for key_name, value_situation in situations.iteritems():
            simulation_generator.add_situation_to_simulator(value_situation)


        if reform != None:
            simulation_generator.set_reform(reform)
        # compute
        simulation_generator.generate_simulation()
        property_dict_viewer = {"paragraph": "202020ff", "link": "33AAFFff", "background": "ffffffff",
                                "bullet": "000000ff", "title": "971640ff"}
        for type,color_type in property_dict_viewer.items():
            self.ids.document_results_simulation_viewer.colors[type] = color_type

        # visualize results
        self.string_rst_documents = simulation_generator.generate_rst_strings_document_after_simulation()
        self.current_index = 0
        self.ids.document_results_simulation_viewer.text = self.string_rst_documents[self.current_index]



    def next_rst_result(self):
        if self.current_index < (len(self.string_rst_documents)-1):
            self.current_index = self.current_index + 1
        self.ids.document_results_simulation_viewer.text = self.string_rst_documents[self.current_index]


    def previous_rst_result(self):
        if self.current_index > 0:
            self.current_index = self.current_index -1
        self.ids.document_results_simulation_viewer.text = self.string_rst_documents[self.current_index]

    def go_to_home(self):
        if self.manager.current == "execute_simulation":
            self.manager.get_screen("choose_entity").entity_box_layout.clear_widgets()
            self.manager.get_screen('output_variable').ids.variable_added_output.clear_widgets()
            self.manager.get_screen('make_simulation').ids.variable_added.clear_widgets()
            #common_modules.dict_entita = {}
            self.manager.current = "home"
