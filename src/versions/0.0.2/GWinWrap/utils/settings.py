# Python imports
import os
import json
import inspect

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .logger import Logger




class Settings:
    def __init__(self):
        self._SCRIPT_PTH       = os.path.dirname(os.path.realpath(__file__))
        self._USER_HOME        = os.path.expanduser('~')
        self._USR_PATH         = f"/usr/share/{app_name.lower()}"
        self._USR_CONFIG_FILE  = f"{self._USR_PATH}/settings.json"
        self._HOME_CONFIG_PATH = f"{self._USER_HOME}/.config/{app_name.lower()}"
        self._DEFAULT_ICONS    = f"{self._HOME_CONFIG_PATH}/icons"
        self._CONFIG_FILE      = f"{self._HOME_CONFIG_PATH}/settings.json"
        self._GLADE_FILE       = f"{self._HOME_CONFIG_PATH}/Main_Window.glade"
        self._CSS_FILE         = f"{self._HOME_CONFIG_PATH}/stylesheet.css"
        self._PID_FILE         = f"{self._HOME_CONFIG_PATH}/{app_name.lower()}.pid"
        self._WINDOW_ICON      = f"{self._DEFAULT_ICONS}/{app_name.lower()}.png"

        if not os.path.exists(self._HOME_CONFIG_PATH):
            os.mkdir(self._HOME_CONFIG_PATH)

        if not os.path.exists(self._CONFIG_FILE):
            import shutil
            try:
                shutil.copyfile(self._USR_CONFIG_FILE, self._CONFIG_FILE)
            except Exception as e:
                raise

        if not os.path.exists(self._GLADE_FILE):
            self._GLADE_FILE   = f"{self._USR_PATH}/Main_Window.glade"
        if not os.path.exists(self._CSS_FILE):
            self._CSS_FILE     = f"{self._USR_PATH}/stylesheet.css"
        if not os.path.exists(self._DEFAULT_ICONS):
            self.DEFAULT_ICONS = f"{self._USR_PATH}/icons"
        if not os.path.exists(self._WINDOW_ICON):
            self._WINDOW_ICON  = f"{self.DEFAULT_ICONS}/{app_name.lower()}.png"

        thumbnail_path = f"{self._USER_HOME}/.thumbnails/normal"
        if not os.path.exists(thumbnail_path):
            os.system(f"mkdir -p '{thumbnail_path}'")

        self._logger         = Logger(self._HOME_CONFIG_PATH).get_logger()
        self._builder        = Gtk.Builder()
        self._builder.add_from_file(self._GLADE_FILE)

        self._debug          = False
        self._trace_debug    = False
        self._dirty_start    = False

        self._settings       = None
        self._config         = None
        self._theming        = None

        self.load_settings()


    def is_trace_debug(self) -> str:  return self._trace_debug
    def is_debug(self)       -> str:  return self._debug
    def is_dirty_start(self) -> bool: return self._dirty_start
    def clear_pid(self): self._clean_pid()

    def do_dirty_start_check(self):
        if not os.path.exists(self._PID_FILE):
            self._write_new_pid()
        else:
            with open(self._PID_FILE, "r") as _pid:
                pid = _pid.readline().strip()
                if pid not in ("", None):
                    self._check_alive_status(int(pid))
                else:
                    self._write_new_pid()

    """ Check For the existence of a unix pid. """
    def _check_alive_status(self, pid):
        print(f"PID Found: {pid}")
        try:
            os.kill(pid, 0)
        except OSError:
            print(f"{app_name} is starting dirty...")
            self._dirty_start = True
            self._write_new_pid()
            return

        print("PID is alive... Let downstream errors (sans debug args) handle app closure propigation.")

    def _write_new_pid(self):
        pid = os.getpid()
        self._write_pid(pid)

    def _clean_pid(self):
        os.unlink(self._PID_FILE)

    def _write_pid(self, pid):
        with open(self._PID_FILE, "w") as _pid:
            _pid.write(f"{pid}")

    def register_signals_to_builder(self, classes=None):
        handlers = {}

        for c in classes:
            methods = None
            try:
                methods = inspect.getmembers(c, predicate=inspect.ismethod)
                handlers.update(methods)
            except Exception as e:
                print(repr(e))

        self._builder.connect_signals(handlers)

    def get_monitor_data(self, window):
        screen = window.get_screen()
        monitors = []
        for m in range(screen.get_n_monitors()):
            monitors.append(screen.get_monitor_geometry(m))

        for monitor in monitors:
            print("{}x{}|{}+{}".format(monitor.width, monitor.height, monitor.x, monitor.y))

        return monitors

    def get_builder(self)        -> any:     return self._builder
    def get_config_file(self)    -> str:     return self._CONFIG_FILE
    def get_glade_file(self)     -> str:     return self._GLADE_FILE
    def get_logger(self)         -> Logger:  return self._logger
    def get_icon_theme(self)     -> str:     return self._ICON_THEME
    def get_css_file(self)       -> str:     return self._CSS_FILE
    def get_window_icon(self)    -> str:     return self._WINDOW_ICON
    def get_home_path(self)      -> str:     return self._USER_HOME

    def get_success_color(self)  -> str:     return self._theming["success_color"]
    def get_warning_color(self)  -> str:     return self._theming["warning_color"]
    def get_error_color(self)    -> str:     return self._theming["error_color"]

    def get_xscreensavers(self)  -> str:     return self._config["xscreensaver_path"]
    def get_start_path(self)     -> str:     return self._config["start_path"]
    def get_default_player(self) -> str:     return self._config["default_player"]
    def get_default_img_viewer(self) -> str: return self._config["default_img_viewer"]

    def get_vids_filter(self)    -> tuple:   return tuple(self._settings["filters"]["videos"])
    def get_images_filter(self)  -> tuple:   return tuple(self._settings["filters"]["images"])



    def set_builder(self, builder):           self._builder = builder
    def set_start_path(self, path):           self._config["start_path"] = path
    def set_default_player(self, player):     self._config["default_player"] = player
    def set_default_img_viewer(self, viewer): self._config["default_img_viewer"] = viewer

    def set_trace_debug(self, trace_debug):
        self._trace_debug = trace_debug

    def set_debug(self, debug):
        self._debug = debug


    def load_settings(self):
        with open(self._CONFIG_FILE) as f:
            self._settings = json.load(f)
            self._config   = self._settings["config"]
            self._theming  = self._settings["theming"]

    def save_settings(self):
        with open(self._CONFIG_FILE, 'w') as outfile:
            json.dump(self._settings, outfile, separators=(',', ':'), indent=4)
