# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains all the function the addon uses in the section "Advanced tools".
    
    Functions:
    
    Advancedsettings.xml related functions are below. Advancedsettings.xml are not automatically imported since they are advanced configurations the user should have control of.
    
   	advanced_menu() -> Main menu
   	import_advancedxml() -> Import recommended advancedsettings.xml
   	backup_advancedxml() -> When importing an advancedsettings.xml file, if a previous file exists on the same directory the addon will automatically make a backup of the file renaming it to advancedsettingsbackup.xml. This is what this function does
   	recoverbackup_advancedxml() -> Recover an advancedsettings.xml file resulting from a previous backup
   	delete_advancedxml() -> Delete the advancedsettings.xml file
   	
   Acestream related functions:
   	set_engine_setting(file) -> Set an acestreamengine setting to a given value. This is used in macosx and linux arm since the acestreamengine is not officially provided by acestream.org and the user doesn't have any other way to change them.
   	remove_lock() -> function to remove .lock files created during the acestream loop.
   	

"""
    
import xbmc,xbmcgui,xbmcplugin,xbmcvfs,sys,os,re
from utils.pluginxbmc import *
from utils.directoryhandle import addLink,addDir
from utils.iofile import *
from utils.webutils import download_tools
from utils.utilities import getDirectorySize


def advanced_menu():
	addLink('[COLOR orange]XBMC Advancedsettings.xml:[/COLOR]','',addonpath + art + 'settings_menu.png')
	lock_file = xbmc.translatePath('special://temp/'+ 'ts.lock')
	if xbmcvfs.exists(lock_file):
		addDir(translate(40068),MainURL,306,'',2,False)
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	addDir(translate(40058),MainURL,301,'p2p',2,False)
	if xbmcvfs.exists(advancedsettings_var):
		addDir(translate(40063),MainURL,303,'p2p',2,False)
		addDir(translate(40065),MainURL,304,'p2p',2,False)
	if xbmcvfs.exists(advancedsettingsbackup_var):
		addDir(translate(40061),MainURL,302,'p2p',2,False)
	addLink('','','p2p')
	if xbmcvfs.exists(advancedsettings_var):
		content = readfile(advancedsettings_var)
		match = re.compile('<cachemembuffersize>(.+?)</cachemembuffersize>').findall(content)
		if match:
			if match[0] != '252420': valuebuff = '[COLOR red]' + match[0] + '[/COLOR]'
			else : valuebuff =  '[COLOR green]' + match[0] + '[/COLOR]'
			addLink(translate(40067) +valuebuff+']','','p2p')
			addLink('','','p2p')
	#Change engine settings from xbmc menus
	eligible = False
	if xbmc.getCondVisibility('system.platform.linux') and settings.getSetting('force_android') != "true":
		if os.uname()[4] == "armv6l" or os.uname()[4] == "armv7l":
			eligible = True
	elif xbmc.getCondVisibility('system.platform.OSX'): eligible = True
	elif settings.getSetting('openeleci386') == "true": eligible = False
	elif settings.getSetting('force_android') == "true": eligible = False
	else: eligible = False
	if eligible and xbmcvfs.exists(os.path.join(pastaperfil,'acestream','ace','ACEStream','values')):
		addLink('[COLOR orange]Acestream engine settings:[/COLOR]','',addonpath + art + 'settings_menu.png')
		acestream_cachefolder = os.path.join(os.getenv("HOME"),'.ACEStream','cache')
		acestream_cache_size = str(int(getDirectorySize(acestream_cachefolder))/(1024*1024))
		addDir(translate(70003) + '[COLOR orange] [' + acestream_cache_size + ' MB][/COLOR]',acestream_cachefolder,307,'p2p',1,False)
		try:
			porta = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","port.txt"))
		except: porta = "N/A"
		addDir(translate(600015) +"[COLOR orange][ " + str(int(porta))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","port.txt"),305,'p2p',2,False)
		try:
			vodbuffer = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","vodbuffer.txt"))
		except: vodbuffer = "N/A"
		addDir(translate(600016) + "[COLOR orange][ " + str(int(vodbuffer))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","vodbuffer.txt"),305,'p2p',2,False)
		try:
			livebuffer = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","livebuffer.txt"))
		except: livebuffer = "N/A"
		addDir(translate(600017)+"[COLOR orange][ " + str(int(livebuffer))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","livebuffer.txt"),305,'p2p',2,False)
		try:
			downloadlimit = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","downloadlimit.txt"))
		except: downloadlimit = "N/A"
		addDir(translate(600018) +"[COLOR orange][ " + str(int(downloadlimit))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","downloadlimit.txt"),305,'p2p',2,False)
		try:
			uploadlimit = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","uploadlimit.txt"))
		except: uploadlimit = "N/A"
		addDir(translate(600019)+"[COLOR orange][ " + str(int(uploadlimit))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","uploadlimit.txt"),305,'p2p',2,False)
		try:
			maxconnections = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnections.txt"))
		except: maxconnections = "N/A"
		addDir(translate(600020)+"[COLOR orange][ " + str(int(maxconnections))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnections.txt"),305,'p2p',2,False)
		try:
			maxconnectionsstream = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnectionsstream.txt"))
		except: maxconnectionsstream = "N/A"
		addDir(translate(600021)+"[COLOR orange][ " + str(int(maxconnectionsstream))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnectionsstream.txt"),305,'',2,False)
	elif eligible and not xbmcvfs.exists(os.path.join(pastaperfil,'acestream','ace','ACEStream','values')):
		addLink("[COLOR red][B]"+translate(600027)+"[/COLOR][/B]","",addonpath + art + 'processwarning.png')
	else:
		pass
	if not eligible and xbmc.getCondVisibility('system.platform.linux'):
		addLink('[COLOR orange]Acestream engine settings:[/COLOR]','',addonpath + art + 'settings_menu.png')
		acestream_cachefolder = os.path.join(os.getenv("HOME"),'.ACEStream','cache')
		acestream_cache_size = str(int(getDirectorySize(acestream_cachefolder))/(1024*1024))
		addDir(translate(70003) + '[COLOR orange] [' + acestream_cache_size + ' MB][/COLOR]',acestream_cachefolder,307,'p2p',1,False)
		acestream_settings_file = os.path.join(os.getenv("HOME"),'.ACEStream','playerconf.pickle')
		settings_content = readfile(acestream_settings_file)
		number_of_settings = re.compile('p(\d+)\n').findall(settings_content)
		livebuffervalue = re.compile("S'live_buffer_time'\np(\d+)\nI(\d+)").findall(settings_content)
		if livebuffervalue:	addDir(translate(600017)+"[COLOR orange][ " + livebuffervalue[0][1] + " ][/COLOR]",'live_buffer_time|' + str(livebuffervalue)+'|'+str(len(number_of_settings)),308,'p2p',2,False)
		else: addDir(translate(600017)+"[COLOR orange][3][/COLOR]",'live_buffer_time|'+str(len(number_of_settings)),308,'p2p',2,False)
		vodbuffervalue = re.compile("S'player_buffer_time'\np(\d+)\nI(\d+)").findall(settings_content)
		if vodbuffervalue: addDir(translate(600016)+"[COLOR orange][ " + vodbuffervalue[0][1] + " ][/COLOR]",'player_buffer_time|'+str(vodbuffervalue)+'|'+str(len(number_of_settings)),308,'p2p',2,False)
		else: addDir(translate(600016)+"[COLOR orange][10][/COLOR]",'player_buffer_time|'+str(len(number_of_settings)),308,'p2p',2,False)
		downloadlimit = re.compile("S'total_max_download_rate'\np(\d+)\nI(\d+)").findall(settings_content)
		if downloadlimit: addDir(translate(600018)+"[COLOR orange][ " + downloadlimit[0][1] + " ][/COLOR]",'total_max_download_rate|'+str(downloadlimit)+'|'+str(len(number_of_settings)),308,'p2p',2,False)
		else: addDir(translate(600018)+"[COLOR orange][0][/COLOR]",'total_max_download_rate|'+str(len(number_of_settings)),308,'p2p',2,False)
		uploadlimit = re.compile("S'total_max_upload_rate'\np(\d+)\nI(\d+)").findall(settings_content)
		if uploadlimit: addDir(translate(600019)+"[COLOR orange][ " + uploadlimit[0][1] + " ][/COLOR]",'total_max_upload_rate|'+str(uploadlimit)+'|'+str(len(number_of_settings)),308,'p2p',2,False)
		else: addDir(translate(600019)+"[COLOR orange][0][/COLOR]",'total_max_upload_rate|'+str(len(number_of_settings)),308,'p2p',2,False)
		maxconnection_per_stream = re.compile("S'max_peers'\np(\d+)\nI(\d+)").findall(settings_content)
		if maxconnection_per_stream: addDir(translate(600021)+"[COLOR orange][ " + maxconnection_per_stream[0][1] + " ][/COLOR]",'max_peers|'+str(maxconnection_per_stream)+'|'+str(len(number_of_settings)),308,'p2p',2,False)
		else: addDir(translate(600021)+"[COLOR orange][50][/COLOR]",'max_peers|'+str(len(number_of_settings)),308,'p2p',2,False)

		

"""

