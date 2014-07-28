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

base_url = "http://api.torrent-tv.ru/t/BgF2xM3fd1KWxgEVO21eprkQPkZi55b0LosbJU8oeZVikr1wPAmjkV%2ByixKZYNGt"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: torrenttv()
	elif parserfunction == 'channels': torrenttv_play(name,url)
    
def torrenttv():
	dict_torrent = {}
	html_source = abrir_url(base_url)
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
		addDir(categories,str(dict_torrent),54,os.path.join(current_dir,"icon.png"),2,True,parser="torrenttvruall",parserfunction="channels")
		
def torrenttv_play(name,url):
	dict_torrent=eval(url)
	for channel in dict_torrent[name]:
		try: addDir(channel[0],channel[1],1,os.path.join(current_dir,"icon.png"),2,False)
		except:pass
		
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
	elif string == "Казахстан": return "Kazakstan"
 	else: return string
