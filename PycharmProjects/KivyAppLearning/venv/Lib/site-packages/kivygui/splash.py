import os

import kivy
# kivy.require('1.0.6')
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty

from kivygui.rules import Style
from kivy.clock import Clock


class SplashPage(Screen, Style):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.imgdir = os.path.dirname(__file__)

    def img(self, file):
        return os.path.join(self.imgdir, file)


class SplashApp(App):
    def build(self):
        return SplashPage()

if __name__ == '__main__':
    SplashApp().run()
