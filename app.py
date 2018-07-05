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
from screens.choose_entity import *
from screens.visualize import *
from screens.make_simulation import *
from screens.output_variable import *
from screens.reform import *
from screens.execute_simulation import *

class InitScreen(Screen):
    download_information = StringProperty("[color=000000][b][size=20]If you want to download an openfisca-system\nplease click ones of the following buttons[/size][b][/color]")
    PATH_OPENFISCA = None

    def __init__(self, **kwargs):
        super(InitScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.refresh_system_list_button)


    def refresh_system_list_button(self,dt):
        buttons_instances = []
        system_names = []
        self.dict_button_reference = {} # used to know what button is clicked
        with open('./messages/config_import.json') as f:
            data_config = json.load(f)
        for key,value in data_config.items():
            for key_2, value_2 in value.items():
                if key_2 == 'project_name':
                    system_names.append(value_2)
        system_filename_list = [name for name in os.listdir((os.getcwd()+ "\\openfisca_systems")) if os.path.isdir(os.path.join((os.getcwd()+ "\\openfisca_systems"), name))]
        for file_name in system_filename_list:
            for system_name in system_names:
                if os.path.basename(file_name) == system_name:
                    button = self.ids[system_name] # get button that has the same id of openfisca_project
                    #X image --> Transparency 100%
                    self.ids[system_name + "-x"].color = [0,0,0,0]
                    #Button openfisca-country --> Enabled
                    button.disabled = False
                    button.bind(on_press = self.manager.current_screen.selected_file)
                    btn_image = kivyImage(os.getcwd() + "\\img\\openfisca_system\\"+ file_name + ".png")
                    button.Image = btn_image
                    self.dict_button_reference[button] = os.getcwd()+ "\\openfisca_systems\\" + file_name


    def selected_file(self,button):
        self.PATH_OPENFISCA = self.dict_button_reference[button]
        dict = get_all_paths(self.PATH_OPENFISCA)
        if dict:
            if self.manager.current == 'init':
                self.manager.current = 'home'
                with open('./messages/config_import.json') as f:
                    data_config = json.load(f)
                reload(site)
                if not (check_package_is_installed(country_package_name=os.path.basename(self.PATH_OPENFISCA))):
                    install_country_package(country_package_name=os.path.basename(self.PATH_OPENFISCA),
                                            full_path=self.PATH_OPENFISCA)
                self.init_import_tax_benefit_system(self.PATH_OPENFISCA,data_config)
                load_popup = LoadingPopUp()
                load_popup.ids.txt_log.text = "Loading modules..."
                load_popup.open()
                Clock.schedule_once(self.manager.get_screen('visualize_system').ricevi_inizializza_path,0.5)
                Clock.schedule_once(self.manager.get_screen('home').ricevi_inizializza_path,0.5)
                load_popup.dismiss()
        else:
            self.popup_error_run_simulation = ErrorPopUp()
            self.popup_error_run_simulation.ids.label_error.text = "Environment error, please contact an administrator"
            self.popup_error_run_simulation.open()


    def init_import_tax_benefit_system(self, system_selected, json_config_path_object):
        system_name = str(os.path.basename(system_selected)).replace("-","_")
        for key, value in json_config_path_object[system_name].items():
                if key == 'tax_benefit_system':
                    for key_tax, value_tax in value.items():
                        tbs_module,ext = os.path.splitext(key_tax)
                        tbs_module_class = value_tax
                if key == 'entities':
                    for key_ent, value_ent in value.items():
                        entity_module,ext = os.path.splitext(key_ent)
                        for entity_elements_key,entity_elements_value in value_ent.items():
                            if entity_elements_key == "all_entities":
                                all_entities_classname = entity_elements_value
                if key == 'reforms':
                    reform_father_folder = value
        tax_benefit_system_module = importlib.import_module(system_name + "." + str(tbs_module))
        common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS = getattr(tax_benefit_system_module, tbs_module_class)
        common_modules.ENTITY_MODULE_CLASS = importlib.import_module(system_name + "." + str(entity_module))
        common_modules.ENTITY_MODULE_CLASS_ALL_ENTITIES = all_entities_classname
        if reform_father_folder=="":
            common_modules.REFORM_MODULE = None
        else:
            common_modules.REFORM_MODULE = importlib.import_module(system_name + "." + reform_father_folder)
        reload(site)


    def generate_pop_up(self, title, content):
        popup = Popup(title = title,
                content = content,
                markup = True,
                size_hint=(None, None),
                size=(400, 400))
        popup.open()


    def download_system(self,btn_instance):

        self.id_button = self.get_id(btn_instance)
        self.load_popup = LoadingPopUp()
        self.load_popup.ids.txt_log.text = "Downloading and installing the system"
        self.load_popup.open()
        Clock.schedule_once(self.inner_down_function,0.5)


    def inner_down_function(self,args):
        # read documents
        with open('messages\\config_import.json') as f:
            data_config = json.load(f)
        system_selected = self.id_button.replace("button", "openfisca")
        # get system info depending on the choice
        system_path = os.getcwd() + "\\openfisca_systems"
        github_link = data_config[system_selected]["link"]
        project_name = data_config[system_selected]["project_name"]
        download_and_install_openfisca(system_path, project_name, github_link)
        reload(site)
        self.refresh_system_list_button(dt=None)
        self.load_popup.dismiss()



    def get_id(self, instance):
            for id, widget in self.ids.items():
                if widget.__self__ == instance:
                    return id


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def ricevi_inizializza_path(self,*args):
        path = self.manager.get_screen('init').PATH_OPENFISCA
        self.dict_path = get_all_paths(path)
        self.ids.label_0_0.text = """[color=000000]
        [b][size=24sp]Hello ![/size][/b]\n
        [size=20sp]Thanks for installing [size=20sp][b]OpenFisca Tool Manager[/b][/size]!\n
        This software will help you to manage some feature provided by OpenFisca, in particular you can:
            - Visualize variables, reforms and parameters of the selected country;
            - Create and Execute a reform;
            - Execute a Simulation.
        You have selected this folder: [i] [b]""" + os.path.basename(
            path) + "[/i][/b]" + ".[/color][/size]\n\n"

    def go_to_visualize(self):
        if self.manager.current == 'home':
            self.manager.current = 'visualize_system'

    def go_to_reforms(self):
        if self.manager.current == 'home':
            self.manager.current = 'reforms'

    def go_to_simulation(self):
        if self.manager.current == 'home':
            self.manager.get_screen('choose_entity').init_content_screen()
            self.manager.current = 'choose_entity'


class MyScreenManager(ScreenManager):
    pass



# App
class openfisca_managing_tool(App):
    def build(self):
        Builder.load_file('./folder_kv/reforms.kv')
        Builder.load_file('./folder_kv/app.kv')
        self.icon = 'img/openfisca_man.ico'
        self.title = 'Openfisca Managing Tool'
        return MyScreenManager()


# main
if __name__ == '__main__':
    openfisca_managing_tool().run()
