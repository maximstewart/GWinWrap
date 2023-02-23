# Python imports
import os

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

# Application imports
from .mixins import *
from .controller_data import Controller_Data



class Controller(ThumbnailMixin, ImageViewerMixin, DrawAreaMixin, GridMixin, Controller_Data):
    def __init__(self, args, unknownargs, _window):
        self.window = _window

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_glade_file()

        self.setup_controller_data()
        self.retrieve_settings()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("handle_file_from_ipc", self.handle_file_from_ipc)

    def handle_file_from_ipc(self, path: str) -> None:
        print(f"Path From IPC: {path}")

    def _load_glade_file(self):
        self.builder     = Gtk.Builder()
        self.builder.add_from_file(settings.get_glade_file())
        settings.set_builder(self.builder)
        self.core_widget   = self.builder.get_object("core_widget")

        settings.register_signals_to_builder([self, self.core_widget])

    def get_core_widget(self):
        return self.core_widget

    def tear_down(self, widget=None, eve=None):
        if self.demo_area_pid:
            self.close_demo_popup()

        self.close_image_popup()

    def close_program(self, widget, data=None):
        event_system.emit("close_gwinwrap")


    def apply_settings(self, widget, data=None):
        os.system("killall xwinwrap &")
        user_home = settings.get_home_path()

        if self.apply_type == 1:
            files = os.listdir(user_home)
            for file in files:
                fPath = f"{user_home}/{file}"
                if os.path.isfile(fPath) and "animatedBGstarter" in file:
                    os.system(f"bash -c '~/{file}' &")
        else:
            os.system("nitrogen --restore &")

        self.help_label.set_markup(self.appliedLabel)


    def toggle_xscreen_list(self, widget=None, eve=None):
        use_xscreensvr = self.builder.get_object("useXScrnList")
        if use_xscreensvr.get_active():
            self.builder.get_object("xScreenSvrList").set_sensitive(True)
        else:
            self.builder.get_object("xScreenSvrList").set_sensitive(False)

    def show_settings_popup(self, widget):
        self.builder.get_object("settingsWindow").popup()


    def preview_xscreensaver(self, widget, eve):
        if eve.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
            demoXscrnSaver = self.xscreensavers + self.xscreen_value
            xid            = self.getXID()
            command        = [demoXscrnSaver, "-window-id", str(xid)]
            self.run_demo_in_draw_area(command)

    def pass_xscreen_value(self, widget):
        row                = widget.get_cursor()
        path               = Gtk.TreePath(row.path)
        treeiter           = self.xscreen_store.get_iter(path[0])
        self.xscreen_value = self.xscreen_store.get_value(treeiter, 0)

    def kill_xwinwrap(self, widget, data=None):
        os.system("killall xwinwrap &")
        self.help_label.set_markup(self.stoppedLabel)

    def set_selected_eve_box(self, eveBox):
      if self.selected_eve_box:
          color = Gdk.RGBA(0.0, 0.0, 0.0, 0.0)
          self.selected_eve_box.override_background_color(Gtk.StateType.NORMAL, color)

      color = Gdk.RGBA(0.9, 0.7, 0.4, 0.74)
      eveBox.override_background_color(Gtk.StateType.NORMAL, color)
      self.selected_eve_box = eveBox

    def mouse_over(self, widget, eve, args):
        hand_cursor = Gdk.Cursor(Gdk.CursorType.HAND2)
        self.window.get_window().set_cursor(hand_cursor)

    def mouse_out(self, widget, eve, args):
        watch_cursor = Gdk.Cursor(Gdk.CursorType.LEFT_PTR)
        self.window.get_window().set_cursor(watch_cursor)
