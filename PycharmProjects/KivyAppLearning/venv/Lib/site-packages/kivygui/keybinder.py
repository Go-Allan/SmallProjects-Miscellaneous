'''
    The kivy way of handling keybinds is nice for working with data.
    The frontent can wait for a backend/core/other program to define
    what ui elements should do when a key is pressed. Great for customizability!

    But for hacking up a simple application that doesn't need this flexibility
    this is less planning and work.

    Limitations: only can do on_key_down right now

'''
from contextlib import suppress
from collections import Iterable

from kivy.core.window import Window
from kivy.uix.behaviors.focus import FocusBehavior

# TODO would be nice to have something like tkinter so binding to any event
# such as mouse down etc can happen throught the same api

# TODO check the keys that are bound match the keys that kivy sends :/

class KeyBindUnRegister(Exception): pass


# TODO kivy has a func like this ??
def _hash_key(hotkey):
    # Order doesn't matter for modifiers, so we force an order here
    # control - shift - alt - win, and when we read back the modifers we spit them
    # out in the same value so our dictionary keys always match
    new_hotkey = []
    if len(hotkey) < 3:
        new_hotkey = [x for x in hotkey]
    else:
        # TODO these modifiers strings are wrong...
        for mod in hotkey[:-1]:
            if 'control' == mod:
                new_hotkey.append(mod)
        for mod in hotkey[:-1]:
            if 'shift' == mod:
                new_hotkey.append(mod)
        for mod in hotkey[:-1]:
            if 'alt' == mod:
                new_hotkey.append(mod)
        for mod in hotkey[:-1]:
            if 'super' == mod:
                new_hotkey.append(mod)
        new_hotkey.append(hotkey[-1])
    # Ensure consistent format for ints
    with suppress(ValueError):
        new_hotkey[-1] = int(hotkey[-1])
    return tuple(new_hotkey)


class FocusMixin():
    def kb_focus_next(self):
        '''Returns True if we could change focus'''
        try:
            self.focus_next.focus = True
            return True
        except AttributeError:
            # Let someone else handle the event
            return False

    def kb_focus_previous(self):
        '''Returns True if we could change focus'''
        try:
            self.focus_previous.focus = True
            return True
        except AttributeError:
            # Let someone else handle the event
            return False



class KeyBinder(FocusBehavior, FocusMixin):
    '''
    Keybind a little more sanely in Kivy
    '''

    def __init__(self, kb_mode=None, **kwargs):
        '''
        kb_mode: see key_bind()
        '''
        # {mode: {key: [functions]}}
        super().__init__(**kwargs)
        self._keybinds_down = {}

        self.kb_mode = kb_mode

    def run_down_funcs(self, mode, hk):
        consumed = False
        try:
            if hk in self._keybinds_down[mode]:
                for func in self._keybinds_down[mode][hk]:
                    if func():
                        consumed = True
            else:
                return False
        except KeyError:
            return False
        else:
            return consumed

    def kb_set_mode(self, mode=None):
        '''
        a mode can be passed when binding / undinding to allow binds to be fired
        only when the mode is set.

        this functions sets the active mode. the default mode is None
        and can be applied by calling this function with no args
        '''
        self.kb_mode = mode


    # This function is called because we have the FocusBehavior
    def keyboard_on_key_down(self, _, keycode, keychar, modifiers):
        keysym = keycode[1]
        hk = _hash_key((*modifiers, keysym))
        consumed = self.run_down_funcs(self.kb_mode, hk)
        if not consumed:
            # Key consumed
            if super().keyboard_on_key_down(_, keycode, keychar, modifiers):
                return True
            else:
                return False
        return True

    def kb_bind(self, hotkey, on_down=None, mode=None) -> int:
        '''
        add a key bind that will run a function

        the same keybind can have multiple callbacks, but only one callback
        can be added per call to this function.

        returns an id that can be used to unregister the function

        The event will be propergated higher up unless one of the callbacks
        for the bind returns True
        '''
        assert on_down
        try:
            assert isinstance(hotkey, Iterable) and type(hotkey) not in (bytes, str)
        except Exception:
            import pdb;pdb.set_trace()
        if not mode:
            mode = self.kb_mode
        hk = _hash_key(hotkey)

        self._keybinds_down.setdefault(mode, {}).setdefault(hk, []).append(on_down)
        return self._keybinds_down[mode][hk].index(on_down)


    def kb_unbind(self, hotkey, on_down_id, mode=None):
        '''
        remove a cb from a key bind given the hotkey and id of the callback
        '''
        assert isinstance(hotkey, Iterable) and type(hotkey) not in (bytes, str)
        if not mode:
            mode = self.kb_mode
        hk = _hash_key(hotkey)

        try:
            self._keybinds_down[mode][hk][on_down_id]
        except KeyError:
            raise KeyBindUnRegister('Keybind does not exist..', mode, on_down_id, *hk)
        del self._keybinds_down[mode][hk][on_down_id]


if __name__ == '__main__':
    # EXAMPLE

    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.uix.gridlayout import GridLayout

    # Note Keybinder inherits from FocusBehavior and MUST be on the left of other widget i.e first subclassed class
    class FocusButton(KeyBinder, Button):
        def on_focus(self, *args):
            if self.focus:
                self.color = (1,1,0,1)
            else:
                self.color = (1,1,1,1)

        # Can intercept calls here like this
        # def keyboard_on_key_down(self, *args):
            # return super().keyboard_on_key_down(*args)

    class MyApp(App):
        def build(self):
            grid = GridLayout(cols=4)
            for i in range(40):
                btn = FocusButton(text=str(i))
                btn.kb_bind(('ctrl', 'alt', 'p'), on_down=lambda: print('esc'))
                # btn.kb_bind((i,), on_down=lambda i=i:print('cb 1 ',i))
                # btn.kb_bind((i,), on_down=lambda i=i:print('cb 2 ', i*2))
                grid.add_widget(btn)
            return grid

    MyApp().run()



