# -*- coding: utf-8 -*-

""" p2p-streams
    2014 enen92 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time,subprocess,xbmcvfs,socket
from resources.core.utils.pluginxbmc import *
from resources.core import acestream as ace
from resources.core import sopcast as sop
from resources.core.autoconf import *
from resources.core.utils.directoryhandle import addLink,addDir
from resources.core.favourites import *
from resources.core.advancedfunctions import *
from resources.core.livestreams import *
from resources.core.parsers import parsers
                                                                                                                                                                                                                                                                  
def menu_principal():
      addDir(traducao(40114),MainURL,53,addonpath + art + 'web-parsers-menu.png',2,True)
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
      sop.break_sopcast()

      
#Esta é para ficar aqui!		
def go_to_id(p2p_type):
	if p2p_type=='ace':
		keyb = xbmc.Keyboard('', traducao(40033))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				ace.acestreams(traducao(40035),'',str(channel_id))
	elif p2p_type=='sop_id':
		channel_id = xbmcgui.Dialog().numeric(0, traducao(40033))
		sop.sopstreams(traducao(40035),'',str(channel_id))
	elif p2p_type=='sop_url':
		keyb = xbmc.Keyboard('sop://', traducao(40034) + ' sop://')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				sop.sopstreams(traducao(40036),'',str(channel_id))


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

params=get_params()
url=None
name=None
mode=None
iconimage=None
parser=None
parserfunction=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: regexs=params["regexs"]
except:pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: parser=urllib.unquote_plus(params["parser"])
except: pass
try:parserfunction=params["parserfunction"]
except: pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Parser: "+str(parser)
print "Parserfunction: "+str(parserfunction)

if mode==None or url==None or len(url)<1:
      print "Versao Instalada: v" + versao
      if settings.getSetting('autoconfig') == "true": autoconf()
      menu_principal()

elif mode==1:
	ace.acestreams(name,iconimage,url)
elif mode==2: 
	sop.sopstreams(name,iconimage,url)
elif mode==3:
	go_to_id('sop_id')
elif mode==4:
	go_to_id('ace')
elif mode==5:
	go_to_id('sop_url')
#
elif mode==6: lista_sop()
elif mode==7: sopserver()
elif mode==15: advanced_menu()
elif mode==16: import_advancedxml()
elif mode==17: recoverbackup_advancedxml()
elif mode==18: backup_advancedxml()
elif mode==19: delete_advancedxml()
elif mode==20: remove_lock()
elif mode==21: import_playerxml()
elif mode==22: backup_playercorexml()
elif mode==23: delete_playercorexml()
elif mode==27: xml_lists_menu()
elif mode==28: get_groups(url)
elif mode==29: get_channels(name,url)
elif mode==30: getChannelItems(name,url,"fanart")
elif mode==31: getRegexParsed(regexs, url)
elif mode==32: item = xbmcgui.ListItem(path=url); xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
elif mode==33: xbmc.executebuiltin(url.replace(';',''))
elif mode==34: addlista()
elif mode==46: add_to_addon_favourites(name,url)
elif mode==47: addon_favourites()
elif mode==48: remove_addon_favourites(url)
elif mode==49: remove_list(name)
elif mode==51: set_engine_setting(url)
elif mode==52: ace.load_local_torrent()
#parser stuff
elif mode==53: parsers.addon_parsers_menu()
elif mode==54:
	if not parser: print "não é um parser"
	else: 
		print "é o parser",parser
		#from resources.core.parsers.livefootballws import main as pa
		#pa.module_tree(name,url,iconimage,mode,parser,parserfunction)
		package = 'resources.core.parsers.' + parser
		name = "main"
		parser_module = getattr(__import__(package, fromlist=[name]), name)
		parser_module.module_tree(name,url,iconimage,mode,parser,parserfunction)
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
