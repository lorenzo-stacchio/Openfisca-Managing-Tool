
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


class MakeSimulation(Screen):
    """
    Make Simulation screen, where I insert input variables for the simulation
    """
    variable_added = ObjectProperty()
    dict_of_entity_variable_value = {}
    previous_text_typed = ""

    def __init__(self, **kwargs):
        super(MakeSimulation, self).__init__(**kwargs)


    def inizializza_make_simulation(self):
        """
        Inizialize make simulation
        """
        #Resize max height of dropdown
        self.ids.menu_a_tendina_entita.dropdown_cls.max_height = self.ids.menu_a_tendina_entita.height*30
        self.ids.menu_a_tendina_variabili.dropdown_cls.max_height = self.ids.menu_a_tendina_variabili.height*30

        self.situations = {}
        try:
            for k, v in self.manager.get_screen('choose_entity').number_of_entity.items():
                for entity in self.manager.get_screen('choose_entity').type_of_entity:
                    if entity.key == k:
                        for index in xrange(1, int(v) + 1):
                            real_entity = Entity(entity = entity)
                            period =  str(self.manager.get_screen('choose_entity').period).split("-")
                            if len(period) == 1:
                                real_entity.generate_associated_variable_filter(year = period[0])
                            elif len(period) == 2:
                                real_entity.generate_associated_variable_filter(year = period[0],month = period[1])
                            elif len(period) == 3:
                                real_entity.generate_associated_variable_filter(year = period[0],month = period[1],day = period[2])
                            for name_ent, variables in real_entity.get_associated_variables().iteritems():
                                string_name_list = []
                                for variable in variables:
                                    string_name_list.append(variable.name)
                                string_name_list.sort()
                            common_modules.dict_entita[k + str(index)] = string_name_list
                            # CREATE SITUATIONS
                            app_situation = Situation(name_of_situation = str(k + str(index)))
                            app_situation.set_entity_choose(real_entity)
                            if len(period) == 1:
                                app_situation.set_period(year = period[0])
                            elif len(period) == 2:
                                app_situation.set_period(year = period[0],month = period[1])
                            elif len(period) == 3:
                                app_situation.set_period(year = period[0],month = period[1],day = period[2])
                            self.situations[str(k + str(index))] = app_situation
            self.ids.menu_a_tendina_entita.values = common_modules.dict_entita.keys()
            self.ids.menu_a_tendina_entita.text = self.ids.menu_a_tendina_entita.values[0]
            self.ids.menu_a_tendina_variabili.values = common_modules.dict_entita[self.ids.menu_a_tendina_entita.text]
            self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
            self.ids.information.text = ""
            with open("messages/instruction_make_simulation_input.txt", 'r') as f:
                for line in f.readlines():
                    self.ids.information.text = self.ids.information.text + line
        except Exception as e:
            self.popup_error_run_simulation = ErrorPopUp()
            self.popup_error_run_simulation.ids.label_error.text = str(e)
            self.popup_error_run_simulation.open()

    def change_spinner(self):
        """
        Action when I change value of spinner
        """
        variables_name = []
        if self.ids.id_search_box_input_variable != "":
            valori = common_modules.dict_entita[self.ids.menu_a_tendina_entita.text]
            for key_variable in valori:
                if (self.ids.id_search_box_input_variable.text.lower() in key_variable.lower()):
                    variables_name.append(key_variable)
        elif self.previous_text_typed.lower() in self.ids.id_search_box_input_variable.text.lower():
            for key_variable in self.ids.menu_a_tendina_variabili.values:
                if (self.previous_text_typed.lower() not in key_variable.lower()):
                    variables_name.remove(key_variable)
        else:
            valori = common_modules.dict_entita[self.ids.menu_a_tendina_entita.text]
            for key_variable in valori:
                if ((key_variable.lower() not in variables_name.lower()) and self.previous_text_typed.lower() in key_variable.lower()):
                    variables_name.append(key_variable)

        variables_name.sort()
        self.ids.menu_a_tendina_variabili.values = variables_name
        if self.ids.menu_a_tendina_variabili.values:
            self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
        else:
            self.ids.menu_a_tendina_variabili.text = ""


    def update_form(self):
        """
        Update form
        """
        self.ids.menu_a_tendina_variabili.values = common_modules.dict_entita[self.ids.menu_a_tendina_entita.text]
        self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
        self.ids.variable_added.clear_widgets()
        if self.ids.menu_a_tendina_entita.text in self.dict_of_entity_variable_value.keys():
            for tuple in self.dict_of_entity_variable_value[self.ids.menu_a_tendina_entita.text]:
                self.ids.variable_added.add_widget(
                    Button( text=self.ids.menu_a_tendina_entita.text + " - " + tuple[0] + " - " + tuple[1],
                            font_size='12sp',
                            on_release=self.destroy_button,
                            background_color=(255, 255, 255, 0.9),
                            color=(0, 0, 0, 1)
                ))







    def go_to_home(self):
        """
        Go to home
        """
        if self.manager.current == 'make_simulation':
            self.ids.variable_added.clear_widgets()
            self.manager.get_screen("choose_entity").entity_box_layout.clear_widgets();
            self.ids.menu_a_tendina_variabili.text = ''
            self.ids.input_value_variable.text = ''
            self.manager.current = 'home'


    def go_to_output_variables(self):
        """
        Go to output variables screen
        """
        if self.manager.current == 'make_simulation':
            if len(self.dict_of_entity_variable_value) ==  len(self.ids.menu_a_tendina_entita.values):
                self.manager.transition = kivy.uix.screenmanager.SlideTransition(direction='left')
                self.manager.transition.duration = .6
                self.manager.get_screen('output_variable').inizializza_output_variable()
                self.manager.current = 'output_variable'
                self.manager.transition = kivy.uix.screenmanager.TransitionBase()
                self.manager.transition.duration = .4
            else:
                error_popup = ErrorPopUp()
                error_popup.ids.label_error.text = "Insert at least a variable for each entity"
                error_popup.open()


    def exist_tuple(self, dictionary, input_entity, input_variable):
        """
        Check if a tuple exist
        :param dictionary: input dictionary
        :param input_entity: input entity to find
        :param input_variable: input variable to find
        :return: true if exist else false
        """
        if not input_entity in dictionary.keys():
            return False
        elif dictionary[input_entity] == []:
            return False
        else:
            for tuple in dictionary[input_entity]:
                if tuple[0] == input_variable:
                    return True
        return False


    def add_value_and_reset_form(self):
        """
        Add a new variable and reset the form
        """
        for key in self.dict_of_entity_variable_value.keys():
            for tuple in self.dict_of_entity_variable_value[key]:
                if tuple[0] == self.ids.input_value_variable.text and tuple[1] == self.ids.input_value_variable.text:
                    return

        if self.ids.menu_a_tendina_variabili.text != '' and self.ids.input_value_variable.text != '':
            if not self.exist_tuple(self.dict_of_entity_variable_value, self.ids.menu_a_tendina_entita.text,
                                    self.ids.menu_a_tendina_variabili.text):
                try:
                    self.situations[self.ids.menu_a_tendina_entita.text ].add_variable_to_choosen_input_variables(choosen_input_variable = self.ids.menu_a_tendina_variabili.text, value = self.ids.input_value_variable.text)
                    self.ids.variable_added.add_widget(Button(
                        text=self.ids.menu_a_tendina_entita.text + " - " + self.ids.menu_a_tendina_variabili.text + " - " + self.ids.input_value_variable.text,
                        on_release=self.destroy_button,
                        font_size='14sp',
                        background_color=(255, 255, 255, 0.9),
                        color=(0, 0, 0, 1)))
                    if not self.ids.menu_a_tendina_entita.text in self.dict_of_entity_variable_value.keys():
                        self.dict_of_entity_variable_value[self.ids.menu_a_tendina_entita.text] = []
                    tuple = [self.ids.menu_a_tendina_variabili.text, self.ids.input_value_variable.text]
                    self.dict_of_entity_variable_value[self.ids.menu_a_tendina_entita.text].append(tuple)
                except Exception as e:
                    self.popup_error_run_simulation = ErrorPopUp()
                    self.popup_error_run_simulation.ids.label_error.text = str(e)
                    self.popup_error_run_simulation.open()


            else:
                i = 0
                try:
                    self.situations[self.ids.menu_a_tendina_entita.text].add_variable_to_choosen_input_variables(choosen_input_variable = self.ids.menu_a_tendina_variabili.text, value = self.ids.input_value_variable.text)
                    for el in self.ids.variable_added.children:
                        entity, variable, value = el.text.split(' - ')
                        if (self.ids.menu_a_tendina_entita.text + " - " + self.ids.menu_a_tendina_variabili.text) == (
                                entity + " - " + variable):
                            self.ids.variable_added.children[i].text = entity + " - " + variable + " - " + \
                            self.ids.input_value_variable.text
                            break
                        i += 1

                    for tuple in self.dict_of_entity_variable_value[self.ids.menu_a_tendina_entita.text]:
                        if self.ids.menu_a_tendina_variabili.text in tuple:
                            tuple[1] = self.ids.input_value_variable.text
                            break
                except Exception as e:
                    self.popup_error_run_simulation = ErrorPopUp()
                    self.popup_error_run_simulation.ids.label_error.text = str(e)
                    self.popup_error_run_simulation.open()

            self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
            self.ids.input_value_variable.text = ""
            self.ids.id_search_box_input_variable.text = ""
        else:
            error_popup = ErrorPopUp()
            error_popup.ids.label_error.text = "You can't insert an empty variable and/or value"
            error_popup.open()


    def destroy_button(self, button):
        """
        Destroy button when I click it
        :param button: button clicked
        """
        entity, variable, value = button.text.split(" - ")
        for tuple in self.dict_of_entity_variable_value[entity]:
            if tuple[0] == variable and tuple[1] == value:
                self.dict_of_entity_variable_value[entity].remove(tuple)
                break
        self.variable_added.remove_widget(button)
        try:
            self.situations[entity].remove_variable_from_choosen_input_variables(choosen_input_variable_to_remove = variable)
        except Exception as e:
            self.popup_error_run_simulation = ErrorPopUp()
            self.popup_error_run_simulation.ids.label_error.text = str(e)
            self.popup_error_run_simulation.open()
