# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.button import Button


class LineOfChooser(BoxLayout):
    name_label = StringProperty()
    def decrementa(self):
        if int(self.ids.value.text) > 0:
            self.ids.value.text = str(int(self.ids.value.text) - 1)

    def incrementa(self):
        self.ids.value.text = str(int(self.ids.value.text) + 1)

class LabelLeftTop(Label):
    pass


class RigaSelezione(BoxLayout):
    text = StringProperty()


class ButtonReforms(Button):
    pass


class ModifyFormulaPopup(Popup):
    def __init__(self, screen_manager = None , **kwargs):
        super(ModifyFormulaPopup, self).__init__(**kwargs)
        if (screen_manager is None) or not (isinstance(screen_manager, ScreenManager)) :
            raise TypeError("You have to insert a screen manager to instantiate a Modify Formula Popup")
        else:
            self.screen_manager = screen_manager
        Clock.schedule_once(self._finish_init)


    def _finish_init(self,dt):
        if not(self.screen_manager.get_screen("form_variable_screen").formula_to_write_in_popup is None):
            self.ids.txt_modify_formula.text = "" + self.screen_manager.get_screen("form_variable_screen").formula_to_write_in_popup
        else:
            self.ids.txt_modify_formula.text = ""
        self.open()


    def update_lines_basing_on(self, *args):
        self.screen_manager.get_screen('form_variable_screen').formula_to_write_in_popup = args[0]


class WatchingFormulaPopUp(Popup):
    pass


class ConfirmPopup(GridLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass
