# Python imports
import signal
from os import listdir
from os.path import isfile, join

# Lib imports
from gi.repository import GLib

# Application imports
from . import SaveStateToXWinWarp, SaveGWinWrapSettings



class Controller_Data:
    def has_method(self, obj, name):
        return callable(getattr(obj, name, None))

    def setup_controller_data(self, _settings):
        self.settings       = _settings
        self.state_saver    = SaveStateToXWinWarp(_settings)
        self.settings_saver = SaveGWinWrapSettings(_settings)


        self.builder       = self.settings.get_builder()
        self.window        = self.settings.get_main_window()
        self.logger        = self.settings.get_logger()

        self.home_path     = self.settings.get_home_path()
        self.success_color = self.settings.get_success_color()
        self.warning_color = self.settings.get_warning_color()
        self.error_color   = self.settings.get_error_color()


        self.image_grid    = self.builder.get_object("imageGrid")
        self.grid_label    = self.builder.get_object("gridLabel")
        self.help_label    = self.builder.get_object("helpLabel")
        self.xscreen_store = self.builder.get_object("XScreensaverStore")

        self.defaultLabel = "<span>Note: Double click an image to view the video or image.</span>"
        self.savedLabel   = f"<span foreground='{self.success_color}'>Saved settings...</span>"
        self.appliedLabel = f"<span foreground='{self.success_color}'>Running xwinwrap...</span>"
        self.stoppedLabel = f"<span foreground='{self.success_color}'>Stopped xwinwrap...</span>"

        # Add filter to allow only folders to be selected
        dialog             = self.builder.get_object("selectedDirDialog")
        file_filter        = self.builder.get_object("Folders")
        dialog.add_filter(file_filter)

        self.xscreensavers = self.settings.get_xscreensavers()
        list               = [f for f in listdir(self.xscreensavers) if isfile(join(self.xscreensavers , f))]
        list.sort()
        for file in list:
            self.xscreen_store.append((file,))


        self.selected_eve_box   = None
        self.start_path         = None
        self.default_player     = None
        self.default_img_viewer = None
        self.demo_area_pid      = None

        self.apply_type       = 1    # 1 is XWinWrap and 2 is Nitrogen
        self.xscreen_value    = None
        self.to_be_background = None # Global file path and type for saving to file


        self.window.connect("delete-event", self.tear_down)
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, self.tear_down)

        self.set_monitor_offset_data()
        self.retrieve_settings()


    def set_monitor_offset_data(self):
        monitors = self.settings.get_monitor_data()
        monitorOffsetData = self.builder.get_object("monitorOffsetData")

        for monitor in monitors:
            if monitor.x >= 0 and monitor.y >= 0:
                monitorOffsetData.append_text("+" + str(monitor.x) + "+" + str(monitor.y))
            elif monitor.x <= 0 and monitor.y <= 0:
                monitorOffsetData.append_text(str(monitor.x) + str(monitor.y))
            elif monitor.x >= 0 and monitor.y <= 0:
                monitorOffsetData.append_text("+" + str(monitor.x) + str(monitor.y))
            elif monitor.x <= 0 and monitor.y >= 0:
                monitorOffsetData.append_text(str(monitor.x) + "+" + str(monitor.y))

        monitorOffsetData.set_active(0)

    def retrieve_settings(self):
        data                    = self.settings_saver.retrieve_settings()
        self.start_path         = data[0]
        self.default_player     = data[1]
        self.default_img_viewer = data[2]

        self.builder.get_object("customStartPath").set_text(self.start_path)
        self.builder.get_object("customVideoPlayer").set_text(self.default_player)
        self.builder.get_object("customImgViewer").set_text(self.default_img_viewer)
        self.builder.get_object("selectedDirDialog").set_filename(self.start_path)

        if self.start_path:
            self.load_path(None, self.start_path)
