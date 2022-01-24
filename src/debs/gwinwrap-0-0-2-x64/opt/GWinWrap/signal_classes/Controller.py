# Python imports
import threading, signal, subprocess, inspect, os, time

# Gtk imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GLib, Gdk

# Application imports
from .mixins import *
from . import Controller_Data


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


class Controller(ThumbnailMixin, ImageViewerMixin, DrawAreaMixin, GridMixin, Controller_Data):
    def __init__(self, _settings, args, unknownargs):
        self.setup_controller_data(_settings)
        self.window.show()
        self.retrieve_settings()


    def tear_down(self, widget=None, eve=None):
        event_system.send_ipc_message("close server")
        if self.demo_area_pid:
            self.close_demo_popup()

        self.close_image_popup()
        time.sleep(event_sleep_time)
        Gtk.main_quit()

    def close_program(self, widget, data=None):
        self.tear_down()


    @threaded
    def gui_event_observer(self):
        while True:
            time.sleep(event_sleep_time)
            event = event_system.consume_gui_event()
            if event:
                try:
                    type, target, data = event
                    method = getattr(self.__class__, type)
                    GLib.idle_add(method, (self, data,))
                except Exception as e:
                    print(repr(e))



    def apply_settings(self, widget, data=None):
        os.system("killall xwinwrap &")
        user_home = self.settings.get_home_path()

        if self.apply_type == 1:
            files = os.listdir(user_home)
            for file in files:
                fPath = f"{user_home}/{file}"
                if os.path.isfile(fPath) and "animatedBGstarter" in file:
                    os.system(f"bash -c '~/{file}' &")
        elif self.apply_type == 2:
            os.system("nitrogen --restore &")
        else:
            os.system("nitrogen --restore &")

        self.help_label.set_markup(self.appliedLabel)

    def save_to_settings_file(self, widget):
        self.start_path = self.builder.get_object("customStartPath").get_text().strip()
        self.default_player  = self.builder.get_object("customVideoPlayer").get_text().strip()
        self.default_img_viewer  = self.builder.get_object("customImgViewer").get_text().strip()

        self.settings_saver.save_settings(self.start_path, self.default_player, self.default_img_viewer)

    def save_to_file(self, widget, data=None):
        save_location   = self.builder.get_object("saveLoc").get_active_text()
        use_xscreensvr = self.builder.get_object("useXScrnList").get_active()
        playBackRes     = self.builder.get_object("playbackResolution")
        monitorOffset   = self.builder.get_object("monitorOffsetData")
        resolution      = playBackRes.get_active_text() + monitorOffset.get_active_text()
        self.apply_type = self.state_saver.save_to_file(self.to_be_background, resolution, save_location, use_xscreensvr, self.xscreen_value, self.default_player)

        if self.apply_type == -1:
            self.help_label.set_markup("<span foreground='#e0cc64'>Nothing saved...</span>")
            return

        self.help_label.set_markup(self.savedLabel)


    def toggle_xscreen_list(self, widget, data=None):
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

    def get_clipboard_data(self):
        proc    = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        retcode = proc.wait()
        data    = proc.stdout.read()
        return data.decode("utf-8").strip()

    def set_clipboard_data(self, data):
        proc = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
        proc.stdin.write(data)
        proc.stdin.close()
        retcode = proc.wait()
