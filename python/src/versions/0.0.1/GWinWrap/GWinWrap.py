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
        self.xScreenVal = None
        self.toSavePath = None # Global file path and type for saving to file
        self.applyType  = 1 # 1 is XWinWrap and 2 is Nitrogen

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
        self.clear()
        imageGrid  = self.builder.get_object("imageGrid")
        path       = dir
        files      = []
        list       = [f for f in listdir(path) if isfile(join(path, f))]
        row        = 0
        col        = 0

        for file in list:
            if file.lower().endswith(('.mkv', '.avi', '.flv', '.mov', '.m4v', '.mpg', '.wmv', '.mpeg', '.mp4', '.webm', '.png', '.jpg', '.jpeg', '.gif')):
                files.append(file)

        imageGrid.remove_column(0)
        for file in files:
            fullPathFile = path + "/" + file
            eveBox       = gtk.EventBox()
            thumbnl      = gtk.Image()

            if file.lower().endswith(('.mkv', '.avi', '.flv', '.mov', '.m4v', '.mpg', '.wmv', '.mpeg', '.mp4', '.webm')):
                subprocess.call(["ffmpegthumbnailer", "-t", "65%", "-s", "300", "-c", "jpg", "-i", fullPathFile, "-o", "/tmp/image.png"])
                thumbnl = self.createImage("/tmp/image.png")
                eveBox.connect("button_press_event", self.runMplayerProcess, fullPathFile)
            elif file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                thumbnl = self.createImage(fullPathFile)
                eveBox.connect("button_press_event", self.runImageViewerProcess, fullPathFile)
            else:
                print("Not a video or image file.")
                return

            gobject.idle_add(self.preGridSetup, (eveBox, thumbnl, ))
            gobject.idle_add(self.addToGrid, (imageGrid, eveBox, col, row,))

            col += 1
            if col == 2:
                col = 0
                row += 1

    def preGridSetup(self, args):
        args[0].show()
        args[1].show()
        args[0].add(args[1])

    def createImage(self, arg):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    filename  = arg,
                    width     = 310,
                    height    = 310,
                    preserve_aspect_ratio = True)
        return gtk.Image.new_from_pixbuf(pixbuf)

    def addToGrid(self, args):
        args[0].attach(args[1], args[2], args[3], 1, 1)

    def runMplayerProcess(self, widget, eve, fullPathFile):
        if eve.type == gdk.EventType.DOUBLE_BUTTON_PRESS:
            subprocess.call(["mplayer", "-really-quiet", "-ao", "null", "-loop", "0", fullPathFile])

        self.toSavePath = fullPathFile
        self.applyType  = 1  # Set to XWinWrap

    def runImageViewerProcess(self, widget, eve, fullPathFile):
        if eve.type == gdk.EventType.DOUBLE_BUTTON_PRESS:
            subprocess.call(["xdg-open",  fullPathFile])

        self.toSavePath = fullPathFile
        self.applyType  = 2  # Set to Nitrogen

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

    def applySttngs(self, widget, data=None):
        os.system("killall xwinwrap &")
        if self.applyType == 1:
            os.system("bash -c '~/.animatedBGstarter.sh' &")
            os.system("bash -c '~/.animatedBGstarter2.sh' &")
        elif self.applyType == 2:
            os.system("nitrogen --restore &")
        else:
            os.system("nitrogen --restore &")


    def killXWinWrp(self, widget, data=None):
        os.system("killall xwinwrap &")

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
        self.toSavePath = None
        self.applyType  = 1  # Default to XWinWrap

    def closeProgram(self, widget, data=None):
        sys.exit(0)



if __name__ == "__main__":
  main = GWinWrap()
  gtk.main()
