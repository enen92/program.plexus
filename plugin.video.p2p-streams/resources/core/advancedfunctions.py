# -*- coding: utf-8 -*-

""" p2p-streams
    2014 enen92 fightnight"""
    
import xbmc,xbmcgui,xbmcplugin,xbmcvfs,sys,os,re
from utils.pluginxbmc import *
from utils.directoryhandle import addLink,addDir
from utils.iofile import *
from utils.webutils import download_tools


def advanced_menu():
	addLink('[COLOR orange]XBMC Advancedsettings.xml:[/COLOR]','',addonpath + art + 'settings_menu.png')
	lock_file = xbmc.translatePath('special://temp/'+ 'ts.lock')
	if xbmcvfs.exists(lock_file):
		addDir(traducao(40068),MainURL,306,'',2,False)
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	addDir(traducao(40058),MainURL,301,'p2p',2,False)
	if xbmcvfs.exists(advancedsettings_var):
		addDir(traducao(40063),MainURL,303,'p2p',2,False)
		addDir(traducao(40065),MainURL,304,'p2p',2,False)
	if xbmcvfs.exists(advancedsettingsbackup_var):
		addDir(traducao(40061),MainURL,302,'p2p',2,False)
	addLink('','','p2p')
	if xbmcvfs.exists(advancedsettings_var):
		content = readfile(advancedsettings_var)
		match = re.compile('<cachemembuffersize>(.+?)</cachemembuffersize>').findall(content)
		if match:
			if match[0] != '252420': valuebuff = '[COLOR red]' + match[0] + '[/COLOR]'
			else : valuebuff =  '[COLOR green]' + match[0] + '[/COLOR]'
			addLink(traducao(40067) +valuebuff+']','','p2p')
			addLink('','','p2p')
	#Change engine settings from xbmc menus
	eligible = False
	if xbmc.getCondVisibility('system.platform.linux') and settings.getSetting('force_android') != "true":
		if os.uname()[4] == "armv6l" or os.uname()[4] == "armv7l":
			eligible = True
	elif xbmc.getCondVisibility('system.platform.OSX'): eligible = True
	elif settings.getSetting('openeleci386') == "true": eligible = True
	elif settings.getSetting('force_android') == "true": eligible = False
	else: eligible = False
	if eligible and xbmcvfs.exists(os.path.join(pastaperfil,'acestream','ace','ACEStream','values')):
		addLink('[COLOR orange]Acestream engine settings:[/COLOR]','',addonpath + art + 'settings_menu.png')
		try:
			porta = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","port.txt"))
		except: porta = "N/A"
		addDir(traducao(600015) +"[COLOR orange][ " + str(int(porta))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","port.txt"),305,'p2p',2,False)
		try:
			vodbuffer = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","vodbuffer.txt"))
		except: vodbuffer = "N/A"
		addDir(traducao(600016) + "[COLOR orange][ " + str(int(vodbuffer))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","vodbuffer.txt"),305,'p2p',2,False)
		try:
			livebuffer = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","livebuffer.txt"))
		except: livebuffer = "N/A"
		addDir(traducao(600017)+"[COLOR orange][ " + str(int(livebuffer))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","livebuffer.txt"),305,'p2p',2,False)
		try:
			downloadlimit = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","downloadlimit.txt"))
		except: downloadlimit = "N/A"
		addDir(traducao(600018) +"[COLOR orange][ " + str(int(downloadlimit))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","downloadlimit.txt"),305,'p2p',2,False)
		try:
			uploadlimit = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","uploadlimit.txt"))
		except: uploadlimit = "N/A"
		addDir(traducao(600019)+"[COLOR orange][ " + str(int(uploadlimit))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","uploadlimit.txt"),305,'p2p',2,False)
		try:
			maxconnections = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnections.txt"))
		except: maxconnections = "N/A"
		addDir(traducao(600020)+"[COLOR orange][ " + str(int(maxconnections))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnections.txt"),305,'p2p',2,False)
		try:
			maxconnectionsstream = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnectionsstream.txt"))
		except: maxconnectionsstream = "N/A"
		addDir(traducao(600021)+"[COLOR orange][ " + str(int(maxconnectionsstream))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnectionsstream.txt"),305,'',2,False)
	elif eligible and not xbmcvfs.exists(os.path.join(pastaperfil,'acestream','ace','ACEStream','values')):
		addLink("[COLOR red][B]"+traducao(600027)+"[/COLOR][/B]","",addonpath + art + 'processwarning.png')
	else:
		pass

"""

AdvancedSettings.xml Related functions

"""

def import_advancedxml():
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	if xbmcvfs.exists(advancedsettings_var):
		print "An advanced settings XML file already exists"
		if xbmcvfs.exists(advancedsettingsbackup_var):
			print "An advanced settings backup already exists"
			xbmcvfs.delete(advancedsettingsbackup_var)
			xbmcvfs.rename(advancedsettings_var,advancedsettingsbackup_var)
			advancedname = ["Cachemembuffer=252420","freememorycachepercent=5"]
			advancedurl = ["http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettings.xml","http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettingstonicillo.xml"]
			index = xbmcgui.Dialog().select(traducao(40185), advancedname)
    			if index > -1:
    				download_tools().Downloader(advancedurl[index],advancedsettings_var,traducao(40059),traducao(40000))
				mensagemok(traducao(40000),traducao(40060))
		else:	
			xbmcvfs.rename(advancedsettings_var,advancedsettingsbackup_var)
			advancedname = ["Cachemembuffer=252420","freememorycachepercent=5"]
			advancedurl = ["http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettings.xml","http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettingstonicillo.xml"]
			index = xbmcgui.Dialog().select(traducao(40185), advancedname)
    			if index > -1:
    				download_tools().Downloader(advancedurl[index],advancedsettings_var,traducao(40059),traducao(40000))
				mensagemok(traducao(40000),traducao(40060))
	else:
		print "No advancedsettings.xml in the system yet"
		advancedname = ["Cachemembuffer=252420","freememorycachepercent=5"]
		advancedurl = ["http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettings.xml","http://p2p-strm.googlecode.com/svn/trunk/Advancedsettings/advancedsettingstonicillo.xml"]
		index = xbmcgui.Dialog().select(traducao(40185), advancedname)
    		if index > -1:
    			download_tools().Downloader(advancedurl[index],advancedsettings_var,traducao(40059),traducao(40000))
			mensagemok(traducao(40000),traducao(40060))
	xbmc.executebuiltin("Container.Refresh")
	

def backup_advancedxml():
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	if xbmcvfs.exists(advancedsettingsbackup_var):
		xbmcvfs.delete(advancedsettingsbackup_var)
	xbmcvfs.copy(advancedsettings_var,advancedsettingsbackup_var)
	mensagemok(traducao(40000),traducao(40064))
	xbmc.executebuiltin("Container.Refresh")

	
def recoverbackup_advancedxml():
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	xbmcvfs.delete(advancedsettings_var)
	xbmcvfs.rename(advancedsettingsbackup_var,advancedsettings_var)
	mensagemok(traducao(40000),traducao(40062))
	xbmc.executebuiltin("Container.Refresh")
	
def delete_advancedxml():
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	xbmcvfs.delete(advancedsettings_var)
	mensagemok(traducao(40000),traducao(40066))
	xbmc.executebuiltin("Container.Refresh")

		
		
"""

Acestream/Sopcast Engine Related functions

"""
		
def set_engine_setting(file):
	value = readfile(file)
	keyb = xbmc.Keyboard(str(int(value)), traducao(600024))
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		try:
			int(search)
			integer = True
		except: integer = False
		if integer == True:
			savefile(file, search)
			xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(600026), 1,addonpath+"/icon.png"))
			xbmc.executebuiltin("Container.Refresh")
		else:
			mensagemok(traducao(40000),traducao(600025))
			sys.exit(0)

def remove_lock():
	lock_file = xbmc.translatePath('special://temp/'+ 'ts.lock')
	xbmcvfs.delete(lock_file)
	mensagemok(traducao(40000),traducao(40069))
	xbmc.executebuiltin("Container.Refresh")

