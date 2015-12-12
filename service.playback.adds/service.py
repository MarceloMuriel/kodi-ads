'''
Created on Dec 08, 2015

@author: Hugo Marcelo Muriel A.
'''

import xbmc, xbmcgui
import subprocess, os
import xbmcaddon
import json

PLUGIN_ID = "service.playback.ads"
addon = xbmcaddon.Addon(PLUGIN_ID)

# Read the ads.json
ads = json.load(open('ressources/ads.json')) 
print(ads)

# Try to create the required folders
videos = addon.getSetting('video_folder')
ads = addon.getSetting('ads_folder')
audios = addon.getSetting('audio_folder')

while(not xbmc.abortRequested):
    # Playback time in seconds
    if xbmc.getGlobalIdleTime() > (10 * 60):
        if xbmc.Player().isPlaying():
            xbmc.Player().stop()
    # Sleep in ms
    xbmc.sleep(60000)
