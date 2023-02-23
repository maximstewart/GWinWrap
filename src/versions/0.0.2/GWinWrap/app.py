# Python imports
import os
import time

# Lib imports

# Application imports
from utils.ipc_server import IPCServer
from core.window import Window




class AppLaunchException(Exception):
    ...

class ControllerStartExceptiom(Exception):
    ...


class Application(IPCServer):
    ''' Create Settings and Controller classes. Bind signal to Builder. Inherit from Builtins to bind global methods and classes.'''

    def __init__(self, args, unknownargs):
        super(Application, self).__init__()
        if not settings.is_trace_debug():
            try:
                self.create_ipc_listener()
            except Exception:
                ...

            if not self.is_ipc_alive:
                for arg in unknownargs + [args.new_tab,]:
                    if os.path.isdir(arg):
                        message = f"FILE|{arg}"
                        self.send_ipc_message(message)

                raise AppLaunchException(f"{app_name} IPC Server Exists: Will send path(s) to it and close...")

        Window(args, unknownargs)
