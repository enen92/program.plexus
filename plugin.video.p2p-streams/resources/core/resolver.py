# -*- coding: utf-8 -*-

""" p2p-streams
    2014 enen92 fightnight"""
    
import xbmc,sys
from utils.pluginxbmc import *
import sopcast as sop
import acestream as ace
    
def go_to_id(p2p_type):
	if p2p_type=='ace':
		keyb = xbmc.Keyboard('', traducao(40033))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				ace.acestreams(traducao(40035),'',str(channel_id))
	elif p2p_type=='sop_id':
		channel_id = xbmcgui.Dialog().numeric(0, traducao(40033))
		sop.sopstreams(traducao(40035),'',str(channel_id))
	elif p2p_type=='sop_url':
		keyb = xbmc.Keyboard('sop://', traducao(40034) + ' sop://')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				sop.sopstreams(traducao(40036),'',str(channel_id))
