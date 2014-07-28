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

base_url = 'http://api.torrent-tv.ru/t/BgF2xM3fd1KWxgEVO21eprkQPkZi55b0LosbJU8oeZVikr1wPAmjkV%2ByixKZYNGt'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: torrent_tv_sports()
    
def torrent_tv_sports():
	try:
		source = abrir_url(base_url)
	except: source = "";mensagemok(traducao(40000),traducao(40128))
	if source:
		match= re.compile("#EXTINF:-1,(.+?)\(Спорт\)\n(.*)").findall(source)
		for titulo,acestream in match:
			clean = re.compile("\((.+?)\)").findall(titulo)
			for categorie in clean:
				titulo = titulo.replace("(" + categorie +")","")
			addDir(titulo,acestream,1,os.path.join(addonpath,'resources','art','torrenttvru.png'),len(match),False)
		xbmc.executebuiltin("Container.SetViewMode(51)")
