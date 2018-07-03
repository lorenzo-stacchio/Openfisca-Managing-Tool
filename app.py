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


TAX_BENEFIT_SYSTEM_MODULE_CLASS = None
ENTITY_MODULE_CLASS = None
ENTITY_MODULE_CLASS_ALL_ENTITIES = None
REFORM_MODULE = None
dict_entita ={}


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
        global TAX_BENEFIT_SYSTEM_MODULE_CLASS
        TAX_BENEFIT_SYSTEM_MODULE_CLASS = getattr(tax_benefit_system_module, tbs_module_class)
        global ENTITY_MODULE_CLASS
        ENTITY_MODULE_CLASS = importlib.import_module(system_name + "." + str(entity_module))
        global ENTITY_MODULE_CLASS_ALL_ENTITIES
        ENTITY_MODULE_CLASS_ALL_ENTITIES = all_entities_classname
        global REFORM_MODULE
        if reform_father_folder=="":
            REFORM_MODULE = None
        else:
            REFORM_MODULE = importlib.import_module(system_name + "." + reform_father_folder)
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


class ChooseEntityScreen(Screen):

    def __init__(self, **kwargs):
        super(ChooseEntityScreen, self).__init__(**kwargs)
        self.number_of_entity = {}
        self.entity_box_layout = BoxLayout(orientation='vertical', padding=(50,50,50,50))
        self.add_widget(self.entity_box_layout)


    def init_content_screen(self):
        global ENTITY_MODULE_CLASS
        global ENTITY_MODULE_CLASS_ALL_ENTITIES
        self.type_of_entity = getattr(ENTITY_MODULE_CLASS, ENTITY_MODULE_CLASS_ALL_ENTITIES)
        for entity in self.type_of_entity:
            self.entity_box_layout.add_widget(LineOfChooser())
            self.entity_box_layout.children[0].children[-1].text = entity.key

        layout_period = BoxLayout(orientation = "horizontal")
        layout_period.add_widget(Label(text="[color=000000]Period[/color]", markup=True, font_size="20sp"))
        txt_input = TextInput(id="txt_period", text=time.strftime("%Y"), multiline=False)
        layout_period.add_widget(txt_input)

        self.entity_box_layout.add_widget(layout_period)
        self.entity_box_layout.add_widget(Label(
            text="[color=000000]You must insert:\n- This type of [b]period[/b]: AAAA or AAAA-MM or AAAA-MM-DD\n- At least an [b]entity[/b][/color]",markup=True,
            font_size="17sp"))
        boxButtons = BoxLayout(orientation="horizontal")
        boxButtons.add_widget(Button(id="button_go_to_insert_input_variables", text="Confirm", size_hint=(1.0,0.4), background_color=(0.151, 0.022, 0.064, 1)))
        boxButtons.add_widget(Button(id="button_go_to_home", text="Come back to home",size_hint=(1.0,0.4),  background_color=(0.151, 0.022, 0.064, 1)))
        self.entity_box_layout.add_widget(boxButtons)
        Clock.schedule_once(self._finish_init)


    def _finish_init(self, dt):
        # go to make_simulation bind button
        self.children[0].children[0].children[1].bind(on_release=self.go_to_insert_input_variables)
        self.children[0].children[0].children[0].bind(on_release=self.go_to_home)


    def go_to_home(self, a):
        self.manager.get_screen("choose_entity").entity_box_layout.clear_widgets();
        self.manager.current = 'home'


    def go_to_insert_input_variables(self, instance):
        # verify that there aren't all zeros
        condition = False
        box_layout = self.children[0].children
        for el in box_layout:
            if isinstance(el, LineOfChooser):
                # value of this lineOfChooser
                self.number_of_entity[el.children[3].text] = el.children[2].text
                if el.children[2].text != "0":
                    condition = True

        if not condition:
            error_popup = ErrorPopUp()
            error_popup.ids.label_error.text = "Enter at least one entity"
            error_popup.open()

        #save period
        self.period = box_layout[2].children[0].text
        if not self.check_data(self.period):
            self.period = ""
            condition = False
            error_popup = ErrorPopUp()
            error_popup.ids.label_error.text = "Data format isn't correct!"
            error_popup.open()
        if condition:
            self.manager.get_screen('make_simulation').inizializza_make_simulation()
            self.manager.current = 'make_simulation'



    def check_data(self, data):
        if(len(data)==4):
            try:
                year = int(data)
                if year <= 1900 :
                    return False
                datetime.date(year,01,01)
            except:
                return False
        elif (len(data)==7):
            try:
                year,month = data.split("-")
                if year <= 1900 :
                    return False
                datetime.date(int(year),int(month),01)
            except:
                return False
        elif (len(data)==10):
            try:
                year,month,day = data.split("-")
                if year <= 1900 :
                    return False
                datetime.date(int(year), int(month), int(day))
            except:
                return False
        else:
            return False
        return True


