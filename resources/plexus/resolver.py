# -*- coding: utf-8 -*-

""" Plexus  (c)  2015 enen92

    This file contains functions to link acestream or sopcast depending on the given argument (id or url). 
    It is used for the items in the main menu
    
    Functions:
    
    go_to_id(p2p_type) -> Receives the type of stream (sop or ace) and activates the keyboard to receive the next argument. This can be the sop id, the acestream hash or the sop url.

"""
    
import xbmc,sys
from plexusutils.pluginxbmc import *
import sopcast as sop
import acestream as ace
    
def go_to_id(p2p_type):
	if p2p_type=='ace':
		keyb = xbmc.Keyboard('', translate(30022))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				ace.acestreams(translate(30020) + ' ( ' + str(channel_id) + ')','',str(channel_id))
	elif p2p_type=='sop_id':
		channel_id = xbmcgui.Dialog().numeric(0, translate(30018))
		sop.sopstreams(translate(30020) + ' ( ' + str(channel_id) + ')','',str(channel_id))
	elif p2p_type=='sop_url':
		keyb = xbmc.Keyboard('sop://', translate(30019) + ' sop://')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				sop.sopstreams(translate(30021) + ' ( ' + str(channel_id) + ')','',str(channel_id))
