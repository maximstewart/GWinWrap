import builtins

# Python imports
import builtins

# Lib imports

# Application imports
from signal_classes import IPCServerMixin



class Builtins(IPCServerMixin):
    """Docstring for __builtins__ extender"""

    def __init__(self):
        # NOTE: The format used is list of [type, target, data]
        #       Where data may be any kind of data
        self._gui_events    = []
        self._fm_events     = []
        self.is_ipc_alive   = False
        self.ipc_authkey    = b'GWinWrap-ipc'
        self.ipc_address    = '127.0.0.1'
        self.ipc_port       = 8888
        self.ipc_timeout    = 15.0

    # Makeshift fake "events" type system FIFO
    def _pop_gui_event(self):
        if len(self._gui_events) > 0:
            return self._gui_events.pop(0)
        return None

    def _pop_fm_event(self):
        if len(self._fm_events) > 0:
            return self._fm_events.pop(0)
        return None


    def push_gui_event(self, event):
        if len(event) == 3:
            self._gui_events.append(event)
            return None

        raise Exception("Invald event format! Please do:  [type, target, data]")

    def push_fm_event(self, event):
        if len(event) == 3:
            self._fm_events.append(event)
            return None

        raise Exception("Invald event format! Please do:  [type, target, data]")

    def read_gui_event(self):
        return self._gui_events[0]

    def read_fm_event(self):
        return self._fm_events[0]

    def consume_gui_event(self):
        return self._pop_gui_event()

    def consume_fm_event(self):
        return self._pop_fm_event()



# NOTE: Just reminding myself we can add to builtins two different ways...
# __builtins__.update({"event_system": Builtins()})
builtins.app_name          = "GWinWrap"
builtins.event_system      = Builtins()
builtins.event_sleep_time  = 0.2
builtins.debug             = False
builtins.trace_debug       = False