# Python imports
from os import listdir
from os.path import isfile
from os.path import join

# Lib imports
from gi.repository import GLib

# Application imports
from .save_state_to_xwinwarp import SaveStateToXWinWarp



class Controller_Data:
    def has_method(self, obj, name):
        return callable(getattr(obj, name, None))

    def setup_controller_data(self):
        self.state_saver    = SaveStateToXWinWarp()
        self.logger         = settings.get_logger()

        self.home_path      = settings.get_home_path()
        self.success_color  = settings.get_success_color()
        self.warning_color  = settings.get_warning_color()
        self.error_color    = settings.get_error_color()
        self.vids_filter    = settings.get_vids_filter()
        self.imgs_filter    = settings.get_images_filter()

        self.image_grid     = self.builder.get_object("imageGrid")
        self.grid_label     = self.builder.get_object("gridLabel")
        self.help_label     = self.builder.get_object("helpLabel")
        self.xscreen_store  = self.builder.get_object("XScreensaverStore")

        self.defaultLabel   = "<span>Note: Double click an image to view the video or image.</span>"
        self.savedLabel     = f"<span foreground='{self.success_color}'>Saved settings...</span>"
        self.appliedLabel   = f"<span foreground='{self.success_color}'>Running xwinwrap...</span>"
        self.stoppedLabel   = f"<span foreground='{self.success_color}'>Stopped xwinwrap...</span>"

        # Add filter to allow only folders to be selected
        dialog             = self.builder.get_object("selectedDirDialog")
        file_filter        = self.builder.get_object("Folders")
        dialog.add_filter(file_filter)

        self.xscreensavers = settings.get_xscreensavers()
        list               = [f for f in listdir(self.xscreensavers) if isfile(join(self.xscreensavers , f))]
        list.sort()
        for file in list:
            self.xscreen_store.append((file,))

        self.selected_eve_box   = None
        self.start_path         = None
        self.default_player     = None
        self.default_img_viewer = None
        self.demo_area_pid      = None

        self.apply_type         = 1    # 1 is XWinWrap and 2 is Nitrogen
        self.xscreen_value      = None
        self.to_be_background   = None # Global file path and type for saving to file

        self.set_monitor_offset_data()
        self.retrieve_settings()


    def retrieve_settings(self):
        self.start_path         = settings.get_start_path()
        self.default_player     = settings.get_default_player()
        self.default_img_viewer = settings.get_default_img_viewer()

        self.builder.get_object("customStartPath").set_text(self.start_path)
        self.builder.get_object("customVideoPlayer").set_text(self.default_player)
        self.builder.get_object("customImgViewer").set_text(self.default_img_viewer)
        self.builder.get_object("selectedDirDialog").set_filename(self.start_path)

        if self.start_path:
            self.load_path(None, self.start_path)

    def set_monitor_offset_data(self):
        monitors = settings.get_monitor_data(self.window)
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

    def save_to_settings_file(self, widget=None):
        settings.save_settings()

    def update_start_path(self, widget=None, eve=None):
        start_path = self.builder.get_object("customStartPath").get_text().strip()
        settings.set_start_path(start_path)

    def update_default_player(self, widget=None, eve=None):
        default_player  = self.builder.get_object("customVideoPlayer").get_text().strip()
        settings.set_default_player(default_player)

    def update_default_img_viewer(self, widget=None, eve=None):
        default_img_viewer  = self.builder.get_object("customImgViewer").get_text().strip()
        settings.set_default_img_viewer(default_img_viewer)

    def save_to_file(self, widget=None, eve=None):
        save_location   = self.builder.get_object("saveLoc").get_active_text()
        use_xscreensvr  = self.builder.get_object("useXScrnList").get_active()
        playBackRes     = self.builder.get_object("playbackResolution")
        monitorOffset   = self.builder.get_object("monitorOffsetData")
        resolution      = playBackRes.get_active_text() + monitorOffset.get_active_text()
        self.apply_type = self.state_saver.save_to_file(self.to_be_background, resolution, save_location, use_xscreensvr, self.xscreen_value, self.default_player)

        if self.apply_type == -1:
            self.help_label.set_markup("<span foreground='#e0cc64'>Nothing saved...</span>")
            return

        self.help_label.set_markup(self.savedLabel)
