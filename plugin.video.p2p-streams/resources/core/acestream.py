# -*- coding: utf-8 -*-

""" p2p-streams
    2014 enen92 fightnight"""
    
import xbmc,xbmcgui,xbmcplugin,urllib,xbmcvfs,os
from utils.pluginxbmc import *

aceport=62062

def load_local_torrent():
	torrent_file = xbmcgui.Dialog().browse(int(1), traducao(600028), 'myprograms','.torrent')
	if torrent_file:
		if xbmc.getCondVisibility('system.platform.windows'):
			acestreams("Local .torrent","",'file:\\' + torrent_file)
		else:
			acestreams("Local .torrent","",'file://' + torrent_file)
	else: pass

def acestreams(name,iconimage,chid):
	if not iconimage: iconimage=os.path.join(addonpath,'resources','art','acelogofull.jpg')
	else: iconimage = urllib.unquote(iconimage)
	if settings.getSetting('aceplay_type') == "2":
		pDialog = xbmcgui.DialogProgress()
		ret = pDialog.create('P2P-Streams', traducao(40154),traducao(40155),traducao(40156))
		pDialog.update(0)
		xbmc.sleep(3000)
		pDialog.update(100)
		pDialog.close()
		ip_adress = settings.getSetting('ip_addr')
		proxy_port = settings.getSetting('aceporta')
		chid=chid.replace('acestream://','').replace('ts://','').replace('st://','')
		strm = "http://" + ip_adress + ":" + proxy_port + "/pid/" + chid + "/stream.mp4"
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		listitem.setLabel(name + " (" + chid + ")")
		listitem.setInfo('video', {'Title': name + " (" + chid + ")"})
		xbmc.Player().play(strm,listitem)
	else: acestreams_builtin(name,iconimage,chid)

def acestreams_builtin(name,iconimage,chid):
    try:from acecore import TSengine as tsengine
    except:
        mensagemok(traducao(40000),traducao(40037))
        return
    xbmc.executebuiltin('Action(Stop)')
    lock_file = xbmc.translatePath('special://temp/'+ 'ts.lock')
    if xbmcvfs.exists(lock_file):
    	xbmcvfs.delete(lock_file)
    if chid != '':
        chid=chid.replace('acestream://','').replace('ts://','').replace('st://','')
        print "Starting Player Ace hash: " + chid
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
            mensagemok(traducao(40000),traducao(40038))
            TSPlayer.end()
            return
    else:
        mensagemprogresso.close()
