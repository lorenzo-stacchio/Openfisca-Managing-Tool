
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

class ChooseEntityScreen(Screen):

    def __init__(self, **kwargs):
        super(ChooseEntityScreen, self).__init__(**kwargs)
        self.number_of_entity = {}
        self.entity_box_layout = BoxLayout(orientation='vertical', padding=(50,50,50,50))
        self.add_widget(self.entity_box_layout)


    def init_content_screen(self):
        self.type_of_entity = getattr(common_modules.ENTITY_MODULE_CLASS, common_modules.ENTITY_MODULE_CLASS_ALL_ENTITIES)
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


