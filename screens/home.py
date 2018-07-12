import kivy
kivy.require("1.10.0")
from kivy.uix.screenmanager import ScreenManager, Screen
from script.get_parameters_reforms_tests_variables_folder_paths import *

class HomeScreen(Screen):
    """
    Home screen where i can choose all func of OpenFisca managing tool
    """
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def ricevi_inizializza_path(self,*args):
        """
        Inizialize path
        :param args:
        :return:
        """
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
        """
        Go to visualized tax and system benefit
        :return:
        """
        if self.manager.current == 'home':
            self.manager.current = 'visualize_system'

    def go_to_reforms(self):
        """
        Go to manage a reform(s)
        """
        if self.manager.current == 'home':
            self.manager.current = 'reforms'

    def go_to_simulation(self):
        """
        Go to make a simulation
        """
        if self.manager.current == 'home':
            self.manager.get_screen('choose_entity').init_content_screen()
            self.manager.current = 'choose_entity'

