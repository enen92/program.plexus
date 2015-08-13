# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2015 enen92

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
   	set_acestream_engine_cache_folder(url) -> Change acestreamengine cache folder
   	set_linux_engine_setting(url) -> change acestreamengine settings from gui for linux/android
   	clear_cache(url) -> Clear the contents of the acestream cache folder
   	shutdown_hooks() -> Function to set a costum shutdown hook to the used skin and costum stop shortcuts
   	set_android_port() -> Import sessionconfig.pickle for android
   	set_android_cache_aloc() -> Set android cache allocation for the internal engine
   	

"""
    
import xbmc,xbmcgui,xbmcplugin,xbmcvfs,sys,os,re
from plexusutils.pluginxbmc import *
from plexusutils.directoryhandle import addLink,addDir
from plexusutils.iofile import *
from plexusutils.webutils import download_tools
from plexusutils.utilities import getDirectorySize


def advanced_menu():
	addLink('[COLOR orange]Advancedsettings.xml:[/COLOR]','',addonpath + art + 'settings_menu.png')
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
	#Apply shutdown hooks
	addLink('[COLOR orange]'+translate(70025)+'[/COLOR]','',addonpath + art + 'settings_menu.png')
	addDir(translate(70026),MainURL,310,'p2p',2,False)
	#Change engine settings from xbmc menus
	eligible = False
	if xbmc.getCondVisibility('system.platform.linux') and settings.getSetting('force_android') != "true":
		if os.uname()[4] == "armv6l" or os.uname()[4] == "armv7l":
			eligible = True
	elif xbmc.getCondVisibility('system.platform.OSX'): eligible = False
	elif settings.getSetting('openeleci386') == "true": eligible = False
	elif settings.getSetting('force_android') == "true": eligible = False
	else: eligible = False
	if eligible and os.path.exists(os.path.join(pastaperfil,'acestream','ace','ACEStream','values')):
		addLink('[COLOR orange]Acestream engine settings:[/COLOR]','',addonpath + art + 'settings_menu.png')
		acestream_cachefolder = os.path.join(os.getenv("HOME"),'.ACEStream','cache')
		acestream_cache_size = str(int(getDirectorySize(acestream_cachefolder))/(1024*1024))
		addDir(translate(70003) + '[COLOR orange] [' + acestream_cache_size + ' MB][/COLOR]',acestream_cachefolder,307,'p2p',1,False)
		try:
			porta = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","port.txt"))
		except: porta = "N/A"
		try:
			acestream_settings_file = os.path.join(os.getenv("HOME"),'.ACEStream','sessconfig.pickle')
			sessconfig = readfile(acestream_settings_file)
			portvector = re.compile("S'minport'\np(\d+)\nI(\d+)\n").findall(sessconfig)
			maxport = re.compile("S'maxport'\np(\d+)\nI(\d+)\n").findall(sessconfig)
		except: portvector = [];maxport=[]
		addDir(translate(600015) +"[COLOR orange][ " + str(int(porta))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","port.txt") + '|' + str(portvector)+'|'+str(maxport),305,'p2p',2,False)
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
	elif eligible and not os.path.exists(os.path.join(pastaperfil,'acestream','ace','ACEStream','values')):
		addLink("[COLOR red][B]"+translate(600027)+"[/COLOR][/B]","",addonpath + art + 'processwarning.png')
	else:
		pass
	if (not eligible and xbmc.getCondVisibility('system.platform.linux') and settings.getSetting('ace_cmd') == "0") or (not eligible and xbmc.getCondVisibility('system.platform.windows')) or (not eligible and xbmc.getCondVisibility('system.platform.Android') and settings.getSetting('engine_app') == "0") or (settings.getSetting('force_android') == "true" and settings.getSetting('engine_app') == "0"):
		if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android'):
			default_acefolder = os.path.join(os.getenv("HOME"),'.ACEStream')
			default_cachefolder = os.path.join(os.getenv("HOME"),'.ACEStream','cache','.acestream_cache')
			pickle_repo = 'http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/playerconf.pickle'
			if settings.getSetting('acestream_cachefolder') == '': acestream_cachefolder = os.path.join(os.getenv("HOME"),'.ACEStream','cache','.acestream_cache')
			else: acestream_cachefolder = settings.getSetting('acestream_cachefolder')
			acestream_settings_file = os.path.join(os.getenv("HOME"),'.ACEStream','playerconf.pickle')
		elif xbmc.getCondVisibility('system.platform.Android'):
			default_acefolder = os.path.join('/sdcard','.ACEStream')
			default_cachefolder = os.path.join('/sdcard','.ACEStream','.acestream_cache')
			pickle_repo = 'http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/playerconf.pickle'
			if settings.getSetting('acestream_cachefolder') == '': acestream_cachefolder = os.path.join('/sdcard','.ACEStream','.acestream_cache')
			else:
				acestream_cachefolder = os.path.join(settings.getSetting('acestream_cachefolder'),'.acestream_cache')
				if not os.path.exists(acestream_cachefolder):xbmcvfs.mkdir(acestream_cachefolder)
			acestream_settings_file = os.path.join('/sdcard','.ACEStream','playerconf.pickle')
		elif xbmc.getCondVisibility('system.platform.windows'):
			default_acefolder = os.path.join(os.getenv("APPDATA"),".ACEStream")
			pickle_repo = 'http://p2p-strm.googlecode.com/svn/trunk/Modules/Windows/playerconf.pickle'
			default_cachefolder = os.path.join(os.getenv("SystemDrive"),'\_acestream_cache_')
			acestream_cachefolder = default_cachefolder
			acestream_settings_file = os.path.join(os.getenv("APPDATA"),".ACEStream","playerconf.pickle")
		#workaround to keep settings file in place if they get deleted
		if not os.path.exists(default_acefolder): xbmcvfs.mkdir(default_acefolder)
		if not os.path.exists(default_cachefolder): xbmcvfs.mkdir(default_cachefolder)
		if not os.path.exists(acestream_settings_file):
			local_file = os.path.join(default_acefolder,pickle_repo.split("/")[-1])
			download_tools().Downloader(pickle_repo,local_file,'',translate(40000))
			xbmc.sleep(200)
			if xbmcvfs.exists(acestream_settings_file):
				settings_text = readfile(acestream_settings_file)
				save(acestream_settings_file,settings_text.replace('my_cache_folder',default_cachefolder))
		if xbmcvfs.exists(acestream_settings_file) and os.path.exists(acestream_cachefolder):
			addLink('[COLOR orange]Acestream engine settings:[/COLOR]','',addonpath + art + 'settings_menu.png')
			xbmc.sleep(200)
			#Change default port for Android
			if xbmc.getCondVisibility('system.platform.Android'):
				android_port = settings.getSetting('android_port')
				addDir(translate(600015) +"[COLOR orange] [ " + android_port + " ][/COLOR]",'p2p',311,'p2p',2,False)
			#
			acestream_cache_size = str(int(getDirectorySize(acestream_cachefolder))/(1024*1024))
			addDir(translate(70003) + '[COLOR orange] [' + acestream_cache_size + ' MB][/COLOR]',acestream_cachefolder,307,'p2p',1,False)
			settings_content = readfile(acestream_settings_file)
			number_of_settings = re.compile('p(\d+)\n').findall(settings_content)
			cachefoldersetting = re.compile("'download_dir'\np\d+\n.+?/(.+?)\n").findall(settings_content)
			if not cachefoldersetting:
				if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android'):
					if not 'arm' in os.uname()[4]:
						cachefoldersetting = os.path.join(os.getenv("HOME"),'.ACEStream','cache','.acestream_cache')
						settings.setSetting('acestream_cachefolder',cachefoldersetting)
					else:
						cachefoldersetting = os.path.join('/sdcard','.ACEStream','cache')
						settings.setSetting('acestream_cachefolder',cachefoldersetting)
				elif xbmc.getCondVisibility('system.platform.windows'):
					cachefoldersetting = os.path.join(os.getenv("SystemDrive"),'_acestream_cache_')
					settings.setSetting('acestream_cachefolder',cachefoldersetting)
				else:
					cachefoldersetting = os.path.join('/sdcard','.ACEStream','cache')
					settings.setSetting('acestream_cachefolder',cachefoldersetting)
			else:
				if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android'):
					if not 'arm' in os.uname()[4]:
						cachefoldersetting = os.path.join('/',cachefoldersetting[0].replace("'",""),'.acestream_cache')
						settings.setSetting('acestream_cachefolder',cachefoldersetting)
				else:
					cachefoldersetting = cachefoldersetting[0]
			if cachefoldersetting: addDir(translate(70013)+"[COLOR orange][ " + cachefoldersetting + " ][/COLOR]",str(cachefoldersetting),309,'p2p',2,False)
			else: addDir(translate(70013)+"[COLOR orange][" + cachefoldersetting + "][/COLOR]",cachefoldersetting,309,'p2p',2,False)
			buffer_type = re.compile("S'live_cache_type'\np(\d+)\nS(.*)").findall(settings_content)
			if xbmc.getCondVisibility('system.platform.Android'):
				if buffer_type: 
					if 'memory' in buffer_type[0][1]: addDir(translate(70041)+"[COLOR orange] [ Memory ][/COLOR]",'p2p',312,'p2p',2,False)
					elif 'disk' in buffer_type[0][1]: addDir(translate(70041)+"[COLOR orange] [ Disk ][/COLOR]",'p2p',312,'p2p',2,False)
				else: pass
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
	if 'port.txt' in file:
		ficheiro = file.split('|')[0]
	else: ficheiro = file
	acestream_settings_file = os.path.join(os.getenv("HOME"),'.ACEStream','sessconfig.pickle')
	value = readfile(ficheiro)
	keyb = xbmc.Keyboard(str(int(value)), translate(600024))
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		try:
			int(search)
			integer = True
		except: integer = False
		if integer == True:
			save(ficheiro, search)
			if 'port.txt' in file:
				try:
					text = readfile(acestream_settings_file)
					minport = eval(file.split('|')[1])
					maxport = eval(file.split('|')[2])
					text = text.replace("S'minport'\np" + minport[0][0] +"\nI" + minport[0][1] +"\n","S'minport'\np" + minport[0][0] +"\nI" + search +"\n").replace("S'maxport'\np" + maxport[0][0] +"\nI" + maxport[0][1] +"\n","S'maxport'\np" + maxport[0][0] +"\nI" + search +"\n")
					save(acestream_settings_file,text)
				except: pass
			xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(600026), 1,os.path.join(addonpath,"icon.png")))
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
	if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android'):
		acestream_settings_file = os.path.join(os.getenv("HOME"),'.ACEStream','playerconf.pickle')
	elif xbmc.getCondVisibility('system.platform.Android'):
		acestream_settings_file = os.path.join('/sdcard','.ACEStream','playerconf.pickle')
	elif xbmc.getCondVisibility('system.platform.windows'):
		acestream_settings_file = os.path.join(os.getenv("APPDATA"),".ACEStream","playerconf.pickle")
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
			if 'total_max_download_rate' in url: settings.setSetting('total_max_download_rate',value=search)
			if 'total_max_upload_rate' in url:	settings.setSetting('total_max_upload_rate',value=search)	
		else:
			mensagemok(translate(40000),translate(600025))
			sys.exit(0)
			
def set_android_port():
	ports = ['8621','8622','8623']
	ports_pickle = ['http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/sessconf/8621/sessconfig.pickle','http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/sessconf/8622/sessconfig.pickle','http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/sessconf/8623/sessconfig.pickle']
	choose=xbmcgui.Dialog().select(translate(600015),ports)
	if choose > -1:
		escolha = ports_pickle[choose]
		session_pickle_android = os.path.join('/sdcard','.ACEStream','sessconfig.pickle')
		download_tools().Downloader(escolha,session_pickle_android,'',translate(40000))
		settings.setSetting('android_port',ports[choose])
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(600026), 1,addonpath+"/icon.png"))
		xbmc.executebuiltin("Container.Refresh")
		
def set_android_cache_aloc():
	acestream_settings_file = os.path.join('/sdcard','.ACEStream','playerconf.pickle')
	settings_content = readfile(acestream_settings_file)
	types = ['Memory','Disk']
	choose=xbmcgui.Dialog().select(translate(70041),types)
	if choose > -1:
		escolha = types[choose]
		if escolha == 'Memory':
			settings_content = settings_content.replace("S'disk'","S'memory'")
		elif escolha == 'Disk':
			settings_content = settings_content.replace("S'memory'","S'disk'")
		else:pass
		save(acestream_settings_file, settings_content)		
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(600026), 1,addonpath+"/icon.png"))
		xbmc.executebuiltin("Container.Refresh")
	
				
def set_acestream_engine_cache_folder(url):
	if not xbmc.getCondVisibility('system.platform.windows'):
		opcao= xbmcgui.Dialog().yesno(translate(40000), translate(70011))
	else: opcao = ''
	if opcao:
		if not xbmc.getCondVisibility('system.platform.Android'):
			acestream_settings_file = os.path.join(os.getenv("HOME"),'.ACEStream','playerconf.pickle')
		else:
			acestream_settings_file = os.path.join('/sdcard','.ACEStream','playerconf.pickle')
		settings_content = readfile(acestream_settings_file)
		cachefolder = xbmcgui.Dialog().browse(3, translate(70012) , 'myprograms','')
		if cachefolder:
			settings_content = settings_content.replace(url,cachefolder)
			save(acestream_settings_file, settings_content)
			settings.setSetting('acestream_cachefolder',cachefolder)
			xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(600026), 1,addonpath+"/icon.png"))
			xbmc.executebuiltin("Container.Refresh")
		
def shutdown_hooks():
	opcao= xbmcgui.Dialog().yesno(translate(40000), translate(70027),translate(70028) + str(xbmc.getSkinDir()) )
	if opcao:
		mensagemok(translate(40000),translate(70029),translate(70030))
		mensagemok(translate(40000),translate(70031))
		opcao= xbmcgui.Dialog().yesno(translate(40000), translate(70032) )
		if opcao:
			import xml.etree.ElementTree as ET
			skin_path = xbmc.translatePath("special://skin/")
			tree = ET.parse(os.path.join(skin_path, "addon.xml"))
			try: res = tree.findall("./res")[0]
			except: res = tree.findall("./extension/res")[0]
			xml_specific_folder = str(res.attrib["folder"])
			xml_video_osd = os.path.join(xbmc.translatePath("special://skin/"),xml_specific_folder,"VideoOSD.xml")
			xml_content = readfile(xml_video_osd).replace('PlayerControl(Stop)','RunPlugin(plugin://plugin.video.p2p-streams/?mode=7)')
			try:
				save(xml_video_osd,xml_content)
				xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(600026), 1,addonpath+"/icon.png"))
			except: mensagemok(translate(40000),'No permissions.')
			opcao= xbmcgui.Dialog().yesno(translate(40000), translate(70033) )
			if opcao:
				from peertopeerutils.keymapeditor import *
				run()					
