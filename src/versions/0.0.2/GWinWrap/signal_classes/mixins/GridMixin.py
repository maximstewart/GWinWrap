# Python imports
import threading, hashlib
from os import listdir
from os.path import isfile, join

# Gtk imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

# Application imports





def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


class GridMixin:
    """docstring for GridMixin."""

    def set_new_path(self, widget, data=None):
        dir = widget.get_filename()
        self.load_path(None, dir)

    def load_path(self, widget=None, dir=''):
        path    = dir
        list    = [f for f in listdir(path) if isfile(join(path, f))]
        files   = []
        row     = 0
        col     = 0

        for file in list:
            if file.lower().endswith(self.settings.get_vids_filter() + \
                                        self.settings.get_images_filter()):
                files.append(file)

        # fractionTick = 1.0 / 1.0 if len(files) == 0 else len(files)
        # tickCount    = 0.0
        self.clear()
        self.image_grid.remove_column(0)
        # self.loadProgress.set_text("Loading...")
        # self.loadProgress.set_fraction(0.0)
        self.help_label.set_markup(f"<span foreground='#b30ec2'>{path.strip(self.settings.get_home_path())}</span>")
        for file in files:
            self.porocess_file(path, file, col, row)

            col += 1
            if col == 2:
                col = 0
                row += 1

        # self.loadProgress.set_text("Finished...")

    @threaded
    def porocess_file(self, path, file, col, row):
        fPath = f"{path}/{file}"
        eveBox       = Gtk.EventBox()
        thumbnl      = Gtk.Image()

        if file.lower().endswith(self.settings.get_vids_filter()):
            fileHash   = hashlib.sha256(str.encode(fPath)).hexdigest()
            hashImgPath = f"{self.settings.get_home_path()}/.thumbnails/normal/{fileHash}.png"
            if isfile(hashImgPath) == False:
                self.generate_thumbnail(fPath, hashImgPath)

            thumbnl = self.create_gtk_image(hashImgPath, [310, 310])
            eveBox.connect("button_press_event", self.run_mplayer_process, (fPath, file, eveBox,))
            eveBox.connect("enter_notify_event", self.mouse_over, ())
            eveBox.connect("leave_notify_event", self.mouse_out, ())
        elif file.lower().endswith(self.settings.get_images_filter()):
            thumbnl = self.create_gtk_image(fPath, [310, 310])
            eveBox.connect("button_press_event", self.run_image_viewer_process, (fPath, file, eveBox,))
            eveBox.connect("enter_notify_event", self.mouse_over, ())
            eveBox.connect("leave_notify_event", self.mouse_out, ())
        else:
            print("Not a video or image file.")
            return

        GLib.idle_add(self.pre_grid_setup, (eveBox, thumbnl, ))
        GLib.idle_add(self.add_to_grid, (self.image_grid, eveBox, col, row,))
        # tickCount = tickCount + fractionTick
        # self.loadProgress.set_fraction(tickCount)

    def pre_grid_setup(self, args):
        args[0].show()
        args[1].show()
        args[0].add(args[1])

    def add_to_grid(self, args):
        args[0].attach(args[1], args[2], args[3], 1, 1)

    def clear_selection(self, widget, data=None):
        self.clear()

    def clear(self):
        while True:
            if self.image_grid.get_child_at(0,0)!= None:
                self.image_grid.remove_row(0)
            else:
                break

        self.image_grid.attach(self.grid_label, 0, 0, 1, 1)
        self.builder.get_object("xScreenSvrList").set_sensitive(False)
        self.builder.get_object("useXScrnList").set_active(False)
        self.help_label.set_markup(self.defaultLabel)
        # self.loadProgress.set_text("")
        # self.loadProgress.set_fraction(0.0)
        self.xscreen_value    = None
        self.to_be_background     = None
        self.apply_type       = 1
