from os.path import join
import importlib
from typing import Callable
from contextlib import suppress

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.behaviors import FocusBehavior
from kivy.properties import BooleanProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput

from timstools import make_class_name

from kivygui.rules import Style
from kivygui.keybinder import KeyBinder
import kivygui.cmdpane_elements as elements

class DisplayArea(ScreenManager):
    def goto_homepage(self):
        self.current = self.rvscreen.name


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    # TODO Tab switching between the searchitems..
    # def __init__(self, **kwargs):
        # super().__init__(**kwargs)
        # self.kb_bind(('tab',), self.tab_pressed)
        # self.kb_bind(('shift', 'tab',), self.shift_tab_pressed)

    # def tab_pressed(self):
        # import pdb;pdb.set_trace()
        # self.focus_next.focus = True

    # def shift_tab_pressed(self):
        # import pdb;pdb.set_trace()
        # self.focus_previous.focus = True

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            # Focus searchbox on touch
            self._proxy_ref.parent.parent.parent.parent.parent.searchbox.focus = True
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, node, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

class RVScreen(Screen): pass

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

class SearchBox(KeyBinder, TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kb_bind(('down',), self.go_down)
        self.kb_bind(('up',), self.go_up)
        self.kb_bind(('enter',), self.enter_pressed)
        self.kb_bind(('tab',), self.tab_pressed)
        self.kb_bind(('shift', 'tab',), self.shift_tab_pressed)

        #TODO on click focus the item

    def tab_pressed(self):
        self.kb_focus_next()
        # Always consume the event
        return True

    def shift_tab_pressed(self):
        self.kb_focus_previous()
        # Always consume the event
        return True

    def go_down(self):
        self.set_active(1)

    def go_up(self):
        self.set_active(-1)

    def _get_selected(self) -> int:
        '''return node of the selected item or -1 if nothing'''
        selecter = self.recycleview.layout_manager
        try:
            return selecter.selected_nodes[0]
        except IndexError:
            return -1

    def set_active(self, offset):
        rv = self.recycleview
        max_index = len(rv.data) - 1
        selected = self._get_selected()
        # Nothing selected
        if selected == -1:
            if max_index < 0:
                return
            elif offset == 1:
                new_pos = 0
            else:
                new_pos = max_index
        # Something selected
        else:
            new_pos = offset + selected
            # loop back_around
            if offset == 1 and new_pos > max_index:
                new_pos = 0
            elif offset == -1 and new_pos < 0:
                new_pos = max_index

        rv.layout_manager.select_node(new_pos)
        self.displayarea.goto_homepage()

    def item_select_init(self):
        ''' Initalize selection to first item if nothing selected '''
        if self._get_selected() == -1:
            self.recycleview.layout_manager.select_node(0)

        # set the focusable elements

    def enter_pressed(self):
        selected = self._get_selected()
        with suppress(IndexError):
            heading = self.recycleview.data[selected]['text'].splitlines()[0]
            self.app.unc.req_cmdpane_item_open(heading)

class TimsBuilder():
    def __init__(self, clean: Callable):
        self.clean = clean

    def get(self, unc, ui: str, element: str):
        ''' get a ui and build it '''
        # Clean anything
        self.clean()
        # Import some element somehow
        builder_function = getattr(elements, ui)
        # kivy_obj = builder_function(self.app.unc)
        kivy_obj = builder_function(unc)
        return kivy_obj

    def screen_get(self, manager, element: str):
        '''get an existing screen given its name, or None'''
        for screen in manager.screens:
            if screen.name == element:
                return screen
        return False

    def screen_make(self, manager, kivy_obj, name: str):
        '''add an object to the given manager with name'''
        screen = Screen(name=name)
        layout = AnchorLayout(anchor_y='top')
        layout.add_widget(kivy_obj)
        screen.add_widget(layout)
        manager.add_widget(screen)

        from kivy.graphics import Color, Rectangle
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        with layout.canvas.before:
            Color(0, 1, 0, 1) # green; colors range from 0-1 instead of 0-255
            layout.rect = Rectangle(size=layout.size,
                                    pos=layout.pos)

        # listen to size and position changes
        # layout.size_hint = (None, None)
        layout.bind(pos=update_rect, size=update_rect)
        return screen


class CommandPane(KeyBinder, FloatLayout, Style):
    visible = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tb = TimsBuilder(clean=self._clear_list)

        Clock.schedule_once(lambda e: self.setup_binds(), 1)

    def setup_binds(self):
        # TODO plug system
        self.searchbox.kb_bind(('escape',), self.toggle)
        self.searchbox.kb_bind(('ctrl', 'spacebar'), self.toggle)

    def toggle(self):
        '''
        toggle the cmd pane open or close
        '''
        if self.visible:
            self.visible = False
            self.parent.ids.editor.focus_current()
        else:
            self.visible = True
            self.searchbox.focus = True

        # Consume the event
        return True

    # @rate_limited(1) TODO this is already fucking up because of async.... wait till async is not bugging..

    # TODO how to use lru_cache with async...
    def search(self):
        '''
        query the uncrumpled core for results from a search
        and display them
        '''
        query = self.searchbox.text
        if query:
            # This request results in a call to display_search_results
            print('doing search request')
            self.app.unc.req_cmdpane_search(query)
            self.searchbox.item_select_init()
            self.displayarea.goto_homepage()

    def display_search_results(self, headings, bodies):
        bodies = map(lambda x: x if x else '', bodies)
        self.recycleview.data = [{'text': '{}\n{}'.format(h, b)}
                                    for h, b in zip(headings, bodies)]

    def _clear_list(self):
        self.recycleview.data = []

    def ui_build(self, ui):
        ''' get a ui and build it '''
        kivy_obj = self.tb.get(self.app.unc, ui, ui)
        screen = self.tb.screen_get(self.displayarea, ui)

        # Create a New Screen
        if not screen:
            screen = self.tb.screen_make(self.displayarea, kivy_obj, ui)
        # Display an exisiting
        else:
            self.displayarea.current = ui
            kivy_obj.clear_values()

        self.displayarea.current = ui

        # set the focusable elements
        self.searchbox.focus_next = screen.children[0].children[0].first_focusable()
        self.searchbox.focus_previous = screen.children[0].children[0].last_focusable()
        screen.children[0].children[0].first_focusable().focus_previous = self.searchbox

class CmdPane(App):
    def build(self):
        return CommandPane()

if __name__ == '__main__':
    CmdPane().run()