class VisualizeSystemScreen(Screen):

    def __init__(self, **kwargs):
        super(VisualizeSystemScreen, self).__init__(**kwargs)

    def ricevi_inizializza_path(self,*args):
        path = self.manager.get_screen('init').PATH_OPENFISCA
        self.dict_path = get_all_paths(path)
        self.PATH_OPENFISCA = self.dict_path['inner_system_folder']
        with open('./messages/config_import.json') as f:
            data_config = json.load(f)
        # init dynamic loading in classes
        global TAX_BENEFIT_SYSTEM_MODULE_CLASS
        global ENTITY_MODULE_CLASS
        global ENTITY_MODULE_CLASS_ALL_ENTITIES
        global REFORM_MODULE
        Variable_File_Interpeter.import_depending_on_system(tax_benefit_system_module_class = TAX_BENEFIT_SYSTEM_MODULE_CLASS) #static method
        Reform_File_Interpeter.import_depending_on_system(tax_benefit_system_module_class = TAX_BENEFIT_SYSTEM_MODULE_CLASS) #static method
        # entity of situation for simulator
        Entity.import_depending_on_system(tax_benefit_system_module_class = TAX_BENEFIT_SYSTEM_MODULE_CLASS, entity_module_class = ENTITY_MODULE_CLASS,entity_module_all_entities = ENTITY_MODULE_CLASS_ALL_ENTITIES)
        if not(REFORM_MODULE is None):
            Reform.import_depending_on_system(tax_benefit_system_module_class = TAX_BENEFIT_SYSTEM_MODULE_CLASS, reform_module = REFORM_MODULE)
        Simulation_generator.import_depending_on_system(tax_benefit_system_module_class = TAX_BENEFIT_SYSTEM_MODULE_CLASS)
        Variable_To_Reform.import_depending_on_system(tax_benefit_system_module_class = TAX_BENEFIT_SYSTEM_MODULE_CLASS, system_entity_module = ENTITY_MODULE_CLASS, system_all_entities_name = ENTITY_MODULE_CLASS_ALL_ENTITIES)

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

    def show_parameters(self):
        self.ids.visualize_file_chooser_parameters.path = self.dict_path['parameters']
        self.ids.current_path_parameters.text = self.ids.visualize_file_chooser_parameters.path

    def show_reforms(self):
        self.ids.visualize_file_chooser_reforms.path = self.dict_path['reforms']
        self.ids.current_path_reforms.text = self.ids.visualize_file_chooser_reforms.path

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
            self.ids.document_variables_viewer.source = "messages\\file_not_allowed.rst"
            self.ids.document_parameters_viewer.source = "messages\\file_not_allowed.rst"
            self.ids.document_reforms_viewer.source = "messages\\file_not_allowed.rst"
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


