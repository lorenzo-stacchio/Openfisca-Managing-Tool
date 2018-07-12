import kivy
kivy.require("1.10.0")
import json
import os
import sys
import datetime
from kivy.core.image import Image as kivyImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
import common_modules
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
        system_filename_list = [name for name in os.listdir((os.getcwd()+ "/openfisca_systems")) if os.path.isdir(os.path.join((os.getcwd()+ "/openfisca_systems"), name))]
        for file_name in system_filename_list:
            for system_name in system_names:
                if os.path.basename(file_name) == system_name:
                    button = self.ids[system_name] # get button that has the same id of openfisca_project
                    #X image --> Transparency 100%
                    self.ids[system_name + "-x"].color = [0,0,0,0]
                    #Button openfisca-country --> Enabled
                    button.disabled = False
                    button.bind(on_press = self.manager.current_screen.selected_file)
                    btn_image = kivyImage(os.getcwd() + "/img/openfisca_system/"+ file_name + ".png")
                    button.Image = btn_image
                    self.dict_button_reference[button] = os.getcwd()+ "/openfisca_systems/" + file_name


    def selected_file(self,button):
        self.PATH_OPENFISCA = self.dict_button_reference[button]
        dict = get_all_paths(self.PATH_OPENFISCA)
        if dict:
            if self.manager.current == 'init':
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
                self.manager.current = 'home'
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
        with open('messages/config_import.json') as f:
            data_config = json.load(f)
        system_selected = self.id_button.replace("button", "openfisca")
        # get system info depending on the choice
        system_path = os.getcwd() + "/openfisca_systems"
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
