# Python imports
import os, inspect, time

# Lib imports

# Application imports
from utils import Settings
from signal_classes import Controller
from __builtins__ import Builtins




class Main(Builtins):
    def __init__(self, args, unknownargs):
        if not debug:
            event_system.create_ipc_server()

        time.sleep(0.2)
        if not trace_debug:
            if not event_system.is_ipc_alive:
                if unknownargs:
                    for arg in unknownargs:
                        if os.path.isdir(arg):
                            message = f"FILE|{arg}"
                            event_system.send_ipc_message(message)

                raise Exception("IPC Server Exists: Will send data to it and close...")


        settings = Settings()
        settings.create_window()

        controller = Controller(settings, args, unknownargs)
        if not controller:
            raise Exception("Controller exited and doesn't exist...")

        # Gets the methods from the classes and sets to handler.
        # Then, builder from settings will connect to any signals it needs.
        classes  = [controller]
        handlers = {}
        for c in classes:
            methods = None
            try:
                methods = inspect.getmembers(c, predicate=inspect.ismethod)
                handlers.update(methods)
            except Exception as e:
                print(repr(e))

        settings.get_builder().connect_signals(handlers)
