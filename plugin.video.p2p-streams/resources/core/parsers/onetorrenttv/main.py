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

base_url = 'http://1torrent.tv'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: onetorrent_main()
	elif parserfunction == 'play_torrent': onetorrent_resolver(name,url)
  
def onetorrent_main():
    html_source = clean(abrir_url(base_url+"/channels.php"))
    categorias=re.compile('<div class="tab_caption.+?" id="tcap_(.+?)".+?>(.+?)</div>').findall(html_source)
    print categorias
    for catid,catname in categorias:
        canais=re.compile('<div class=".+?" id="tcon_'+catid+'"(.+?)</div></div></div></div>').findall(html_source)
        if len(canais)!=0: addLink('[B][COLOR blue]'+catname+'[/B][/COLOR]','','')
        for lista in canais:
            individual=re.compile('<img src="(.+?)">.+?<a href="(.+?)">(.+?)</a>').findall(lista)
            for img,link,nomech in individual:
                addDir(nomech,base_url+link,401,base_url + img,2,False,parser="1torrent.tv",parserfunction='play_torrent')
                pass
        addLink('','','')

def onetorrent_resolver(name,url):
	try:
		conteudo=abrir_url(url)
	except: conteudo = ''
	if conteudo:
		try:torrent=re.compile('this.loadTorrent.+?"(.+?)",').findall(conteudo)[0]
		except:torrent=re.compile('this.loadPlayer.+?"(.+?)",').findall(conteudo)[0]
		logo=re.compile('<img id="cur_logo" src="(.+?)">').findall(conteudo)[0]
		ace.acestreams(name,base_url + logo,torrent)
