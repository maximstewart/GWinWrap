# Python imports
import subprocess

# Gtk imports
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

# Application imports


class ImageViewerMixin:
    """docstring for ImageViewerMixin"""

    def close_image_popup(self, widget=None):
        self.builder.get_object("previewWindow").popdown()

    def open_main_image_viewer(self, widget):
        subprocess.call([self.default_img_viewer, self.to_be_background])

    def run_image_viewer_process(self, widget, eve, params):
        image, file, eveBox = params
        self.set_selected(eveBox)

        if eve.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
            previewWindow = self.builder.get_object("previewWindow")
            previewImg    = self.builder.get_object("previewImg")
            previewImg.set_from_file(image)
            previewWindow.show_all()
            previewWindow.popup()

        self.to_be_background = image
        self.apply_type       = 2
        self.help_label.set_markup(f"<span foreground='#e0cc64'>{file}</span>")
