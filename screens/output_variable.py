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

class OutputVariableScreen(Screen):
    string_var_input = ""
    string_var_output = ""
    variable_added_output = ObjectProperty()
    dict_of_entity_variable_value_output = {}
    previous_text_typed = ""

    def __init__(self, **kwargs):
        super(OutputVariableScreen, self).__init__(**kwargs)

    def inizializza_output_variable(self):
        # Resize max height of dropdown
        self.ids.menu_a_tendina_entita_output.dropdown_cls.max_height = self.ids.menu_a_tendina_entita_output.height * 30
        self.ids.menu_a_tendina_variabili_output.dropdown_cls.max_height = self.ids.menu_a_tendina_variabili_output.height * 30

        self.ids.menu_a_tendina_entita_output.values = common_modules.dict_entita.keys()
        self.ids.menu_a_tendina_entita_output.text = self.ids.menu_a_tendina_entita_output.values[0]

        self.ids.menu_a_tendina_variabili_output.values = common_modules.dict_entita[
            self.ids.menu_a_tendina_entita_output.text]
        self.ids.menu_a_tendina_variabili_output.text = self.ids.menu_a_tendina_variabili_output.values[0]
        self.ids.information_output.text = ""
        with open("messages\\instruction_make_simulation_output.txt", 'r') as f:
            for line in f.readlines():
                self.ids.information_output.text = self.ids.information_output.text + line

    def change_spinner(self):
        variables_name = []
        if self.ids.id_search_box_input_variable != "":
            #TOFIX
            valori = common_modules.dict_entita[self.ids.menu_a_tendina_entita_output.text]
            for key_variable in valori:
                if (self.ids.id_search_box_input_variable.text.lower() in key_variable.lower()):
                    variables_name.append(key_variable)
        # Se la vecchia stringa è contenuta nella nuova significa che ho aggiunto una lettera
        # Quindi devo eliminare ciò che contiene non contiene la nuova stringa
        elif self.previous_text_typed.lower() in self.ids.id_search_box_input_variable.text.lower():
            for key_variable in self.ids.menu_a_tendina_variabili_output.values:
                if (self.previous_text_typed.lower() not in key_variable.lower()):
                    variables_name.remove(key_variable)
        # Se la vecchia stringa non è contenuta nella nuova significa che ho ELIMINATO una lettera
        # Quindi devo aggiungere degli oggetti alla lista dato che filtro meno valori
        else:
            valori = common_modules.dict_entita[self.ids.menu_a_tendina_entita_output.text]
            for key_variable in valori:
                if ((key_variable.lower() not in variables_name.lower()) and self.previous_text_typed.lower() in key_variable.lower()):
                    variables_name.append(key_variable)

        # Ordina alfabeticamente
        variables_name.sort()
        self.ids.menu_a_tendina_variabili_output.values = variables_name
        if self.ids.menu_a_tendina_variabili_output.values:
            self.ids.menu_a_tendina_variabili_output.text = self.ids.menu_a_tendina_variabili_output.values[0]
        else:
            self.ids.menu_a_tendina_variabili_output.text = ""

    def go_to_home(self):
        if self.manager.current == 'output_variable':
            self.ids.variable_added_output.clear_widgets()
            self.ids.menu_a_tendina_variabili_output.text = ''
            self.manager.get_screen("choose_entity").entity_box_layout.clear_widgets();
            self.manager.get_screen('make_simulation').ids.variable_added.clear_widgets()
            self.manager.get_screen('make_simulation').ids.menu_a_tendina_variabili.text = ''
            self.manager.get_screen('make_simulation').ids.input_value_variable.text = ''
            self.manager.current = 'home'

    def update_form(self):
        self.ids.menu_a_tendina_variabili_output.values = common_modules.dict_entita[
            self.ids.menu_a_tendina_entita_output.text]
        self.ids.menu_a_tendina_variabili_output.text = self.ids.menu_a_tendina_variabili_output.values[0]
        self.ids.variable_added_output.clear_widgets()
        if self.ids.menu_a_tendina_entita_output.text in self.dict_of_entity_variable_value_output.keys():
            for tuple in self.dict_of_entity_variable_value_output[
                self.ids.menu_a_tendina_entita_output.text]:
                self.ids.variable_added_output.add_widget(
                    Button(text=self.ids.menu_a_tendina_entita_output.text + " - " + tuple[0],
                           font_size='14sp',
                           on_release=self.destroy_button, background_color=(255, 255, 255, 0.9), color=(0, 0, 0, 1)))

    def exist_tuple(self, dictionary, input_entity, input_variable):
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
        if self.ids.menu_a_tendina_variabili_output.text != '':
            if not self.exist_tuple(self.dict_of_entity_variable_value_output, self.ids.menu_a_tendina_entita_output.text,
                                    self.ids.menu_a_tendina_variabili_output.text):
                self.ids.variable_added_output.add_widget(Button(
                    text=self.ids.menu_a_tendina_entita_output.text + " - " + self.ids.menu_a_tendina_variabili_output.text,
                    on_release=self.destroy_button, background_color=(255, 255, 255, 0.9), color=(0, 0, 0, 1)))
                try:
                    self.manager.get_screen('make_simulation').situations[self.ids.menu_a_tendina_entita_output.text].add_variable_to_choosen_output_variables(choosen_output_variable = self.ids.menu_a_tendina_variabili_output.text)
                except Exception as e:
                    self.popup_error_run_simulation = ErrorPopUp()
                    self.popup_error_run_simulation.ids.label_error.text = str(e)
                    self.popup_error_run_simulation.open()

                if not self.ids.menu_a_tendina_entita_output.text in self.dict_of_entity_variable_value_output.keys():
                    self.dict_of_entity_variable_value_output[self.ids.menu_a_tendina_entita_output.text] = []

                tuple = [self.ids.menu_a_tendina_variabili_output.text, ""]
                self.dict_of_entity_variable_value_output[self.ids.menu_a_tendina_entita_output.text].append(tuple)

            else:
                i = 0
                try:
                    self.manager.get_screen('make_simulation').situations[self.ids.menu_a_tendina_entita_output.text].add_variable_to_choosen_output_variables(choosen_output_variable = self.ids.menu_a_tendina_variabili_output.text)
                except Exception as e:
                    self.popup_error_run_simulation = ErrorPopUp()
                    self.popup_error_run_simulation.ids.label_error.text = str(e)
                    self.popup_error_run_simulation.open()

                for el in self.ids.variable_added_output.children:
                    entity, variable = el.text.split(' - ')
                    if (self.ids.menu_a_tendina_entita_output.text + " - " + self.ids.menu_a_tendina_variabili_output.text) == (
                            entity + " - " + variable):
                        self.ids.variable_added_output.children[i].text = entity + " - " + variable
                        break
                    i += 1

            self.ids.menu_a_tendina_variabili_output.text = self.ids.menu_a_tendina_variabili_output.values[0]
            self.ids.id_search_box_input_variable.text = ""
        else:
            error_popup = ErrorPopUp()
            error_popup.ids.label_error.text = "You can't insert an empty variable"
            error_popup.open()

    def destroy_button(self, button):
        entity, variable = button.text.split(" - ")
        for tuple in self.dict_of_entity_variable_value_output[entity]:
            if tuple[0] == variable:
                self.dict_of_entity_variable_value_output[entity].remove(tuple)
                break
        self.variable_added_output.remove_widget(button)
        try:
            self.manager.get_screen('make_simulation').situations[entity].remove_variable_from_choosen_output_variables(choosen_output_variable_to_remove = variable)
        except Exception as e:
            self.popup_error_run_simulation = ErrorPopUp()
            self.popup_error_run_simulation.ids.label_error.text = str(e)
            self.popup_error_run_simulation.open()


    def go_to_execute_simulation(self):
        if self.manager.current == 'output_variable':
            dictionary_of_input = self.manager.get_screen('make_simulation').dict_of_entity_variable_value
            dictionary_of_output = self.dict_of_entity_variable_value_output
            if len(dictionary_of_input.keys()) != len(dictionary_of_output.keys()):
                error_popup = ErrorPopUp()
                error_popup.ids.label_error.text = "You must insert at least an output variable for each entity"
                error_popup.open()
            else:
                dictionary_of_input = self.manager.get_screen('make_simulation').dict_of_entity_variable_value
                dictionary_of_output = self.dict_of_entity_variable_value_output
                list = []
                i = 0
                for key in dictionary_of_input.keys():
                    str = ""
                    str += key + "\n\n"
                    str += "[b]Input[/b]\n"
                    for element in dictionary_of_input[key]:
                        str += "\t" + element[0] + ": " + element[1]
                        str += "\n"
                    str += "\n[b]Output[/b]\n"
                    for element in dictionary_of_output[key]:
                        str += "\t" + element[0]
                        str += "\n"
                    list.append(str)

                for el in list:
                    print el
                print list

                pop = Pop("Summary - Entity inserted", list, self.close_summary(), width=self.width - 20,
                          height=self.height - 20)
                pop.open()


    def close_summary(self):
        message_popup = "Are you sure to continue?"
        content = ConfirmPopup(text=message_popup)
        content.bind(on_answer=self._on_answer)
        self.popup = Popup(title="Question", content=content, auto_dismiss=False)
        self.popup.open()

    def _on_answer(self, instance, answer):
        if answer == 'Yes':
            try:

                self.popup.dismiss()
                #CREATE A NEW POPUP
                #Creo l'oggetto riforma
                reform = Reform()
                #Creo il popup e lo apro passandogli la riforma
                popup_select_reform = PopupSelectReform(reform,self.manager)
                popup_select_reform.open()


            except Exception as e:
                self.popup.dismiss()
                self.popup_error_run_simulation = ErrorPopUp()
                self.popup_error_run_simulation.ids.label_error.text = str(e)
                self.popup_error_run_simulation.open()
                self.manager.current = 'home'
        self.popup.dismiss()


    def go_to_make_simulation(self):
        if self.manager.current == 'output_variable':
            self.manager.current = 'make_simulation'
