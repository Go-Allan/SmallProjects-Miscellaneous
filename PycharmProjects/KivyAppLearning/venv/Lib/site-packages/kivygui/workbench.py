from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty

from kivygui.rules import Style


class Workbench(FloatLayout, Style):
    visible = BooleanProperty(False)
    def __init__(self, **kwargs):
        super().__init__()

    def toggle(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True


class WorkbenchApp(App):
    def build(self):
        return Workbench()

if __name__ == '__main__':
    WorkbenchApp().run()
