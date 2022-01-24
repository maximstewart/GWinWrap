#!/usr/bin/env python

import os, json

class SaveGWinWrapSettings:
    def __init__(self, settings):
        self.config_file = settings.get_config_file()

        if os.path.isfile(self.config_file) == False:
            open(self.config_file, 'a').close()


    def save_settings(self, start_path, default_player, default_img_viewer):
        data = {}
        data['settings'] = []

        data['settings'].append({
          'start_path': start_path,
          'default_player': default_player,
          'default_img_viewer': default_img_viewer
        })

        with open(self.config_file, 'w') as outfile:
            json.dump(data, outfile, separators=(',', ':'), indent=4)


    def retrieve_settings(self):
        data = []

        with open(self.config_file) as infile:
            try:
                _data = json.load(infile)
                for obj in _data['settings']:
                    data = [obj['start_path'], obj['default_player'], obj['default_img_viewer']]
            except Exception as e:
                print(repr(e))
                data = ['', 'mplayer', 'xdg-open']


        if data[0] == '':
            data[0] = ''

        if data[1] == '':
            data[1] = 'mplayer'

        if data[2] == '':
            data[2] = 'xdg-open'

        return data
