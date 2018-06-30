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
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.graphics import Rectangle, Color


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


class ErrorPopUp(Popup):
    pass


class ConfirmPopup(GridLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass


class Pop(ModalView):
    list=[]
    index = 0
    def __init__(self, title, list=[""], callback=None,
                 width=None, height=None, **kwargs):
        super(Pop, self).__init__(**kwargs)

        self.list = list
        self.callback = callback
        self.auto_dismiss = False
        self.size_hint = (None, None)
        self.preferred_width = width
        self.preferred_height = height

        if self.preferred_width:
            self.width = self.preferred_width
        elif Window.width > 500:  # Big screen?
            self.width = 0.7 * Window.width
        else:
            self.width = Window.width - 2

        self.playout = BoxLayout(orientation='vertical',
                                 padding=["2dp", "5dp",
                                          "2dp", "5dp"],
                                 spacing="5dp")

        self.title = Label(size_hint_y=None,
                           text_size=(self.width - dp(20), None),
                           text=title,
                           halign='left',
                           font_size="16sp",
                           markup=True)

        self.separator = BoxLayout(size_hint_y=None, height="1dp")

        self.pscroll = ScrollView(do_scroll_x=False)

        self.content = Label(size_hint_y=None,
                             text=self.list[0],
                             halign='justify',
                             font_size="16sp",
                             markup=True,
                             text_size=(self.width- dp(20), None))

        self.pbutton = Button(text='Close',
                              size_hint_y=None, height="18dp")
        self.pbutton.bind(on_release=self.close)

        self.buttonforward = Button(text='<',
                              size_hint_y=None, height="18dp")

        self.buttonforward.bind(on_release=self.minus_one_index)
        self.buttonbackward = Button(text='>',
                              size_hint_y=None, height="18dp")
        self.buttonbackward.bind(on_release=self.plus_one_index)

        self.boxlayout_button = BoxLayout(orientation="horizontal")
        self.add_widget(self.playout)
        self.playout.add_widget(self.title)
        self.playout.add_widget(self.separator)
        self.playout.add_widget(self.pscroll)
        self.pscroll.add_widget(self.content)
        self.boxlayout_button.add_widget(self.buttonforward)
        self.boxlayout_button.add_widget(self.buttonbackward)
        self.boxlayout_button.add_widget(self.pbutton)
        self.playout.add_widget(self.boxlayout_button)

        self.title.bind(texture_size=self.update_height)
        self.content.bind(texture_size=self.update_height)

        with self.separator.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.separator.pos,
                                  size=self.separator.size)

        self.separator.bind(pos=self.update_sep,
                            size=self.update_sep)

        Window.bind(size=self.update_width)

    def update_width(self, *args):
        # hack to resize dark background on window resize
        self.center = Window.center
        self._window = None
        self._window = Window

        if self.preferred_width:
            self.width = self.preferred_width
        elif Window.width > 500:  # Big screen?
            self.width = 0.7 * Window.width
        else:
            self.width = Window.width - 2

        self.title.text_size = (self.width - dp(20), None)
        self.content.text_size = (self.width - dp(20), None)

    def update_height(self, *args):
        self.title.height = self.title.texture_size[1]
        self.content.height = self.content.texture_size[1]
        temp = self.title.height + self.content.height + dp(56)
        if self.preferred_height:
            self.height = self.preferred_height
        elif temp > Window.height - dp(40):
            self.height = Window.height - dp(40)
        else:
            self.height = temp
        self.center = Window.center

    def update_sep(self, *args):
        self.rect.pos = self.separator.pos
        self.rect.size = self.separator.size

    def minus_one_index(self, instance):
        if(self.index != 0):
            self.index-=1
        else:
            self.index = len(self.list)-1
        self.content.text = self.list[self.index]
    def plus_one_index(self, instance):
        if(len(self.list)-1 != self.index):
            self.index += 1
        else:
            self.index = 0
        self.content.text = self.list[self.index]
    def close(self, instance):
        self.dismiss(force=True)
        if self.callback:
            self.callback()

