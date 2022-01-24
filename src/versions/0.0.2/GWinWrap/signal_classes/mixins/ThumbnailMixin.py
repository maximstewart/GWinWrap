# Python imports
import subprocess

# Gtk imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

# Application imports


class ThumbnailMixin:
    """docstring for ThumbnailMixin"""

    def create_gtk_image(self, path, wxh):
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename  = path,
                width     = wxh[0],
                height    = wxh[1],
                preserve_aspect_ratio = True)
            return Gtk.Image.new_from_pixbuf(pixbuf)
        except Exception as e:
            print(repr(e))

        return Gtk.Image()

    def generate_thumbnail(self, fullPathFile, hashImgpth):
        # Stream duration
        command  = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", fullPathFile]
        data     = subprocess.run(command, stdout=subprocess.PIPE)
        duration = data.stdout.decode('utf-8')

        # Format (container) duration
        if "N/A" in duration:
            command  = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", fullPathFile]
            data     = subprocess.run(command , stdout=subprocess.PIPE)
            duration = data.stdout.decode('utf-8')

        # Stream duration type: image2
        if "N/A" in duration:
            command  = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-f", "image2", "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", fullPathFile]
            data     = subprocess.run(command, stdout=subprocess.PIPE)
            duration = data.stdout.decode('utf-8')

        # Format (container) duration type: image2
        if "N/A" in duration:
            command  = ["ffprobe", "-v", "error", "-f", "image2", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", fullPathFile]
            data     = subprocess.run(command , stdout=subprocess.PIPE)
            duration = data.stdout.decode('utf-8')

        # Get frame roughly 35% through video
        grabTime = str( int( float( duration.split(".")[0] ) * 0.35) )
        command = ["ffmpeg", "-ss", grabTime, "-i", fullPathFile, "-an", "-vframes", "1", "-s", "320x180", "-q:v", "2", hashImgpth]
        subprocess.call(command)
