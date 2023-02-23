# Python imports
import os
import subprocess

# Lib imports

# Application imports



class SaveStateToXWinWarp:
    def __init__(self):
        self.user_home         = settings.get_home_path()

        self._file_writer      = None
        self._to_be_background = None
        self._use_xscreensvr   = None
        self._xscreen_value    = None
        self._save_file_target = None
        self._resolution       = None
        self._player           = None


    def save_to_file(self, to_be_background, resolution, save_location,
                                use_xscreensvr, xscreen_value, player):

        self._to_be_background = to_be_background
        self._use_xscreensvr   = use_xscreensvr
        self._xscreen_value    = xscreen_value
        self._resolution       = resolution
        self._player           = player

        # Saves to file with selected and needed settings
        if to_be_background:
            if to_be_background.lower().endswith(settings.get_images_filter()):
                self._save_file_target = f"{self.user_home}/.config/nitrogen/bg-saved.cfg"
            else:
                self._save_file_target = f"{self.user_home}/{save_location}"
        elif use_xscreensvr and xscreen_value:
            self._save_file_target = f"{self.user_home}/{save_location}"
        else:
            return -1

        if self._save_file_target:
            self._file_writer = open(self._save_file_target, "w")

        return self.save()

    def save(self):
        applyType = 1
        output    = None

        # XSCREENSAVER
        if self._use_xscreensvr:
            output = f"xwinwrap -ov -g {self._resolution} -st -sp -b -nf -s -ni -- /usr/lib/xscreensaver/{self._xscreen_value} -window-id WID -root";
        # GIF
        elif self._to_be_background.lower().endswith(('.gif')):
                output = f"xwinwrap -ov -g {self._resolution} -st -sp -b -nf -s -ni -- gifview -a -w WID {self._to_be_background}";
        # Standard images using nitrogen
        elif self._to_be_background.lower().endswith(('.png', 'jpg', '.jpeg')):
            output = f"[xin_0] \nfile={self._to_be_background}\nmode=0 \nbgcolor=#000000\n\n[xin_1] \nfile={self._to_be_background}\nmode=0 \nbgcolor=#000000";
            applyType = 2;
        # VIDEO
        else:
            output = f"xwinwrap -ov -g {self._resolution} -st -sp -b -nf -s -ni -- {self._player} -wid WID -really-quiet -ao null -loop 0 '{self._to_be_background}'";

        self.write_to_launch_file(output)
        self.set_as_executable()

        return applyType;


    def write_to_launch_file(self, output):
        try:
            if self._file_writer:
                self._file_writer.write(output)
                self._file_writer.close()
        except Exception as e:
            print("::  Write failed!  ::")
            print(e)

    def set_as_executable(self):
        os.access(self._save_file_target, os.X_OK)
        try:
            command = ["chmod", "764", self._save_file_target]
            with subprocess.Popen(command, stdout=subprocess.PIPE) as proc:
                result = proc.stdout.read().decode("UTF-8").strip()
        except Exception as e:
            print(f"Couldn't chmod\nFile:  {properties.file_uri}")
            print( repr(e) )
