# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains the function that brigdes the addon to the acecore.py file
    
    Functions:
    
    load_local_torrent() -> Load a local .torrent file
    acestreams(name,iconimage,chid) -> Function that interprets the received url (acestream://,*.acelive,ts://) and sends it to acestreams_builtin
    acestreams_builtin(name,iconimage,chid -> Bridge to acecore.py file
   	

"""
    
import xbmc,xbmcgui,xbmcplugin,urllib,xbmcvfs,os,subprocess
from peertopeerutils.pluginxbmc import *
from history import *

aceport=62062

def load_local_torrent():
	torrent_file = xbmcgui.Dialog().browse(int(1), translate(600028), 'myprograms','.torrent')
	if torrent_file:
		if xbmc.getCondVisibility('system.platform.windows'):
			acestreams("Local .torrent ("+str("file:\\" + torrent_file) +")","",'file:\\' + torrent_file)
		else:
			acestreams("Local .torrent ("+str("file://" + torrent_file) +")","",'file://' + torrent_file)
	else: pass

def acestreams(name,iconimage,chid):
	if not iconimage: iconimage=os.path.join(addonpath,'resources','art','acelogofull.jpg')
	else: iconimage = urllib.unquote(iconimage)
	if settings.getSetting('addon_history') == "true":
		try: add_to_history(name, str(chid),1, iconimage)
		except: pass
	if settings.getSetting('engine_app') != '2' and settings.getSetting('engine_app') != '3':
		if settings.getSetting('aceplay_type') == "2":
			pDialog = xbmcgui.DialogProgress()
			ret = pDialog.create(translate(40000), translate(40154),translate(40155),translate(40156))
			pDialog.update(0)
			xbmc.sleep(3000)
			pDialog.update(100)
			pDialog.close()
			ip_adress = settings.getSetting('ip_addr')
			proxy_port = settings.getSetting('aceporta')
			chid=chid.replace('acestream://','').replace('ts://','')
			strm = "http://" + ip_adress + ":" + proxy_port + "/pid/" + chid + "/stream.mp4"
			listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
			listitem.setLabel(name + " (" + chid + ")")
			listitem.setInfo('video', {'Title': name + " (" + chid + ")"})
			xbmc.Player().play(strm,listitem)
		else: acestreams_builtin(name,iconimage,chid)
	else:
		if '.acelive' in chid: pass
		elif '.torrent' in chid: pass
		else:
			if 'acestream://' in chid: pass
			else: chid = 'acestream://' + chid
		if settings.getSetting('engine_app') == '2':
			xbmc.executebuiltin('XBMC.StartAndroidActivity("org.acestream","android.intent.action.VIEW","","'+chid+'")')
		elif settings.getSetting('engine_app') == '3':
			xbmc.executebuiltin('XBMC.StartAndroidActivity("ru.vidsoftware.acestreamcontroller.free","android.intent.action.VIEW","","'+chid+'")')

def acestreams_builtin(name,iconimage,chid):
    if xbmc.getCondVisibility('system.platform.windows'):
        try:
            import _winreg
            t = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\AceStream')
            needed_value =  _winreg.QueryValueEx(t , 'EnginePath')[0]
            print needed_value.replace('\\','\\\\')
            subprocess.Popen("wmic process where ExecutablePath='"+needed_value.replace('\\','\\\\')+"' delete",shell=True)
            xbmc.sleep(200)
            subprocess.Popen('taskkill /F /IM ace_player.exe /T',shell=True)
            xbmc.sleep(200)
        except: pass
    elif xbmc.getCondVisibility('System.Platform.OSX'):
        if settings.getSetting('shutdown-engine') == "true":
            os.system("kill $(ps aux | grep '[s]tart.py')")
    try:from acecore import TSengine as tsengine
    except:
        mensagemok(translate(40000),translate(40037))
        return
    xbmc.executebuiltin('Action(Stop)')
    lock_file = xbmc.translatePath('special://temp/'+ 'ts.lock')
    if xbmcvfs.exists(lock_file):
    	xbmcvfs.delete(lock_file)
    if chid != '':
        chid=chid.replace('acestream://','').replace('ts://','').replace('st://','')
        print("Starting Player Ace hash: " + chid)
        TSPlayer = tsengine()
        out = None
        if chid.find('http://') == -1 and chid.find('.torrent') == -1:
            out = TSPlayer.load_torrent(chid,'PID',port=aceport)
        elif chid.find('http://') == -1 and chid.find('.torrent') != -1:
            out = TSPlayer.load_torrent(chid,'TORRENT',port=aceport)
        else:
            out = TSPlayer.load_torrent(chid,'TORRENT',port=aceport)
        if out == 'Ok':
            TSPlayer.play_url_ind(0,name + ' (' + chid + ')',iconimage,iconimage)
            TSPlayer.end()
            return
        else:    
            mensagemok(translate(40000),translate(40038))
            TSPlayer.end()
            return
    else:
        mensagemprogresso.close()
