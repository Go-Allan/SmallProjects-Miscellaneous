# TODO refactor this shit
# TODO signal_defocus needs to be called from select_tab

'''
TODO

Uncrumpeld Settings should be able to be dependant on the
same rules for our note settings.

Settings files are just files with a setting extension.
Default behavior is coded in vim?
What does this mean for Non text settings viewers?
The plus is that the settings are customizable from text
and we have all the power that comes with that
'''
import logging
import io
from pprint import pformat
import webbrowser
import json
from collections import defaultdict

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.clock import Clock

from kivygui.keybinder import KeyBinder

_welcome='''
        [size=70][font=Inconsolata]uncrumpled[/font][/size]

        Welcome to the latest version of Uncrumpled.
        If you are new please check out the Online `Docs`
        You can also use the `Command Pane` for quick
        help on anything in Uncrumpled `Ctrl + Space`

        If you run into any problems please report them on `Github`!
        '''

class MultiLineLabel(Label):
    def __init__(self, **kwargs):
        super(MultiLineLabel, self).__init__( **kwargs)
        self.markup = True
        self.text_size = self.size
        self.bind(size= self.on_size)
        self.bind(text= self.on_text_changed)
        self.size_hint_y = None # Not needed here

    def on_size(self, widget, size):
        self.text_size = size[0], None
        self.texture_update()
        if self.size_hint_y == None and self.size_hint_x != None:
            self.height = max(self.texture_size[1], self.line_height)
        elif self.size_hint_x == None and self.size_hint_y != None:
            self.width  = self.texture_size[0]

    def on_text_changed(self, widget, text):
        self.on_size(self, self.size)


class UncrumpledEditor(TabbedPanel):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.pageref = {}
        self.settingsref = {}

    # file = None # type: str
    # welcome_text = StringProperty(_welcome)
    # def open_link(link):
        # webbrowser.open(link)
    # def on_touch_down(self, touch):
        # if super().on_touch_down(touch):
            # print('true')
            # return True
        # Select the widget..
        # else:
            # self.get_current().focus = True
            # return True

    def unc_page_load(self, file):
        logging.info('unc_page_load '+ file)
        tab_id = self.pageref.get(file)
        if tab_id == None:
            page = Page(self, file)
        else:
            page = tab_id.content
        self.do_load(page, tab_id)
        self.focus_current()

    def unc_page_close(self, file):
        '''
        Close the tab containing the file
        '''
        logging.info('unc_page_close '+ file)

        widget = self.pageref.get(file).content

        # Save and what not
        widget.on_remove()

        # Remove the tab
        tab = self.pageref.pop(file)
        self.remove_widget(tab)

    def do_load(self, widget, tab):
        '''
        open a tab and load the file
        alternativley switch to the tab if the file is already open
        '''
        # Create a new tab
        if not tab:
            widget.on_load()
            # TODO plug system
            widget.kb_bind(('ctrl', 'spacebar'), self.app.unc._unc_cmdpane_toggle)

            self.insert_widget(widget)

            widget.on_tab_change()

            tab = self.tab_list[0]
            self.switch_to(tab)

            widget.add_tab_id(tab)
        # Swith to existing tab
        else:
            self.switch_to(tab)
            widget.on_tab_change()

    def unc_page_settings_view(self, settings):
        ''' Switch to or pen a settings viewer '''
        import pdb;pdb.set_trace()
        logging.info('unc_page_settings_view')
        file = settings['UFile']
        tab_id = file + 'settings_viewer'
        tab = self.pageref.get(tab_id)
        if tab == None:
            page = SettingsViewer(self, settings)
        else:
            page = tab.content
        self.do_load(page, tab)
        # TODO this should be called from backend
        self.focus_current()

    def page_settings_close(self, data):
        '''
        Close a settings file
        '''
        import pdb;pdb.set_trace()

    def insert_widget(self, widget):
        th = TabbedPanelHeader()
        th.text = str(len(self.tab_list))
        th.content = widget
        widget.on_insert(th)
        self.add_widget(th)

    def on_page_settings_closed(self):
        # TODO BIND ON_DELETE TO CALL THIS
        del self.pageref['settings_viewer']

    def get_active_widget(self):
        '''return active widget or None if no widget in tab,
        no widget currently happens on startup...'''
        return self.current_tab.content

    def focus_current(self):
        widg = self.get_active_widget()
        if widg:
            widg.focus = True
        # Focus the editor instead
        else:
            self.focus = True

    def current_file(self):
        return self.get_active_widget().data


