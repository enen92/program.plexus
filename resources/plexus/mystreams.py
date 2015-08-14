# -*- coding: utf-8 -*-

""" Plexus (c) 2015 enen92
   
   This file contains the main menu and the addon directory tree.
   All the necessary modules are present in ~/resources/plexus directory
    
"""

import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import os
import hashlib
import sys
from plexusutils.pluginxbmc import *
from plexusutils.directoryhandle import *
from plexusutils.iofile import *

def my_streams_menu():
	if not os.path.exists(mystrm_folder): xbmcvfs.mkdir(mystrm_folder)
	files = os.listdir(mystrm_folder)
	if files:
		for fic in files:
			content = readfile(os.path.join(mystrm_folder,fic)).split('|')
			if content:
				if 'acestream://' in content[1] or '.acelive' in content[1] or '.torrent' in content[1]:
					addDir(content[0],content[1],1,content[2],1,False) 
				elif 'sop://' in content[1]:
					addDir(content[0],content[1],2,content[2],1,False) 
				else:
					pass
	addDir('[B][COLOR maroon]'+translate(30009)+'[/COLOR][/B]',MainURL,11,os.path.join(addonpath,art,'plus-menu.png'),1,False)

def add_stream(name='',url='',iconimage=''):
	if not name or not url:
		keyb = xbmc.Keyboard('', translate(30010))
		keyb.doModal()
		if (keyb.isConfirmed()):
			stream = keyb.getText()
			if stream == '' : sys.exit(0)
			else:
				if 'acestream://' not in stream and '.acelive' not in stream and 'sop://' not in stream:
					mensagemok(translate(40000),translate(30011))
					sys.exit(0)
				else:
					#icon
					yes = xbmcgui.Dialog().yesno(translate(30000), translate(30012))
					if yes:
						iconimage = xbmcgui.Dialog().browse(1, translate(30013),'video','.png|.jpg|.jpeg|.gif',True)
					else:
						if 'acestream://' in stream or '.acelive' in stream or '.torrent' in stream:
							iconimage = os.path.join(addonpath,'resources','art','acestream-menu-item.png')
						elif 'sop://' in stream:
							iconimage = os.path.join(addonpath,'resources','art','sopcast-menu-item.png')
						else:
							iconimage = ''
					#name
					keyb = xbmc.Keyboard('', translate(30014))
					keyb.doModal()
					if (keyb.isConfirmed()):
						name = keyb.getText()
						if name == '' : sys.exit(0)
						else:
						#save
							content = name + '|' + stream + '|' + iconimage
							filename = hashlib.md5(name + '|' + stream).hexdigest() + '.txt'
							save(os.path.join(mystrm_folder,filename),content)
							xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(30000), translate(30015), 1,os.path.join(addonpath,"icon.png")))
							xbmc.executebuiltin("Container.Refresh")
	else:
		content = name + '|' + url + '|' + iconimage
		filename = hashlib.md5(name + '|' + url).hexdigest() + '.txt'
		save(os.path.join(mystrm_folder,filename),content)
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(30000), translate(30015), 1,os.path.join(addonpath,"icon.png")))
		xbmc.executebuiltin("Container.Refresh")
						
def remove_stream(name,url):
	filename = hashlib.md5(name + '|' + url).hexdigest() + '.txt'
	ficheiro = os.path.join(mystrm_folder,filename)
	try:
		os.remove(ficheiro)
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(30000), translate(30016), 1,os.path.join(addonpath,"icon.png")))
		xbmc.executebuiltin("Container.Refresh")
	except: pass
				
				
	
