# -*- coding: utf-8 -*-

""" Plexus (c) 2015 enen92
   
   This file manages the history of recent played p2p addon items
   
   Functions:
   
   list_history() -> Function list addon history. It grabs the info from history.txt in the userdata
   add_to_history(name,url,mode,iconimage) -> Add to addon history. It appends a new line to history.txt
   remove_history() -> delete history.txt if the file exists
   
    
"""
import xbmcvfs,xbmc,os,sys
from plexusutils.pluginxbmc import *
from plexusutils.iofile import *
from plexusutils.directoryhandle import addDir

history_file = os.path.join(pastaperfil,'history.txt')

def list_history():
	if xbmcvfs.exists(history_file):
		lines = open(history_file).readlines()
		i=0
		for line in lines:
			info = line.split('|')
			if i < int(settings.getSetting('items_per_page')):
				try:
					addDir(info[0],info[1],int(info[2]),info[3].replace('\n',''),1,False)	
				except: pass
			i+=1
	else:
		sys.exit(0)
	
def add_to_history(name,url,mode,iconimage):
	line = str(name) + '|' + str(url) + '|' +str(mode) +'|' + str(iconimage) + '\n'
	if xbmcvfs.exists(history_file):
		lines = open(history_file).readlines()
		if len(lines) < int(settings.getSetting('items_per_page')):
			if name in lines[0]: pass
			else:
				lines.insert(0,line)
				open(history_file, 'w').writelines(lines)
		else:
			lines = open(history_file).readlines()
			newlines = lines[0:-1*int(settings.getSetting('items_per_page'))-1]
			newlines.insert(0,line)
			open(history_file, 'w').writelines(newlines)
	else:
		save(history_file,line)
	return
	
def remove_history():
	if xbmcvfs.exists(history_file):
		xbmcvfs.delete(history_file)
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(30000), translate(30017), 1,os.path.join(addonpath,"icon.png")))
		
