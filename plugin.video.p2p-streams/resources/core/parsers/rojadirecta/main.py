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
import acestream as ace
import sopcast as sop

base_url = "http://www.rojadirecta.me/"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: rojadirecta_events()
	elif parserfunction == 'resolve_and_play': rojadirecta_resolver(name,url)
    
def rojadirecta_events():
	try:
		source = abrir_url(base_url)
	except: source = "";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.findall('<span class="(\d+)">.*?<div class="menutitle".*?<span class="t">([^<]+)</span>(.*?)</div>',source,re.DOTALL)
		for id,time,eventtmp in match:
			try:
                                import datetime
                                from utils import pytzimp
                                d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2014, 6, 7, hour=int(time.split(':')[0]), minute=int(time.split(':')[-1])))
                                timezona= settings.getSetting('timezone_new')
                                lisboa=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                                convertido=d.astimezone(lisboa)
                                fmt = "%H:%M"
                                time=convertido.strftime(fmt)
				
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
                        					addLink("[B][COLOR orange]"+time+ " - " + sport + " - " + event + "[/B][/COLOR]",'',os.path.join(current_dir,'icon.png'))
                       						already = True
							if "ArenaVision" in canal: thumbnail = os.path.join(current_dir,'media','arenavisionlogo.png')
							else: thumbnail = os.path.join(current_dir,'icon.png')
                   					addDir("[B]["+tipo.replace("<","").replace(">","")+"][/B]-"+canal.replace("<","").replace(">","")+" - ("+language.replace("<","").replace(">","")+") - ("+qualidade.replace("<","").replace(">","")+" Kbs)",urltmp.replace("goto/",""),401,thumbnail,43,False,parser='rojadirecta',parserfunction='resolve_and_play')
                   			p2pdirect = re.compile('<td>P2P</td><td></td><td></td><td>(.+?)</td><td></td><td>.+?href="(.+?)"').findall(streamdata)
                   			for tipo,link in p2pdirect:
                   				if tipo == "SopCast" and "sop://" in link:
                   					addDir("[B][SopCast][/B]- (no info)",link,401,os.path.join(current_dir,'icon.png'),43,False,parser='rojadirecta',parserfunction='resolve_and_play')

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
		if matchsop: sop.sopstreams(name,os.path.join(current_dir,'icon.png'),"sop://" + matchsop[0])
		else:
			match = re.compile('this.loadPlayer\("(.+?)"').findall(source)
			if match: ace.acestreams(name,os.path.join(current_dir,'icon.png'),match[0])
			else: 
				if matchredirect:
					rojadirecta_resolver(name,matchredirect[0])
				else:
					mensagemok(traducao(40000),traducao(40022))
	elif "sop://" in url: so.sopstreams(name,os.path.join(current_dir,'icon.png'),url)
	elif "acestream://" in url: ace.acestreams(name,os.path.join(current_dir,'icon.png'),url)
	else: mensagemok(traducao(40000),traducao(40022))		
