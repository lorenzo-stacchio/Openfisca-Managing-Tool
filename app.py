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
import os
from script.get_parameters_reforms_tests_variables_folder_paths import *
# Screen

PATH_OPENFISCA = ""

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
                 self.manager.get_screen('home'). __path_ricevuto__(PATH_OPENFISCA)
        else:
            print "Path errato"
            self.ids.lbl_txt_2.text = "The selected directory doesn't \n contain an openfisca regular system"
            # TODO: cambiare colore quando si sbaglia directory e ridimensionare label


class HomeScreen(Screen):

    def __init__(self,**kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self,dt):
        pass

    def __path_ricevuto__(self,path):
        dict = get_all_paths(path)
        print dict


class VisualizeSystemScreen(Screen):

    def __init__(self,**kwargs):
        super(VisualizeSystemScreen, self).__init__(**kwargs)


class MyScreenManager(ScreenManager):
    pass


# App
class openfisca_managing_tool(App):
    def build(self):
        Builder.load_file('app.kv')
        return MyScreenManager()

# main
if __name__ == '__main__':
    openfisca_managing_tool().run()