class EmbedInEditor(KeyBinder, TextInput):
    def __init__(self, tabbedpanel, data, **kwargs):
        super().__init__(**kwargs)
        self.tp = tabbedpanel
        self.data = data


class Page(EmbedInEditor):
    def on_remove(self):
        # Save
        with open(self.data, 'w') as f:
            f.write(self.text)

    def on_load(self):
        def set_text(data):
            self.text = data

        with open(self.data, 'r') as f:
            data = f.read()
            # Errors out sometimes without schedule_once...
            # This means we require a delay on hotkey presses otherwise
            # a dirty state could be picked up and saved inbetween
            Clock.schedule_once(lambda _: set_text(data))

    def on_tab_change(self):
        ''' we let uncrumpled know a window has lost focus'''
        if self.tp.tab_list and len(self.tp.tab_list) > 1:
            file = self.tp.current_tab.uncrumpled_file
            self.tp.app.unc.req_page_deactivate(file)

    def on_insert(self, tab):
        # add a backlink
        tab.uncrumpled_file = self.data

    def add_tab_id(self, tab):
        self.tp.pageref[self.data] = tab

    # def keyboard_on_key_down(self, _, keycode, *args):
        # k = self.interesting_keys.get(keycode[0])
        # Let binds be handled by plugins above #TODO
        # if k:
            # super().keyboard_on_key_down(_, keycode, *args)
            # Consume
            # return True

        # Let editor handle as normal insert
        # return False

class SettingsViewer(EmbedInEditor):
    '''
    A hacked up settings editor
    '''
    def on_load(self):
        # TODO see Clock and rate limiting  for Page.on_load
        groups = defaultdict(list)
        for title, attrs in self.data.items():
            lines = groups[title]
            lines.append('_____________')
            # Order the individual settings in a group
            _section = ( k + ' => ' + json.dumps(v) for k,v in attrs.items())
            for x in sorted(_section):
                lines.append(x)
            lines.append('')
            lines.append('')

        ordered_groups = []
        # Order the groups
        profile = groups.get('profile_settings')
        if profile:
            profile.insert(0, 'Profile')
            ordered_groups.append(profile)
        book = groups.get('book_settings')
        if book:
            book.insert(0, 'Book')
            ordered_groups.append(book)
        page = groups.get('page_settings')
        if page:
            page.insert(0, 'Page')
            ordered_groups.append(page)

        flat = []
        for group in ordered_groups:
            for line in group:
                flat.append(line)

        self.text = '\n'.join(flat)

    def on_tab_change(self):
        ''' Automatically saves and sources the files,
        TODO We should probably hook into vims autocomands???
        Texteditor type tihings like settings viewers
        could be programmed as vim plugins...'''
        # uncrumpled backend should know if ANY file is open, allows customizable behavior, first make sure we have some use cases
        # print('on tab change')
        # import pdb;pdb.set_trace()
        pass

    def on_insert(self, tab):
        # add a backlink
        tab.uncrumpled_file = 'settings_viewer'
        pass

    def add_tab_id(self, tab):
        self.tp.pageref['settings_viewer'] = tab

class EditorApp(App):
    def build(self):
        return UncrumpledEditor()

if __name__ == '__main__':
    EditorApp().run()
