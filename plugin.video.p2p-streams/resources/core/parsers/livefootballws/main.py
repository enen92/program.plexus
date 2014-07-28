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

base_url = "http://www.livefootball.ws"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: livefootballws_events()
	elif parserfunction == 'streams': livefootballws_streams(url)

def livefootballws_events():
	try:
		source = mechanize_browser(base_url)
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
                                                import datetime
                                                from utils import pytzimp
                                                timezona= settings.getSetting('timezone_new')
                                                d = pytzimp.timezone(str(pytzimp.timezone('Europe/Moscow'))).localize(datetime.datetime(2014, 6, int(match[0][0]), hour=int(match[0][2]), minute=int(match[0][3])))
                                                lisboa=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                                                convertido=d.astimezone(lisboa)
                                                fmt = "%d %H:%M"
                                                time=convertido.strftime(fmt)

                                                addDir("[B][COLOR orange]("+traducao(600012)+time+")[/COLOR][/B] "+teams[0],url[0],39,os.path.join(current_dir,'icon.png'),number_of_items,True,parser="livefootballws",parserfunction="streams")
					except:
						if '<span style="color: #000000;">' not in data_item:
							addDir("[B][COLOR green]("+data_item+")[/COLOR][/B] "+teams[0],url[0],401,os.path.join(current_dir,'icon.png'),number_of_items,True,parser="livefootballws",parserfunction="streams")
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
								addDir("[B][COLOR orange][SopCast] [/COLOR]"+channel+"[/B] ("+stream_quality[0]+' Kbs)',match[-1],2,os.path.join(current_dir,'icon.png'),number_of_items,False)
							except: pass
						elif "acestream://" in match[-1]:
							link = re.compile("acestream://(.*)").findall(match[-1])
							try:
								addDir("[B][COLOR orange][Acestream] [/COLOR]"+channel+"[/B] ("+stream_quality[0]+' Kbs)',link[0],1,os.path.join(current_dir,'icon.png'),number_of_items,False)
							except: pass
						elif "torrentstream" in match[-1]:
							link = re.compile("http://torrentstream.org/stream/test.php\?id=(.*)").findall(match[-1])
							try:
								addDir("[B][COLOR orange][Acestream] [/COLOR]"+channel+"[/B] ("+stream_quality[0]+' Kbs)',link[0],1,os.path.join(current_dir,'icon.png'),number_of_items,False)
							except: pass
						else:pass
		else:
			mensagemok(traducao(40000),traducao(40022))
			sys.exit(0)