AdvancedSettings.xml Related functions

"""

def import_advancedxml():
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	if xbmcvfs.exists(advancedsettings_var):
		print("An advanced settings XML file already exists")
		if xbmcvfs.exists(advancedsettingsbackup_var):
			print("An advanced settings backup already exists")
			xbmcvfs.delete(advancedsettingsbackup_var)
			xbmcvfs.rename(advancedsettings_var,advancedsettingsbackup_var)
			advancedname = ["Cachemembuffer=252420","freememorycachepercent=5"]
			advancedurl = ["http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettings.xml","http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettingstonicillo.xml"]
			index = xbmcgui.Dialog().select(translate(40185), advancedname)
    			if index > -1:
    				download_tools().Downloader(advancedurl[index],advancedsettings_var,translate(40059),translate(40000))
				mensagemok(translate(40000),translate(40060))
		else:	
			xbmcvfs.rename(advancedsettings_var,advancedsettingsbackup_var)
			advancedname = ["Cachemembuffer=252420","freememorycachepercent=5"]
			advancedurl = ["http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettings.xml","http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettingstonicillo.xml"]
			index = xbmcgui.Dialog().select(translate(40185), advancedname)
    			if index > -1:
    				download_tools().Downloader(advancedurl[index],advancedsettings_var,translate(40059),translate(40000))
				mensagemok(translate(40000),translate(40060))
	else:
		print("No advancedsettings.xml in the system yet")
		advancedname = ["Cachemembuffer=252420","freememorycachepercent=5"]
		advancedurl = ["http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettings.xml","http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettingstonicillo.xml"]
		index = xbmcgui.Dialog().select(translate(40185), advancedname)
    		if index > -1:
    			download_tools().Downloader(advancedurl[index],advancedsettings_var,translate(40059),translate(40000))
			mensagemok(translate(40000),translate(40060))
	xbmc.executebuiltin("Container.Refresh")
	

def backup_advancedxml():
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	if xbmcvfs.exists(advancedsettingsbackup_var):
		xbmcvfs.delete(advancedsettingsbackup_var)
	xbmcvfs.copy(advancedsettings_var,advancedsettingsbackup_var)
	mensagemok(translate(40000),translate(40064))
	xbmc.executebuiltin("Container.Refresh")

	
def recoverbackup_advancedxml():
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	xbmcvfs.delete(advancedsettings_var)
	xbmcvfs.rename(advancedsettingsbackup_var,advancedsettings_var)
	mensagemok(translate(40000),translate(40062))
	xbmc.executebuiltin("Container.Refresh")
	
def delete_advancedxml():
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	xbmcvfs.delete(advancedsettings_var)
	mensagemok(translate(40000),translate(40066))
	xbmc.executebuiltin("Container.Refresh")

		
		
"""

