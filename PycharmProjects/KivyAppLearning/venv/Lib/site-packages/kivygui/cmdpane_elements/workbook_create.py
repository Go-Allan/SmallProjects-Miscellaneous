from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from kivygui.keybinder import KeyBinder

import pdb

Y = 40

def add_bind(layout, widget, func, *args, **kwargs):
    '''allows a widget to bind action against the core'''
    if not hasattr(layout, 'mabinds'):
        layout.mabinds = {}
    layout.mabinds[widget] = {'func': func, 'args': args, 'kwargs': kwargs}


class CmdPaneElement():
    def clear_values(self):
        raise NotImplementedError

    def first_focusable(self, x):
        raise NotImplementedError


class WorkbookCreate(BoxLayout, CmdPaneElement):
    def clear_values(self):
        pass

    def insert_values(self, **kwargs):
        '''insert the values into fields for initialization'''
        pass


class SmartText(KeyBinder, TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kb_bind(('tab',), self.tab_pressed)
        self.kb_bind(('shift', 'tab',), self.shift_tab_pressed)

    def tab_pressed(self):
        self.focus_next.focus = True

    def shift_tab_pressed(self):
        self.focus_previous.focus = True


def validate_on_create(name, profile, hotkey):
    if not name:
        return 'A name is required', 0
    elif not profile:
        return 'Please select a Profile', 0
    elif not hotkey:
        return 'A hotkey is required', 0
    return 1, 1


def get_no_process(text):
    if not text:
        return 'Please set a value for Dynamic Note Creation', 0
    elif 'write' in text:
        no_process = 'write'
    elif 'shelve' in text:
        no_process = 'shelve'
    elif 'prompt' in text:
        no_process = 'prompt'
    elif 'read' in text:
        no_process = 'read'
        raise NotImplementedError
    elif 'bookmark' in text:
        no_process = 'bookmark'
    else:
        return 'Invalid value for no process', 0
    return no_process, 1

def get_widget(layout, name:str):
    for widg in layout.children:
        if name == widg.id:
            return widg


def on_create(unc, layout, widget):
    name = get_widget(layout, 'name').text
    profile = get_widget(layout, 'profile').text
    hotkey = [x for x in get_widget(layout, 'hotkey').text.split(' ')]
    msg, code = validate_on_create(name, profile, hotkey)
    if not code:
        unc._unc_status_update(msg, code)
        return
    # TODO - add the no process widget
    # no_process = get_widget(layout, 'no_process').text
    # msg, code = get_no_process(no_process)
    # if not code:
        # unc._unc_status_update(no_process, code)
        # return
    # The no process value has been transformed
    # else:
        # no_process = msg
    no_process = 'write'
    options = {'no_process':no_process}

    unc.req_book_create(profile, name, hotkey,
                        unc.active_profile, **options)


def workbook_create(unc):
    '''
    return a KivyWidget to be added to the cmdpane
    '''
    layout = WorkbookCreate(orientation='vertical',
                            spacing=5)
    # layout.size_hint_y = None
    # layout.height = 700
    # layout.pos_hint = {'top':1}
    # layout.pos_hint_y = None
    label_args = {}
    # label_args = {'height': Y}
    # label_args = {'size_hint_y': None, 'height': Y}
    # label_args = {'pos_hint_y': None, 'size_hint_y': None, 'pos': layout.pos,'height': Y}
    name = SmartText(id='name')
    hotkey = SmartText(id='hotkey')
    profile = SmartText(id='profile')
    name.focus_next = hotkey
    hotkey.focus_next = profile
    profile.focus_next = name
    layout.add_widget(Label(text='Create Workbook', **label_args))
    layout.add_widget(Label(text='Name', **label_args))
    layout.add_widget(name)
    layout.add_widget(Label(text='Hotkey', **label_args))
    layout.add_widget(hotkey)
    layout.add_widget(Label(text='Profile', **label_args))
    layout.add_widget(profile)
    create = Button(text='Create', on_press=lambda x, layout=layout, unc=unc: on_create(unc, layout, x), **label_args)
    # create = Button(text='Create', on_press=lambda x: print('nice'), **label_args)
    layout.add_widget(create)

    layout.first_focusable = lambda: name
    layout.last_focusable = lambda: profile
    return layout


if __name__ == '__main__':
    # EXAMPLE

    from kivy.app import App

    class MyApp(App):
        def build(self):
            return workbook_create()

    MyApp().run()



