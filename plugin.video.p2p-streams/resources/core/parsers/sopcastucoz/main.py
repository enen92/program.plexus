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
import acestream as ace
import sopcast as sop

base_url = 'http://livefootballvideo.com/streaming'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: sopcast_ucoz()
	elif parserfunction == 'play': sopcast_ucoz_play(name,url)
    
def sopcast_ucoz():
    conteudo=clean(abrir_url('http://sopcast.ucoz.com'))
    listagem=re.compile('<div class="eTitle" style="text-align:left;"><a href="(.+?)">(.+?)</a>').findall(conteudo)
    for urllist,titulo in listagem:
    	try:
    		match = re.compile('\((.*?)\.(.*?)\.(.*?)\. (.*?):(.*?) UTC\) (.*)').findall(titulo)
    		if match:
    			for dia,mes,ano,hora,minuto,evento in match:
                                import datetime
                                from utils import pytzimp
                                d = pytzimp.timezone(str(pytzimp.timezone('Europe/London'))).localize(datetime.datetime(int(ano), int(mes), int(dia), hour=int(hora), minute=int(minuto)))
                                timezona= settings.getSetting('timezone_new')
                                lisboa=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                                convertido=d.astimezone(lisboa)
                                fmt = "%y-%m-%d %H:%M"
                                time=convertido.strftime(fmt)
    				
    				addDir('[B][COLOR orange]' + time + '[/B][/COLOR]-' + evento,urllist,54,'',len(listagem),False,parser="sopcastucoz",parserfunction="play")
    		else:
    			addDir(titulo,urllist,54,'',len(listagem),False,parser="sopcastucoz",parserfunction="play")
    	except:
    			addDir(titulo,urllist,54,'',len(listagem),False,parser="sopcastucoz",parserfunction="play")

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
    			if re.search('acestream',nomeescolha,re.IGNORECASE) or re.search('TorrentStream',nomeescolha,re.IGNORECASE): ace.acestreams(nomeescolha,'',linkescolha)
    			elif re.search('sopcast',nomeescolha,re.IGNORECASE):
                		if xbmc.getCondVisibility('system.platform.windows'):sopserver()
				else:sop.sopstreams(nomeescolha,'',linkescolha)
		        else: mensagemok(traducao(40000),traducao(40024))  
    else:
    	mensagemok(traducao(40000),traducao(40008))
