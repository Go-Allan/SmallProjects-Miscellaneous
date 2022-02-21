'''
    This module holds configuration settings that will need to be
    mostly set by -> uncrumpled/presenter

    they are simply here because i haven't designed the system
    for config well enough yet, and i'm lazy
'''


class _Config():
    binds = {}
    def setup_config(self):
        self._keyboard = self.window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # self.binds['escape'] = self.window.hide
        # self.binds[('ctrl', 'f')] = self.window.hide


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode, text, modifiers)
        if modifiers:
            key = tuple(modifiers + [keycode[1]])
        else:
            key = keycode[1]
        print(key)
        callback = None
        if not modifiers:
            callback = self.binds.get(key)
        else:
            for k, v in self.binds.items():
                if set(tuple(modifiers + [keycode[1]])) == set(k):
                    callback = v
                    break
        if callback:
            callback()
        return True
