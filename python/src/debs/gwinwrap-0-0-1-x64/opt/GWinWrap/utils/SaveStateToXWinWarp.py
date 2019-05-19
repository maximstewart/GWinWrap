#!/usr/bin/env python

import os

class SaveStateToXWinWarp:
    def __init__(self):
        self.fileWriter  = None
        self.toSavePath    = None
        self.useXSvrn    = None
        self.xScreenVal  = None
        self.sveFileLoc  = None
        self.resolution  = None

    def saveToFile(self, toSavePath, resolution,
                    saveLoc, useXSvrn, xScreenVal):

        self.toSavePath = toSavePath
        self.useXSvrn   = useXSvrn
        self.xScreenVal = xScreenVal
        self.resolution = resolution
        userPth         = os.path.expanduser('~')

        # Saves to file with selected and needed settings
        if toSavePath:
            if toSavePath.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                self.sveFileLoc = userPth + "/" + ".config/nitrogen/bg-saved.cfg"
            else:
                self.sveFileLoc = userPth + "/" + saveLoc
        elif useXSvrn and xScreenVal:
            self.sveFileLoc = userPth + "/" + saveLoc
        else:
            return -1

        if self.sveFileLoc:
            self.fileWriter = open(self.sveFileLoc, "w")

        return self.startSave()

    def startSave(self):
        applyType = 1
        output    = None

        print("XScreen: " + str(self.useXSvrn))
        print(self.fileWriter)

        # XSCREENSAVER
        if self.useXSvrn:
            output = "xwinwrap -ov -g " + self.resolution + " -st -sp -b -nf -s -ni -- /usr/lib/xscreensaver/" + self.xScreenVal + " -window-id WID -root";
        # GIF
        elif self.toSavePath.lower().endswith(('.gif')):
            output = "xwinwrap -ov -g " + self.resolution + " -st -sp -b -nf -s -ni -- gifview -a -w WID " + self.toSavePath;
        # Standard images using nitrogen
        elif self.toSavePath.lower().endswith(('.png', 'jpg', '.jpeg')):
            output = "[xin_0] \n file=" + self.toSavePath + "\nmode=0 \nbgcolor=#000000\n[xin_1] \nfile=" + self.toSavePath + "\nmode=0 \nbgcolor=#000000";
            applyType = 2;
        # VIDEO
        else:
            output = "xwinwrap -ov -g " + self.resolution + " -st -sp -b -nf -s -ni -- mplayer -wid WID -really-quiet -ao null -loop 0 " + self.toSavePath;
            pass

        if self.fileWriter:
            self.fileWriter.write(output)
            self.fileWriter.close()

        return applyType;
