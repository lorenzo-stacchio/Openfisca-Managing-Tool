# -*- coding: utf-8 -*-
import kivy
import json
import os, sys
kivy.require("1.10.0")
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
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
from script.Simulation.Situation_for_simulation import *
from script.reforms_maker.reform_variables import *
from multiprocessing.pool import ThreadPool


TAX_BENEFIT_SYSTEM_MODULE_CLASS = None
ENTITY_MODULE_CLASS = None
ENTITY_MODULE_CLASS_ALL_ENTITIES = None

# Screen
class InitScreen(Screen):
    download_information = StringProperty("[color=000000] [b] [size=20] Select an openfisca-system[/size] [b][/color]")
    PATH_OPENFISCA = None

    def __init__(self, **kwargs):
        super(InitScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.ids.home_file_chooser.path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    def selected_file(self, *args):
        self.PATH_OPENFISCA = args[1][0]
        dict = get_all_paths(self.PATH_OPENFISCA)
        if dict:
            if self.manager.current == 'init':
                self.manager.current = 'home'
                with open('./messages/config_import.json') as f:
                    data_config = json.load(f)
                self.init_import_tax_benefit_system(self.PATH_OPENFISCA,data_config)
                self.manager.get_screen('visualize_system').ricevi_inizializza_path(self.PATH_OPENFISCA)
                self.manager.get_screen('home').ricevi_inizializza_path(self.PATH_OPENFISCA)
                #self.manager.get_screen('choose_entity').import_entities_system(self.PATH_OPENFISCA,data_config)
        else:
            self.ids.lbl_txt_2.text = "[u][b]The selected directory doesn't \n contain an openfisca regular system[/b][/u]"


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
        reload(site)
        tax_benefit_system_module = importlib.import_module(system_name + "." + str(tbs_module))
        global TAX_BENEFIT_SYSTEM_MODULE_CLASS
        TAX_BENEFIT_SYSTEM_MODULE_CLASS = getattr(tax_benefit_system_module, tbs_module_class)
        global ENTITY_MODULE_CLASS
        ENTITY_MODULE_CLASS = importlib.import_module(system_name + "." + str(entity_module))
        global ENTITY_MODULE_CLASS_ALL_ENTITIES
        ENTITY_MODULE_CLASS_ALL_ENTITIES = all_entities_classname
        reload(site)


    def generate_pop_up(self, title, content):
        popup = Popup(title = title,
                content = content,
                markup = True,
                size_hint=(None, None),
                size=(400, 400))
        popup.open()


    def download_system(self,btn_instance):
        id_button = self.get_id(btn_instance)
        # read documents
        with open('messages\\config_import.json') as f:
            data_config = json.load(f)
        system_selected = id_button.replace("button","openfisca")
        # get system info depending on the choice
        user_desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        github_link = data_config[system_selected]["link"]
        project_name = data_config[system_selected]["project_name"]
        # waiting popup
        # TODO: AGGIUSTA IL CAMBIAMENTO DELLA LABEL
        self.download_information= "[color=FF033D] [b] [size=20] [u] Downloading and installing the system[/size] [u] [b] [/color]"

        result = download_and_install_openfisca(user_desktop, project_name, github_link)
        if result:
            self.generate_pop_up( title = 'System saved!',
                                    content = Label(text='The system [b]' + system_selected + '[b] was saved in:' + user_desktop, size = self.parent.size, halign="left", valign="middle"))
        else:
            self.generate_pop_up( title = 'System already exist!',
                            content = Label(text='The system [b]' + system_selected + '[b] already exist in:' + user_desktop + "\n If you want to download a newest version, please erase it!", size = self.parent.size, halign="left", valign="middle"))


    def get_id(self, instance):
            for id, widget in self.ids.items():
                print id, widget
                if widget.__self__ == instance:
                    return id


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def ricevi_inizializza_path(self, path):
        self.dict_path = get_all_paths(path)
        self.ids.label_0_0.text = """[color=000000]
        [b][size=24sp]Hello ![/size][/b]\n
        [size=20sp]Thanks for installing [size=20sp][b]OpenFisca Tool Manager[/b][/size]!\n
        This software will help you to manage some feature provided by OpenFisca, in particular you can:
            - Visualize variables, reforms and parameters of the selected country;
            - Create and Execute a reform;
            - Execute a Simulation.
        You have selected this folder: [i]""" + path[:path.rindex('\\') + 1] + "[b]" + os.path.basename(
            path) + "[/i][/b]" + ".[/color][/size]\n\n"

    def go_to_visualize(self):
        if self.manager.current == 'home':
            self.manager.current = 'visualize_system'

    def go_to_reforms(self):
        if self.manager.current == 'home':
            self.manager.current = 'reforms'

    def go_to_simulation(self):
        if self.manager.current == 'home':
            # initialize the simulator entity manager
            self.manager.get_screen('choose_entity').init_content_screen()
            self.manager.current = 'choose_entity'


class ChooseEntityScreen(Screen):
    type_of_entity = None
    number_of_entity = {}
    period = None
    global_box_layout = None

    def __init__(self, **kwargs):
        super(ChooseEntityScreen, self).__init__(**kwargs)
        self.entity_box_layout = BoxLayout(orientation='vertical')
        self.add_widget(self.entity_box_layout)


    def init_content_screen(self):
        global ENTITY_MODULE_CLASS
        global ENTITY_MODULE_CLASS_ALL_ENTITIES
        self.type_of_entity = getattr(ENTITY_MODULE_CLASS, ENTITY_MODULE_CLASS_ALL_ENTITIES)
        for entity in self.type_of_entity:
            self.entity_box_layout.add_widget(LineOfChooser())
            self.entity_box_layout.children[0].children[-1].text = entity.key

        layout_period = BoxLayout(orientation = "horizontal")
        layout_period.add_widget(Label(text="Period", markup=True))
        txt_input = TextInput(id="txt_period")
        layout_period.add_widget(txt_input)

        self.entity_box_layout.add_widget(layout_period)
        self.entity_box_layout.add_widget(Label(text="You can insert this type of period AAAA or AAAA-MM or AAAA-MM-DD"))
        self.entity_box_layout.add_widget(Button(id="button_go_to_insert_input_variables", text="Click"))
        Clock.schedule_once(self._finish_init)



    def _finish_init(self, dt):
        # go to make_simulation bind button
        self.children[0].children[0].bind(on_release=self.go_to_insert_input_variables)


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

        #save period
        self.period = box_layout[2].children[0].text

        if not self.check_data(self.period):
            self.period = ""
            condition = False

        if condition:
            self.manager.get_screen('make_simulation').inizializza_make_simulation()
            self.manager.current = 'make_simulation'


    def check_data(self, data):
        if(len(data)==4):
            try:
                datetime.date(int(data),01,01)
            except:
                return False
        elif (len(data)==7):
            try:
                year,month = data.split("-")
                datetime.date(int(year),int(month),01)
            except:
                return False
        elif (len(data)==10):
            try:
                year,month,day = data.split("-")
                datetime.date(int(year), int(month), int(day))
            except:
                return False
        else:
            return False
        return True


class LineOfChooser(BoxLayout):
    name_label = StringProperty()

    def decrementa(self):
        if int(self.ids.value.text) > 0:
            self.ids.value.text = str(int(self.ids.value.text) - 1)

    def incrementa(self):
        self.ids.value.text = str(int(self.ids.value.text) + 1)


class VisualizeSystemScreen(Screen):

    def __init__(self, **kwargs):
        super(VisualizeSystemScreen, self).__init__(**kwargs)

    def ricevi_inizializza_path(self, path):
        self.dict_path = get_all_paths(path)
        self.PATH_OPENFISCA = self.dict_path['inner_system_folder']
        with open('./messages/config_import.json') as f:
            data_config = json.load(f)
        # init dynamic loading in classes
        global TAX_BENEFIT_SYSTEM_MODULE_CLASS
        global ENTITY_MODULE_CLASS
        global ENTITY_MODULE_CLASS_ALL_ENTITIES
        Variable_File_Interpeter.import_depending_on_system(tax_benefit_system_module_class = TAX_BENEFIT_SYSTEM_MODULE_CLASS) #static method
        Reform_File_Interpeter.import_depending_on_system(tax_benefit_system_module_class = TAX_BENEFIT_SYSTEM_MODULE_CLASS) #static method
        # entity of situation for simulator
        Entity.import_depending_on_system_entity_for_simulation(system_selected = self.PATH_OPENFISCA, json_config_path_object = data_config)
        Simulation_generator.import_depending_on_system_situation_for_simulation(system_selected = self.PATH_OPENFISCA, json_config_path_object = data_config)
        Variable_To_Reform.import_depending_on_system(tax_benefit_system_module_class = TAX_BENEFIT_SYSTEM_MODULE_CLASS, system_entity_module = ENTITY_MODULE_CLASS, system_all_entities_name = ENTITY_MODULE_CLASS_ALL_ENTITIES)

        with open('./messages/config_import.json') as f:
            data_config = json.load(f)
        v = Variable_To_Reform()
        v.set_name("RP62_periodo_2013")
        v.set_type("float")
        v.set_entity("person")
        v.set_definition_period("month")
        v.set_set_input("set_input_divide_by_period")
        v.set_formula("def formula(person, period, parameters):\n\t\treturn person('reddito_lavoro_dipendente_annuale', period) * parameters(period).tasse.aliquota_IRPEF")
        os.chdir(os.getcwd())
        self.ids.document_variables_viewer.colors["paragraph"] = "202020ff"
        self.ids.document_variables_viewer.colors["link"] = "33AAFFff"
        self.ids.document_variables_viewer.colors["background"] = "ffffffff"
        self.ids.document_variables_viewer.colors["bullet"] = "000000ff"
        self.ids.document_variables_viewer.colors["title"] = "971640ff"
        self.ids.document_variables_viewer.underline_color = "971640ff"

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
            # print "Path ok"
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
                # the file could be a parameter or a variable
                if file_extension == '.yaml':
                    parameter_interpeter = ParameterInterpeter(path_file_scelto)
                    if (parameter_interpeter.understand_type() == ParameterType.normal):
                        parameter_interpeter.__interpeter_normal_parameter__()
                        path_prm = parameter_interpeter.generate_RST_parameter()
                        self.ids.document_variables_viewer.source = path_prm
                        self.ids.document_parameters_viewer.source = path_prm
                        self.ids.document_reforms_viewer.source = path_prm
                    elif (parameter_interpeter.understand_type() == ParameterType.scale):
                        parameter_interpeter.__interpeter_scale_parameter__()
                        path_prm = parameter_interpeter.generate_RST_parameter()
                        self.ids.document_variables_viewer.source = path_prm
                        self.ids.document_parameters_viewer.source = path_prm
                        self.ids.document_reforms_viewer.source = path_prm
                    elif (parameter_interpeter.understand_type() == ParameterType.fancy_indexing):
                        parameter_interpeter.__interpeter_fancy_indexing_parameter__()
                        path_prm = parameter_interpeter.generate_RST_parameter()
                        self.ids.document_variables_viewer.source = path_prm
                        self.ids.document_parameters_viewer.source = path_prm
                        self.ids.document_reforms_viewer.source = path_prm
                elif file_extension == '.py':
                    variable_interpeter = Variable_File_Interpeter(path_file_scelto)
                    reform_interpeter = Reform_File_Interpeter(path_file_scelto)
                    if (variable_interpeter.file_is_a_variable() and not (reform_interpeter.file_is_a_reform())):
                        variable_interpeter.start_interpetration()
                        path_rst = variable_interpeter.generate_RSTs_variables()
                        self.ids.document_variables_viewer.source = path_rst
                        self.ids.document_parameters_viewer.source = path_rst
                        self.ids.document_reforms_viewer.source = path_rst
                    elif (reform_interpeter.file_is_a_reform()):
                        reform_interpeter.start_interpetration_reforms()
                        path_rst = reform_interpeter.generate_RST_reforms()
                        self.ids.document_variables_viewer.source = path_rst
                        self.ids.document_parameters_viewer.source = path_rst
                        self.ids.document_reforms_viewer.source = path_rst
                else:  # file for which the interpretation is not defined yet
                    self.ids.document_variables_viewer.source = path_file_scelto
                    self.ids.document_parameters_viewer.source = path_file_scelto
                    self.ids.document_reforms_viewer.source = path_file_scelto
                self.ids.current_path_variables.text = self.ids.visualize_file_chooser_variables.path
                self.ids.current_path_parameters.text = self.ids.visualize_file_chooser_parameters.path
                self.ids.current_path_reforms.text = self.ids.visualize_file_chooser_reforms.path
        except Exception as e:
            print "Some error ", e

    def go_to_home(self):
        if self.manager.current == 'visualize_system':
            self.manager.current = 'home'


class MakeSimulation(Screen):
    variable_added = ObjectProperty()
    dict_entita = DictProperty()
    dict_of_entity_variable_value = {}

    def __init__(self, **kwargs):
        super(MakeSimulation, self).__init__(**kwargs)


    def inizializza_make_simulation(self):
        #Resize max height of dropdown
        self.ids.menu_a_tendina_entita.dropdown_cls.max_height = self.ids.menu_a_tendina_entita.height*30
        self.ids.menu_a_tendina_variabili.dropdown_cls.max_height = self.ids.menu_a_tendina_variabili.height*30

        self.dict_entita = {}
        self.situations = {}
        # Cicla il dizionario contenente l'input fornito in precedenza
        #Esempio "person":1,"household":2
        for k, v in self.manager.get_screen('choose_entity').number_of_entity.items():
            #Per ogni oggetto entità esistente in type_of_entity
            for entity in self.manager.get_screen('choose_entity').type_of_entity:
                #Se la chiave dell'oggetto è uguale a k
                if entity.key == k:
                    #Per ogni indice da 1 a numero di elementi di quell'entità
                    for index in xrange(1, int(v) + 1):
                        #ostruisco l'entità
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
                        self.dict_entita[k + str(index)] = string_name_list
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

        self.ids.menu_a_tendina_entita.values = self.dict_entita.keys()
        self.ids.menu_a_tendina_entita.text = self.ids.menu_a_tendina_entita.values[0]

        self.ids.menu_a_tendina_variabili.values = self.dict_entita[self.ids.menu_a_tendina_entita.text]
        self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
        self.ids.information.text = """
[b]Instructions[/b]:
    - Select a variable
    - Insert into the text input form its value
    - Click on "Add Variable"

[b]Rules[/b]:
    - You can't insert a blank variable
    - You can't insert a blank variable value"""

    def update_form(self):
        # print "Hai selezionato "+self.ids.menu_a_tendina_entita.text
        self.ids.menu_a_tendina_variabili.values = self.dict_entita[self.ids.menu_a_tendina_entita.text]
        self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
        self.ids.variable_added.clear_widgets()
        # If the selected entity exists
        if self.ids.menu_a_tendina_entita.text in self.dict_of_entity_variable_value.keys():
            # cycle it
            for tuple in self.dict_of_entity_variable_value[self.ids.menu_a_tendina_entita.text]:
                # add all variable and value of this entity
                self.ids.variable_added.add_widget(
                    Button(text=self.ids.menu_a_tendina_entita.text + " - " + tuple[0] + " - " + tuple[1],

                           font_size='14sp',
                           on_release=self.destroy_button,
                           background_color=(255, 255, 255, 0.9),
                           color=(0, 0, 0, 1)))


    def go_to_home(self):
        if self.manager.current == 'make_simulation':
            # Reset when you go to home
            self.ids.variable_added.clear_widgets()
            self.ids.menu_a_tendina_variabili.text = ''
            self.ids.input_value_variable.text = ''
            #TODO: Resetta bene le variabili
            # Go to home
            self.manager.current = 'home'


    def go_to_output_variables(self):
        if self.manager.current == 'make_simulation':
            # you can't go to output variable if you haven't insert nothing
            if len(self.ids.variable_added.children) != 0:
                # change transition
                self.manager.transition = kivy.uix.screenmanager.SlideTransition(direction='left')
                self.manager.transition.duration = .6
                self.manager.get_screen('output_variable').inizializza_output_variable()
                # Go to output_variable
                self.manager.current = 'output_variable'
                # reset transition
                self.manager.transition = kivy.uix.screenmanager.TransitionBase()
                self.manager.transition.duration = .4


    def exist_tuple(self, dictionary, input_entity, input_variable):
        # dictionary hasn't "input_entity" into its keys
        if not input_entity in dictionary.keys():
            return False
        # Example I add something then I delete it
        elif dictionary[input_entity] == []:
            return False
        else:
            for tuple in dictionary[input_entity]:
                if tuple[0] == input_variable:
                    return True
        # otherwise
        return False


    def add_value_and_reset_form(self):

        # if exist value do nothing
        for key in self.dict_of_entity_variable_value.keys():
            for tuple in self.dict_of_entity_variable_value[key]:
                if tuple[0] == self.ids.input_value_variable.text and tuple[1] == self.ids.input_value_variable.text:
                    return

        # If there are blank value
        if self.ids.menu_a_tendina_variabili.text != '' and self.ids.input_value_variable.text != '':
            # You can't add again a certain variable of a certain entity
            if not self.exist_tuple(self.dict_of_entity_variable_value, self.ids.menu_a_tendina_entita.text,
                                    self.ids.menu_a_tendina_variabili.text):
                # Add button
                self.ids.variable_added.add_widget(Button(
                    text=self.ids.menu_a_tendina_entita.text + " - " + self.ids.menu_a_tendina_variabili.text + " - " + self.ids.input_value_variable.text,
                    on_release=self.destroy_button,
                    font_size= '14sp',
                    background_color=(255, 255, 255, 0.9),
                    color=(0, 0, 0, 1)))

                # CORRADOOOOOOO
                # QUESTA PARTE MI SERVE PER INIZIALIZZARE LE INPUT VARIABLE PER OGNI SITUAZIONE
                # PERCHE' LE AGGIUNTO VOLTA VOLTA, QUINDI SE LE RAGGRUPPAVI IN QUALCHE DICT PUOI ANCHE TOGLIERLO
                self.situations[self.ids.menu_a_tendina_entita.text ].add_variable_to_choosen_input_variables(choosen_input_variable = self.ids.menu_a_tendina_variabili.text, value = self.ids.input_value_variable.text)
                print self.situations[self.ids.menu_a_tendina_entita.text ].get_choosen_input_variables()

                # EXAMPLE dict_of_entity_variable_value[Persona] = [reddito_totale,10000,prova,10,prova2,11]
                # inizialize if key is not exists
                if not self.ids.menu_a_tendina_entita.text in self.dict_of_entity_variable_value.keys():
                    self.dict_of_entity_variable_value[self.ids.menu_a_tendina_entita.text] = []

                # Add value
                # add name of variable and value
                tuple = [self.ids.menu_a_tendina_variabili.text, self.ids.input_value_variable.text]
                self.dict_of_entity_variable_value[self.ids.menu_a_tendina_entita.text].append(tuple)

            else:
                i = 0
                # In this case the tuple already exists

                # CORRADOOOOOOO
                # QUESTA PARTE MI SERVE PER INIZIALIZZARE LE INPUT VARIABLE PER OGNI SITUAZIONE
                # PERCHE' LE AGGIUNTO VOLTA VOLTA, QUINDI SE LE RAGGRUPPAVI IN QUALCHE DICT PUOI ANCHE TOGLIERLO
                self.situations[self.ids.menu_a_tendina_entita.text].add_variable_to_choosen_input_variables(choosen_input_variable = self.ids.menu_a_tendina_variabili.text, value = self.ids.input_value_variable.text)

                # ROBA DI CORRADO
                for el in self.ids.variable_added.children:
                    # splitting
                    entity, variable, value = el.text.split(' - ')
                    # If "entity - variabile" in button text
                    if (self.ids.menu_a_tendina_entita.text + " - " + self.ids.menu_a_tendina_variabili.text) == (entity + " - " + variable):
                        # update button value
                        self.ids.variable_added.children[i].text = entity + " - " + variable + " - " + \
                                                                   self.ids.input_value_variable.text
                        break
                    i += 1

                # Replace value of variable
                for tuple in self.dict_of_entity_variable_value[self.ids.menu_a_tendina_entita.text]:
                    if self.ids.menu_a_tendina_variabili.text in tuple:
                        tuple[1] = self.ids.input_value_variable.text
                        break

            # Reset form
            self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
            self.ids.input_value_variable.text = ''


    def change_view_added_variables(self):
        pass


    def destroy_button(self, button):
        # Persona1 - Reddito - 1000
        # entity = Persona1
        # variable = Reddito
        # value = 1000

        # Splitting
        entity, variable, value = button.text.split(" - ")
        # Find the tuple to delete
        for tuple in self.dict_of_entity_variable_value[entity]:
            if tuple[0] == variable and tuple[1] == value:
                # delete from dict
                self.dict_of_entity_variable_value[entity].remove(tuple)
                break
        # now i can delete the button
        self.variable_added.remove_widget(button)


class OutputVariableScreen(Screen):
    string_var_input = ""
    string_var_output = ""
    variable_added_output = ObjectProperty()
    dict_of_entity_variable_value_output = {}

    def __init__(self, **kwargs):
        super(OutputVariableScreen, self).__init__(**kwargs)

    def inizializza_output_variable(self):
        # Resize max height of dropdown
        self.ids.menu_a_tendina_entita_output.dropdown_cls.max_height = self.ids.menu_a_tendina_entita_output.height * 30
        self.ids.menu_a_tendina_variabili_output.dropdown_cls.max_height = self.ids.menu_a_tendina_variabili_output.height * 30

        # i take the dict with association of enitites
        print self.manager.get_screen('choose_entity').number_of_entity
        print self.manager.get_screen('choose_entity').period

        self.ids.menu_a_tendina_entita_output.values = self.manager.get_screen('make_simulation').dict_entita.keys()
        self.ids.menu_a_tendina_entita_output.text = self.ids.menu_a_tendina_entita_output.values[0]

        self.ids.menu_a_tendina_variabili_output.values = self.manager.get_screen('make_simulation').dict_entita[
            self.ids.menu_a_tendina_entita_output.text]
        self.ids.menu_a_tendina_variabili_output.text = self.ids.menu_a_tendina_variabili_output.values[0]
        self.ids.information_output.text = """
        [b]Instructions[/b]:
            - Select a variable
            - Insert into the text input form its value
            - Click on "Add Variable"

        [b]Rules[/b]:
            - You can't insert a blank variable
            - You can't insert a blank variable value"""


    def go_to_home(self):
        if self.manager.current == 'output_variable':
            # Reset when you go to home
            self.ids.variable_added_output.clear_widgets()
            self.ids.menu_a_tendina_variabili_output.text = ''
            # Reset also the variable of MakeSimulation
            self.manager.get_screen('make_simulation').ids.variable_added.clear_widgets()
            self.manager.get_screen('make_simulation').ids.menu_a_tendina_variabili.text = ''
            self.manager.get_screen('make_simulation').ids.input_value_variable.text = ''
            self.manager.current = 'home'

    def update_form(self):
        self.ids.menu_a_tendina_variabili_output.values = self.manager.get_screen('make_simulation').dict_entita[
            self.ids.menu_a_tendina_entita_output.text]
        self.ids.menu_a_tendina_variabili_output.text = self.ids.menu_a_tendina_variabili_output.values[0]
        self.ids.variable_added_output.clear_widgets()
        # If the selected entity exists
        if self.ids.menu_a_tendina_entita_output.text in self.dict_of_entity_variable_value_output.keys():
            # cycle it
            for tuple in self.dict_of_entity_variable_value_output[
                self.ids.menu_a_tendina_entita_output.text]:
                # add all variable and value of this entity
                self.ids.variable_added_output.add_widget(
                    Button(text=self.ids.menu_a_tendina_entita_output.text + " - " + tuple[0] + " - " + tuple[1],

                           font_size='14sp',
                           on_release=self.destroy_button, background_color=(255, 255, 255, 0.9), color=(0, 0, 0, 1)))

    def exist_tuple(self, dictionary, input_entity, input_variable):
        # dictionary hasn't "input_entity" into its keys
        if not input_entity in dictionary.keys():
            return False
        # Example I add something then I delete it
        elif dictionary[input_entity] == []:
            return False
        else:
            for tuple in dictionary[input_entity]:
                if tuple[0] == input_variable:
                    return True
        # otherwise
        return False

    def add_value_and_reset_form(self):
        # If there are blank value
        if self.ids.menu_a_tendina_variabili_output.text != '':
            # You can't add again a certain variable of a certain entity
            if not self.exist_tuple(self.dict_of_entity_variable_value_output, self.ids.menu_a_tendina_entita_output.text,
                                    self.ids.menu_a_tendina_variabili_output.text):
                # Add button
                self.ids.variable_added_output.add_widget(Button(
                    text=self.ids.menu_a_tendina_entita_output.text + " - " + self.ids.menu_a_tendina_variabili_output.text,
                    on_release=self.destroy_button, background_color=(255, 255, 255, 0.9), color=(0, 0, 0, 1)))

                # CORRADOOOOOOO
                # QUESTA PARTE MI SERVE PER INIZIALIZZARE LE INPUT VARIABLE PER OGNI SITUAZIONE
                # PERCHE' LE AGGIUNTO VOLTA VOLTA, QUINDI SE LE RAGGRUPPAVI IN QUALCHE DICT PUOI ANCHE TOGLIERLO

                self.manager.get_screen('make_simulation').situations[self.ids.menu_a_tendina_entita_output.text].add_variable_to_choosen_output_variables(choosen_output_variable = self.ids.menu_a_tendina_variabili_output.text)
                print self.manager.get_screen('make_simulation').situations[self.ids.menu_a_tendina_entita_output.text ].get_choosen_output_variables()

                # EXAMPLE dict_of_entity_variable_value[Persona] = [reddito_totale,10000,prova,10,prova2,11]
                # inizialize if key is not exists
                if not self.ids.menu_a_tendina_entita_output.text in self.dict_of_entity_variable_value_output.keys():
                    self.dict_of_entity_variable_value_output[self.ids.menu_a_tendina_entita_output.text] = []
                # Add value
                # add name of variable and value
                tuple = [self.ids.menu_a_tendina_variabili_output.text, ""]
                self.dict_of_entity_variable_value_output[self.ids.menu_a_tendina_entita_output.text].append(tuple)

            else:
                i = 0
                # In this case the tuple already exists
                # CORRADOOOOOOO
                # QUESTA PARTE MI SERVE PER INIZIALIZZARE LE INPUT VARIABLE PER OGNI SITUAZIONE
                # PERCHE' LE AGGIUNTO VOLTA VOLTA, QUINDI SE LE RAGGRUPPAVI IN QUALCHE DICT PUOI ANCHE TOGLIERLO
                self.manager.get_screen('make_simulation').situations[self.ids.menu_a_tendina_entita_output.text].add_variable_to_choosen_output_variables(choosen_output_variable = self.ids.menu_a_tendina_variabili_output.text)
                print self.manager.get_screen('make_simulation').situations[self.ids.menu_a_tendina_entita_output.text ].get_choosen_output_variables()

                for el in self.ids.variable_added_output.children:
                    # splitting
                    entity, variable = el.text.split(' - ')
                    # If "entity - variabile" in button text
                    if (self.ids.menu_a_tendina_entita_output.text + " - " + self.ids.menu_a_tendina_variabili_output.text) == (
                            entity + " - " + variable):
                        # update button value
                        self.ids.variable_added_output.children[i].text = entity + " - " + variable
                        break
                    i += 1


            # Reset form
            self.ids.menu_a_tendina_variabili_output.text = self.ids.menu_a_tendina_variabili_output.values[0]

    def destroy_button(self, button):
        # Splitting
        entity, variable = button.text.split(" - ")
        # Find the tuple to delete
        for tuple in self.dict_of_entity_variable_value_output[entity]:
            if tuple[0] == variable:
                # delete from dict
                self.dict_of_entity_variable_value_output[entity].remove(tuple)
                break
        # now i can delete the button
        self.variable_added_output.remove_widget(button)


    def go_to_execute_simulation(self):
        if self.manager.current == 'output_variable':
            #Content of popup
            string_var_input = "The situation is following:\nInput\n"
            for el_input in self.manager.get_screen('make_simulation').ids.variable_added.children:
                string_var_input += "-" + str(el_input.text) + "\n"
            string_var_output = "Output\n"
            for el_output in self.ids.variable_added_output.children:
                string_var_output += "-" + str(el_output.text) + "\n"
            #Create a popup
            content = ConfirmPopup(text=str(string_var_input) + "\n" + str(string_var_output))
            content.bind(on_answer=self._on_answer)
            self.popup = Popup(title="Answer Question", content=content, size_hint=(None, None), size=(480, 400),
                               auto_dismiss=False)
            self.popup.open()

    def _on_answer(self, instance, answer):
        # print "Risposta: " , repr(answer)
        if answer == 'Yes':
            self.manager.get_screen('execute_simulation').run_simulation()
            self.popup.dismiss()
            self.manager.current = 'execute_simulation'
        self.popup.dismiss()

    def go_to_make_simulation(self):
        if self.manager.current == 'output_variable':
            self.manager.current = 'make_simulation'

class ExecuteSimulationScreen(Screen):

    def __init__(self, **kwargs):
        super(ExecuteSimulationScreen, self).__init__(**kwargs)

    def run_simulation(self):
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
        # compute
        simulation_generator.generate_simulation()
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


class LabelLeftTop(Label):
    pass


class ReformsScreen(Screen):
    choice = StringProperty()

    def __init__(self, **kwargs):
        super(ReformsScreen, self).__init__(**kwargs)

    def go_to_home(self):
        if self.manager.current == 'reforms':
            self.manager.current = 'home'

    def go_to_add_variable(self):
        self.manager.get_screen('select_variable_screen').choice = "Add variable"
        self.manager.get_screen('select_variable_screen').inizialize_form()
        self.manager.current = 'form_variable_screen'

    def go_to_update_variable(self):
        self.manager.get_screen('select_variable_screen').choice = "Update variable"
        self.manager.get_screen('select_variable_screen').inizialize_form()
        self.manager.current = 'select_variable_screen'

    def go_to_neutralize_variable(self):
        self.manager.get_screen('select_variable_screen').choice = "Neutralize variable"
        self.manager.get_screen('select_variable_screen').inizialize_form()
        self.manager.current = 'select_variable_screen'


class SelectVariableScreen(Screen):
    choice = StringProperty()

    def __init__(self, **kwargs):
        super(SelectVariableScreen, self).__init__(**kwargs)


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
        else:
            pass

    def _on_answer(self, instance, answer):
        if answer == 'Yes':
            global TAX_BENEFIT_SYSTEM_MODULE_CLASS
            variables_name = []
            for key_variable, variables_content in TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables().iteritems():
                if key_variable == self.ids.id_spinner_select_variable_screen.text:
                    v_r_man = Variable_reform_manager(path_to_save_reform = self.manager.get_screen('visualize_system').dict_path['reforms'], variable = Variable_To_Reform(name = key_variable), reform_name = "neutralize_" + self.ids.id_spinner_select_variable_screen.text)
                    v_r_man.do_reform(TYPEOFREFORMVARIABILE.neutralize_variable)
                    break
            # TODO HERE YOU MUSH NEUTRALIZE VARIABLE, CONTROLLA PRIMA CHE NON SIA GIA NEUTRALIZZATA
        self.popup.dismiss()
        self.popup = Popup(title="Variable neutralized", content = Label(text = "The reform that neutralized\n" + self.ids.id_spinner_select_variable_screen.text + "\nwas written, you can check in the legislation explorer!"), size_hint=(None, None), size=(480, 400),
                           auto_dismiss=True)
        self.popup.open()
        self.manager.current = 'reforms'


class FormVariableScreen(Screen):

    def __init__(self, **kwargs):
        super(FormVariableScreen, self).__init__(**kwargs)

    def setting_up_form_variable(self):
        if self.manager.get_screen('select_variable_screen').choice == "Update variable":
            self.ids.value_type_input.text = self.ids.value_type_input.values[0] #TODO cambia con quella della variabile
            self.ids.entity_input.text = "x" #TODO Mettere dinamicamente l'entità
            self.ids.label_input.text = "x"
            self.ids.definition_period_input.text = self.ids.definition_period_input.values[0]
            self.ids.reference_input.text = "x"
        elif self.manager.get_screen('select_variable_screen').choice == "Add variable":
            self.ids.value_type_input.text = self.ids.value_type_input.values[0]
            self.ids.entity_input.text = "" #TODO Mettere dinamicamente l'entità
            self.ids.label_input.text = ""
            self.ids.definition_period_input.text = self.ids.definition_period_input.values[0]
            self.ids.reference_input.text = ""
        else:
            pass

    def run_operation(self):
        #delete all whitespace
        name_input = self.ids.name_input.text.replace(" ","")
        value_type_input=self.ids.value_type_input.text.replace(" ","")
        entity_input=self.ids.entity_input.text.replace(" ","")
        label_input=self.ids.label_input.text.replace(" ","")
        definition_period_input=self.ids.definition_period_input.text.replace(" ","")
        reference_input=self.ids.reference_input.text.replace(" ","")
        #If there are empty text
        if name_input == "" or value_type_input == "" or entity_input == "" or label_input == "" or definition_period_input == "":
            print "Error"
            return
        if self.manager.get_screen('select_variable_screen').choice == "Update variable":
            #TODO Operazione di aggiornamento
            #Cerca la variabile selezionata (qui sotto troviamo il testo della variabile)
            print "Hai aggiornato "+self.ids.name_input.text
            #Aggiornala
            pass
        elif self.manager.get_screen('select_variable_screen').choice == "Add variable":
            #TODO Operazione di aggiunta
            #Aggiungi la variabile
            print "Hai aggiunto "+self.ids.name_input.text
            pass
        #Print di quello che hai aggiunto/aggiornato
        print " ".join([name_input,
                        value_type_input,
                        entity_input,
                        label_input,
                        definition_period_input,
                        reference_input])

    def go_to_home(self):
        if self.manager.current == 'form_variable_screen':
            #TODO Resetta variabili
            self.manager.current = 'home'



class MyScreenManager(ScreenManager):
    pass


class RigaSelezione(BoxLayout):
    text = StringProperty()


class ConfirmPopup(GridLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass


# App
class openfisca_managing_tool(App):
    def build(self):
        Builder.load_file('./folder_kv/reforms.kv')
        Builder.load_file('./folder_kv/app.kv')
        self.icon = 'img/openfisca.ico'
        self.title = 'Openfisca Managing Tool'
        return MyScreenManager()


# main
if __name__ == '__main__':
    openfisca_managing_tool().run()
