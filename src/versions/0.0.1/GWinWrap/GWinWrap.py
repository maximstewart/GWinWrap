#!/usr/bin/env python

import os, cairo, sys, gi, re, threading, subprocess, hashlib, signal, time

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk as gtk, Gdk as gdk, GObject as gobject, GdkPixbuf

from os import listdir
from os.path import isfile, join
from threading import Thread

from utils import SaveStateToXWinWarp, SaveGWinWrapSettings

gdk.threads_init()


class GWinWrap:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("resources/GWinWrap.glade")
        self.builder.connect_signals(self)

        # Get window and connect signals
        self.stateSaver = SaveStateToXWinWarp()
        self.sttngsSver = SaveGWinWrapSettings()
        window          = self.builder.get_object("Main")
        monitors        = self.setWindowData(window)
        window.connect("delete-event", gtk.main_quit)

        print(monitors[1])

        # Add filter to allow only folders to be selected
        dialog         = self.builder.get_object("selectedDirDialog")
        filefilter     = self.builder.get_object("Folders")
        dialog.add_filter(filefilter)

        # Get reference to remove and add it back...
        self.gridLabel    = self.builder.get_object("gridLabel")

        self.focusedImg   = gtk.Image()
        self.usrHome      = os.path.expanduser('~')
        self.xScreenVal   = None
        self.toSavePath   = None # Global file path and type for saving to file
        self.applyType    = 1    # 1 is XWinWrap and 2 is Nitrogen

        self.loadProgress = self.builder.get_object("loadProgress")
        self.helpLabel    = self.builder.get_object("helpLabel")
        self.defaultLabel = "<span>Note: Double click an image to view the video or image.</span>"
        self.savedLabel   = "<span foreground=\"#88cc27\">Saved settings...</span>"
        self.appliedLabel = "<span foreground=\"#88cc27\">Running xwinwrap...</span>"
        self.stoppedLabel = "<span foreground=\"#88cc27\">Stopped xwinwrap...</span>"
        # foreground=\"#ffa800\"
        # foreground=\"#88cc27\"
        # foreground=\"#ff0000\"

        # Fill list xscreensaver
        self.xscrPth      = "/usr/lib/xscreensaver/"
        xscreenList       = self.builder.get_object("XScreensaver List")
        list              = [f for f in listdir(self.xscrPth) if isfile(join(self.xscrPth, f))]
        list.sort()

        for file in list:
            xscreenList.append((file,))

        self.selectedImg  = None  # EventBox holder
        self.defPath      = None
        self.player       = None
        self.imgVwr       = None
        self.demoAreaPid  = None

        self.retrieveSettings()
        window.show()

    def setWindowData(self, window):
        screen    = window.get_screen()
        visual    = screen.get_rgba_visual()
        if visual != None and screen.is_composited():
            window.set_visual(visual)

        window.set_app_paintable(True)
        window.connect("draw", self.area_draw)

        # bind css file
        cssProvider  = gtk.CssProvider()
        cssProvider.load_from_path('resources/stylesheet.css')
        screen       = gdk.Screen.get_default()
        styleContext = gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider, gtk.STYLE_PROVIDER_PRIORITY_USER)

        return self.getMonitorData(screen)

    def area_draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0.64)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def getMonitorData(self, screen):
        monitors = []
        wxhxny   = []

        for m in range(screen.get_n_monitors()):
            monitors.append(screen.get_monitor_geometry(m))

        wxhxny.append(monitors)
        for monitor in monitors:
            wxhxny.append(str(monitor.width) + "x" + str(monitor.height) + "+" + str(monitor.x) + "+" + str(monitor.y))

        return wxhxny


    def setNewDir(self, widget, data=None):
        dir = widget.get_filename()
        Thread(target=self.newDir, args=(dir,)).start()

    def newDir(self, dir):
        imageGrid  = self.builder.get_object("imageGrid")
        dirPath    = dir
        list       = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
        files      = []
        row        = 0
        col        = 0

        for file in list:
            if file.lower().endswith(('.mkv', '.avi', '.flv', '.mov', '.m4v', '.mpg', '.wmv', '.mpeg', '.mp4', '.webm', '.png', '.jpg', '.jpeg', '.gif')):
                files.append(file)

        fractionTick = 1.0 / 1.0 if len(files) == 0 else len(files)
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
                fileHash   = hashlib.sha256(str.encode(fullPathFile)).hexdigest()
                hashImgpth = self.usrHome + "/.thumbnails/normal/" + fileHash + ".png"
                if isfile(hashImgpth) == False:
                    self.generateThumbnail(fullPathFile, hashImgpth)

                thumbnl = self.createGtkImage(hashImgpth, [310, 310])
                eveBox.connect("button_press_event", self.runMplayerProcess, (fullPathFile, file, eveBox,))
                eveBox.connect("enter_notify_event", self.mouseOver, ())
                eveBox.connect("leave_notify_event", self.mouseOut, ())
            elif file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                thumbnl = self.createGtkImage(fullPathFile, [310, 310])
                eveBox.connect("button_press_event", self.runImageViewerProcess, (fullPathFile, file, eveBox,))
                eveBox.connect("enter_notify_event", self.mouseOver, ())
                eveBox.connect("leave_notify_event", self.mouseOut, ())
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

    def generateThumbnail(self, fullPathFile, hashImgpth):
        subprocess.call(["ffmpegthumbnailer", "-t", "65%", "-s", "300", "-c", "jpg", "-i", fullPathFile, "-o", hashImgpth])

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


    def openMainImageViewer(self, widget):
        subprocess.call([self.imgVwr, self.toSavePath])

    def runImageViewerProcess(self, widget, eve, params):
        self.setSelected(params[2])

        if eve.type == gdk.EventType.DOUBLE_BUTTON_PRESS:
            previewWindow = self.builder.get_object("previewWindow")
            previewImg    = self.builder.get_object("previewImg")
            previewImg.set_from_file(params[0])
            previewWindow.show_all()
            previewWindow.popup()

        self.toSavePath = params[0]
        self.applyType  = 2
        self.helpLabel.set_markup("<span foreground=\"#e0cc64\">" + params[1] + "</span>")

    def setSelected(self, eveBox):
      if self.selectedImg:
          col = gdk.RGBA(0.0, 0.0, 0.0, 0.0)
          self.selectedImg.override_background_color(gtk.StateType.NORMAL, col)

      col = gdk.RGBA(0.9, 0.7, 0.4, 0.74)
      eveBox.override_background_color(gtk.StateType.NORMAL, col)
      self.selectedImg = eveBox

    def closePopup(self, widget):
        self.builder.get_object("previewWindow").popdown()

    def mouseOver(self, widget, eve, args):
        hand_cursor = gdk.Cursor(gdk.CursorType.HAND2)
        self.builder.get_object("Main").get_window().set_cursor(hand_cursor)

    def mouseOut(self, widget, eve, args):
        watch_cursor = gdk.Cursor(gdk.CursorType.LEFT_PTR)
        self.builder.get_object("Main").get_window().set_cursor(watch_cursor)

    def toggleXscreenUsageField(self, widget, data=None):
        useXscreenSaver = self.builder.get_object("useXScrnList")
        if useXscreenSaver.get_active():
            self.builder.get_object("xScreenSvrList").set_sensitive(True)
        else:
            self.builder.get_object("xScreenSvrList").set_sensitive(False)

    def popSttingsWindow(self, widget):
        self.builder.get_object("settingsWindow").popup()

    def saveToSettingsFile(self, widget):
        self.defPath = self.builder.get_object("customDefaultPath").get_text().strip()
        self.player  = self.builder.get_object("customVideoPlyr").get_text().strip()
        self.imgVwr  = self.builder.get_object("customImgVwr").get_text().strip()

        self.sttngsSver.saveSettings(self.defPath, self.player, self.imgVwr)

    def retrieveSettings(self):
        data         = self.sttngsSver.retrieveSettings()
        self.defPath = data[0]
        self.player  = data[1]
        self.imgVwr  = data[2]

        self.builder.get_object("customDefaultPath").set_text(self.defPath)
        self.builder.get_object("customVideoPlyr").set_text(self.player)
        self.builder.get_object("customImgVwr").set_text(self.imgVwr)
        self.builder.get_object("selectedDirDialog").set_filename(self.defPath)

    def saveToFile(self, widget, data=None):
        saveLoc         = self.builder.get_object("saveLoc").get_active_text()
        useXscreenSaver = self.builder.get_object("useXScrnList").get_active()
        plyBckRes       = self.builder.get_object("playbackResolution")
        offset4Res      = self.builder.get_object("posOffset")
        resolution      = plyBckRes.get_active_text() + offset4Res.get_active_text()
        self.applyType  = self.stateSaver.saveToFile(self.toSavePath, resolution,
                            saveLoc, useXscreenSaver, self.xScreenVal)
        if self.applyType == -1:
            self.helpLabel.set_markup("<span foreground=\"#e0cc64\">Nothing saved...</span>")
            return

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


    def runMplayerProcess(self, widget, eve, params):
        self.setSelected(params[2])
        video = params[0]

        if eve.type == gdk.EventType.DOUBLE_BUTTON_PRESS:
            if self.player == "mplayer":
                xid     = self.getXID()
                command = [self.player, video, "-slave", "-wid", str(xid), "-really-quiet", "-ao", "null", "-loop", "0"]
                self.runDemoToDrawArea(command)
            else:
                subprocess.call([self.player, video, "-really-quiet", "-ao", "null", "-loop", "0"])

        self.toSavePath = params[0]
        self.applyType  = 1
        self.helpLabel.set_markup("<span foreground=\"#e0cc64\">" + params[1] + "</span>")

    def previewXscreen(self, widget, eve):
        if eve.type == gdk.EventType.DOUBLE_BUTTON_PRESS:
            demoXscrnSaver = self.xscrPth + self.xScreenVal
            xid            = self.getXID()
            command        = [demoXscrnSaver, "-window-id", str(xid)]
            self.runDemoToDrawArea(command)

    def getXID(self):
        # Must be actualized before getting window
        demoWindowPopup = self.builder.get_object("demoPreviewPopWindow")

        if demoWindowPopup.get_visible() == False:
            demoWindowPopup.show_all()
            demoWindowPopup.popup()

        demoPreview = self.builder.get_object("demoPreview")
        drwWindow   = demoPreview.get_window()
        return drwWindow.get_xid()

    def runDemoToDrawArea(self, command):
        self.helpLabel.set_markup("<span foreground=\"#e0cc64\"></span>")

        if self.demoAreaPid:
            os.kill(self.demoAreaPid, signal.SIGTERM) #or signal.SIGKILL
            self.demoAreaPid = None

        time.sleep(.800) # 800 mili-seconds to ensure first process dead
        process          = subprocess.Popen(command)
        self.demoAreaPid = process.pid

    def closeDemoWindow(self, widget, data=None):
        self.builder.get_object("demoPreviewPopWindow").popdown()
        os.kill(self.demoAreaPid, signal.SIGTERM) #or signal.SIGKILL
        self.demoAreaPid = None

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
        self.builder.get_object("xScreenSvrList").set_sensitive(False)
        self.builder.get_object("useXScrnList").set_active(False)
        self.helpLabel.set_markup(self.defaultLabel)
        self.loadProgress.set_text("")
        self.loadProgress.set_fraction(0.0)
        self.toSavePath = None
        self.xScreenVal = None
        self.applyType  = 1  # Default to XWinWrap

    def closeProgram(self, widget, data=None):
        sys.exit(0)



if __name__ == "__main__":
  main = GWinWrap()
  gtk.main()
