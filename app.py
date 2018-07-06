# -*- coding: utf-8 -*-

import kivy
kivy.require("1.10.0")
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from screens.choose_entity import *
from screens.visualize import *
from screens.make_simulation import *
from screens.output_variable import *
from screens.reform import *
from screens.execute_simulation import *
from screens.init import *
from screens.home import *

class MyScreenManager(ScreenManager):
    pass



# App
class openfisca_managing_tool(App):
    def build(self):
        Builder.load_file('./folder_kv/app.kv')
        Builder.load_file('./folder_kv/init.kv')
        Builder.load_file('./folder_kv/home.kv')
        Builder.load_file('./folder_kv/personalized_widget.kv')
        Builder.load_file('./folder_kv/output_variable.kv')
        Builder.load_file('./folder_kv/execute_simulation.kv')
        Builder.load_file('./folder_kv/make_simulation.kv')
        Builder.load_file('./folder_kv/choose_entity.kv')
        Builder.load_file('./folder_kv/visualize.kv')
        Builder.load_file('./folder_kv/reform.kv')
        self.icon = 'img/openfisca_man.ico'
        self.title = 'Openfisca Managing Tool'
        return MyScreenManager()


# main
if __name__ == '__main__':
    openfisca_managing_tool().run()
