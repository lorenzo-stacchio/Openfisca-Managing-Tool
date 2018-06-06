import kivy
kivy.require("1.10.0")
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class HomeScreen(PageLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(HomeScreen, self).__init__(**kwargs)
        self.ids.home_file_chooser.path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    # to access elements in .kv self.ids.idrobatua
    def selected_file(self,*args): #in args ci sta il filepath di openfisca scelto
        try: print args[1][0]
        except: pass

class openfisca_managing_tool(App):
    def build(self): #metodo che ci sta sempre nell'app
        self.load_kv('screens\home_screen.kv')
        return HomeScreen()

if __name__ == '__main__':
    openfisca_managing_tool().run()
