# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    The code present on this file had as
    initial input the X-Sopcast plugin code
    by Cristi-Atlanta

"""
     
import xbmc,xbmcgui,xbmcplugin,urllib2,os,sys,subprocess,xbmcvfs,socket    
from utils.pluginxbmc import *
from utils.utilities import handle_wait    
    
""" Sopcast Dependent variables are listed below"""   
    
LISTA_SOP='http://www.sopcast.com/chlist.xml'
SPSC_BINARY = "sp-sc-auth"
SPSC_LOG = os.path.join(pastaperfil,'sopcast','sopcast.log')
LOCAL_PORT = settings.getSetting('local_port')
VIDEO_PORT = settings.getSetting('video_port')
BUFER_SIZE = int(settings.getSetting('buffer_size'))
if(settings.getSetting('auto_ip')):
    LOCAL_IP=xbmc.getIPAddress()
else: LOCAL_IP=settings.getSetting('localhost')

""" 
Addon functions related to sopcast

Main functions:
sopstreams(name,iconimage,sop) -> This function processes the id/sop url received as argument and does the magic for windows. If the OS is not windows, it sends the processed url to sopstreams_function
sopstreams_builtin(name,iconimage,sop) -> This function processes the url received from sopstreams and does the magic for all *nix based OS's.

Classes:
SopWindowsPlayer -> Inheritance of XBMC Player class used only for Windows
streamplayer -> Inheritance of XBMC Player class used for Linux/osx/Android