class MakeSimulation(Screen):
    variable_added = ObjectProperty()
    dict_of_entity_variable_value = {}
    previous_text_typed = ""

    def __init__(self, **kwargs):
        super(MakeSimulation, self).__init__(**kwargs)


    def inizializza_make_simulation(self):
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
                            dict_entita[k + str(index)] = string_name_list
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
            self.ids.menu_a_tendina_entita.values = dict_entita.keys()
            self.ids.menu_a_tendina_entita.text = self.ids.menu_a_tendina_entita.values[0]
            self.ids.menu_a_tendina_variabili.values = dict_entita[self.ids.menu_a_tendina_entita.text]
            self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
            self.ids.information.text = ""
            with open("messages\\instruction_make_simulation_input.txt", 'r') as f:
                for line in f.readlines():
                    self.ids.information.text = self.ids.information.text + line
        except Exception as e:
            self.popup_error_run_simulation = ErrorPopUp()
            self.popup_error_run_simulation.ids.label_error.text = str(e)
            self.popup_error_run_simulation.open()

    def change_spinner(self):
        variables_name = []
        if self.ids.id_search_box_input_variable != "":
            valori = dict_entita[self.ids.menu_a_tendina_entita.text]
            for key_variable in valori:
                if (self.ids.id_search_box_input_variable.text.lower() in key_variable.lower()):
                    variables_name.append(key_variable)
        elif self.previous_text_typed.lower() in self.ids.id_search_box_input_variable.text.lower():
            for key_variable in self.ids.menu_a_tendina_variabili.values:
                if (self.previous_text_typed.lower() not in key_variable.lower()):
                    variables_name.remove(key_variable)
        else:
            valori = dict_entita[self.ids.menu_a_tendina_entita.text]
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
        self.ids.menu_a_tendina_variabili.values = dict_entita[self.ids.menu_a_tendina_entita.text]
        self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
        self.ids.variable_added.clear_widgets()
        if self.ids.menu_a_tendina_entita.text in self.dict_of_entity_variable_value.keys():
            for tuple in self.dict_of_entity_variable_value[self.ids.menu_a_tendina_entita.text]:
                self.ids.variable_added.add_widget(
                    Button(text=self.ids.menu_a_tendina_entita.text + " - " + tuple[0] + " - " + tuple[1],
                           font_size='14sp',
                           on_release=self.destroy_button,
                           background_color=(255, 255, 255, 0.9),
                           color=(0, 0, 0, 1)))


    def go_to_home(self):
        if self.manager.current == 'make_simulation':
            self.ids.variable_added.clear_widgets()
            self.manager.get_screen("choose_entity").entity_box_layout.clear_widgets();
            self.ids.menu_a_tendina_variabili.text = ''
            self.ids.input_value_variable.text = ''
            self.manager.current = 'home'


    def go_to_output_variables(self):
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

        self.ids.menu_a_tendina_entita_output.values = dict_entita.keys()
        self.ids.menu_a_tendina_entita_output.text = self.ids.menu_a_tendina_entita_output.values[0]

        self.ids.menu_a_tendina_variabili_output.values = dict_entita[
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
            valori = dict_entita[self.ids.menu_a_tendina_entita_output.text]
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
            valori = dict_entita[self.ids.menu_a_tendina_entita_output.text]
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
        self.ids.menu_a_tendina_variabili_output.values = dict_entita[
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
            self.manager.get_screen("choose_entity").entity_box_layout.clear_widgets();
            self.manager.current = "home"

class ReformsScreen(Screen):
    choice = StringProperty()

    def __init__(self, **kwargs):
        super(ReformsScreen, self).__init__(**kwargs)

    def go_to_home(self):
        if self.manager.current == 'reforms':
            self.manager.current = 'home'

    def go_to_add_variable(self):
        self.manager.get_screen('select_variable_screen').choice = "Add variable"
        self.manager.get_screen('select_variable_screen').ids.id_text_search_box.disabled = True
        self.manager.get_screen('select_variable_screen').ids.id_spinner_select_variable_screen.disabled = True
        self.manager.get_screen('select_variable_screen').ids.id_input_reform_description.text = ""
        self.manager.get_screen('select_variable_screen').ids.id_spinner_select_variable_screen.text = ""
        self.manager.get_screen('select_variable_screen').ids.id_input_reform_name.text = ""
        self.manager.current = 'select_variable_screen'

    def go_to_update_variable(self):
        self.manager.get_screen('select_variable_screen').choice = "Update variable"
        self.manager.get_screen('select_variable_screen').ids.id_spinner_select_variable_screen.disabled = False
        self.manager.get_screen('select_variable_screen').ids.id_input_reform_description.text = ""
        self.manager.get_screen('select_variable_screen').ids.id_spinner_select_variable_screen.text = ""
        self.manager.get_screen('select_variable_screen').ids.id_input_reform_name.text = ""
        self.manager.get_screen('select_variable_screen').inizialize_form()
        self.manager.current = 'select_variable_screen'

    def go_to_neutralize_variable(self):
        self.manager.get_screen('select_variable_screen').choice = "Neutralize variable"
        self.manager.get_screen('select_variable_screen').ids.id_spinner_select_variable_screen.disabled = False
        self.manager.get_screen('select_variable_screen').ids.id_input_reform_description.text = ""
        self.manager.get_screen('select_variable_screen').ids.id_spinner_select_variable_screen.text = ""
        self.manager.get_screen('select_variable_screen').ids.id_input_reform_name.text = ""
        self.manager.get_screen('select_variable_screen').inizialize_form()
        self.manager.current = 'select_variable_screen'

    def to_do(self):
        self.box_popup = BoxLayout(orientation='horizontal')

        self.box_popup.add_widget(Label(text="In the future"))

        self.popup_exit = Popup(title="To Do!",
                                content=self.box_popup,
                                size_hint=(0.4, 0.4),
                                auto_dismiss=True)
        self.popup_exit.open()


class SelectVariableScreen(Screen):
    choice = StringProperty()
    previous_text_typed = ""
    def __init__(self, **kwargs):
        super(SelectVariableScreen, self).__init__(**kwargs)

    def change_spinner(self):
        global TAX_BENEFIT_SYSTEM_MODULE_CLASS
        if(TAX_BENEFIT_SYSTEM_MODULE_CLASS):
            variables_name = []
            if self.ids.id_text_search_box != "":
                dict = TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables().iteritems()
                for key_variable, variables_content in dict:
                    if (self.ids.id_text_search_box.text.lower() in key_variable.lower()):
                        variables_name.append(key_variable)
            elif self.previous_text_typed.lower() in self.ids.id_text_search_box.lower():
                for key_variable in self.ids.id_spinner_select_variable_screen.values:
                    if(self.previous_text_typed not in key_variable):
                        variables_name.remove(key_variable)
            else:
                dict = TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables().iteritems()
                for key_variable, variables_content in dict:
                    if((key_variable.lower() not in variables_name.lower()) and self.previous_text_typed.lower() in key_variable.lower()):
                        variables_name.append(key_variable)


            # Ordina alfabeticamente
            variables_name.sort()
            self.ids.id_spinner_select_variable_screen.values = variables_name
            if self.ids.id_spinner_select_variable_screen.values:
                self.ids.id_spinner_select_variable_screen.text = self.ids.id_spinner_select_variable_screen.values[0]
            else:
                self.ids.id_spinner_select_variable_screen.text = ""

    def go_to_home(self):
        if self.manager.current == 'select_variable_screen':
            self.manager.current = 'home'

    def inizialize_form(self):
        self.ids.id_spinner_select_variable_screen.dropdown_cls.max_height = self.ids.id_spinner_select_variable_screen.height*3
        global TAX_BENEFIT_SYSTEM_MODULE_CLASS
        variables_name = []
        for key_variable, variables_content in TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables().iteritems():
            variables_name.append(key_variable)
        #Ordina alfabeticamente
        variables_name.sort()
        self.ids.id_spinner_select_variable_screen.values = variables_name
        self.ids.id_spinner_select_variable_screen.text = self.ids.id_spinner_select_variable_screen.values[0]

    def select_variable(self):
        if self.manager.get_screen('select_variable_screen').choice == "Neutralize variable":
            # Create a popup
            content = ConfirmPopup(text=str("Are you sure to neutralize?"))
            content.bind(on_answer=self._on_answer)
            self.popup = Popup(title="Answer Question", content=content, size_hint=(None, None), size=(480, 400),
                               auto_dismiss=False)
            self.popup.open()
        elif self.manager.get_screen('select_variable_screen').choice == "Update variable":
            self.manager.get_screen('form_variable_screen').setting_up_form_variable()
            self.manager.current = 'form_variable_screen'
        elif self.manager.get_screen('select_variable_screen').choice == "Add variable":
            self.manager.get_screen('form_variable_screen').ids.name_input.text = ""
            self.manager.get_screen('form_variable_screen').ids.value_type_input.text = ""
            self.manager.get_screen('form_variable_screen').ids.entity_input.text = ""
            self.manager.get_screen('form_variable_screen').ids.set_input_period.text = ""
            self.manager.get_screen('form_variable_screen').ids.label_input.text = ""
            self.manager.get_screen('form_variable_screen').ids.definition_period_input.text = ""
            self.manager.get_screen('form_variable_screen').ids.reference_input.text = ""
            self.manager.get_screen('form_variable_screen').setting_up_form_variable()
            self.manager.current = 'form_variable_screen'
        else:
            pass

    def _on_answer(self, instance, answer):
        if answer == 'Yes':
            global TAX_BENEFIT_SYSTEM_MODULE_CLASS
            variables_name = []
            for key_variable, variables_content in TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables().iteritems():
                if key_variable == self.ids.id_spinner_select_variable_screen.text:
                    var = Variable_To_Reform()
                    var.set_name(key_variable)
                    v_r_man = Variable_reform_manager(path_to_save_reform = self.manager.get_screen('visualize_system').dict_path['reforms'], variable = var, reform_name = "neutralize_" + self.ids.id_spinner_select_variable_screen.text)
                    v_r_man.do_reform(TYPEOFREFORMVARIABILE.neutralize_variable)
                    break
        self.popup.dismiss()
        self.popup = Popup(title="Variable neutralized", content = Label(text = "The reform that neutralized\n" + self.ids.id_spinner_select_variable_screen.text + "\nwas written, you can check in the legislation explorer!"), size_hint=(None, None), size=(480, 400),
                           auto_dismiss=True)
        self.popup.open()
        self.manager.current = 'reforms'


class FormVariableScreen(Screen):


    def __init__(self, **kwargs):
        super(FormVariableScreen, self).__init__(**kwargs)


    def setting_up_form_variable(self):
        # get type members
        list_of_type = []
        for el in TYPEOFVARIABLE.__members__:
            list_of_type.append(el)
        self.ids.value_type_input.values = list_of_type
        # get the entities
        global ENTITY_MODULE_CLASS
        global ENTITY_MODULE_CLASS_ALL_ENTITIES
        list_of_type_entity = getattr(ENTITY_MODULE_CLASS, ENTITY_MODULE_CLASS_ALL_ENTITIES)
        list_key_name_entity = []
        for ent in list_of_type_entity:
            list_key_name_entity.append(ent.key)
        self.ids.entity_input.values = list_key_name_entity
        # get type members
        list_of_type_definition_period = []
        for el in TYPEOFDEFINITIONPERIOD.__members__:
            list_of_type_definition_period.append(el)
        self.ids.definition_period_input.values = list_of_type_definition_period
        # get set_input_period
        list_of_set_input_period = []
        for el in TYPEOFSETINPUT.__members__:
            list_of_set_input_period.append(el)
        self.ids.set_input_period.values = list_of_set_input_period
        # update vs add variable
        if self.manager.get_screen('select_variable_screen').choice == "Update variable":
            # get all the system variables and compare
            global TAX_BENEFIT_SYSTEM_MODULE_CLASS
            vars = TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables()
            # fill the fields with the existing variables
            for key_var, value_var in vars.iteritems():
                if key_var == self.manager.get_screen('select_variable_screen').ids.id_spinner_select_variable_screen.text:
                    self.ids.name_input.text = self.manager.get_screen('select_variable_screen').ids.id_spinner_select_variable_screen.text
                    self.ids.name_input.disabled = True
                    self.ids.value_type_input.text = value_var.value_type.__name__
                    self.ids.entity_input.text = value_var.entity.__name__

                    if value_var.label:
                        self.ids.label_input.text = value_var.label.encode("utf-8")

                    if value_var.set_input:
                        self.ids.set_input_period.text = value_var.set_input.__name__
                    else:
                        self.ids.set_input_period.text = TYPEOFSETINPUT.no_set_input_period.name

                    if value_var.definition_period:
                        self.ids.definition_period_input.text = value_var.definition_period

                    if value_var.reference:
                        self.ids.reference_input.text = value_var.reference[0]

                    if not (value_var.is_input_variable()):
                        self.formula_to_write_in_popup = inspect.getsource(value_var.get_formula())  # get formula if the variable if exist
                        if "\n" in self.formula_to_write_in_popup: # if there is more than one line
                            lines = self.formula_to_write_in_popup.split("\n")
                            formatted_lines = []
                            final_formatted_lines = []
                            for line in lines:
                                formatted_lines.append(line.strip())
                            final_formatted_lines.append(formatted_lines[0])
                            for line in formatted_lines[1:]: #except the first line
                                final_formatted_lines.append("\t" + line)
                            self.formula_to_write_in_popup = ""
                            for line in final_formatted_lines:
                                self.formula_to_write_in_popup = self.formula_to_write_in_popup + line + "\n"
                    else:
                        self.formula_to_write_in_popup = None
                    break
        elif self.manager.get_screen('select_variable_screen').choice == "Add variable":
            self.ids.name_input.disabled = False
            self.ids.value_type_input.text = self.ids.value_type_input.values[0]
            self.ids.entity_input.text = self.ids.entity_input.values [0]
            self.ids.set_input_period.text = TYPEOFSETINPUT.no_set_input_period.name
            self.ids.definition_period_input.text = self.ids.definition_period_input.values[0]
            self.formula_to_write_in_popup = None
        else:
            pass


    def create_pop_up_watch_formula(self):
        w_f_p = WatchingFormulaPopUp()
        if not(self.formula_to_write_in_popup is None):
            w_f_p.ids.formula_view_from_update.text = ".. code:: python\n\n\n " + self.formula_to_write_in_popup
        else:
            w_f_p.ids.formula_view_from_update.text = ""
        w_f_p.open()


    def create_pop_up_modify_formula(self):
        m_f_p = ModifyFormulaPopup(screen_manager = self.manager)
        # there is a method inside the modify formula because we need to attempt the finish of the init to get the id


    def run_operation(self):
        #delete all whitespace and che that variable doesn't exist
        if self.ids.name_input.text == "":
            name_input = None
        else:
            name_input = self.ids.name_input.text

        value_type_input=self.ids.value_type_input.text.replace(" ","")
        entity_input=self.ids.entity_input.text.replace(" ","")
        definition_period_input=self.ids.definition_period_input.text.replace(" ","")
        set_input_period = self.ids.set_input_period.text

        if self.ids.label_input.text == "":
            label_input = None
        else:
            label_input = self.ids.label_input.text
        if self.ids.reference_input.text == "":
            reference_input = None
        else:
            reference_input = self.ids.reference_input.text.encode("utf-8")

        if self.formula_to_write_in_popup == "":
            formula = None
        else:
            formula = self.formula_to_write_in_popup
        # get the reform name and reform reference if defined
        if self.manager.get_screen('select_variable_screen').ids.id_input_reform_name.text == "":
            reform_name = None
        else:
            reform_name = self.manager.get_screen('select_variable_screen').ids.id_input_reform_name.text

        if self.manager.get_screen('select_variable_screen').ids.id_input_reform_description.text == "":
            reform_description = None
        else:
            reform_description = self.manager.get_screen('select_variable_screen').ids.id_input_reform_description.text

        try:
            v_to_add = Variable_To_Reform()
            v_to_add.set_name(name_input)
            v_to_add.set_entity(entity_input)
            v_to_add.set_type(value_type_input)
            v_to_add.set_reference(reference_input)
            v_to_add.set_formula(formula)
            v_to_add.set_label(label_input)
            v_to_add.set_definition_period(definition_period_input)
            v_to_add.set_set_input(set_input_period)
            ref_var_man = Variable_reform_manager(variable = v_to_add, path_to_save_reform = self.manager.get_screen('visualize_system').dict_path['reforms'], reform_full_description = reform_description , reform_name = reform_name)

            if self.manager.get_screen('select_variable_screen').choice == "Update variable":
                ref_var_man.do_reform(command = TYPEOFREFORMVARIABILE.update_variable)
                self.popup = Popup(title="Variable updated", content = Label(text = "The reform that update\n" + name_input + "\nwas written, you can check in the legislation explorer!"), size_hint=(None, None), size=(480, 400),
                                   auto_dismiss=True)
                self.popup.open()
                self.manager.current = 'reforms'

            elif self.manager.get_screen('select_variable_screen').choice == "Add variable":
                ref_var_man.do_reform(command = TYPEOFREFORMVARIABILE.add_variable)
                self.popup = Popup(title="Variable added", content = Label(text = "The reform that add\n" + name_input + "\nwas written, you can check in the legislation explorer!"), size_hint=(None, None), size=(480, 400),
                                   auto_dismiss=True)
                self.popup.open()
                self.manager.current = 'reforms'
        except Exception as e:
            self.popup_error_run_simulation = ErrorPopUp()
            self.popup_error_run_simulation.ids.label_error.text = str(e)
        self.popup_error_run_simulation.open()


    def go_to_home(self):
        if self.manager.current == 'form_variable_screen':
            self.manager.current = 'home'


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
