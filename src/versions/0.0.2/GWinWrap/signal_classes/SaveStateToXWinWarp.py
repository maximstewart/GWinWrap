
class SaveStateToXWinWarp:
    def __init__(self, _settings):
        self.settings          = _settings
        self.user_home         = self.settings.get_home_path()

        self._file_writer      = None
        self._to_be_background = None
        self._use_xscreensvr   = None
        self._xscreen_value     = None
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
            if to_be_background.lower().endswith(self.settings.get_images_filter()):
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
            pass

        try:
            if self._file_writer:
                self._file_writer.write(output)
                self._file_writer.close()
        except Exception as e:
            print("::  Write failed!  ::")
            print(e)

        return applyType;