Sopcast Utils:
sop_sleep(time , spsc_pid) -> sopcast_binary pid sleep function. For all supported OS's except Windows.
handle_wait_socket(time_to_wait,title,text,segunda='') -> Timer to check if sopcast local server has started (attempt to connect on sopcast local server port). This function is Windows only.
break_sopcast() -> intentionally break the sopcast player in windows to avoid double sound created by the running sopcastp2p service
"""


""" Sopcast Main functions"""   

def sopstreams(name,iconimage,sop):
	if not iconimage: iconimage = os.path.join(addonpath,'resources','art','sopcast_logo.jpg')
	if "sop://" not in sop: sop = "sop://broker.sopcast.com:3912/" + sop
	else: pass
	print "Starting Player Sop URL: " + str(sop)
	if not xbmc.getCondVisibility('system.platform.windows'):
	    if xbmc.getCondVisibility('System.Platform.Android') or settings.getSetting('force_android') == "true":
	    	if  settings.getSetting('external_sopcast') == "0":
			versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
			if versionNumber >= 13:
				xbmc.executebuiltin('XBMC.StartAndroidActivity("org.sopcast.android","android.intent.action.VIEW","",'+sop+')')
			else:	mensagemok(traducao(40000),traducao(40196),traducao(40197))    
		else: sopstreams_builtin(name,iconimage,sop)
            else: sopstreams_builtin(name,iconimage,sop)
        else:
            cmd = ['sc','sdshow','sopcastp2p']
            import subprocess
            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
            config = True  
            for line in proc.stdout:
                    if " 1060:" in line.rstrip():
                        config = False
                        print "Configuration is not DONE!"
            if config == False: mensagemok(traducao(40000),traducao(40180),traducao(40181), traducao(40182))
            else:
                import _winreg
                aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                #Dirty hack to break sopcast h264 codec so double sound can be avoided
                try:
                	aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
                	name, value, type = _winreg.EnumValue(aKey, 0)
                	codec_file = os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx')
                	_winreg.CloseKey(aKey)
                	if xbmcvfs.exists(codec_file): xbmcvfs.rename(codec_file,os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx.old'))
                except:pass
                aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                aKey = _winreg.OpenKey(aReg, r'SYSTEM\CurrentControlSet\Services\sopcastp2p\Parameters', 3, _winreg.KEY_WRITE)
                _winreg.SetValueEx(aKey,"AppParameters",0, _winreg.REG_SZ, sop)  
                _winreg.CloseKey(aKey)
                cmd = ['sc','start','sopcastp2p']
                import subprocess
                proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                servicecreator = False
                for line in proc.stdout:
                        print "linha " + line.rstrip()
                res = handle_wait_socket(int(settings.getSetting('socket_time')),traducao(40000),traducao(40183))
                print "rest",res
                if res == True:
                        print "Server created, waiting 5 seconds for confirmation"
                        try: sock.close()
                        except: pass
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        handle_wait(int(settings.getSetting('stream_time')),traducao(40000),traducao(40184),segunda='')
                        try:
                                result = sock.connect(('127.0.0.1',8902))
                                connected = True
                        except: connected = False
                        if connected == True:
                                playlist = xbmc.PlayList(1)
                                playlist.clear()
                                listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
                                listitem.setLabel(name)
                                listitem.setInfo("Video", {"Title":name})
                                listitem.setProperty('mimetype', 'video/x-msvideo')
                                listitem.setProperty('IsPlayable', 'true')
				windows_sop_url = "http://127.0.0.1:8902/tv.asf"
				listitem.setPath(path=windows_sop_url)
                                playlist.add(windows_sop_url, listitem)
				xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
                                player = SopWindowsPlayer()
				if int(sys.argv[1]) < 0:
                                	player.play(playlist)
                                while player._playbackLock:
                                    xbmc.sleep(5000)
                        else: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40040), 1,addonpath+"/icon.png"))
                print "Player reached the end"
                cmd = ['sc','stop','sopcastp2p']
                import subprocess
                proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                servicecreator = False
                for line in proc.stdout:
                        print "linha " + line.rstrip()
			 #dirty hack to break sopcast.exe player codec - renaming the file later
                import _winreg
                aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                try:
                	aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
                	name, value, type = _winreg.EnumValue(aKey, 0)
                	codec_file = os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx.old')
                	_winreg.CloseKey(aKey)
                	if xbmcvfs.exists(codec_file): xbmcvfs.rename(codec_file,os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx'))
                except:pass


def sopstreams_builtin(name,iconimage,sop):
    try:
        os.system("killall -9 "+SPSC_BINARY)
        global spsc
        if xbmc.getCondVisibility('System.Platform.Linux') and settings.getSetting('force_android') == "false":

        	if os.uname()[4] == "armv6l" or os.uname()[4] == "armv7l" or settings.getSetting('openelecx86_64') == "true":
        		if settings.getSetting('sop_debug_mode') == "false":
        			cmd = [os.path.join(pastaperfil,'sopcast','qemu-i386'),os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT)]
			else: 
				cmd = [os.path.join(pastaperfil,'sopcast','qemu-i386'),os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT),">",SPSC_LOG]

		elif settings.getSetting('openeleci386') == "true":
        		if settings.getSetting('sop_debug_mode') == "false":
        			cmd = [os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT)]
			else: 
				cmd = [os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT),">",SPSC_LOG]

		else: 
			if settings.getSetting('sop_debug_mode') == "false":
				cmd = [os.path.join(pastaperfil,'sopcast','ld-linux.so.2'),'--library-path',os.path.join(pastaperfil,'sopcast','lib'),os.path.join(pastaperfil,'sopcast',SPSC_BINARY), sop, str(LOCAL_PORT), str(VIDEO_PORT)]
			else:
				cmd = [os.path.join(pastaperfil,'sopcast','ld-linux.so.2'),'--library-path',os.path.join(pastaperfil,'sopcast','lib'),os.path.join(pastaperfil,'sopcast',SPSC_BINARY), sop, str(LOCAL_PORT), str(VIDEO_PORT),">",SPSC_LOG]
        elif xbmc.getCondVisibility('System.Platform.OSX'):
        	if settings.getSetting('sop_debug_mode') == "false":
			cmd = [os.path.join(pastaperfil,'sopcast','sp-sc-auth'), str(sop), str(LOCAL_PORT), str(VIDEO_PORT)]
		else:
			cmd = [os.path.join(pastaperfil,'sopcast','sp-sc-auth'), str(sop), str(LOCAL_PORT), str(VIDEO_PORT),">",str(SPSC_LOG)]	
        elif xbmc.getCondVisibility('System.Platform.Android') or settings.getSetting('force_android') == "true":
        	if settings.getSetting('sop_debug_mode') == "false":
			cmd = [str(settings.getSetting('android_sopclient')), str(sop), str(LOCAL_PORT), str(VIDEO_PORT)]
		else:
			cmd = [str(settings.getSetting('android_sopclient')), str(sop), str(LOCAL_PORT), str(VIDEO_PORT),">",str(SPSC_LOG)]	
	print sop
        print cmd
        spsc = subprocess.Popen(cmd, shell=False, bufsize=BUFER_SIZE,stdin=None, stdout=None, stderr=None)
        listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        listitem.setLabel(name)
        listitem.setInfo('video', {'Title': name})
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
	listitem.setPath(path=url)
        xbmc.sleep(int(settings.getSetting('wait_time')))
        res=False
        counter=50
        print "tou aqui"
        ret = mensagemprogresso.create(traducao(40000),"SopCast",traducao(40039))
        print "criei a msg progresso"
        mensagemprogresso.update(0)
        while counter > 0 and spsc.pid:
	    if mensagemprogresso.iscanceled():
	    	mensagemprogress.close()
           	try: os.kill(self.spsc_pid,9)
            	except: pass
                break
            xbmc.sleep(400)
            counter -= 1
	    mensagemprogresso.update(int((1-(counter/50.0))*100))
            try:
                urllib2.urlopen(url)
                counter=0
                res=sop_sleep(200 , spsc.pid)
                break
            except:pass
                    
        if res:
	    mensagemprogresso.update(100)
	    xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
            player = streamplayer(xbmc.PLAYER_CORE_AUTO , spsc_pid=spsc.pid , listitem=listitem)
            if int(sys.argv[1]) < 0:
            	player.play(url, listitem)
            while player._playbackLock:
                xbmc.sleep(500)
        else: xbmc.executebuiltin("Notification(%s,%s,%i)" % (traducao(40000), traducao(40040), 1))
    except: pass
    try: os.kill(self.spsc_pid,9)
    except: pass
    xbmc.sleep(100)
    try:os.system("killall -9 "+SPSC_BINARY)
    except:pass
    xbmc.sleep(100)
    try:spsc.kill()
    except:pass
    xbmc.sleep(100)
    try:spsc.wait()
    except:pass
    xbmc.sleep(100)           
    try: os.kill(spsc.pid,9)
    except: pass
    mensagemprogresso.close()
    print "Player chegou mesmo ao fim"
    
    
""" Sopcast Player classes """   


class SopWindowsPlayer(xbmc.Player):
      def __init__(self):
            self._playbackLock = True
            print "Criou o player"
            
      def onPlayBackStarted(self):
            print "Comecou o player"
                              
      def onPlayBackStopped(self):
            print "Parou o player"
            self._playbackLock = False
            import subprocess
            cmd = ['sc','stop','sopcastp2p']
            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
            for line in proc.stdout:
                    print line.rstrip()


      def onPlayBackEnded(self):              
            self.onPlayBackStopped()
            print 'Chegou ao fim. Playback terminou.'



class streamplayer(xbmc.Player):
    def __init__( self , *args, **kwargs):
        self.spsc_pid=kwargs.get('spsc_pid')
        self.listitem=kwargs.get('listitem')
        self._playbackLock = True

    def onPlayBackStarted(self):
        mensagemprogresso.close()
        if xbmc.Player(xbmc.PLAYER_CORE_AUTO).getPlayingFile() != "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/":
            try: os.kill(self.spsc_pid,9)
            except: pass
        else: pass

    def onPlayBackEnded(self):
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
        xbmc.sleep(300)
        if os.path.exists("/proc/"+str(self.spsc_pid)) and xbmc.getCondVisibility("Window.IsActive(epg.xml)") and settings.getSetting('safe_stop')=="true":
            if not xbmc.Player(xbmc.PLAYER_CORE_AUTO).isPlaying():
                player = streamplayer(xbmc.PLAYER_CORE_AUTO , spsc_pid=self.spsc_pid , listitem=self.listitem)
                player.play(url, self.listitem)     

    def onPlayBackStopped(self):
        self._playbackLock = False
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
        xbmc.sleep(300)
        if os.path.exists("/proc/"+str(self.spsc_pid)) and xbmc.getCondVisibility("Window.IsActive(epg.xml)") and settings.getSetting('safe_stop')=="true":
            if not xbmc.Player(xbmc.PLAYER_CORE_AUTO).isPlaying(): 
                player = streamplayer(xbmc.PLAYER_CORE_AUTO , spsc_pid=self.spsc_pid , listitem=self.listitem)
                player.play(url, self.listitem)
        else:
            try: os.kill(self.spsc_pid,9)
            except: pass
                         
""" Sopcast Utils"""   

def handle_wait_socket(time_to_wait,title,text,segunda=''):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        ret = mensagemprogresso.create(' '+title)
        secs=0
        percent=0
        increment = int(100 / time_to_wait)
        cancelled = False
        while secs < time_to_wait:
                try:
                        result = sock.connect(('127.0.0.1',8902))
                        connected = True
                        print "Connected to port 8902, server is working"
                        break
                        sock.close()
                except:
                        print "Still hasn't connected"
                secs = secs + 1
                percent = increment*secs
                secs_left = str((time_to_wait - secs))
                if segunda=='': remaining_display = traducao(40187) + " " + str(percent) + " %"
                else: remaining_display=segunda
                mensagemprogresso.update(percent,text,remaining_display)
                xbmc.sleep(1000)
                if (mensagemprogresso.iscanceled()):
                        cancelled = True
                        break
        if cancelled == True:
                return False
        elif connected == True:
                print "connected true na condicao"
                mensagemprogresso.close()
                return True
        else:
                mensagemprogresso.close()
                return False
                
def sop_sleep(time , spsc_pid):
    counter=0
    increment=200
    path="/proc/%s" % str(spsc_pid)
    try:
      while counter < time and spsc_pid>0 and not xbmc.abortRequested:
        counter += increment
        xbmc.sleep(increment)
    except: return True
        
    if counter < time: return False
    else: return True

#dirty hack to break sopcast.exe player codec - renaming the file again in case xbmc crashed    
def break_sopcast():
	if xbmc.getCondVisibility('system.platform.windows'):
		import _winreg
		aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
		try:
			aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
			name, value, type = _winreg.EnumValue(aKey, 0)
			codec_file = os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx.old')
			_winreg.CloseKey(aKey)
			if xbmcvfs.exists(codec_file): xbmcvfs.rename(codec_file,os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx'))
		except:pass

