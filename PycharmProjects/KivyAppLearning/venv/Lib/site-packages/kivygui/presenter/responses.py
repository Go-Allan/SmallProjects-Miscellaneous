'''
    resposnes from uncrumpled invoke methods defined here.
    if we can, delegate to a widget that handles the response
    some response types don't have widget and so are defined here
    e.g bind_add
'''
import logging
import json
from pprint import pprint
import sys
from contextlib import suppress

from peasoup import pidutil


def _run_bind(unc, callback_string):
    def _():
        ''' The order of checking is important '''
        # TODO plugin architecture..
        # The problem arises when bind req and resp have the same name
        # - Not all response handlers should be callable...
        # - cmdpane_toggle should be but some others not...
        # - find a solution that reducers complexity
        callback = callback_string.split('(')[0]
        # The callback must be meant for the core...
        if hasattr(unc, 'req_' + callback):
            eval('unc.req_' + callback_string)
        # Nope was meant as a response
        else:
            eval('unc._unc_' + callback_string)
    return _


class Responses():
    '''run the responses from uncrumpled'''
    def _unc_bind_add(self, hotkey, event_type, command, command_kwargs):
        hotkey = json.loads(hotkey)
        assert event_type in self.supported_bind_handlers
        command_str = '{cmd}(**{kwargs})'.format(cmd=command,
                                                 kwargs=command_kwargs)
        self.kb_bind(hotkey, _run_bind(self, command_str))

    def _unc_bind_remove(self, hotkey, event_type, command):
        import pdb;pdb.set_trace()

    def _unc_cmdpane_search_results(self, headings, bodies):
        self.ids.commandpane.display_search_results(headings, bodies)

    def _unc_cmdpane_ui_build(self, ui):
        self.ids.commandpane.ui_build(ui)

    def _unc_cmdpane_toggle(self):
        self.ids.commandpane.toggle()

    def _unc_status_update(self, msg, code):
        self.ids.statusbar.update_status(msg, code)

    def _unc_window_show(self):
        logging.info('unc_window_show')
        self.window.show()
        if 'linux' in sys.platform:
            with suppress(AttributeError):
                pidutil.move_active_window(*self._last_dims)

    def _unc_window_hide(self): #TODO
        '''hide the window, also tell uncrumpled all the pages we closed'''
        logging.info('unc_window_hide')
        if 'linux' in sys.platform:
            self._last_dims = pidutil.get_active_window_pos()
        self.window.hide()

    def _unc_welcome_screen(self):
        logging.warning('unc_welcome_screen')
        # self.unc_welcome_screen()

    def _unc_page_load(self, file):
        self.ids.editor.unc_page_load(file)

    def _unc_page_close(self, file):
        self.ids.editor.unc_page_close(file)

    def _unc_system_hotkey_register(self, hotkey):
        # TODO handle a failed register...
        logging.info('binding hotkey ' + str(hotkey))
        self.hk.register(hotkey)

    def _unc_profile_set_active(self, profile):
        logging.warning('profile_set_active')
        self.active_profile = profile
        # self.kivy_app.pf.set_active(profile)

    def _unc_system_gotten(self, system):
        import json
        system = json.loads(system)
        pprint(system)

    # Careful this has the same name as the request, see _run_bind
    def _unc_page_settings_view(self, settings):
        self.ids.editor.unc_page_settings_view(settings)

    def _unc_api_error(self, msg, **kwargs):
        import pdb;pdb.set_trace()
