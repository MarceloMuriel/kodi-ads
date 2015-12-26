'''
Created on Dec 08, 2015

@author: Hugo Marcelo Muriel A.
'''

import xbmc, xbmcgui
import subprocess, os
import xbmcaddon
import json
import re
import sys

PLUGIN_ID = "service.playback.ads"
addon = xbmcaddon.Addon(PLUGIN_ID)
ROOT_DIR = addon.getAddonInfo('path')
PLAYER_AUDIO = 'mpg321' if 'linux' in sys.platform else 'afplay'

def isVideo(file):
    ''' It checks if the given file has a common video extension '''
    video_file_extensions = (
'.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec', '.aep', '.aepx',
'.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf', '.asx', '.avb',
'.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik', '.bin', '.bix',
'.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel', '.cine', '.cip',
'.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat', '.dav', '.dce',
'.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm', '.dmsm3d', '.dmss',
'.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms', '.dvx', '.dxr',
'.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp', '.fcproject',
'.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp', '.h264', '.hdmov',
'.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf', '.ivr', '.ivs',
'.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg', '.m1v', '.m21',
'.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv', '.mj2', '.mjp',
'.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov', '.movie', '.mp21',
'.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2', '.mpgindex', '.mpl',
'.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv', '.mvb', '.mvc',
'.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv', '.nvc', '.ogm',
'.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs', '.playlist', '.plproj',
'.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva', '.pvr', '.pxv',
'.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm', '.rmd', '.rmd',
'.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl', '.sbk', '.sbt',
'.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv', '.smi', '.smi',
'.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf', '.ssm', '.stl', '.str', '.stx', '.svi', '.swf', '.swi',
'.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp', '.ts', '.tsp', '.ttxt',
'.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg', '.vem', '.vep', '.vf', '.vft',
'.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3', '.vp6', '.vp7', '.vpj',
'.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv', '.wmx', '.wot', '.wp3',
'.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog', '.yuv', '.zeg',
'.zm1', '.zm2', '.zm3', '.zmv')
    isVideo = False
    if os.path.isfile(file):
        if file[file.rfind('.'):] in video_file_extensions:
            isVideo = True
    
    return isVideo

class XBMCPlayer( xbmc.Player ):
    def __init__( self, *args ):
	self.enabled = True

    def onPlayBackStarted( self ):
        xbmc.log("KODIPUB: Playback Started")

    def onPlayBackEnded( self ):
        xbmc.log("KODIPUB: Playback Ended")

    def onPlayBackStopped( self ):
	# The stop command can only come from the user or another addon
	self.enabled = False
        xbmc.log("KODIPUB: Playback Stopped")

    def canRun(self):
	return self.enabled

player = XBMCPlayer()

class PictureWindow(xbmcgui.Window):
    def __init__(self):
        pass
    def setPic(self, path):
        self.addControl(xbmcgui.ControlImage(0, 0, self.getWidth(), self.getHeight(), path))
    def closeAfter(self, msecs):
        xbmc.sleep(msecs)
        self.close()
    
