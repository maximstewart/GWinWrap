#!/usr/bin/python3

# Gtk imports
import gi, faulthandler, signal
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GLib

# Python imports
import inspect

from setproctitle import setproctitle

# Application imports
from utils import Settings
from signal_classes import CrossClassSignals


class Main:
    def __init__(self):
        setproctitle('GWinWrap')
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, gtk.main_quit)
        faulthandler.enable()  # For better debug info

        settings = Settings()
        builder  = settings.returnBuilder()

        # Gets the methods from the classes and sets to handler.
        # Then, builder connects to any signals it needs.
        classes  = [CrossClassSignals(settings)]
        
        handlers = {}
        for c in classes:
            methods = inspect.getmembers(c, predicate=inspect.ismethod)
            handlers.update(methods)

        builder.connect_signals(handlers)
        window = settings.createWindow()
        window.show()


if __name__ == "__main__":
    try:
        main = Main()
        gtk.main()
    except Exception as e:
        print(e)
