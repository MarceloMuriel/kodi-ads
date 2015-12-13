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
ROOT_DIR = addon.getAddonInfo('path')

def run():
    # Try to create the required folders
    videos_dir = addon.getSetting('video_folder')
    audios_dir = addon.getSetting('audio_folder')
    # Read the files
    videos = os.listdir(videos_dir) if os.path.isdir(videos_dir) else []
    audios = os.listdir(audios_dir) if os.path.isdir(audios_dir) else []
    
    if not videos: print('No videos to play back at {0}!'.format(videos_dir)); return
    
    while(not xbmc.abortRequested):
        # Playback time in seconds
        if xbmc.getGlobalIdleTime() > (10 * 60):
            if xbmc.Player().isPlaying():
                xbmc.Player().stop()
        # Sleep in ms
        xbmc.sleep(60000)

run()