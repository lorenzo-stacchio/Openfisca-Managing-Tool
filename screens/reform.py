import kivy
kivy.require("1.10.0")
import json
import os
import sys
import importlib
import datetime
from functools import partial
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
import os, sys
from folder_screen_widgets.personalized_widget import *

from screens import *

from folder_screen_widgets.personalized_widget import *
from script.interpeters.reforms_file_interpeter import *
from script.reforms_maker.reform_variables import *
from folder_screen_widgets.personalized_widget import *
import common_modules

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
        self.manager.get_screen('select_variable_screen').ids.id_text_search_box.disabled = False
        self.manager.get_screen('select_variable_screen').ids.id_spinner_select_variable_screen.disabled = False
        self.manager.get_screen('select_variable_screen').ids.id_input_reform_description.text = ""
        self.manager.get_screen('select_variable_screen').ids.id_spinner_select_variable_screen.text = ""
        self.manager.get_screen('select_variable_screen').ids.id_input_reform_name.text = ""
        self.manager.get_screen('select_variable_screen').inizialize_form()
        self.manager.current = 'select_variable_screen'

    def go_to_neutralize_variable(self):
        self.manager.get_screen('select_variable_screen').choice = "Neutralize variable"
        self.manager.get_screen('select_variable_screen').ids.id_text_search_box.disabled = False
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
        if(common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS):
            variables_name = []
            if self.ids.id_text_search_box != "":
                dict = common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables().iteritems()
                for key_variable, variables_content in dict:
                    if (self.ids.id_text_search_box.text.lower() in key_variable.lower()):
                        variables_name.append(key_variable)
            elif self.previous_text_typed.lower() in self.ids.id_text_search_box.lower():
                for key_variable in self.ids.id_spinner_select_variable_screen.values:
                    if(self.previous_text_typed not in key_variable):
                        variables_name.remove(key_variable)
            else:
                dict = common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables().iteritems()
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
        variables_name = []
        for key_variable, variables_content in common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables().iteritems():
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
            variables_name = []
            for key_variable, variables_content in common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables().iteritems():
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
        list_of_type_entity = getattr(common_modules.ENTITY_MODULE_CLASS, common_modules.ENTITY_MODULE_CLASS_ALL_ENTITIES)
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
            vars = common_modules.TAX_BENEFIT_SYSTEM_MODULE_CLASS().get_variables()
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

