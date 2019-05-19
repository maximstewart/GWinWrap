#!/usr/bin/env python

import os, json

class SaveGWinWrapSettings:
    def __init__(self):
        configFolder    = os.path.expanduser('~') + "/.config/gwinwrap/"
        self.configFile = configFolder + "settings.ini"

        if os.path.isdir(configFolder) == False:
            os.mkdir(configFolder)

        if os.path.isfile(self.configFile) == False:
            open(self.configFile, 'a').close()


    def saveSettings(self, player, imgVwr):
        data = {}
        data['gwinwrap_settings'] = []

        data['gwinwrap_settings'].append({
          'player': player,
          'imgvwr': imgVwr
        })

        with open(self.configFile, 'w') as outfile:
            json.dump(data, outfile)



    def retrieveSettings(self):
        returnData = []

        with open(self.configFile) as infile:
            try:
                data = json.load(infile)
                for obj in data['gwinwrap_settings']:
                    returnData = [obj['player'], obj['imgvwr']]
            except Exception as e:
                returnData = ['mplayer', 'xdg-open']

        if returnData[0] == '':
            returnData[0] = 'mplayer'

        if returnData[1] == '':
            returnData[1] = 'xdg-open'

        return returnData