def run():
    # Try to create the required folders
    videos_dir = addon.getSetting('video_folder')
    audios_dir = addon.getSetting('audio_folder')
    # Read the files
    videos = os.listdir(videos_dir) if os.path.isdir(videos_dir) else []
    videos = [v for v in videos if isVideo(os.path.join(videos_dir, v))]
    
    # Kill any previous audio player
    # cmd_kill = "pid=$(<'{0}/audioplayer.pid'); kill $pid; pkill {1}".format(ROOT_DIR, PLAYER_AUDIO)
    with open('{0}/audioplayer.pid'.format(ROOT_DIR)) as f: pid = f.read().strip()
    cmd_kill = "kill {0}; pkill {1};".format(pid, PLAYER_AUDIO)
    os.system(cmd_kill)
    # Launch the audio player in the background
    cmd = "bash '{0}/audioplayer.sh' {1} {2} & echo $! > '{0}/audioplayer.pid'".format(ROOT_DIR, PLAYER_AUDIO, audios_dir)
    os.system(cmd)
    
    if not videos: xbmc.log('KODIPUB: No videos to play back at {0}!'.format(videos_dir)); return

    # Display black image
    blackWindow = PictureWindow()
    blackWindow.setPic(ROOT_DIR + '/black_1280x720.jpg')
    blackWindow.show()   
 
    # Read the ads
    ads = []
    MAX_ADS = 10
    
    def parseAd(mtype, path, time):
        ad = None
        if path and time:
            # parse the time
            s = int(''.join(re.findall(r'\d+', time)) or 0)
            # get the format (s, m, h)
            fidx = len(str(s))
            f = time[fidx: fidx + 1] if fidx < len(time) else 'm'
            if f == 'm': s = s * 60
            elif f == 'h': s = s * 60 * 60
            else: pass  # seconds do nothing
            # Check if it has to repeat
            r = True if 'r' in time else False 
            # Create the add
            ad = {'type': mtype, 'path': path, 'time': s, 'repeat': r}
        
        return ad
    
    for idx in range(1, MAX_ADS + 1):
        v = addon.getSetting('v{0}'.format(idx))
        t = addon.getSetting('v{0}_t'.format(idx))
        ad = parseAd('video', v, t)
        if ad: ads.append(ad)
        i = addon.getSetting('i{0}'.format(idx))
        t = addon.getSetting('i{0}_t'.format(idx))
        ad = parseAd('image', i, t)
        if ad: ads.append(ad)
    
    vidx = 0
    cum_time = 0
    vid_time = 0
    curr_time = 0
    # Set the volume to 0
    xbmc.executebuiltin('SetVolume(1)')
    while(not xbmc.abortRequested and player.canRun()):
        # Default time to sleep every cycle at the end
        sleepSecs = 1
        vid = os.path.join(videos_dir, videos[vidx])
        # Play back video
        if not player.isPlaying():
            # Play back the current video
            player.play(vid)
            # Resuming playback?
            if curr_time > 0:
                xbmc.log('KODIPUB: Resuming playback after ad at {0}s'.format(curr_time))
                player.seekTime(curr_time)
                # Reset time
                curr_time = 0
            else:
                cum_time += vid_time
                # Get a copy of the total video time
                vid_time = player.getTotalTime()
                msg = 'KODIPUB: Playing next video {0} @ idx {1}, {2}s long, {3}s cum_time'
                xbmc.log(msg.format(vid, vidx, vid_time, cum_time))
                # Sleep at least 500 ms to avoid launching the same ad twice
                xbmc.sleep(1000)
            # Point to the next video
            vidx = vidx + 1 if vidx + 1 < len(videos) else 0
        else:
            # Check if it is time to playback an ad
            for ad in ads:
                t = cum_time + player.getTime()
                if t > 0 and int(round(t)) % ad['time'] == 0:
                    print('KODIPUB: total time:', t)
                    # Save the current playback time to resume later
                    curr_time = player.getTime()
                    # Pause while waiting to see if it is a video or image
                    player.pause()
                    xbmc.log('KODIPUB: playing ad: ' + ad['path'])
                    if ad['type'] == 'video':
                        # Point to current video (instead of next)
                        vidx = vidx - 1 if vidx >= 1 else len(videos) - 1
                        # player.stop()
                        # play the ad
                        player.play(ad['path'])
                        # Wait until the ad is over
                        xbmc.sleep(int(round(player.getTotalTime() * 1000)))
                    elif ad['type'] == 'image':
                        picWindow = PictureWindow()
                        picWindow.setPic(ad['path'])
                        picWindow.show()
                        xbmc.sleep(10000)
                        picWindow.close()
                        del picWindow
                        # Resume playback
                        player.pause()
                    # If the ad must not repeat, remove it
                    if not ad['repeat']: ads.remove(ad)
                    # No need to Sleep more
                    sleepSecs = 0
                    # Only play one ad at a time 
                    break
         
        # Sleep for som time in ms
        if sleepSecs > 0:
            # Take the smallest time, the video might be close to finish
            sleepSecs = min(sleepSecs, player.getTotalTime() - player.getTime())
            # xbmc.log('KODIPUB: Sleeping {0}s'.format(sleepSecs))
            xbmc.sleep(int(round(sleepSecs * 1000)))
    
    print("KODIPUB: Stopping KodiPub...")    
    # Kill the audio player
    with open('{0}/audioplayer.pid'.format(ROOT_DIR)) as f: pid = f.read().strip()
    cmd_kill = "kill {0}; pkill {1};".format(pid, PLAYER_AUDIO)
    os.system(cmd_kill)   
    # Set the volume to the max value   
    xbmc.executebuiltin('SetVolume(100)')    
    # Stop the player 
    player.stop()
    # Hide the background
    blackWindow.close()
    
run()
