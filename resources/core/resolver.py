# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains functions to link acestream or sopcast depending on the given argument (id or url). 
    It is used for the items in the main menu
    
    Functions:
    
    go_to_id(p2p_type) -> Receives the type of stream (sop or ace) and activates the keyboard to receive the next argument. This can be the sop id, the acestream hash or the sop url.

"""
    
import xbmc,sys
from peertopeerutils.pluginxbmc import *
import sopcast as sop
import acestream as ace
    
def go_to_id(p2p_type):
	if p2p_type=='ace':
		keyb = xbmc.Keyboard('', translate(40033))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				ace.acestreams(translate(40035) + ' ( ' + str(channel_id) + ')','',str(channel_id))
	elif p2p_type=='sop_id':
		channel_id = xbmcgui.Dialog().numeric(0, translate(40033))
		sop.sopstreams(translate(40035) + ' ( ' + str(channel_id) + ')','',str(channel_id))
	elif p2p_type=='sop_url':
		keyb = xbmc.Keyboard('sop://', translate(40034) + ' sop://')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				sop.sopstreams(translate(40036) + ' ( ' + str(channel_id) + ')','',str(channel_id))
