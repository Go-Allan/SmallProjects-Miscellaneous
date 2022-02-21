from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivygui.rules import Style

class StatusBar(BoxLayout, Style):
    def update_status(self, msg, code):
        self.ids.msg.text = msg


class StatusBarApp(App):
    def build(self):
        return StatusBar()

if __name__ == '__main__':
    StatusBarApp().run()
