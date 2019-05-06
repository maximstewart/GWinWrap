#!/usr/bin/env python

import os, cairo, sys, gi, re, threading, subprocess

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GObject as gobject
from gi.repository import Gtk, GdkPixbuf

from os import listdir
from os.path import isfile, join
from threading import Thread

from utils import SaveState

gdk.threads_init()


class GWinWrap:
    def __init__(self):
        self.builder   = gtk.Builder()
        self.builder.add_from_file("resources/GWinWrap.glade")

        # Get window and connect signals
        self.window    = self.builder.get_object("Main")
        self.builder.connect_signals(self)
        self.window.connect("delete-event", gtk.main_quit)

        self.screen = self.window.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual != None and self.screen.is_composited():
            self.window.set_visual(self.visual)

        self.window.set_app_paintable(True)
        self.window.connect("draw", self.area_draw)

        # Add filter to allow only folders to be selected
        dialog         = self.builder.get_object("selectedDirDialog")
        filefilter     = self.builder.get_object("Folders")
        dialog.add_filter(filefilter)

        # Get reference to remove and add it back...
        self.gridLabel = self.builder.get_object("gridLabel")

        self.stateSaver = SaveState()
        self.focusedImg = gtk.Image()
        self.usrHome    = os.path.expanduser('~')
        self.xScreenVal = None
        self.toSavePath = None # Global file path and type for saving to file
        self.applyType  = 1    # 1 is XWinWrap and 2 is Nitrogen

        self.loadProgress = self.builder.get_object("loadProgress")
        self.helpLabel    = self.builder.get_object("helpLabel")
        self.defaultLabel = "<span>Note: Double click an image to view the video or image.</span>"
        self.savedLabel   = "<span foreground=\"#88cc27\">Saved settings...</span>"
        self.appliedLabel = "<span foreground=\"#88cc27\">Running xwinwrap...</span>"
        self.stoppedLabel = "<span foreground=\"#88cc27\">Stopped xwinwrap...</span>"
        # foreground=\"#ffa800\"
        # foreground=\"#88cc27\"
        # foreground=\"#ff0000\"
        # foreground=\"#ff0000\"

        self.window.show()

    def area_draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0.64)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)




    def setNewDir(self, widget, data=None):
        dir = widget.get_filename()
        Thread(target=self.newDir, args=(dir,)).start()

    def newDir(self, dir):
        imageGrid    = self.builder.get_object("imageGrid")
        dirPath      = dir
        list         = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
        files        = []
        row          = 0
        col          = 0

        for file in list:
            if file.lower().endswith(('.mkv', '.avi', '.flv', '.mov', '.m4v', '.mpg', '.wmv', '.mpeg', '.mp4', '.webm', '.png', '.jpg', '.jpeg', '.gif')):
                files.append(file)


        fractionTick = 1.0 / len(files)
        tickCount    = 0.0
        self.clear()
        imageGrid.remove_column(0)
        self.loadProgress.set_text("Loading...")
        self.loadProgress.set_fraction(0.0)
        self.helpLabel.set_markup("<span foreground=\"#b30ec2\">" + dirPath.strip(self.usrHome) + "</span>")
        for file in files:
            fullPathFile = dirPath + "/" + file
            eveBox       = gtk.EventBox()
            thumbnl      = gtk.Image()

            if file.lower().endswith(('.mkv', '.avi', '.flv', '.mov', '.m4v', '.mpg', '.wmv', '.mpeg', '.mp4', '.webm')):
                self.generateThumbnail(fullPathFile)
                thumbnl = self.createGtkImage("/tmp/image.png", [310, 310])
                eveBox.connect("button_press_event", self.runMplayerProcess, (fullPathFile, file,))
            elif file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                thumbnl = self.createGtkImage(fullPathFile, [310, 310])
                eveBox.connect("button_press_event", self.runImageViewerProcess, (fullPathFile, file))
            else:
                print("Not a video or image file.")
                return

            gobject.idle_add(self.preGridSetup, (eveBox, thumbnl, ))
            gobject.idle_add(self.addToGrid, (imageGrid, eveBox, col, row,))
            tickCount = tickCount + fractionTick
            self.loadProgress.set_fraction(tickCount)

            col += 1
            if col == 2:
                col = 0
                row += 1

        self.loadProgress.set_text("Finished...")

    def preGridSetup(self, args):
        args[0].show()
        args[1].show()
        args[0].add(args[1])

    def addToGrid(self, args):
        args[0].attach(args[1], args[2], args[3], 1, 1)

    def generateThumbnail(self, fullPathFile):
        subprocess.call(["ffmpegthumbnailer", "-t", "65%", "-s", "300", "-c", "jpg", "-i", fullPathFile, "-o", "/tmp/image.png"])

    def createGtkImage(self, path, wxh):
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename  = path,
                width     = wxh[0],
                height    = wxh[1],
                preserve_aspect_ratio = True)
            return gtk.Image.new_from_pixbuf(pixbuf)
        except Exception as e:
            print(e)
        return gtk.Image()

    def runMplayerProcess(self, widget, eve, params):
        if eve.type == gdk.EventType.DOUBLE_BUTTON_PRESS:
            subprocess.call(["mplayer", "-really-quiet", "-ao", "null", "-loop", "0", params[0]])

        self.toSavePath = params[0]
        self.applyType  = 1
        self.helpLabel.set_markup("<span foreground=\"#e0cc64\">" + params[1] + "</span>")

    def runImageViewerProcess(self, widget, eve, params):
        if eve.type == gdk.EventType.DOUBLE_BUTTON_PRESS:
            subprocess.call(["xdg-open", params[0]])

        self.toSavePath = params[0]
        self.applyType  = 2
        self.helpLabel.set_markup("<span foreground=\"#e0cc64\">" + params[1] + "</span>")

    def toggleXscreenUsageField(self, widget, data=None):
        useXscreenSaver = self.builder.get_object("useXScrnList")
        if useXscreenSaver.get_active():
            self.builder.get_object("xScreenSvrList").set_sensitive(True)
        else:
            self.builder.get_object("xScreenSvrList").set_sensitive(False)

    def saveToFile(self, widget, data=None):
        saveLoc         = self.builder.get_object("saveLoc").get_active_text()
        useXscreenSaver = self.builder.get_object("useXScrnList").get_active()
        plyBckRes       = self.builder.get_object("playbackResolution")
        offset4Res      = self.builder.get_object("posOffset")
        resolution      = plyBckRes.get_active_text() + offset4Res.get_active_text()
        self.applyType  = self.stateSaver.saveToFile(self.toSavePath, resolution,
                            saveLoc, useXscreenSaver, self.xScreenVal)
        self.helpLabel.set_markup(self.savedLabel)

    def applySttngs(self, widget, data=None):
        os.system("killall xwinwrap &")
        if self.applyType == 1:
            os.system("bash -c '~/.animatedBGstarter.sh' &")
            os.system("bash -c '~/.animatedBGstarter2.sh' &")
        elif self.applyType == 2:
            os.system("nitrogen --restore &")
        else:
            os.system("nitrogen --restore &")
        self.helpLabel.set_markup(self.appliedLabel)

    def killXWinWrp(self, widget, data=None):
        os.system("killall xwinwrap &")
        self.helpLabel.set_markup(self.stoppedLabel)

    def passXScreenVal(self, widget):
        xSvrListStore   = self.builder.get_object("XScreensaver List")
        row             = widget.get_cursor()
        path            = gtk.TreePath(row.path)
        treeiter        = xSvrListStore.get_iter(path[0])
        self.xScreenVal = xSvrListStore.get_value(treeiter, 0)

    def clearSelection(self, widget, data=None):
        self.clear()

    def clear(self):
        imageGrid = self.builder.get_object("imageGrid")

        while True:
            if imageGrid.get_child_at(0,0)!= None:
                imageGrid.remove_row(0)
            else:
                break

        imageGrid.attach(self.gridLabel, 0, 0, 1, 1)
        self.helpLabel.set_markup(self.defaultLabel)
        self.loadProgress.set_text("")
        self.loadProgress.set_fraction(0.0)
        self.toSavePath = None
        self.applyType  = 1  # Default to XWinWrap

    def closeProgram(self, widget, data=None):
        sys.exit(0)



if __name__ == "__main__":
  main = GWinWrap()
  gtk.main()