Acestream/Sopcast Engine Related functions

"""
		
def set_engine_setting(file):
	value = readfile(file)
	keyb = xbmc.Keyboard(str(int(value)), translate(600024))
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		try:
			int(search)
			integer = True
		except: integer = False
		if integer == True:
			save(file, search)
			xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(600026), 1,addonpath+"/icon.png"))
			xbmc.executebuiltin("Container.Refresh")
		else:
			mensagemok(translate(40000),translate(600025))
			sys.exit(0)

def remove_lock():
	lock_file = xbmc.translatePath('special://temp/'+ 'ts.lock')
	xbmcvfs.delete(lock_file)
	mensagemok(translate(40000),translate(40069))
	xbmc.executebuiltin("Container.Refresh")
	
def clear_cache(url):
	dirs, files = xbmcvfs.listdir(url)
	for fich in files:
		xbmcvfs.delete(os.path.join(url,fich))
	if files: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(40161), 1,addonpath+"/icon.png"))
	xbmc.executebuiltin("Container.Refresh")
	
def set_linux_engine_setting(url):
	print url
	acestream_settings_file = os.path.join(os.getenv("HOME"),'.ACEStream','playerconf.pickle')
	settings_content = readfile(acestream_settings_file)
	keyb = xbmc.Keyboard('',translate(600024))
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		try:
			int(search)
			integer = True
		except: integer = False
		if integer == True:
			if len(url.split('|')) == 3:
				settings_content = settings_content.replace('p'+str(eval(url.split('|')[1])[0][0])+'\nI'+str(eval(url.split('|')[1])[0][1]),'p'+str(eval(url.split('|')[1])[0][0])+'\nI'+search)
				save(acestream_settings_file, settings_content)
				xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(600026), 1,addonpath+"/icon.png"))
				xbmc.executebuiltin("Container.Refresh")
			else:
				settings_content = settings_content.replace('s.',"sS'"+url.split('|')[0]+"'\np"+url.split('|')[1]+"\nI"+search+"\ns.")
				save(acestream_settings_file, settings_content)
				xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(600026), 1,addonpath+"/icon.png"))
				xbmc.executebuiltin("Container.Refresh")		
		else:
			mensagemok(translate(40000),translate(600025))
			sys.exit(0)

