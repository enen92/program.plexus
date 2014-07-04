# -*- coding: utf-8 -*-

""" p2p-streams
    2014 enen92 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time,subprocess,xbmcvfs,livestreams,socket
try:
	import pytz
except: pass

####################################################### CONSTANTES #####################################################

versao = '0.3.6'
addon_id = 'plugin.video.p2p-streams'
MainURL = 'http://google.com'
WiziwigURL = 'http://www.wiziwig.tv'
TorrentTVURL = 'http://torrent-tv.ru/'
OnetorrentURL = 'http://1torrent.tv'
linkwiki = 'http://bit.ly/1j43Bbn'
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
settings = xbmcaddon.Addon(id=addon_id)
addonpath = settings.getAddonInfo('path').decode('utf-8')
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
iconpequeno=addonpath + art + 'iconpq.jpg'
traducaoma= settings.getLocalizedString
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
startpath=os.path.join(pastaperfil,'acestream','ace','start.py')

### SOPCAST ###
LISTA_SOP='http://www.sopcast.com/chlist.xml'
SPSC_BINARY = "sp-sc-auth"
#SPSC = os.path.join(pastaperfil,'sopcast',SPSC_BINARY)
SPSC_LOG = os.path.join(pastaperfil,'sopcast','sopcast.log')
LOCAL_PORT = settings.getSetting('local_port')
VIDEO_PORT = settings.getSetting('video_port')
BUFER_SIZE = int(settings.getSetting('buffer_size'))
if(settings.getSetting('auto_ip')):
    LOCAL_IP=xbmc.getIPAddress()
else: LOCAL_IP=settings.getSetting('localhost')

### ACESTREAM ##

aceport=62062

#################

sopcastidteste='8893'
acestreamidteste='9e4914630f4f9055ffbfb77e70714ce835c1d321'

def traducao(texto):
      return traducaoma(texto).encode('utf-8')
      

def readfile(filename):
	f = open(filename, "r")
	string = f.read()
	return string
	
def russiandictionary(string):
	if string == "Eng": return traducao(40077)
	elif string == "Спорт": return traducao(40078)
	elif string == "Новостные": return traducao(40079)
	elif string == "Свадебный": return traducao(40080)
	elif string == "Общие": return traducao(40081)
	elif string == "Познавательные": return traducao(40082)
	elif string == "СНГ": return traducao(40083)
	elif string == "Мужские": return traducao(40084)
	elif string == "Ukraine": return traducao(40085)
 	elif string == "резерв": return traducao(40086)
 	elif string == "Донецк": return traducao(40087)
 	elif string == "Региональные": return traducao(40088)
 	elif string == "Для взрослых": return traducao(40089)
 	elif string == "TV21": return traducao(40090)
 	elif string == "Украина": return traducao(40091)
 	elif string == "Детские": return traducao(40092)
 	elif string == "Фильмы": return traducao(40093)
 	elif string == "Ночной канал": return traducao(40094)
 	elif string == "Европа": return traducao(40095)
 	elif string == "укр": return traducao(40096)
 	elif string == "Музыка": return traducao(40097)
 	elif string == "Религиозные": return traducao(40098)
 	elif string == "Развлекательные": return traducao(40099)
	elif string == "украина": return traducao(40151)
 	else: return string
                                                                                                                                                                 
 	                                                                                                        
      
      
      
def advanced_menu():
	addLink('[COLOR orange]XBMC Advancedsettings.xml:[/COLOR]','',addonpath + art + 'settings_menu.png')
	lock_file = xbmc.translatePath('special://temp/'+ 'ts.lock')
	if xbmcvfs.exists(lock_file):
		addDir(traducao(40068),MainURL,20,'',2,False)
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	addDir(traducao(40058),MainURL,16,'p2p',2,False)
	if xbmcvfs.exists(advancedsettings_var):
		addDir(traducao(40063),MainURL,18,'p2p',2,False)
		addDir(traducao(40065),MainURL,19,'p2p',2,False)
	if xbmcvfs.exists(advancedsettingsbackup_var):
		addDir(traducao(40061),MainURL,17,'p2p',2,False)
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
		addDir(traducao(600015) +"[COLOR orange][ " + str(int(porta))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","port.txt"),51,'p2p',2,False)
		try:
			vodbuffer = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","vodbuffer.txt"))
		except: vodbuffer = "N/A"
		addDir(traducao(600016) + "[COLOR orange][ " + str(int(vodbuffer))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","vodbuffer.txt"),51,'p2p',2,False)
		try:
			livebuffer = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","livebuffer.txt"))
		except: livebuffer = "N/A"
		addDir(traducao(600017)+"[COLOR orange][ " + str(int(livebuffer))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","livebuffer.txt"),51,'p2p',2,False)
		try:
			downloadlimit = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","downloadlimit.txt"))
		except: downloadlimit = "N/A"
		addDir(traducao(600018) +"[COLOR orange][ " + str(int(downloadlimit))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","downloadlimit.txt"),51,'p2p',2,False)
		try:
			uploadlimit = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","uploadlimit.txt"))
		except: uploadlimit = "N/A"
		addDir(traducao(600019)+"[COLOR orange][ " + str(int(uploadlimit))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","uploadlimit.txt"),51,'p2p',2,False)
		try:
			maxconnections = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnections.txt"))
		except: maxconnections = "N/A"
		addDir(traducao(600020)+"[COLOR orange][ " + str(int(maxconnections))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnections.txt"),51,'p2p',2,False)
		try:
			maxconnectionsstream = readfile(os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnectionsstream.txt"))
		except: maxconnectionsstream = "N/A"
		addDir(traducao(600021)+"[COLOR orange][ " + str(int(maxconnectionsstream))+ " ][/COLOR]",os.path.join(pastaperfil,"acestream","ace","ACEStream","values","maxconnectionsstream.txt"),51,'',2,False)
	elif eligible and not xbmcvfs.exists(os.path.join(pastaperfil,'acestream','ace','ACEStream','values')):
		addLink("[COLOR red][B]"+traducao(600027)+"[/COLOR][/B]","",addonpath + art + 'processwarning.png')
	else:
		pass

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
	

def delete_advancedxml():
	userdatapath = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
	advancedsettings_var = os.path.join(userdatapath,'advancedsettings.xml')
	advancedsettingsbackup_var = os.path.join(userdatapath,'advancedsettingsbackup.xml')
	xbmcvfs.delete(advancedsettings_var)
	mensagemok(traducao(40000),traducao(40066))
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


def add_to_addon_favourites(name,url):
	name = name.replace("[b]","").replace("[/b]","").replace("[color orange]","").replace("[/color]","")
	if "runplugin" in url:
		print "Existe Runplugin"
		match = re.compile("url=(.+?)&mode=(.+?)&").findall(url.replace(";",""))
		for url,mode in match:
			favourite_text = name + " (" + url + ")|" + str(mode) + "|" + url
			favouritetxt = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
			if not xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")): xbmcvfs.mkdir(os.path.join(pastaperfil,"Favourites"))
			print favouritetxt
			savefile(favouritetxt, favourite_text)
			xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40148), 1,addonpath+"/icon.png"))
	else:
		if "sop://" in url:
			tipo = "sopcast"
		elif "acestream://" in url:
			tipo = "acestream"
		else:
			if len(url) < 30: tipo = "sopcast"
			else: tipo = "acestream"
		if tipo == "sopcast":
			favourite_text = name + " (" + url + ")|" + str(2) + "|" + url  
		elif tipo == "acestream":
			favourite_text = name + " (" + url + ")|" + str(1) + "|" + url  
		favouritetxt = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
		if not xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")): xbmcvfs.mkdir(os.path.join(pastaperfil,"Favourites"))
		savefile(favouritetxt, favourite_text)
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40148), 1,addonpath+"/icon.png"))
		xbmc.executebuiltin("Container.Refresh")

def remove_addon_favourites(url):
	print url
	if "runplugin" in url:
		match = re.compile("url=(.+?)&mode").findall(url.replace(";",""))
		if match: ficheiro = os.path.join(pastaperfil,"Favourites",match[0].replace("/","").replace(":","") + ".txt")
	else:
		ficheiro = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
	xbmcvfs.delete(ficheiro)
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40147), 1,addonpath+"/icon.png"))
	xbmc.executebuiltin("Container.Refresh")

def remove_list(name):
	xbmcvfs.delete(name)
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40150), 1,addonpath+"/icon.png"))
	xbmc.executebuiltin("Container.Refresh")
	

def addon_favourites():
	if xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")):
		dirs, files = xbmcvfs.listdir(os.path.join(pastaperfil,"Favourites"))
		if files:
			for file in files:
				f = open(os.path.join(pastaperfil,"Favourites",file), "r")
				string = f.read()
				match = string.split("|")
				addDir("[B][COLOR orange]" + match[0] + "[/B][/COLOR]",match[2],int(match[1]),'',1,False)
			xbmc.executebuiltin("Container.SetViewMode(51)")
		else:
			mensagemok(traducao(40000),traducao(40145));sys.exit(0)


def livefootballaol_menu():
	try:
		source = abrir_url("http://www.livefootballol.com/sopcast-channel-list.html")
	except: source="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile('">(.+?)</s.+?td>\n<td>(.+?)</td>\n<td>(.+?)</td>').findall(source)
		for titulo,sopaddress,language in match:
			addDir("[B][COLOR orange][SopCast] [/COLOR]"+titulo.replace('<strong>','').replace('</a>','')+"[/B] ("+language.replace('<strong>','').replace('</strong>','')+ ')',sopaddress,2,"http://s30.postimg.org/3oznvmo5d/livefootball.png",len(match),False)

def arenavision_menu():
	try:
		source = abrir_url("http://go.arenavision.in/")
	except: source="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile("<li><a href='(.+?)'>(.+?)</a></li>").findall(source)
		for link,name in match:
			if "Agenda" in name:
				addDir("[B][COLOR orange]Agenda/Schedule[/COLOR][/B]",link,37,"http://s30.postimg.org/n6m6le88h/arenavisionlogo.png",1,True)
			if "AV" in name:
				addDir(name,link,36,"http://s30.postimg.org/n6m6le88h/arenavisionlogo.png",1,False)
			else: pass


def arenavision_streams(name,url):
	try:
		source = abrir_url(url)
	except: source="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile('sop://(.+?)"').findall(source)
		if match: sopstreams(name,"http://s30.postimg.org/n6m6le88h/arenavisionlogo.png","sop://" + match[0])
		else:
			match = re.compile('this.loadPlayer\("(.+?)"').findall(source)
			if match: acestreams(name,"http://s30.postimg.org/n6m6le88h/arenavisionlogo.png",match[0])
			else: mensagemok(traducao(40000),traducao(40022))

def arenavision_schedule(url):
	print url
	try:
		source = abrir_url(url)
	except: source="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.findall("<br />(.*?)<div class='post-footer'>", source, re.DOTALL)
		for event in match:
			eventmatch = re.compile('(.+?)/(.+?)/(.+?) (.+?):(.+?) CET (.+?)<').findall(event)
			for dia,mes,year,hour,minute,evento in eventmatch:
				try:
					from datetime import datetime
					from dateutil import tz
					d = datetime(year=2000 + int(year),month=int(mes),day=int(dia),hour=int(hour),minute=int(minute),tzinfo=tz.gettz('Europe/Madrid'))
					fmt = "%d-%m-%y %H:%M"
					timezona= settings.getSetting('timezone')
					time = str(d.astimezone(tz.gettz(pytz.all_timezones[int(timezona)])).strftime(fmt))
					addLink('[B][COLOR orange]' + time + '[/B][/COLOR] ' + evento,'',"http://s30.postimg.org/n6m6le88h/arenavisionlogo.png")
				except:
					addLink(event.replace("&nbsp;",""),'',"http://s30.postimg.org/n6m6le88h/arenavisionlogo.png")
	xbmc.executebuiltin("Container.SetViewMode(51)")

def livefootballws_events():
	try:
		source = mechanize_browser("http://www.livefootball.ws")
	except: source = ""; mensagemok(traducao(40000),traducao(40128))
	if source:
		items = re.findall('<div class="base custom" align="center"(.*?)</center></div><br></div>', source, re.DOTALL)
		number_of_items= len(items)	
		for item in reversed(items):
			data = re.compile('<div style="text-align: center;">(.+?)</div>').findall(item)
			try:
				check = re.compile(" (.+?):(.+?)").findall(data[-1].replace("color:",""))
				if not check and "Online" not in data[-1]:pass
				else:
					data_item = data[-1].replace("<strong>","").replace("</strong>","").replace('<span style="color: #008000;">','').replace("</span>","")
					url = re.compile('<a href="(.+?)">').findall(item)
					teams = re.compile('/.+?-(.+?).html').findall(url[0])
					try:
						match = re.compile('(.+?) (.+?) (.+?):(.*)').findall(data_item)
						from datetime import datetime
						from dateutil import tz
						d = datetime(year=2014,month=6,day=int(match[0][0]),hour=int(match[0][2]),minute=int(match[0][3]),tzinfo=tz.gettz('Europe/Moscow'))
						fmt = "%d %H:%M"
						timezona= settings.getSetting('timezone')
						time = str(d.astimezone(tz.gettz(pytz.all_timezones[int(timezona)])).strftime(fmt))
						addDir("[B][COLOR orange]("+traducao(600012)+time+")[/COLOR][/B] "+teams[0],url[0],39,"http://www.userlogos.org/files/logos/clubber/football_ws___.PNG",number_of_items,True)
					except:
						if '<span style="color: #000000;">' not in data_item:
							addDir("[B][COLOR green]("+data_item+")[/COLOR][/B] "+teams[0],url[0],39,"http://www.userlogos.org/files/logos/clubber/football_ws___.PNG",number_of_items,True)
						else: pass
			except: pass

def livefootballws_streams(url):
	try:
		source = mechanize_browser(url)
	except: source = ""; mensagemok(traducao(40000),traducao(40128))
	if source:
		items = re.findall('<td style="text-align: center;">(.*?)</tr>', source, re.DOTALL)
		number_of_items = len(items)
		if items:
			for item in items:
				match =re.compile('href="(.+?)"').findall(item)
				if match:
					if "sop://" or "torrentstream" or "acestream://" in match[-1]:
						stream_quality = re.compile('>(.+?) kbps</td>').findall(item)
						channel_info_arr = re.compile('<td style="text-align: center;">(.+?)</td>').findall(item)
						try:
							channel = channel_info_arr[-4].replace('<span style="text-align: center;">','').replace('</span>','')
						except: channel = 'N/A'
						if "sop://" in match[-1]:
							try:
								addDir("[B][COLOR orange][SopCast] [/COLOR]"+channel+"[/B] ("+stream_quality[0]+' Kbs)',match[-1],2,"http://www.userlogos.org/files/logos/clubber/football_ws___.PNG",number_of_items,False)
							except: pass
						elif "acestream://" in match[-1]:
							link = re.compile("acestream://(.*)").findall(match[-1])
							try:
								addDir("[B][COLOR orange][Acestream] [/COLOR]"+channel+"[/B] ("+stream_quality[0]+' Kbs)',link[0],1,"http://www.userlogos.org/files/logos/clubber/football_ws___.PNG",number_of_items,False)
							except: pass
						elif "torrentstream" in match[-1]:
							link = re.compile("http://torrentstream.org/stream/test.php\?id=(.*)").findall(match[-1])
							try:
								addDir("[B][COLOR orange][Acestream] [/COLOR]"+channel+"[/B] ("+stream_quality[0]+' Kbs)',link[0],1,"http://www.userlogos.org/files/logos/clubber/football_ws___.PNG",number_of_items,False)
							except: pass
						else:pass
		else:
			mensagemok(traducao(40000),traducao(40022))
			sys.exit(0)

def livefootballvideo_events():
	try:
		source = abrir_url("http://livefootballvideo.com/streaming")
	except: source ="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile('"([^"]+)" alt="[^"]*"/>.*?.*?>([^<]+)</a>\s*</div>\s*<div class="date_time column"><span class="starttime time" rel="[^"]*">([^<]+)</span>.*?<span class="startdate date" rel="[^"]*">([^"]+).*?<span>([^<]+)</span></div>.*?team away column"><span>([^&<]+).*?href="([^"]+)">([^<]+)<').findall(source)
		for icon,comp,timetmp,datetmp,home,away,url,live in match:
			print live
			mes_dia = re.compile(', (.+?) (.+?)<').findall(datetmp)
			for mes,dia in mes_dia:
				dia = re.findall('\d+', dia)
				month = translate_months(mes)
				hora_minuto = re.compile('(\d+):(\d+)').findall(timetmp)
				print hora_minuto
				try:
					from datetime import datetime
					from dateutil import tz
					d = datetime(year=2014,month=int(month),day=int(dia[0]),hour=int(hora_minuto[0][0]),minute=int(hora_minuto[0][1]),tzinfo=tz.gettz('Atlantic/Azores'))
					fmt = "%d/%m %H:%M"
					timezona= settings.getSetting('timezone')
					time = str(d.astimezone(tz.gettz(pytz.all_timezones[int(timezona)])).strftime(fmt))
					if "Online" in live: time = '[B][COLOR green](Online)[/B][/COLOR]'
					else: time = '[B][COLOR orange]' + time + '[/B][/COLOR]'
					addDir(time + ' - [B]('+comp+')[/B] ' + home + ' vs ' + away,url,42,os.path.join(addonpath,'resources','art','football.png'),len(match),True)
				except: addDir('[B][COLOR orange]' + timetmp + ' ' + datetmp + '[/B][/COLOR] - [B]('+comp+')[/B] ' + home + ' vs ' + away,url,42,os.path.join(addonpath,'resources','art','football.png'),len(match),True)


def livefootballvideo_sources(url):
	try:
		source = abrir_url(url)
	except: source = ""; mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile("title='sopcast'>\n<img src='(.+?)' alt='sopcast'/></a></td><td align='left'>(.+?)</td>\n<td>(.+?)</td><td>(.+?)</td><td><a href='(.+?)'").findall(source)
		for logo,name,language,quality,link in match:
			addDir("[B][COLOR orange][SopCast] [/COLOR][/B]" + name + ' (' + language + ') ('+quality+')',link,2,logo,len(match),False)
		match2 = re.compile("title='acestream'>\n<img src='(.+?)' alt='acestream'/></a></td><td align='left'>(.+?)</td>\n<td>(.+?)</td><td>(.+?)</td><td><a href='(.+?)'").findall(source)
		for logo,name,language,quality,link in match2:
			if "acestream://" in link:
				addDir("[B][COLOR orange][Acestream] [/COLOR][/B]" + name + ' (' + language + ') ('+quality+')',link,1,logo,len(match),False)
		if len(match) != 0 or len(match2) !=0:
			xbmc.executebuiltin("Container.SetViewMode(51)")
		else:
			sys.exit(0)

def rojadirecta_events():
	try:
		source = abrir_url("http://www.rojadirecta.me/")
	except: source = "";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.findall('<span class="(\d+)">.*?<div class="menutitle".*?<span class="t">([^<]+)</span>(.*?)</div>',source,re.DOTALL)
		for id,time,eventtmp in match:
			try:
				from datetime import datetime
				from dateutil import tz
				d = datetime(year=2014,month=6,day=7,hour=int(time.split(':')[0]),minute=int(time.split(':')[-1]),tzinfo=tz.gettz('Europe/Madrid'))
				fmt = "%H:%M"
				timezona= settings.getSetting('timezone')
				time = str(d.astimezone(tz.gettz(pytz.all_timezones[int(timezona)])).strftime(fmt))
			except:pass
    			eventnospanish = re.compile('<span class="es">(.+?)</span>').findall(eventtmp)
    			print eventnospanish
    			if eventnospanish:
        			for spanishtitle in eventnospanish:
            				eventtmp = eventtmp.replace('<span class="es">' + spanishtitle + '</span>','')
    			eventclean=eventtmp.replace('<span class="en">','').replace('</span>','').replace(' ()','')
			matchdois = re.compile('(.*)<b>\s*(.*?)\s*</b>').findall(eventclean)	
    			for sport,event in matchdois:
        			express = '<span class="' + id+ '">.*?</span>\s*</span>'
        			streams = re.findall(express,source,re.DOTALL)
        			for streamdata in streams:        			
            				p2pstream = re.compile('<td>P2P</td>\n.+?<td>([^<]*)</td>\n.+?<td>([^<]*)</td>\n.+?<td>([^<]*)</td>\n.+?<td>([^<]*)</td>\n.+?<td><b><a.+?href="(.+?)"').findall(streamdata)
            				already = False
            				for canal,language,tipo,qualidade,urltmp in p2pstream:
               					if "Sopcast" in tipo or "Acestream" in tipo:
                    					if already == False:
                        					addLink("[B][COLOR orange]"+time+ " - " + sport + " - " + event + "[/B][/COLOR]",'',"http://www.ligafutbol.net/wp-content/2010/02/Roja_Directa_logo.jpg")
                       						already = True
							if "ArenaVision" in canal: thumbnail = "http://s30.postimg.org/n6m6le88h/arenavisionlogo.png"
							else: thumbnail = "http://www.ligafutbol.net/wp-content/2010/02/Roja_Directa_logo.jpg"
                   					addDir("[B]["+tipo.replace("<","").replace(">","")+"][/B]-"+canal.replace("<","").replace(">","")+" - ("+language.replace("<","").replace(">","")+") - ("+qualidade.replace("<","").replace(">","")+" Kbs)",urltmp.replace("goto/",""),43,thumbnail,43,False)
                   			p2pdirect = re.compile('<td>P2P</td><td></td><td></td><td>(.+?)</td><td></td><td>.+?href="(.+?)"').findall(streamdata)
                   			for tipo,link in p2pdirect:
                   				if tipo == "SopCast" and "sop://" in link:
                   					addDir("[B][SopCast][/B]- (no info)",link,43,"http://www.ligafutbol.net/wp-content/2010/02/Roja_Directa_logo.jpg",43,False)

	xbmc.executebuiltin("Container.SetViewMode(51)")

def rojadirecta_resolver(name,url):
	print name,url
	if "sop://" not in url and "acestream://" not in url:
		if "http://" not in url: 
			url="http://"+url
		try:
			source = abrir_url(url)
		except: source = "";mensagemok(traducao(40000),traducao(40128))
		matchredirect = re.compile('<frame src="(.+?)"').findall(source)
		matchsop = re.compile('sop://(.+?)"').findall(source)
		if matchsop: sopstreams(name,"http://www.ligafutbol.net/wp-content/2010/02/Roja_Directa_logo.jpg","sop://" + matchsop[0])
		else:
			match = re.compile('this.loadPlayer\("(.+?)"').findall(source)
			if match: acestreams(name,"http://www.ligafutbol.net/wp-content/2010/02/Roja_Directa_logo.jpg",match[0])
			else: 
				if matchredirect:
					rojadirecta_resolver(name,matchredirect[0])
				else:
					mensagemok(traducao(40000),traducao(40022))
	elif "sop://" in url: sopstreams(name,"http://www.ligafutbol.net/wp-content/2010/02/Roja_Directa_logo.jpg",url)
	elif "acestream://" in url: acestreams(name,"http://www.ligafutbol.net/wp-content/2010/02/Roja_Directa_logo.jpg",url)
	else: mensagemok(traducao(40000),traducao(40022))		

def torrent_tv_sports():
	try:
		source = abrir_url("http://api.torrent-tv.ru/t/BgF2xM3fd1KWxgEVO21eprkQPkZi55b0LosbJU8oeZVikr1wPAmjkV%2ByixKZYNGt")
	except: source = "";mensagemok(traducao(40000),traducao(40128))
	if source:
		match= re.compile("#EXTINF:-1,(.+?)\(Спорт\)\n(.*)").findall(source)
		for titulo,acestream in match:
			clean = re.compile("\((.+?)\)").findall(titulo)
			for categorie in clean:
				titulo = titulo.replace("(" + categorie +")","")
			addDir(titulo,acestream,1,os.path.join(addonpath,'resources','art','torrenttvru.png'),len(match),False)
		xbmc.executebuiltin("Container.SetViewMode(51)")
			
def site_parsers_menu():
      addDir(traducao(40001),MainURL,11,os.path.join(addonpath,'resources','art','torrenttvru.png'),2,True)
      addDir(traducao(40140),MainURL,44,os.path.join(addonpath,'resources','art','torrenttvru.png'),2,True)
      addDir(traducao(40106),MainURL,24,'http://1torrent.tv/images/header_logo.png',2,True)
      addDir(traducao(40003),MainURL,13,'http://s1.postimg.org/snkagb15b/sopblog.png',1,True)
      addDir("ArenaVision World Cup 2014",MainURL,53,'http://s30.postimg.org/n6m6le88h/arenavisionlogo.png',1,True,"http://www.happyholidays2014.com/wp-content/uploads/2014/05/Fifa-World-cup-2014-brail.jpg")
      addDir(traducao(40131),MainURL,35,'http://s30.postimg.org/n6m6le88h/arenavisionlogo.png',1,True)
      addDir(traducao(40002),MainURL,8,os.path.join(addonpath,'resources','art','wiziwiglogo.png'),2,True)
      addDir(traducao(40132),MainURL,38,'http://www.userlogos.org/files/logos/clubber/football_ws___.PNG',1,True)
      addDir(traducao(40133),MainURL,40,'http://www.ligafutbol.net/wp-content/2010/02/Roja_Directa_logo.jpg',1,True)
      addDir(traducao(40139),MainURL,41,'http://livefootballvideo.com/images/xlivefootballvideologo.png.pagespeed.ic.3kxaAupa3O.png',1,True)
      addDir(traducao(40157),MainURL,50,'http://s30.postimg.org/3oznvmo5d/livefootball.png',1,True)
      xbmc.executebuiltin("Container.SetViewMode(51)")

def arenavision_mundial():
	try:
		source = abrir_url("http://mundial.arenavision.in/")
	except: source="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile("<li><a href='(.+?)'>(.+?)</a></li>").findall(source)
		for link,name in match:
			if "Agenda/Schedule" in name:
				addDir('[B][COLOR orange]Agenda/Schedule[/B][/COLOR]',link,54,"http://s30.postimg.org/n6m6le88h/arenavisionlogo.png",1,True,"http://www.happyholidays2014.com/wp-content/uploads/2014/05/Fifa-World-cup-2014-brail.jpg")
			if "ArenaMundial" in name:
				addDir(name,link,36,"http://s30.postimg.org/n6m6le88h/arenavisionlogo.png",1,False,"http://www.happyholidays2014.com/wp-content/uploads/2014/05/Fifa-World-cup-2014-brail.jpg")
			else: pass

def arenavision_mundial_agenda(url):
	try:
		source = abrir_url(url)
	except: source="";mensagemok(traducao(40000),traducao(40128))
	if source:
		html_trunk = re.findall("u>(.*?)(?:<br />\n<b><|script)", source, re.DOTALL)
		for trunk in html_trunk:
			data = re.compile('(.*?)</b>').findall(trunk)
			for dias in data:
				dia = re.compile('.* (.+?) de (.+?)<').findall(dias)
				for day,mes in dia:
					if mes == 'junio': month = 6
					elif mes == 'julio': month = 7
					addLink('[B][COLOR orange]' + day + '/' + str(month) + '/2014' + '[/B][/COLOR]',MainURL,"http://s30.postimg.org/n6m6le88h/arenavisionlogo.png","http://www.happyholidays2014.com/wp-content/uploads/2014/05/Fifa-World-cup-2014-brail.jpg")
			eventos = re.compile('(.+?):(.+?) CET(.+?)(?:<|\n<)').findall(trunk)
			for evento in eventos:
				try:
					event_dict = evento[2].split('/')
					from datetime import datetime
					from dateutil import tz
					d = datetime(year=2014,month=6,day=15,hour=int(evento[0]),minute=int(evento[1]),tzinfo=tz.gettz('Europe/Madrid'))
					fmt = "%H:%M"
					timezona= settings.getSetting('timezone')
					time = str(d.astimezone(tz.gettz(pytz.all_timezones[int(timezona)])).strftime(fmt))
					addLink(str(time) + ' - ' + event_dict[2],MainURL,"http://s30.postimg.org/n6m6le88h/arenavisionlogo.png","http://www.happyholidays2014.com/wp-content/uploads/2014/05/Fifa-World-cup-2014-brail.jpg")
				except:pass
	xbmc.executebuiltin("Container.SetViewMode(51)")


def xml_lists_menu():
      if settings.getSetting('sopcast-oficial') == "true":
      	    addDir(traducao(40116),"http://sopcast.org/chlist.xml",28,addonpath + art + 'xml_list_sopcast.png',2,True)
      if settings.getSetting('sopcast-romanian') == "true":
            addDir(traducao(40117),"http://streams.magazinmixt.ro/xsopcast.xml",28,addonpath + art + 'xml_list_sopcast.png',2,True)
      if settings.getSetting('livestreams-spanish') == "true":
            addDir(traducao(40118),"http://dl.dropbox.com/u/4735170/streams.xml",28,addonpath + art + 'xml_lists.png',2,True)
      if settings.getSetting('livestreams-pt-sports') == "true":
            addDir(traducao(40119),"http://dl.dropboxusercontent.com/u/266138381/Desporto.xml",28,addonpath + art + 'xml_lists.png',2,True)
      if settings.getSetting('livestreams-pt-events') == "true":
            addDir(traducao(40120),"http://dl.dropboxusercontent.com/u/266138381/Eventos.xml",28,addonpath + art + 'xml_lists.png',2,True)
      try:
            if xbmcvfs.exists(os.path.join(pastaperfil,"Lists")):
		   dirs, files = xbmcvfs.listdir(os.path.join(pastaperfil,"Lists"))
                   for file in files:
			f = open(os.path.join(pastaperfil,"Lists",file), "r")
	                string = f.read()
                        addDir("[B][COLOR orange]" + file.replace(".txt","") + "[/B][/COLOR]",string,28,addonpath + art + 'xml_lists.png',2,True)
      except: pass
      addDir(traducao(40121),MainURL,34,addonpath + art + 'plus-menu.png',2,False)
      xbmc.executebuiltin("Container.SetViewMode(51)")
			
def menu_principal():
      addDir(traducao(40114),MainURL,26,addonpath + art + 'web-parsers-menu.png',2,True)
      addDir(traducao(40115),MainURL,27,addonpath + art + 'xml_lists.png',2,True)
      addDir(traducao(40144),MainURL,47,addonpath + art + 'Favorites-menu.png',2,True)
      addLink('','','p2p')

      if xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.linux') or xbmc.getCondVisibility('System.Platform.OSX') or xbmc.getCondVisibility('System.Platform.Android'):
          addDir('[COLOR orange]AceStream: [/COLOR]' + traducao(40004),MainURL,4,addonpath + art + 'acestream-menu-item.png',1,False)
          addDir('[COLOR orange]AceStream: [/COLOR]' + traducao(600029),MainURL,52,addonpath + art + 'acestream-menu-item.png',1,False)

      if xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.linux') or xbmc.getCondVisibility('System.Platform.OSX') or xbmc.getCondVisibility('System.Platform.Android'):
          addDir('[COLOR orange]SopCast: [/COLOR]' + traducao(40005),MainURL,3,addonpath + art + 'sopcast-menu-item.png',1,False)
          addDir('[COLOR orange]SopCast: [/COLOR]' + traducao(40006),MainURL,5,addonpath + art + 'sopcast-menu-item.png',1,False)

      elif xbmc.getCondVisibility('system.platform.windows'):
          addDir(traducao(40007),MainURL,7,'',1,False)

      if xbmc.getCondVisibility('System.Platform.IOS') or xbmc.getCondVisibility('System.Platform.ATV2'):
          addLink(traducao(40056),'',addonpath + art + 'processwarning.png')
          
      addLink('','','p2p')
      addDir('[B]' + traducao(40057) + '[/B]',MainURL,15,addonpath + art + 'settings_menu.png',2,True)       
      xbmc.executebuiltin("Container.SetViewMode(50)")
      
      #dirty hack to break sopcast.exe player codec - renaming the file again in case xbmc crashed
      if xbmc.getCondVisibility('system.platform.windows'):
      	import _winreg
      	aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
      	try:
      		aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
      		name, value, type = _winreg.EnumValue(aKey, 0)
      		codec_file = os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx.old')
      		_winreg.CloseKey(aKey)
      		if xbmcvfs.exists(codec_file): xbmcvfs.rename(codec_file,os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx'))
      	except:pass
      
def load_local_torrent():
	torrent_file = xbmcgui.Dialog().browse(int(1), traducao(600028), 'myprograms','.torrent')
	if torrent_file:
		if xbmc.getCondVisibility('system.platform.windows'):
			acestreams("Local .torrent","",'file:\\' + torrent_file)
		else:
			acestreams("Local .torrent","",'file://' + torrent_file)
	else: pass



def sopcast_ucoz():
    conteudo=clean(abrir_url('http://sopcast.ucoz.com'))
    listagem=re.compile('<div class="eTitle" style="text-align:left;"><a href="(.+?)">(.+?)</a>').findall(conteudo)
    for urllist,titulo in listagem:
    	print titulo
    	try:
    		match = re.compile('\((.*?)\.(.*?)\.(.*?)\. (.*?):(.*?) UTC\) (.*)').findall(titulo)
    		if match:
    			for dia,mes,ano,hora,minuto,evento in match:
    				from datetime import datetime
    				from dateutil import tz
    				d = datetime(year=int(ano),month=int(mes),day=int(dia),hour=int(hora),minute=int(minuto),tzinfo=tz.gettz('Europe/London'))
    				fmt = "%y-%m-%d %H:%M"
    				timezona= settings.getSetting('timezone')
    				time = str(d.astimezone(tz.gettz(pytz.all_timezones[int(timezona)])).strftime(fmt))
    				addDir('[B][COLOR orange]' + time + '[/B][/COLOR]-' + evento,urllist,14,'',len(listagem),False)
    		else:
    			addDir(titulo,urllist,14,'',len(listagem),False)
    	except:
    			addDir(titulo,urllist,14,'',len(listagem),False)

def sopcast_ucoz_play(name,url):
    conteudo=clean(abrir_url(url))
    blogpost = re.findall('<tr><td class="eMessage">(.*?)<tr><td colspan', conteudo, re.DOTALL)
    if blogpost:
    	ender=[]
    	titulo=[]
    	match = re.compile('br.+?>(.+?)<').findall(blogpost[0])
	print match
    	for address in match:
    		if "sop://" in address:
    			titulo.append('Sopcast [' + address +']')
    			ender.append(address)
    		elif "(ace stream)" in address:
    			titulo.append('Acestream [' + address.replace(' (ace stream)','') +']')
    			ender.append(address.replace(' (ace stream)',''))
    		else: pass
    	if ender and titulo:
    		index = xbmcgui.Dialog().select(traducao(40023), titulo)
    		if index > -1:
    			nomeescolha=titulo[index]
    			linkescolha=ender[index]
    			if re.search('acestream',nomeescolha,re.IGNORECASE) or re.search('TorrentStream',nomeescolha,re.IGNORECASE): acestreams(nomeescolha,'',linkescolha)
    			elif re.search('sopcast',nomeescolha,re.IGNORECASE):
                		if xbmc.getCondVisibility('system.platform.windows'):sopserver()
				else:sopstreams(nomeescolha,'',linkescolha)
		        else: mensagemok(traducao(40000),traducao(40024))  
    else:
    	mensagemok(traducao(40000),traducao(40008))
   
def onetorrent():
    html_source = clean(abrir_url(OnetorrentURL+"/channels.php"))
    categorias=re.compile('<div class="tab_caption.+?" id="tcap_(.+?)".+?>(.+?)</div>').findall(html_source)
    for catid,catname in categorias:
        canais=re.compile('<div class=".+?" id="tcon_'+catid+'"(.+?)</div></div></div></div>').findall(html_source)
        if len(canais)!=0: addLink('[B][COLOR blue]'+catname+'[/B][/COLOR]','','')
        for lista in canais:
            individual=re.compile('<img src="(.+?)">.+?<a href="(.+?)">(.+?)</a>').findall(lista)
            for img,link,nomech in individual:
                addDir(nomech,OnetorrentURL+link,25,OnetorrentURL+ img,2,False)
        addLink('','','')

def onetorrent_play(name,url):
    conteudo=abrir_url(url)
    try:torrent=re.compile('this.loadTorrent.+?"(.+?)",').findall(conteudo)[0]
    except:torrent=re.compile('this.loadPlayer.+?"(.+?)",').findall(conteudo)[0]
    logo=re.compile('<img id="cur_logo" src="(.+?)">').findall(conteudo)[0]
    acestreams(name,OnetorrentURL + logo,torrent)

def torrenttv():
	dict_torrent = {}
	html_source = abrir_url("http://api.torrent-tv.ru/t/BgF2xM3fd1KWxgEVO21eprkQPkZi55b0LosbJU8oeZVikr1wPAmjkV%2ByixKZYNGt")
	match = re.compile('#EXTINF:-1,(.+?)\n(.*)').findall(html_source)
	for title, acehash in match:
    		channel_name = re.compile('(.+?) \(').findall(title)
    		match_cat = re.compile('\((.+?)\)').findall(title)
    		for i in xrange(0,len(match_cat)):
    			if match_cat[i] == "Для взрослых" and settings.getSetting('hide_porn') == "true":
    				pass
    			elif match_cat[i] == "Ночной канал" and settings.getSetting('hide_porn') == "true":
                                pass
    			else:
                		if settings.getSetting('russian_translation') == "true": categorie = russiandictionary(match_cat[i])
                		else: categorie=match_cat[i]
                		if categorie not in dict_torrent.keys():
                			try:
            					dict_torrent[categorie] = [(channel_name[0],acehash)]
            				except: pass
            			else:
            				try:
            					dict_torrent[categorie].append((channel_name[0],acehash))
            				except: pass
	for categories in dict_torrent.keys():
		addDir(categories,str(dict_torrent),12,'',2,True)
		
def torrenttv_play(name,url):
	dict_torrent=eval(url)
	for channel in dict_torrent[name]:
		try: addDir(channel[0],channel[1],1,'',2,False)
		except:pass

def wiziwig_cats():
    addDir(traducao(40009),WiziwigURL + '/index.php?part=sports',9,os.path.join(addonpath,'resources','art','wiziwiglogo.png'),1,True)
    addDir("World Cup 2014 ",WiziwigURL + '/competition.php?part=sports&discipline=worldcup&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','worldcup.png'),1,True)
    addDir(traducao(40010),WiziwigURL + '/competition.php?part=sports&discipline=americanfootball&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','americanfootball.png'),1,True)
    addDir(traducao(40011),WiziwigURL + '/competition.php?part=sports&discipline=football&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','football.png'),1,True)
    addDir(traducao(40012),WiziwigURL + '/competition.php?part=sports&discipline=basketball&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','Basketball.png'),1,True)
    addDir(traducao(40013),WiziwigURL + '/competition.php?part=sports&discipline=icehockey&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','IceHockey.png'),1,True)
    addDir(traducao(40014),WiziwigURL + '/competition.php?part=sports&discipline=baseball&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','Baseball.png'),1,True)
    addDir(traducao(40015),WiziwigURL + '/competition.php?part=sports&discipline=tennis&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','Tennis.png'),1,True)
    addDir(traducao(40016),WiziwigURL + '/competition.php?part=sports&discipline=motorsports&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','Racing.png'),1,True)
    addDir(traducao(40017),WiziwigURL + '/competition.php?part=sports&discipline=rugby&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','Rugby.png'),1,True)
    addDir(traducao(40018),WiziwigURL + '/competition.php?part=sports&discipline=golf&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','Golf.png'),1,True)
    addDir(traducao(40019),WiziwigURL + '/competition.php?part=sports&discipline=cricket&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','Cricket.png'),1,True)
    addDir(traducao(40020),WiziwigURL + '/competition.php?part=sports&discipline=cycling&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','Cycling.png'),1,True)
    addDir(traducao(40021),WiziwigURL + '/competition.php?part=sports&discipline=other&archive=no&allowedDays=1,2,3,4,5,6,7',9,os.path.join(addonpath,'resources','art','Other_white.png'),1,True)
    xbmc.executebuiltin("Container.SetViewMode(51)")

def translate_months(month):
	if month == "January": return 1
	elif month == "February": return 2
	elif month == "March": return 3
	elif month == "April": return 4
	elif month == "May": return 5
	elif month == "June": return 6
	elif month == "July": return 7
	elif month == "August": return 8
	elif month == "September": return 9
	elif month == "October": return 10
	elif month == "November": return 11
	elif month == "December": return 12
	else: return

def wiziwig_events(url):
    conteudo=clean(abrir_url(url))    
    eventos=re.compile('<div class="date" [^>]+>([^<]+)</div>\s*<span class="time" rel=[^>]+>([^<]+)</span> -\s*<span class="time" rel=[^>]+>([^<]+)</span>\s*</td>\s*<td class="home".+?<img[^>]* src="([^"]*)"[^>]*>([^<]+)<img [^>]+></td>(.*?)<td class="broadcast"><a class="broadcast" href="([^"]+)">Live</a></td>').findall(conteudo)
    for date,time1,time2,icon,team1,palha,url in eventos:
        if re.search('<td class="away">',palha):
            try:team2=' - ' + re.compile('<td class="away"><img.+?>(.+?)<img class="flag"').findall(palha)[0]
            except:team2=''
        else: team2=''
        datefinal=date.split(', ')
	print datefinal,time1
	try:
		month_day = re.compile('(.+?) (.*)').findall(datefinal[1])
		monthname = translate_months(month_day[0][0])
		dayname = int(month_day[0][1])
		hourname = int(time1.split(':')[0])
		minutesname = int(time1.split(':')[1])
		from datetime import datetime
		from dateutil import tz
		d = datetime(year=2014,month=monthname,day=dayname,hour=hourname,minute=minutesname,tzinfo=tz.gettz('Europe/Madrid'))
		fmt = "%m-%d %H:%M"
		madrid = tz.gettz('Europe/Madrid')
		timezona= settings.getSetting('timezone')
		time = str(d.astimezone(tz.gettz(pytz.all_timezones[int(timezona)])).strftime(fmt))
		#print monthname, dayname
		addDir('[B](' + str(time) + ')[/B] ' + team1 + team2,WiziwigURL + url,10,WiziwigURL + icon,len(eventos),True)
	except: addDir('[B](' + datefinal[1] + ' ' + time1 + ')[/B] ' + team1 + team2,WiziwigURL + url,10,WiziwigURL + icon,len(eventos),True)
    xbmc.executebuiltin("Container.SetViewMode(51)")

		
             
    
def wiziwig_servers(url):
	conteudo=clean(abrir_url(url))
	if re.search('Sorry, streams will only appear',conteudo):
		try:nrestacoes='[B]' + re.compile('</h2><p>There.+?<strong>(.+?) ').findall(conteudo)[0] + ' estações[/B] vão transmitir o jogo.'
		except:nrestacoes=''
		mensagemok(traducao(40000),'Os links para o jogo são vão aparecer','uma 1hora antes do jogo começar.',nrestacoes)
		return
	ender=[]
	titulo=[]
	station_name=re.findall('stationname">(.+?)</td>(.*?)<td></td></tr><(?:tr class="broadcast|/tbody>)', conteudo, re.DOTALL)
	for station,html_trunk in station_name:
		streams=re.compile('.*?<tr class="streamrow[^"]*">\s*<td>\s*([^\s]+)\s*</td>\s*<td>\s*<a class="broadcast go" href="((?!adserver|http://torrent-tv.ru|forum|www\.bet365|BWIN)[^"]+)" target="_blank">Play now!</a>\s*<a[^>]*>[^>]*</a>\s*</td>\s*<td>([^<]+)</td>').findall(html_trunk)
		for nome,chid,quality in streams:
			if re.search('Sopcast',nome,re.IGNORECASE) or re.search('Acestream',nome,re.IGNORECASE) or re.search('TorrentStream',nome,re.IGNORECASE):
				if quality.replace(" Kbps","")[-1] != "1":
					titulo.append('['+station+'] ' + '[B][COLOR orange]' + nome +'[/B][/COLOR]'+ ' ('+quality+')')
					ender.append(chid)
				else: pass
	if len(ender)==0:mensagemok(traducao(40000),traducao(40022));sys.exit(0)
	else:
		for i in xrange(0,len(titulo)):
			if re.search('acestream',titulo[i],re.IGNORECASE) or re.search('TorrentStream',titulo[i],re.IGNORECASE):
				addDir(titulo[i],ender[i],1,"http://www.brudvik.org/wp-content/uploads/2011/08/wiziwig-logo.png",1,False)
			elif re.search('sopcast',titulo[i],re.IGNORECASE):
				addDir(titulo[i],ender[i],2,"http://www.brudvik.org/wp-content/uploads/2011/08/wiziwig-logo.png",1,False)
	xbmc.executebuiltin("Container.SetViewMode(51)") 

         
def autoconf():
	import tarfile
	sopcast_raspberry = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/sopcast-raspberry.tar.gz"
	sopcast_linux_generico =  "https://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Sopcastx86_64i386/sopcast_linux.tar.gz"
	acestream_windows = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Windows/windows-aceengine2-3.tar.gz"
    
	if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android') and not settings.getSetting('force_android') == "true":
		print "Detected OS: Linux"
		if os.uname()[4] == "armv6l":
			try:
				if re.search(os.uname()[1],"openelec",re.IGNORECASE): acestream_rpi = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/openelec-acestream.tar.gz"
				elif re.search(os.uname()[1],"raspbmc",re.IGNORECASE): acestream_rpi = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/raspbmc-acestream.tar.gz"
				elif os.path.isfile("/etc/xbian_version"): acestream_rpi = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/xbian-acestream.tar.gz"
				else:
					mensagemok(traducao(40000),"Sorry could not detect your OS.","Select it from the next list")
					OS_list = ["OpenELEC","Raspbmc","Xbian","Pipplware"]
					url_packagerpi_list = ["http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/openelec-acestream.tar.gz","http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/raspbmc-acestream.tar.gz","http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/xbian-acestream.tar.gz","http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/raspbmc-acestream.tar.gz"]
					OS_Rpi_choose = xbmcgui.Dialog().select
					choose=OS_Rpi_choose('Select your OS',OS_list)
					if choose > -1:
						acestream_rpi= url_packagerpi_list[choose]
			except: acestream_rpi = "" #da erro de script no windows, workaround porque diferente rpi
			print "Detected Platform Raspberry PI"
			#Sop

			SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
			download_tools().Downloader(sopcast_raspberry,SPSC_KIT,traducao(40025),traducao(40000))
            
			if tarfile.is_tarfile(SPSC_KIT):
				path_libraries = os.path.join(pastaperfil,"sopcast")
				download_tools().extract(SPSC_KIT,path_libraries)
				xbmc.sleep(500)
				download_tools().remove(SPSC_KIT)

            		#Ace
			SPSC_KIT = os.path.join(addonpath,acestream_rpi.split("/")[-1])
			download_tools().Downloader(acestream_rpi,SPSC_KIT,traducao(40026),traducao(40000))
        
			if tarfile.is_tarfile(SPSC_KIT):
				path_libraries = os.path.join(pastaperfil,"acestream")
				download_tools().extract(SPSC_KIT,path_libraries)
				xbmc.sleep(500)
				download_tools().remove(SPSC_KIT)

			settings.setSetting('autoconfig',value='false')


                elif os.uname()[4] == "armv7l":
			if re.search(os.uname()[1],"openelec",re.IGNORECASE):
				OS_Choose = "OpenELEC"
			elif os.path.isfile("/etc/xbian_version"):
				OS_Choose = "Xbian"
			else:
                		mensagemok(traducao(40000),traducao(40109),traducao(40110))
                		OS_list = ["MXLinux","OpenELEC","Xbian"]
                		choose=xbmcgui.Dialog().select('Select your OS',OS_list)
                		if choose > -1:
                			OS_Choose= OS_list[choose]

			#Linux armv7 configuration according to platform

			#MXLINUX

                	if OS_Choose == "MXLinux":
				acestream_installed = False
				sopcast_installed = False
               			print "MXLinux"
               			SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
               			download_tools().Downloader(sopcast_raspberry,SPSC_KIT,traducao(40025),traducao(40000))
				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"sopcast")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					sopcast_installed = True

				acestream_mxlinux = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Armv7/mxlinux/mxlinux_armv7_acestream.tar.gz"
				SPSC_KIT = os.path.join(addonpath,acestream_mxlinux.split("/")[-1])
				download_tools().Downloader(acestream_mxlinux,SPSC_KIT,traducao(40026),traducao(40000))
        			if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"acestream")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					acestream_installed = True
				if acestream_installed and sopcast_installed:
					settings.setSetting('autoconfig',value='false')	

			#OPENELEC

                	if OS_Choose == "OpenELEC":
				acestream_installed = False
				sopcast_installed = False
                		print "Openelec armv7 platform detected"
                		SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
                		download_tools().Downloader(sopcast_raspberry,SPSC_KIT,traducao(40025),traducao(40000))
				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"sopcast")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					sopcast_installed = True
				acestream_armv7 = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Armv7/openelec/openelec-acestream.tar.gz"
				SPSC_KIT = os.path.join(addonpath,acestream_armv7.split("/")[-1])
				download_tools().Downloader(acestream_armv7,SPSC_KIT,traducao(40026),traducao(40000))
        			if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"acestream")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					acestream_installed = True
				if acestream_installed and sopcast_installed:
					settings.setSetting('autoconfig',value='false')	

			#XBIAN
               		if OS_Choose == "Xbian":
				acestream_installed = False
				sopcast_installed = False
               			print "Xbian armv7 platform detected"
               			SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
               			download_tools().Downloader(sopcast_raspberry,SPSC_KIT,traducao(40025),traducao(40000))
				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"sopcast")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					sopcast_installed = True
				acestream_armv7 = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Armv7/xbian/xbian_acestream.tar.gz"
				SPSC_KIT = os.path.join(addonpath,acestream_armv7.split("/")[-1])
				download_tools().Downloader(acestream_armv7,SPSC_KIT,traducao(40026),traducao(40000))
       				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"acestream")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					acestream_installed = True
				if acestream_installed and sopcast_installed:
					settings.setSetting('autoconfig',value='false')	


			
		elif (os.uname()[4] == "x86_64" and re.search(os.uname()[1],"openelec",re.IGNORECASE)) or settings.getSetting('openelecx86_64') == "true":
			settings.setSetting('openelecx86_64',value='true')
			print "Detected OpenELEC x86_64"
			openelecx86_64_package = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/x86_64/Openelec/openelec_x86_64_userdata.tar.gz"
			SPSC_KIT = os.path.join(addonpath,openelecx86_64_package.split("/")[-1])
			download_tools().Downloader(openelecx86_64_package,SPSC_KIT,traducao(40112),traducao(40000))
			import tarfile
			if tarfile.is_tarfile(SPSC_KIT):
				download_tools().extract(SPSC_KIT,pastaperfil)
				xbmc.sleep(500)
				download_tools().remove(SPSC_KIT)
			settings.setSetting('autoconfig',value='false')

		elif (os.uname()[4] == "i386" and re.search(os.uname()[1],"openelec",re.IGNORECASE)) or (os.uname()[4] == "i686" and re.search(os.uname()[1],"openelec",re.IGNORECASE)) or settings.getSetting('openeleci386') == "true":
			settings.setSetting('openeleci386',value='true')
			print "Detected OpenELEC i386"
			openeleci386_package = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/i386/openelec/openeleci386-acestream-sopcast.tar.gz"
			SPSC_KIT = os.path.join(addonpath,openeleci386_package.split("/")[-1])
			download_tools().Downloader(openeleci386_package,SPSC_KIT,traducao(40112),traducao(40000))
			import tarfile
			if tarfile.is_tarfile(SPSC_KIT):
				download_tools().extract(SPSC_KIT,pastaperfil)
				xbmc.sleep(500)
				download_tools().remove(SPSC_KIT)
			settings.setSetting('autoconfig',value='false')		
	
		else:
			if os.uname()[4] == "x86_64":
				opcao= xbmcgui.Dialog().yesno(traducao(40000), traducao(40113))
				if opcao: 
					settings.setSetting('openelecx86_64',value='true')
					autoconf()
			elif os.uname()[4] == "i386" or os.uname()[4] == "i686":
				opcao= xbmcgui.Dialog().yesno(traducao(40000), traducao(600023))
				if opcao: 
					settings.setSetting('openeleci386',value='true')
					autoconf()

			else: mensagemok(traducao(40000),traducao(40056))
			

			#Linux but not openelec i386 nor openelec x86_64 - General Linux platforms configuration
			
			if settings.getSetting('openeleci386') == "false" and settings.getSetting('openelecx86_64') == "false":

				print "Detected Other Linux Plataform"

            		#Sop
            		#Download and extract sopcast-bundle
				SPSC_KIT = os.path.join(addonpath,sopcast_linux_generico.split("/")[-1])
				download_tools().Downloader(sopcast_linux_generico,SPSC_KIT,traducao(40025),traducao(40000))
				import tarfile
				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"sopcast")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
				#set every single file from the bundle as executable
				path_libraries = os.path.join(pastaperfil,"sopcast")
				dirs, files = xbmcvfs.listdir(path_libraries)
				for ficheiro in files:
					binary_path = os.path.join(path_libraries,ficheiro)
					st = os.stat(binary_path)
					import stat
					os.chmod(binary_path, st.st_mode | stat.S_IEXEC)
				path_libraries = os.path.join(path_libraries,"lib")
				dirs, files = xbmcvfs.listdir(path_libraries)
				for ficheiro in files:
					binary_path = os.path.join(path_libraries,ficheiro)
					st = os.stat(binary_path)
					import stat
					os.chmod(binary_path, st.st_mode | stat.S_IEXEC)
	   		 
	   		 #Ace
	   		 
				import subprocess
				proc_response = []
				proc = subprocess.Popen(['whereis','acestreamengine'],stdout=subprocess.PIPE)
				for line in proc.stdout:
					print "Output of acestream subprocess check",line.rstrip()
					proc_response.append(line.rstrip())
					if "acestreamengine: /" in str(proc_response):
						print "Acestream engine is already installed"
						try:
							proc.kill()
							proc.wait()
						except:pass
					else:
						mensagemok(traducao(40031),traducao(40027),traducao(40028) + linkwiki,traducao(40029))
						sys.exit(0)
				settings.setSetting('autoconfig',value='false')


	elif xbmc.getCondVisibility('system.platform.windows'):
		print "Detected OS: Windows"
		if not xbmcvfs.exists(pastaperfil): xbmcvfs.mkdir(pastaperfil)
        #Sop
		import ctypes
                is_admin=ctypes.windll.shell32.IsUserAnAdmin() != 0
                if is_admin == False:
                    mensagemok(traducao(40000),traducao(40158),traducao(40159))
                else:
		    import subprocess
                    cmd = ['sc','delete','sopcastp2p']
                    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                    for line in proc.stdout:
                        print "linha " + line.rstrip()
                    xbmc.sleep(1000)
                    ret = mensagemprogresso.create(traducao(40000),traducao(40000))
                    mensagemprogresso.update(0,traducao(40160),"  ")
                    xbmc.sleep(1000)
                    import _winreg
                    aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                    try:
                        aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
                        name, value, type = _winreg.EnumValue(aKey, 0)
                        sopcast_executable = value
                        print "Installation executable of sopcast was found: " + sopcast_executable
                        _winreg.CloseKey(aKey)
                        mensagemprogresso.update(10,traducao(40160),traducao(40161))
                    except:
                        sopcast_executable = ""
                        mensagemok(traducao(40000),traducao(40162),traducao(40163))
                    if not sopcast_executable: pass
                    else:
                        xbmc.sleep(1000)
                        mensagemprogresso.update(20,traducao(40164),"  ")
                        xbmc.sleep(1000)
                        print "Getting windows users IDS"
                        aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                        aKey = _winreg.OpenKey(aReg, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList')
                        users = []
                        for i in range(1024):
                            try:
                                asubkey=_winreg.EnumKey(aKey,i)
                                print asubkey
                                aKeydois = _winreg.OpenKey(aReg, os.path.join('SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList',asubkey))
                                val=_winreg.QueryValueEx(aKeydois, "ProfileImagePath")
                                try:
                                    print val[0]
                                except:
                                    print "Notice: User with strange characters, print cmd ignored."
                                if "Windows" in val[0] or "%systemroot%" in val[0]:
                                    pass
                                else:
                                    users.append(asubkey)
                            except:
                                pass
                        if not users:
                            mensagemok(traducao(40000),traducao(40165))
                        else:
                            mensagemprogresso.update(30,traducao(40164),traducao(40161))
                            xbmc.sleep(200)
                            mensagemprogresso.update(30,traducao(40166),"   ")
                            xbmc.sleep(1000)
                            print "System Users", users
			    srvanytargz = os.path.join(sopcast_executable.replace("SopCast.exe",""),"srvany.tar.gz")                               
                            download_tools().Downloader("http://p2p-strm.googlecode.com/svn/trunk/Modules/Windows/srvany.tar.gz",srvanytargz,traducao(40167),traducao(40000)) 
                            xbmc.sleep(1000)
                            import tarfile
                            if tarfile.is_tarfile(srvanytargz):
                                path_libraries = sopcast_executable.replace("SopCast.exe","")
                                download_tools().extract(srvanytargz,path_libraries)
                                download_tools().remove(srvanytargz)
                            xbmc.sleep(1000)
                            ret = mensagemprogresso.create(traducao(40000),traducao(40000))
                            xbmc.sleep(200)
                            mensagemprogresso.update(35,traducao(40168),"  ")
                            xbmc.sleep(1000)
                            import subprocess
                            cmd = ['sc','create','sopcastp2p','binpath=',os.path.join(os.path.join(sopcast_executable.replace("SopCast.exe","")),'srvany.exe')]
                            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                            servicecreator = False
                            for line in proc.stdout:
                                print "linha " + line.rstrip()
                                servicecreator = True
                            if servicecreator == False:
                                mensagemok(traducao(40000),traducao(40169))
                            else:
                                mensagemprogresso.update(40,traducao(40168),traducao(40161))
                                xbmc.sleep(1000)
                                mensagemprogresso.update(45,traducao(40170),"  ")
                                xbmc.sleep(1000)
                                print "Trying to modify regedit...."
                                try:
                                    aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                                    key = _winreg.CreateKey(aReg, r'SYSTEM\CurrentControlSet\Services\sopcastp2p\Parameters')
                                    _winreg.SetValueEx(key, 'AppDirectory', 0, _winreg.REG_SZ, os.path.join(sopcast_executable.replace("SopCast.exe","")))
                                    _winreg.SetValueEx(key, 'Application', 0, _winreg.REG_SZ, os.path.join(os.path.join(sopcast_executable.replace("SopCast.exe","")),"SopCast.exe"))
                                    _winreg.SetValueEx(key, 'AppParameters', 0, _winreg.REG_SZ, "sop://")
                                    mensagemprogresso.update(50,traducao(40170), traducao(40161))
                                    regedit = True
                                except:
                                    mensagemok(traducao(40000),traducao(40171))
                                    regedit = False
                                if regedit == False: pass
                                else:
                                    xbmc.sleep(1000)
                                    mensagemprogresso.update(50,traducao(40172), "   ")
                                    cmd = ['sc','sdshow','sopcastp2p']
                                    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                                    lines = []
                                    for line in proc.stdout:
					print line.rstrip()
                                        if line.rstrip() != "" and "(" in line.rstrip(): lines.append(line.rstrip())
                                        else: pass
				    print lines
				    print len(lines)
                                    if len(lines) != 1: mensagemok(traducao(40000),traducao(40173))
                                    else:
                                        linha_arr = []
                                        for user in users:
                                            linha_arr.append('(A;;RPWPCR;;;' + user + ')')
                                        linha_add = ''
                                        for linha in linha_arr:
                                            linha_add += linha
                                        print "line peace to add: " + linha_add
                                        linha_final = lines[0].replace("S:(",linha_add + "S:(")
                                        print "Final line: " + linha_final
                                        permissions = False
                                        xbmc.sleep(500)
                                        mensagemprogresso.update(60,traducao(40172), traducao(40161))
                                        xbmc.sleep(500)
                                        mensagemprogresso.update(60,traducao(40174), "   ")
                                        cmd = ['sc','sdset','sopcastp2p',linha_final]
                                        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                                        for line in proc.stdout:
                                            print line.rstrip()
                                            permissions = True
                                        if permissions == False: mensagemok(traducao(40000),traducao(40175))
                                        else:
                                            mensagemprogresso.update(70,traducao(40174), traducao(40161))
                                            xbmc.sleep(1000)
                                            mensagemprogresso.update(70,traducao(40176), "   ")
                                            print "Trying to set sopcastp2p service regedit permissions..."
                                            download_tools().Downloader("http://p2p-strm.googlecode.com/svn/trunk/Modules/Windows/sopcastp2p-permissions.txt",os.path.join(pastaperfil,"sopcastp2p-permissions.txt"),traducao(40177),traducao(40000))
                                            xbmc.sleep(500)
                                            ret = mensagemprogresso.create(traducao(40000),traducao(40000))
                                            xbmc.sleep(500)
                                            mensagemprogresso.update(80,traducao(40178), "   ")
                                            xbmc.sleep(1000)
                                            cmd = ['regini',os.path.join(pastaperfil,"sopcastp2p-permissions.txt")]
                                            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                                            for line in proc.stdout:
                                                print line.rstrip()
                                            mensagemprogresso.update(90,traducao(40178), traducao(40178))
                                            mensagemprogresso.update(100,traducao(40179), "   ")
                                            xbmc.sleep(2000)
                                            mensagemprogresso.close()
        #Ace
		SPSC_KIT = os.path.join(addonpath,acestream_windows.split("/")[-1])
		download_tools().Downloader(acestream_windows,SPSC_KIT,traducao(40026),traducao(40000))
		import tarfile
		if tarfile.is_tarfile(SPSC_KIT):
			path_libraries = os.path.join(pastaperfil)
			download_tools().extract(SPSC_KIT,path_libraries)
			download_tools().remove(SPSC_KIT)
		settings.setSetting('autoconfig',value='false')
    
	elif xbmc.getCondVisibility('System.Platform.OSX'):
		print "Detected OS: Mac OSX"
		available = False
		if os.uname()[-1] == "x86_64":
			mac_package = "https://p2p-strm.googlecode.com/svn/trunk/Modules/MacOsx/MacOSX_x86_64_ace_and_sop.tar.gz"
			available = True
		elif os.uname()[-1] == "i386":
			mac_package = "http://p2p-strm.googlecode.com/svn/trunk/Modules/MacOsx/MacOSX_i386_ace_and_sop.tar.gz"
			available = True
		else:
			available = False
		if available == True:		
			if not xbmcvfs.exists(pastaperfil):
				xbmcvfs.mkdir(pastaperfil)		
			MAC_KIT = os.path.join(addonpath,mac_package.split("/")[-1])
			download_tools().Downloader(mac_package,MAC_KIT,traducao(40112),traducao(40000))
			import tarfile
			if tarfile.is_tarfile(MAC_KIT):
				path_libraries = os.path.join(pastaperfil)
				download_tools().extract(MAC_KIT,pastaperfil)
				download_tools().remove(MAC_KIT)
				sp_sc_auth = os.path.join(pastaperfil,"sopcast","sp-sc-auth")
				st = os.stat(sp_sc_auth)
				import stat
				os.chmod(sp_sc_auth, st.st_mode | stat.S_IEXEC)
				settings.setSetting('autoconfig',value='false')
		else:
			mensagemok(traducao(40000),traducao(600014))
			sys.exit(0)
				
	elif xbmc.getCondVisibility('System.Platform.Android') or settings.getSetting('force_android') == "true":

		print "Detected OS: Android"
		#Sopcast configuration
		print "Starting SopCast Configuration"

		#Moving sopclient to ext4 hack - tks steeve from xbmctorrent

		sopclient_builtin_location = os.path.join(addonpath,"resources","binaries","sopclient")

		#Hack to get current xbmc app id
		xbmcfolder=xbmc.translatePath(addonpath).split("/")
		print "XBMC folder",xbmcfolder

		i = 0
		found = False
		sopcast_installed = False
		
		for folder in xbmcfolder:
			if folder.count('.') >= 2 and folder != addon_id :
				found = True
				break
			else:
				i+=1


		if found == True:
			uid = os.getuid()
			print i
			app_id = xbmcfolder[i]
			xbmc_data_path = os.path.join("/data", "data", app_id)
			if os.path.exists(xbmc_data_path) and uid == os.stat(xbmc_data_path).st_uid:
				android_binary_dir = os.path.join(xbmc_data_path, "files", "plugin.video.p2p-streams")
				if not os.path.exists(android_binary_dir):
            				os.makedirs(android_binary_dir)
				android_binary_path = os.path.join(android_binary_dir, "sopclient")
		        	if not os.path.exists(android_binary_path) or os.path.getsize(android_binary_path) != os.path.getsize(sopclient_builtin_location):
					import shutil
					shutil.copy2(sopclient_builtin_location, android_binary_path)
				binary_path = android_binary_path
				st = os.stat(binary_path)
				import stat
				os.chmod(binary_path, st.st_mode | stat.S_IEXEC)
				settings.setSetting('android_sopclient',value=binary_path)
				opcao= xbmcgui.Dialog().yesno(traducao(40000), traducao(50011),traducao(50012))
				if not opcao:
					settings.setSetting('external_sopcast',value='1')
					settings.setSetting('force_android',value='true')
					sopcast_installed = True
					mensagemok(traducao(40000),traducao(50014))
				else:
					sopcast_apk = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/SopCast.apk.tar.gz"
					mensagemok(traducao(40000),traducao(50013))
					if xbmcvfs.exists(os.path.join("sdcard","Download")):
						pasta = os.path.join("sdcard","Download")
						sopfile = os.path.join("sdcard","Download",sopcast_apk.split("/")[-1])
					else:
						dialog = xbmcgui.Dialog()
						pasta = dialog.browse(int(0), traducao(40190), 'myprograms')
						sopfile = os.path.join(pasta,sopcast_apk.split("/")[-1])
					download_tools().Downloader(sopcast_apk,sopfile,traducao(40073),traducao(40000))
					if tarfile.is_tarfile(sopfile):
						download_tools().extract(sopfile,pasta)
						download_tools().remove(sopfile)
					mensagemok(traducao(40000),traducao(50015),pasta,traducao(50016))
					sopcast_installed = True
					settings.setSetting('external_sopcast',value='0')
					mensagemok(traducao(40000),traducao(50014))

		else:
			mensagemok(traducao(40000),traducao(50017))

		#acestream config for android

		if sopcast_installed == True:
			acestreamengine_apk = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/acestream-2.1.11.apk.tar.gz"
			mensagemok(traducao(40000),traducao(50018),traducao(50019),traducao(50020))
			if xbmcvfs.exists(os.path.join("sdcard","Download")):
				pasta = os.path.join("sdcard","Download")
				acefile = os.path.join("sdcard","Download",acestreamengine_apk.split("/")[-1])
			else:
				dialog = xbmcgui.Dialog()
				pasta = dialog.browse(int(0), traducao(40190), 'myprograms')
				acefile = os.path.join(pasta,acestreamengine_apk.split("/")[-1])
			download_tools().Downloader(acestreamengine_apk,acefile,traducao(40072),traducao(40000))
			if tarfile.is_tarfile(acefile):
				download_tools().extract(acefile,pasta)
				download_tools().remove(acefile)
			xbmc.sleep(2000)
			mensagemok(traducao(40000),traducao(50021),pasta,traducao(50016))
			mensagemok(traducao(40000),traducao(50022))
			mensagemok(traducao(40000),traducao(50023),traducao(50024),traducao(50025))
			settings.setSetting('autoconfig',value='false')	
				
				

def handle_wait(time_to_wait,title,text,segunda=''):
        ret = mensagemprogresso.create(' '+title)
        secs=0
        percent=0
        increment = int(100 / time_to_wait)
        cancelled = False
        while secs < time_to_wait:
                secs = secs + 1
                percent = increment*secs
                secs_left = str((time_to_wait - secs))
                if segunda=='': remaining_display = traducao(40188) + str(secs_left) + traducao(40189)
                else: remaining_display=segunda
                mensagemprogresso.update(percent,text,remaining_display)
                xbmc.sleep(1000)
                if (mensagemprogresso.iscanceled()):
                        cancelled = True
                        break
        if cancelled == True:
                return False
        else:
                mensagemprogresso.close()
                return False

def handle_wait_socket(time_to_wait,title,text,segunda=''):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        ret = mensagemprogresso.create(' '+title)
        secs=0
        percent=0
        increment = int(100 / time_to_wait)
        cancelled = False
        while secs < time_to_wait:
                try:
                        result = sock.connect(('127.0.0.1',8902))
                        connected = True
                        print "Connected to port 8902, server is working"
                        break
                        sock.close()
                except:
                        print "Still hasn't connected"
                secs = secs + 1
                percent = increment*secs
                secs_left = str((time_to_wait - secs))
                if segunda=='': remaining_display = traducao(40187) + " " + str(percent) + " %"
                else: remaining_display=segunda
                mensagemprogresso.update(percent,text,remaining_display)
                xbmc.sleep(1000)
                if (mensagemprogresso.iscanceled()):
                        cancelled = True
                        break
        if cancelled == True:
                return False
        elif connected == True:
                print "connected true na condicao"
                mensagemprogresso.close()
                return True
        else:
                mensagemprogresso.close()
                return False
		
def irparaid(yeee):
	if yeee=='ace':
		keyb = xbmc.Keyboard('', traducao(40033))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				acestreams(traducao(40035),'',str(channel_id))
	elif yeee=='sop_id':
		channel_id = xbmcgui.Dialog().numeric(0, traducao(40033))
		sopstreams(traducao(40035),'',str(channel_id))
	elif yeee=='sop_url':
		keyb = xbmc.Keyboard('sop://', traducao(40034) + ' sop://')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				sopstreams(traducao(40036),'',str(channel_id))

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
        
#PODES USAR ESTA FUNCAO PARA VER O OUTPUT DE UM CMD
#def rp():
#	command = [os.path.join(pastaperfil,'sopcast','qemu-i386'),os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),"sop://124.232.150.188:3912/9761","1234","9001"]
#	for line in run_command(command):
#		print(line)  
  

def sopstreams(name,iconimage,sop):
   #Function to decide if addon or external player is used for sopcast streams
	if not iconimage: iconimage = os.path.join(addonpath,'resources','art','sopcast_logo.jpg')
	if "sop://" not in sop: sop = "sop://broker.sopcast.com:3912/" + sop
	else: pass
	print "Starting Player Sop URL: " + str(sop)
	if not xbmc.getCondVisibility('system.platform.windows'):
	    if xbmc.getCondVisibility('System.Platform.Android') or settings.getSetting('force_android') == "true":
	    	if  settings.getSetting('external_sopcast') == "0":
			versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
			if versionNumber >= 13:
				xbmc.executebuiltin('XBMC.StartAndroidActivity("org.sopcast.android","android.intent.action.VIEW","",'+sop+')')
			else:	mensagemok(traducao(40000),traducao(40196),traducao(40197))    
		else: sopstreams_builtin(name,iconimage,sop)
            else: sopstreams_builtin(name,iconimage,sop)
        else:
            cmd = ['sc','sdshow','sopcastp2p']
            import subprocess
            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
            config = True  
            for line in proc.stdout:
                    if " 1060:" in line.rstrip():
                        config = False
                        print "Configuration is not DONE!"
            if config == False: mensagemok(traducao(40000),traducao(40180),traducao(40181), traducao(40182))
            else:
                import _winreg
                aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                #Dirty hack to break sopcast h264 codec so double sound can be avoided
                try:
                	aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
                	name, value, type = _winreg.EnumValue(aKey, 0)
                	codec_file = os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx')
                	_winreg.CloseKey(aKey)
                	if xbmcvfs.exists(codec_file): xbmcvfs.rename(codec_file,os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx.old'))
                except:pass
                aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                aKey = _winreg.OpenKey(aReg, r'SYSTEM\CurrentControlSet\Services\sopcastp2p\Parameters', 3, _winreg.KEY_WRITE)
                _winreg.SetValueEx(aKey,"AppParameters",0, _winreg.REG_SZ, sop)  
                _winreg.CloseKey(aKey)
                cmd = ['sc','start','sopcastp2p']
                import subprocess
                proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                servicecreator = False
                for line in proc.stdout:
                        print "linha " + line.rstrip()
                res = handle_wait_socket(int(settings.getSetting('socket_time')),traducao(40000),traducao(40183))
                print "rest",res
                if res == True:
                        print "Server created, waiting 5 seconds for confirmation"
                        try: sock.close()
                        except: pass
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        handle_wait(int(settings.getSetting('stream_time')),traducao(40000),traducao(40184),segunda='')
                        try:
                                result = sock.connect(('127.0.0.1',8902))
                                connected = True
                        except: connected = False
                        if connected == True:
                                playlist = xbmc.PlayList(1)
                                playlist.clear()
                                listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
                                listitem.setLabel(name)
                                listitem.setInfo("Video", {"Title":name})
                                listitem.setProperty('mimetype', 'video/x-msvideo')
                                listitem.setProperty('IsPlayable', 'true')
				windows_sop_url = "http://127.0.0.1:8902/tv.asf"
				listitem.setPath(path=windows_sop_url)
                                playlist.add(windows_sop_url, listitem)
				xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
                                player = SopWindowsPlayer()
				if int(sys.argv[1]) < 0:
                                	player.play(playlist)
                                while player._playbackLock:
                                    xbmc.sleep(5000)
                        else: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40040), 1,addonpath+"/icon.png"))
                print "Player reached the end"
                cmd = ['sc','stop','sopcastp2p']
                import subprocess
                proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                servicecreator = False
                for line in proc.stdout:
                        print "linha " + line.rstrip()
			 #dirty hack to break sopcast.exe player codec - renaming the file again
                import _winreg
                aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                try:
                	aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
                	name, value, type = _winreg.EnumValue(aKey, 0)
                	codec_file = os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx.old')
                	_winreg.CloseKey(aKey)
                	if xbmcvfs.exists(codec_file): xbmcvfs.rename(codec_file,os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx'))
                except:pass


def sopstreams_builtin(name,iconimage,sop):
    try:
        os.system("killall -9 "+SPSC_BINARY)
        global spsc
        if xbmc.getCondVisibility('System.Platform.Linux') and settings.getSetting('force_android') == "false":

        	if os.uname()[4] == "armv6l" or os.uname()[4] == "armv7l" or settings.getSetting('openelecx86_64') == "true":
        		if settings.getSetting('sop_debug_mode') == "false":
        			cmd = [os.path.join(pastaperfil,'sopcast','qemu-i386'),os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT)]
			else: 
				cmd = [os.path.join(pastaperfil,'sopcast','qemu-i386'),os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT),">",SPSC_LOG]

		elif settings.getSetting('openeleci386') == "true":
        		if settings.getSetting('sop_debug_mode') == "false":
        			cmd = [os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT)]
			else: 
				cmd = [os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT),">",SPSC_LOG]

		else: 
			if settings.getSetting('sop_debug_mode') == "false":
				cmd = [os.path.join(pastaperfil,'sopcast','ld-linux.so.2'),'--library-path',os.path.join(pastaperfil,'sopcast','lib'),os.path.join(pastaperfil,'sopcast',SPSC_BINARY), sop, str(LOCAL_PORT), str(VIDEO_PORT)]
			else:
				cmd = [os.path.join(pastaperfil,'sopcast','ld-linux.so.2'),'--library-path',os.path.join(pastaperfil,'sopcast','lib'),os.path.join(pastaperfil,'sopcast',SPSC_BINARY), sop, str(LOCAL_PORT), str(VIDEO_PORT),">",SPSC_LOG]
        elif xbmc.getCondVisibility('System.Platform.OSX'):
        	if settings.getSetting('sop_debug_mode') == "false":
			cmd = [os.path.join(pastaperfil,'sopcast','sp-sc-auth'), str(sop), str(LOCAL_PORT), str(VIDEO_PORT)]
		else:
			cmd = [os.path.join(pastaperfil,'sopcast','sp-sc-auth'), str(sop), str(LOCAL_PORT), str(VIDEO_PORT),">",str(SPSC_LOG)]	
        elif xbmc.getCondVisibility('System.Platform.Android') or settings.getSetting('force_android') == "true":
        	if settings.getSetting('sop_debug_mode') == "false":
			cmd = [str(settings.getSetting('android_sopclient')), str(sop), str(LOCAL_PORT), str(VIDEO_PORT)]
		else:
			cmd = [str(settings.getSetting('android_sopclient')), str(sop), str(LOCAL_PORT), str(VIDEO_PORT),">",str(SPSC_LOG)]	
	print sop
        print cmd
        spsc = subprocess.Popen(cmd, shell=False, bufsize=BUFER_SIZE,stdin=None, stdout=None, stderr=None)
        listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        listitem.setLabel(name)
        listitem.setInfo('video', {'Title': name})
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
	listitem.setPath(path=url)
        xbmc.sleep(int(settings.getSetting('wait_time')))
        res=False
        counter=50
        ret = mensagemprogresso.create(traducao(40000),"SopCast",traducao(40039))
        mensagemprogresso.update(0)
        while counter > 0 and spsc.pid:
	    if mensagemprogresso.iscanceled():
	    	mensagemprogress.close()
           	try: os.kill(self.spsc_pid,9)
            	except: pass
                break
            xbmc.sleep(400)
            counter -= 1
	    mensagemprogresso.update(int((1-(counter/50.0))*100))
            try:
                urllib2.urlopen(url)
                counter=0
                res=sop_sleep(200 , spsc.pid)
                break
            except:pass
                    
        if res:
	    mensagemprogresso.update(100)
	    xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
            player = streamplayer(xbmc.PLAYER_CORE_AUTO , spsc_pid=spsc.pid , listitem=listitem)
            if int(sys.argv[1]) < 0:
            	player.play(url, listitem)
            while player._playbackLock:
                xbmc.sleep(500)
        else: xbmc.executebuiltin("Notification(%s,%s,%i)" % (traducao(40000), traducao(40040), 1))
    except: pass
    try: os.kill(self.spsc_pid,9)
    except: pass
    xbmc.sleep(100)
    try:os.system("killall -9 "+SPSC_BINARY)
    except:pass
    xbmc.sleep(100)
    try:spsc.kill()
    except:pass
    xbmc.sleep(100)
    try:spsc.wait()
    except:pass
    xbmc.sleep(100)           
    try: os.kill(spsc.pid,9)
    except: pass
    mensagemprogresso.close()
    print "Player chegou mesmo ao fim"


def sop_sleep(time , spsc_pid):
    counter=0
    increment=200
    path="/proc/%s" % str(spsc_pid)
    try:
      while counter < time and spsc_pid>0 and not xbmc.abortRequested:
        counter += increment
        xbmc.sleep(increment)
    except: return True
        
    if counter < time: return False
    else: return True

def checker():
	import socket
	sock = socket.socket(socket.AF_INET, socket.int(VIDEO_PORT))
	result = sock.connect_ex(('127.0.0.1',9000))
	if result == 0:
   		return True
	else:
   		return False

class SopWindowsPlayer(xbmc.Player):
      def __init__(self):
            self._playbackLock = True
            print "Criou o player"
            
      def onPlayBackStarted(self):
            print "Comecou o player"
                              
      def onPlayBackStopped(self):
            print "Parou o player"
            self._playbackLock = False
            import subprocess
            cmd = ['sc','stop','sopcastp2p']
            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
            for line in proc.stdout:
                    print line.rstrip()


      def onPlayBackEnded(self):              
            self.onPlayBackStopped()
            print 'Chegou ao fim. Playback terminou.'



class streamplayer(xbmc.Player):
    def __init__( self , *args, **kwargs):
        self.spsc_pid=kwargs.get('spsc_pid')
        self.listitem=kwargs.get('listitem')
        self._playbackLock = True

    def onPlayBackStarted(self):
        mensagemprogresso.close()
        if xbmc.Player(xbmc.PLAYER_CORE_AUTO).getPlayingFile() != "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/":
            try: os.kill(self.spsc_pid,9)
            except: pass
        else: pass

    def onPlayBackEnded(self):
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
        xbmc.sleep(300)
        if os.path.exists("/proc/"+str(self.spsc_pid)) and xbmc.getCondVisibility("Window.IsActive(epg.xml)") and settings.getSetting('safe_stop')=="true":
            if not xbmc.Player(xbmc.PLAYER_CORE_AUTO).isPlaying():
                player = streamplayer(xbmc.PLAYER_CORE_AUTO , spsc_pid=self.spsc_pid , listitem=self.listitem)
                player.play(url, self.listitem)     


    def onPlayBackStopped(self):
        self._playbackLock = False
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
        xbmc.sleep(300)
        if os.path.exists("/proc/"+str(self.spsc_pid)) and xbmc.getCondVisibility("Window.IsActive(epg.xml)") and settings.getSetting('safe_stop')=="true":
            if not xbmc.Player(xbmc.PLAYER_CORE_AUTO).isPlaying(): 
                player = streamplayer(xbmc.PLAYER_CORE_AUTO , spsc_pid=self.spsc_pid , listitem=self.listitem)
                player.play(url, self.listitem)
        else:
            try: os.kill(self.spsc_pid,9)
            except: pass


################################################## PASTAS ################################################################

def addLink(name,url,iconimage,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path")):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', fan_art)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path")):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
      contextmen = []
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', fan_art)
      if mode == 1 or mode == 2:
	    try:
		 dirs, files = xbmcvfs.listdir(os.path.join(pastaperfil,"Favourites"))
		 if url.replace(":","").replace("/","") + ".txt" in files: contextmen.append((traducao(40146), 'XBMC.RunPlugin(%s?mode=48&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], urllib.quote_plus(url),name,iconimage)))
		 else: contextmen.append((traducao(40143), 'XBMC.RunPlugin(%s?mode=46&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], urllib.quote_plus(url),name,iconimage)))
            except: pass
      elif mode == 28:
	    try:
		ficheiro = os.path.join(pastaperfil,"Lists",name.replace("[B][COLOR orange]","").replace("[/B][/COLOR]","") + ".txt")
		if xbmcvfs.exists(ficheiro):
			contextmen.append((traducao(40149), 'XBMC.RunPlugin(%s?mode=49&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], urllib.quote_plus(url),ficheiro,iconimage)))
			#contextmen.append((traducao(), 'XBMC.RunPlugin(%s?mode=49&url=%s)' % (sys.argv[0], urllib.quote_plus(ficheiro))))
	    except: pass
      #print contextmen
      liz.addContextMenuItems(contextmen,replaceItems=False)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)           

######################################################## OUTRAS FUNCOES ###############################################

def savefile(filename, contents):
    try:
        destination = os.path.join(pastaperfil, filename)
        fh = open(destination, 'wb')
        fh.write(contents)  
        fh.close()
    except: print "Nao gravou o marcador de: %s" % filename

def openfile(filename):
    try:
        destination = os.path.join(pastaperfil, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu o marcador de: %s" % filename
        return None

def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def mechanize_browser(url):
	import mechanize
	br = mechanize.Browser()
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	r = br.open(url)
	html = r.read()
	html_source= br.response().read()
	return html_source


def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                  params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]                 
      return param

def clean(text):
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&#039;':'','&#39;':"'",'&#227;':'ã','&170;':'ª','&#233;':'é','&#231;':'ç','&#243;':'ó','&#226;':'â','&ntilde;':'ñ','&#225;':'á','&#237;':'í','&#245;':'õ','&#201;':'É','&#250;':'ú','&amp;':'&','&#193;':'Á','&#195;':'Ã','&#202;':'Ê','&#199;':'Ç','&#211;':'Ó','&#213;':'Õ','&#212;':'Ó','&#218;':'Ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)

class download_tools():
	def Downloader(self,url,dest,description,heading):
		dp = xbmcgui.DialogProgress()
		dp.create(heading,description,'')
		dp.update(0)
		urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: self._pbhook(nb,bs,fs,dp))
		
	def _pbhook(self,numblocks, blocksize, filesize,dp=None):
		try:
			percent = int((int(numblocks)*int(blocksize)*100)/int(filesize))
			dp.update(percent)
		except:
			percent = 100
			dp.update(percent)
		if dp.iscanceled(): 
			dp.close()
	
	def extract(self,file_tar,destination):
		import tarfile
		dp = xbmcgui.DialogProgress()
		dp.create(traducao(40000),traducao(40044))
		tar = tarfile.open(file_tar)
		tar.extractall(destination)
		dp.update(100)
		tar.close()
		dp.close()
		
	def remove(self,file_):
		dp = xbmcgui.DialogProgress()
		dp.create(traducao(40000),traducao(40045))
		os.remove(file_)
		dp.update(100)
		dp.close()


params=get_params()
url=None
name=None
mode=None
iconimage=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try:
    regexs=params["regexs"]
except:
    pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

if mode==None or url==None or len(url)<1:
      print "Versao Instalada: v" + versao
      if settings.getSetting('autoconfig') == "true": autoconf()
      menu_principal()

#plugin.video.p2p-streams/?url=idstream&mode=1or2&name=nameofstream
elif mode==1: acestreams(name,iconimage,url)
elif mode==2: sopstreams(name,iconimage,url)
elif mode==3: irparaid('sop_id')
elif mode==4: irparaid('ace')
elif mode==5: irparaid('sop_url')
elif mode==6: lista_sop()
elif mode==7: sopserver()
elif mode==8: wiziwig_cats()
elif mode==9: wiziwig_events(url)
elif mode==10: wiziwig_servers(url)
elif mode==11: torrenttv()
elif mode==12: torrenttv_play(name,url)
elif mode==13: sopcast_ucoz()
elif mode==14: sopcast_ucoz_play(name,url)
elif mode==15: advanced_menu()
elif mode==16: import_advancedxml()
elif mode==17: recoverbackup_advancedxml()
elif mode==18: backup_advancedxml()
elif mode==19: delete_advancedxml()
elif mode==20: remove_lock()
elif mode==21: import_playerxml()
elif mode==22: backup_playercorexml()
elif mode==23: delete_playercorexml()
elif mode==24: onetorrent()
elif mode==25: onetorrent_play(name,url)
elif mode==26: site_parsers_menu()
elif mode==27: xml_lists_menu()
elif mode==28: livestreams.get_groups(url)
elif mode==29: livestreams.get_channels(name,url)
elif mode==30: livestreams.getChannelItems(name,url,"fanart")
elif mode==31: livestreams.getRegexParsed(regexs, url)
elif mode==32: item = xbmcgui.ListItem(path=url); xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
elif mode==33: xbmc.executebuiltin(url.replace(';',''))
elif mode==34: livestreams.addlista()
elif mode==35: arenavision_menu()
elif mode==36: arenavision_streams(name,url)
elif mode==37: arenavision_schedule(url)
elif mode==38: livefootballws_events()
elif mode==39: livefootballws_streams(url)
elif mode==40: rojadirecta_events()
elif mode==41: livefootballvideo_events()
elif mode==42: livefootballvideo_sources(url)
elif mode==43: rojadirecta_resolver(name,url)
elif mode==44: torrent_tv_sports()
elif mode==45: pass
elif mode==46: add_to_addon_favourites(name,url)
elif mode==47: addon_favourites()
elif mode==48: remove_addon_favourites(url)
elif mode==49: remove_list(name)
elif mode==50: livefootballaol_menu()
elif mode==51: set_engine_setting(url)
elif mode==52: load_local_torrent()
elif mode==53: arenavision_mundial()
elif mode==54: arenavision_mundial_agenda("http://mundial.arenavision.in/p/agenda-tvschedule-tv.html")


    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
