# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class LineOfChooser(BoxLayout):
    name_label = StringProperty()
    def decrementa(self):
        if int(self.ids.value.text) > 0:
            self.ids.value.text = str(int(self.ids.value.text) - 1)

    def incrementa(self):
        self.ids.value.text = str(int(self.ids.value.text) + 1)
