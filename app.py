# -*- coding: utf-8 -*-

import kivy
kivy.require("1.10.0")
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager  import ScreenManager,Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty,ObjectProperty
from kivy.utils import get_color_from_hex
from kivy.graphics import Rectangle, Color
from kivy.uix.progressbar import ProgressBar
import os,sys
from script.get_parameters_reforms_tests_variables_folder_paths import *
from script.interpeters.variables_file_interpeter import *
from script.interpeters.parameters_interpeter import *
from script.interpeters.reforms_file_interpeter import *
from kivy.config import Config
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty

# Screen
class InitScreen(Screen):

    def __init__(self,**kwargs):
        super(InitScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        #Builder.load_file("screens\init_screen_folder\init_screen_body.kv")
        self.ids.home_file_chooser.path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    def selected_file(self,*args): #in args ci sta il filepath di openfisca scelto
        PATH_OPENFISCA = args[1][0]
        #self.manager.get_screen('home').ids.btn_visual_system.text = PATH_OPENFISCA
        dict = get_all_paths(PATH_OPENFISCA)
        if dict:
            if self.manager.current == 'init':
                 self.manager.current = 'home'
                 self.manager.get_screen('visualize_system').ricevi_inizializza_path(PATH_OPENFISCA)
                 self.manager.get_screen('home').ricevi_inizializza_path(PATH_OPENFISCA)
        else:
            #print "Path errato"
            self.ids.lbl_txt_2.text = "[u][b]The selected directory doesn't \n contain an openfisca regular system[/b][/u]"


class HomeScreen(Screen):


    def __init__(self,**kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def ricevi_inizializza_path(self,path):
        self.dict_path = get_all_paths(path)
        self.ids.label_0_0.text = """[color=000000]
[b][size=24sp]Hello ![/size][/b]\n
[size=20sp]Thanks for installing [size=20sp][b]OpenFisca Tool Manager[/b][/size]!\n
This software will help you to manage some feature provided by OpenFisca, in particular you can:
    - Visualize variables, reforms and parameters of the selected country;
    - Create and Execute a reform;
    - Execute a Simulation.
You have selected this folder: [i]"""+path[:path.rindex('\\')+1]+"[b]"+os.path.basename(path)+"[/i][/b]"+".[/color][/size]\n\n"


    def go_to_visualize(self):
        if self.manager.current == 'home':
             self.manager.current = 'visualize_system'

    def go_to_reforms(self):
        if self.manager.current == 'home':
             self.manager.current = 'reforms'

    def go_to_simulation(self):
        if self.manager.current == 'home':
            self.manager.current = 'choose_entity'


class ChooseEntityScreen(Screen):
    type_of_entity = ['Persona','Famiglia']
    def __init__(self,**kwargs):
        super(ChooseEntityScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        for entity in self.type_of_entity:
            #TOFIX self.ids.id_box_layout_choose.add_widget(Label(text=entity))

class VisualizeSystemScreen(Screen):
    dict_path = ''
    PATH_OPENFISCA = ''

    def __init__(self,**kwargs):
        super(VisualizeSystemScreen, self).__init__(**kwargs)

    def ricevi_inizializza_path(self,path):
        self.dict_path = get_all_paths(path)
        self.PATH_OPENFISCA = self.dict_path['inner_system_folder']
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


    def file_allowed(self,directory,filename):
        filename, file_extension = os.path.splitext(filename)
        return ((file_extension in ['.py','.yaml'] and not(os.path.basename(filename) == '__init__')) or (os.path.isdir(os.path.join(directory, filename))))


    def __check_path__(self,path_file_scelto):
        path_file_scelto = str(os.path.normpath(path_file_scelto))
        path_variable = str(os.path.normpath(self.dict_path['variables']))
        path_reforms = str(os.path.normpath(self.dict_path['reforms']))
        path_parameter = str(os.path.normpath(self.dict_path['parameters']))
        if (path_variable in path_file_scelto) or (path_parameter in path_file_scelto) or (path_reforms in path_file_scelto):
            #print "Path ok"
            return True
        else:
            self.ids.visualize_file_chooser_variables.path = self.dict_path['variables']
            self.ids.visualize_file_chooser_parameters.path = self.dict_path['parameters']
            self.ids.visualize_file_chooser_reforms.path = self.dict_path['reforms']
            self.ids.document_variables_viewer.source = "messages\\file_not_allowed.rst"
            self.ids.document_parameters_viewer.source = "messages\\file_not_allowed.rst"
            self.ids.document_reforms_viewer.source = "messages\\file_not_allowed.rst"
            return False


    def selected_file(self,*args):
        # clear document viewer
        self.ids.document_variables_viewer.source = ""
        self.ids.document_parameters_viewer.source = ""
        self.ids.document_reforms_viewer.source = ""
        try:
            path_file_scelto = args[1][0]
            if self.__check_path__(path_file_scelto):
                filename, file_extension = os.path.splitext(path_file_scelto)
                # the file could be a parameter or a variable
                if file_extension =='.yaml':
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
                elif file_extension =='.py':
                    variable_interpeter = Variable_File_Interpeter(path_file_scelto, openfisca_system_path = self.PATH_OPENFISCA )
                    reform_interpeter = Reform_File_Interpeter(path_file_scelto, openfisca_system_path = self.PATH_OPENFISCA )
                    if (variable_interpeter.file_is_a_variable() and not(reform_interpeter.file_is_a_reform())):
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
                else: # file for which the interpretation is not defined yet
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

    def __init__(self,**kwargs):
        super(MakeSimulation, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self,dt):
        self.dict_entita = {
    		"Persona" : ['','Pluto','Paperino','Aldo','Rodo'],
    		"Prova1" : ['','blablabla1'],
    		"Prova2" : ['','blablabla2'],
    		"Prova3" : ['','blablabla3']
    	}
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
    - You can't insert a blank variable value
            """

    def update_spinner(self):
        #print "Hai selezionato "+self.ids.menu_a_tendina_entita.text
        self.ids.menu_a_tendina_variabili.values = self.dict_entita[self.ids.menu_a_tendina_entita.text]
        self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]

    def go_to_home(self):
        if self.manager.current == 'make_simulation':
            #Reset when you go to home
            self.ids.variable_added.clear_widgets()
            self.ids.menu_a_tendina_variabili.text = ''
            self.ids.input_value_variable.text = ''
            #Go to home
            self.manager.current = 'home'

    def go_to_output_variables(self):
        if self.manager.current == 'make_simulation':
            #you can't go to output variable if you haven't insert nothing
            if len(self.ids.variable_added.children)!=0:
                #change transition
                self.manager.transition  = kivy.uix.screenmanager.SlideTransition(direction='left')
                self.manager.transition.duration = 1
                #Go to output_variable
                self.manager.current = 'output_variable'
                #reset transition
                self.manager.transition  = kivy.uix.screenmanager.TransitionBase()
                self.manager.transition.duration = .4

    def add_value_and_reset_form(self):
        if self.ids.menu_a_tendina_variabili.text != '' and self.ids.input_value_variable.text != '':
            self.ids.variable_added.add_widget(Button(text=self.ids.menu_a_tendina_entita.text+" - "+self.ids.menu_a_tendina_variabili.text+" - "+self.ids.input_value_variable.text,
                                                        on_release=self.destroy_button, background_color = (255,255,255, 0.9), color = (0,0,0,1)))
            self.ids.menu_a_tendina_variabili.text = self.ids.menu_a_tendina_variabili.values[0]
            self.ids.input_value_variable.text = ''

    def destroy_button(self,button):
        self.variable_added.remove_widget(button)


class OutputVariableScreen(Screen):

    string_var_input = ""
    string_var_output = ""
    variable_added_output = ObjectProperty()

    def __init__(self,**kwargs):
        super(OutputVariableScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self,dt):
        valori = ['','Pluto','Paperino','Aldo','Rodo']
        self.ids.menu_a_tendina_variabili_output.values = valori
        self.ids.menu_a_tendina_variabili_output.text = valori[0]
        self.ids.information.text = """
[b]Instructions[/b]:
    - Select a variable
    - Insert into the text input form its value
    - Click on "Add Variable"

[b]Rules[/b]:
    - You can't insert a blank variable
    - You can't insert a blank variable value
            """

    def go_to_home(self):
        if self.manager.current == 'output_variable':
            #Reset when you go to home
            self.ids.variable_added_output.clear_widgets()
            self.ids.menu_a_tendina_variabili_output.text = ''
            self.ids.input_value_variable_output.text = ''
            #Reset also the variable of MakeSimulation
            self.manager.get_screen('make_simulation').ids.variable_added.clear_widgets()
            self.manager.get_screen('make_simulation').ids.menu_a_tendina_variabili.text = ''
            self.manager.get_screen('make_simulation').ids.input_value_variable.text = ''
            self.manager.current = 'home'

    def go_to_execute_simulation(self):
        if self.manager.current == 'output_variable':

            string_var_input = "The situation is following:\nInput\n"
            for el_input in self.manager.get_screen('make_simulation').ids.variable_added.children:
                string_var_input += "-"+str(el_input.text)+"\n"
            string_var_output = "Output\n"
            for el_output in self.ids.variable_added_output.children:
                string_var_output += "-"+str(el_output.text)+"\n"
            content = ConfirmPopup(text=str(string_var_input)+"\n"+str(string_var_output))
            content.bind(on_answer=self._on_answer)
            self.popup = Popup(title="Answer Question",content=content,size_hint=(None, None),size=(480,400),auto_dismiss= False)
            self.popup.open()

    def _on_answer(self, instance, answer):
        #print "Risposta: " , repr(answer)
        if answer == 'Yes':
            self.manager.current = 'execute_simulation'
        self.popup.dismiss()

    def add_value_and_reset_form(self):
        if self.ids.menu_a_tendina_variabili_output.text != '' and self.ids.input_value_variable_output.text != '':
            self.ids.variable_added_output.add_widget(Button(text=self.ids.menu_a_tendina_variabili_output.text+": "+self.ids.input_value_variable_output.text,
                                                        on_release=self.destroy_button, background_color = (255,255,255, 0.9), color = (0,0,0,1)))
            self.ids.menu_a_tendina_variabili_output.text = self.ids.menu_a_tendina_variabili_output.values[0]
            self.ids.input_value_variable_output.text = ''

    def destroy_button(self,button):
        self.variable_added_output.remove_widget(button)




class ExecuteSimulationScreen(Screen):
    def __init__(self,**kwargs):
        super(ExecuteSimulationScreen, self).__init__(**kwargs)


class LabelLeftTop(Label):
    pass

class ReformsScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass


class RigaSelezione(BoxLayout):
    text = StringProperty()



class ConfirmPopup(GridLayout):
	text = StringProperty()

	def __init__(self,**kwargs):
		self.register_event_type('on_answer')
		super(ConfirmPopup,self).__init__(**kwargs)

	def on_answer(self, *args):
		pass


# App
class openfisca_managing_tool(App):
    def build(self):
        Builder.load_file('app.kv')
        self.icon = 'openfisca.ico'
        self.title = 'Openfisca Managing Tool'
        return MyScreenManager()

# main
if __name__ == '__main__':
    openfisca_managing_tool().run()
