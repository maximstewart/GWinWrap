# Python imports
import os
import subprocess
import signal
import time

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

# Application imports



class DrawAreaMixin:
    """docstring for DrawAreaMixin"""

    def close_demo_popup(self, widget=None, data=None):
        os.kill(self.demo_area_pid, signal.SIGTERM) # or signal.SIGKILL
        self.demo_area_pid = None
        time.sleep(.200)
        self.builder.get_object("demoPreviewPopWindow").popdown()

    def run_mplayer_process(self, widget, eve, params):
        video, file, eveBox = params
        self.set_selected_eve_box(eveBox)

        if eve.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
            if self.default_player == "mplayer":
                xid     = self.getXID()
                command = [self.default_player, video, "-slave", "-wid", str(xid), "-really-quiet", "-ao", "null", "-loop", "0"]
                self.run_demo_in_draw_area(command)
            else:
                subprocess.call([self.default_player, video, "-really-quiet", "-ao", "null", "-loop", "0"])


        self.to_be_background = video
        self.applyType        = 1
        self.help_label.set_markup(f"<span foreground='#e0cc64'>{file}</span>")

    def run_demo_in_draw_area(self, command):
        self.help_label.set_markup("<span foreground='#e0cc64'></span>")

        if self.demo_area_pid:
            os.kill(self.demo_area_pid, signal.SIGTERM) #or signal.SIGKILL
            self.demo_area_pid = None
            time.sleep(.800) # 800 mili-seconds to ensure first process dead

        process            = subprocess.Popen(command)
        self.demo_area_pid = process.pid

    def getXID(self):
        # Must be actualized before getting window
        popup = self.builder.get_object("demoPreviewPopWindow")

        if popup.get_visible() == False:
            popup.show_all()
            popup.popup()

        preview = self.builder.get_object("demoPreview")
        window   = preview.get_window()
        return window.get_xid()
