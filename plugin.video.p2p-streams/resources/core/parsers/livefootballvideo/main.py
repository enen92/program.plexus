# -*- coding: utf-8 -*-

""" P2P-STREAMS XBMC ADDON

http://1torrent.tv module parser

"""
import sys,os
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.pluginxbmc import *
from utils.directoryhandle import *
from utils.timeutils import translate_months

base_url = 'http://livefootballvideo.com/streaming'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: livefootballvideo_events()
	elif parserfunction == 'sources': livefootballvideo_sources(url)

def livefootballvideo_events():
	try:
		source = abrir_url(base_url)
	except: source ="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile('"([^"]+)" alt="[^"]*"/>.*?.*?>([^<]+)</a>\s*</div>\s*<div class="date_time column"><span class="starttime time" rel="[^"]*">([^<]+)</span>.*?<span class="startdate date" rel="[^"]*">([^"]+).*?<span>([^<]+)</span></div>.*?team away column"><span>([^&<]+).*?href="([^"]+)">([^<]+)<').findall(source)
		for icon,comp,timetmp,datetmp,home,away,url,live in match:
			mes_dia = re.compile(', (.+?) (.+?)<').findall(datetmp)
			for mes,dia in mes_dia:
				dia = re.findall('\d+', dia)
				month = translate_months(mes)
				hora_minuto = re.compile('(\d+):(\d+)').findall(timetmp)
				try:
                                        import datetime
					from utils import pytzimp
					d = pytzimp.timezone(str(pytzimp.timezone('Atlantic/Azores'))).localize(datetime.datetime(2014, int(month), int(dia[0]), hour=int(hora_minuto[0][0]), minute=int(hora_minuto[0][1])))
					timezona= settings.getSetting('timezone_new')
                                        lisboa=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                                        convertido=d.astimezone(lisboa)
                                        fmt = "%d/%m %H:%M"
                                        time=convertido.strftime(fmt)
					
					if "Online" in live: time = '[B][COLOR green](Online)[/B][/COLOR]'
					else: time = '[B][COLOR orange]' + time + '[/B][/COLOR]'
					addDir(time + ' - [B]('+comp+')[/B] ' + home + ' vs ' + away,url,401,os.path.join(addonpath,'resources','art','football.png'),len(match),True,parser='livefootballvideo',parserfunction='sources')
				except: addDir('[B][COLOR orange]' + timetmp + ' ' + datetmp + '[/B][/COLOR] - [B]('+comp+')[/B] ' + home + ' vs ' + away,url,401,os.path.join(addonpath,'resources','art','football.png'),len(match),True,parser='livefootballvideo',parserfunction='sources')


def livefootballvideo_sources(url):
	try:
		source = abrir_url(url)
	except: source = ""; mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile("alt='sopcast'/></a></td><td align='left'>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td><a href='(.+?)'").findall(source)
		for name,language,quality,link in match:
			addDir("[B][COLOR orange][SopCast] [/COLOR][/B]" + name + ' (' + language + ') ('+quality+')',link,2,os.path.join(addonpath,'resources','art','sopcast_logo.jpg'),len(match),False)
		match2 = re.compile("alt='acestream.+?'/></a></td><td align='left'>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td><a href='(.+?)'").findall(source)
		for name,language,quality,link in match2:
			if "acestream://" in link:
				addDir("[B][COLOR orange][Acestream] [/COLOR][/B]" + name + ' (' + language + ') ('+quality+')',link,1,os.path.join(addonpath,'resources','art','acelogofull.jpg'),len(match),False)
		if len(match) != 0 or len(match2) !=0:
			xbmc.executebuiltin("Container.SetViewMode(51)")
		else:
			sys.exit(0)
