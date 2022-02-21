# no!! idk why it worked for a second then flashed away
# this works running in the debugger for some reason but not just when i hit the run button lol
# ie just hit the debugger button instead...
import kivy
kivy.require("1.10.1")
# import main app class from kivy (builds window and does graphics stuff)
from kivy.app import App
# importing widgets and things from kivy to use in our interface
from kivy.uix.button import Button


class Thing(App):
    def build(self):  # initialization method
        return Button(text="Testing")


if __name__ == "__main__":
    thingy = Thing()
    thingy.run()

else:
    print("error")


