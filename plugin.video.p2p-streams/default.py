# -*- coding: utf-8 -*-

""" p2p-streams (c) 2014 enen92 fightnight
   
   This file contains the main menu and the addon directory tree.
   All the necessary modules are present in ~/resources/core directory
   Parsers are in ~/resources/core/parsers
    
"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time,subprocess,xbmcvfs,socket
from resources.core.peertopeerutils.pluginxbmc import *
from resources.core import acestream as ace
from resources.core import sopcast as sop
from resources.core.autoconf import *
from resources.core.peertopeerutils.directoryhandle import addLink,addDir
from resources.core.favourites import *
from resources.core.advancedfunctions import *
from resources.core.livestreams import *
from resources.core.parsers import parsers
from resources.core.resolver import go_to_id
from resources.core.acecore import stop_aceengine
from resources.core.history import *
                                                                                                                                                                                                                                                                  
def main_menu():
      addDir(translate(40114),MainURL,400,addonpath + art + 'web-parsers-menu.png',2,True)
      addDir(translate(40115),MainURL,100,addonpath + art + 'xml_lists.png',2,True)
      addDir(translate(40144),MainURL,200,addonpath + art + 'Favorites-menu.png',2,True)
      if settings.getSetting('addon_history') == "true":
      	addDir(translate(70036),MainURL,8,addonpath + art + 'history.png',2,True)
      if "confluence" in xbmc.getSkinDir(): addLink('','','p2p')
      if xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.linux') or xbmc.getCondVisibility('System.Platform.OSX') or xbmc.getCondVisibility('System.Platform.Android'):
          addDir('[COLOR orange]AceStream: [/COLOR]' + translate(40004),MainURL,4,addonpath + art + 'acestream-menu-item.png',1,False)
          addDir('[COLOR orange]AceStream: [/COLOR]' + translate(600029),MainURL,6,addonpath + art + 'acestream-menu-item.png',1,False)
      if xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.linux') or xbmc.getCondVisibility('System.Platform.OSX') or xbmc.getCondVisibility('System.Platform.Android'):
          addDir('[COLOR orange]SopCast: [/COLOR]' + translate(40005),MainURL,3,addonpath + art + 'sopcast-menu-item.png',1,False)
          addDir('[COLOR orange]SopCast: [/COLOR]' + translate(40006),MainURL,5,addonpath + art + 'sopcast-menu-item.png',1,False)
      if xbmc.getCondVisibility('System.Platform.IOS') or xbmc.getCondVisibility('System.Platform.ATV2'):
          addLink(translate(40056),'',addonpath + art + 'processwarning.png')
      if "confluence" in xbmc.getSkinDir(): addLink('','','p2p')
      addDir('[B]' + translate(40057) + '[/B]',MainURL,300,addonpath + art + 'settings_menu.png',2,True)       
      xbmc.executebuiltin("Container.SetViewMode(50)")
      #break_sopcast is a function used in windows to intentionally break the sopcast.exe setup by renaming one of its codec files. It's ran here to rename the file again in case it failed when played before
      sop.break_sopcast()
      
      
""" 
Addon tree is below  
"""

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


print("Mode: "+str(mode))
print("URL: "+str(url))
print("Name: "+str(name))
print("Iconimage: "+str(iconimage))
print("Parser: "+str(parser))
print("Parserfunction: "+str(parserfunction))

#from 1-99 functions related to the addon menu functions 
if mode==None:
      print("Installed version: v" + versao)
      if settings.getSetting('autoconfig') == "true": first_conf()
      else:
          if settings.getSetting('last_version_check') != versao:
              try:check_for_updates()
              except: pass
      if settings.getSetting('enter_channel_list') == "false":
      	main_menu()
      else:
      	parsers.addon_parsers_menu()
elif mode==1: ace.acestreams(name,iconimage,url)
elif mode==2: sop.sopstreams(name,iconimage,url)
elif mode==3: go_to_id('sop_id')
elif mode==4: go_to_id('ace')
elif mode==5: go_to_id('sop_url')
elif mode==6: ace.load_local_torrent()
elif mode==7: stop_aceengine()
elif mode==8: list_history()
elif mode==9: remove_history()
#from 100-199 functions related to xml lists
elif mode==100: xml_lists_menu()
elif mode==101: list_type(url)
elif mode==102: get_channels(name,url)
elif mode==103: getChannelItems(name,url,"fanart")
elif mode==104: getRegexParsed(regexs, url)
elif mode==105: item = xbmcgui.ListItem(path=url); xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
elif mode==106: xbmc.executebuiltin(url.replace(';',''))
elif mode==107: addlista()
elif mode==108: remove_list(name)
elif mode==109: get_groups(url)
#from 200-299 Favourites
elif mode==200: addon_favourites()
elif mode==201: add_to_addon_favourites(name,url,iconimage)
elif mode==202: remove_addon_favourites(url)
elif mode==203: manual_add_to_favourites()
#from 300-399 Advanced functions
elif mode==300: advanced_menu()
elif mode==301: import_advancedxml()
elif mode==302: recoverbackup_advancedxml()
elif mode==303: backup_advancedxml()
elif mode==304: delete_advancedxml()
elif mode==305: set_engine_setting(url)
elif mode==306: remove_lock()
elif mode==307: clear_cache(url)
elif mode==308: set_linux_engine_setting(url)
elif mode==309: set_acestream_engine_cache_folder(url)
elif mode==310: shutdown_hooks()
elif mode==311: set_android_port()
elif mode==312: set_android_cache_aloc()
#from 400-499 Site parsers
elif mode==400: parsers.addon_parsers_menu()
elif mode==401:
	parsers.parser_check()
	package = 'resources.core.parsers.' + parser
	tree = "main"
	parser_module = getattr(__import__(package, fromlist=[tree]), tree)
	parser_module.module_tree(name,url,iconimage,mode,parser,parserfunction)
elif mode==402: parsers.add_new_parser(url='')
elif mode==403: parsers.remove_parser(iconimage)
elif mode==404: parsers.runscript()
elif mode==405: parsers.add_new_parser(url)
elif mode==406: parsers.sync_parser()
elif mode==407: parsers.sync_single_parser(parser)
elif mode==408: parsers.clear_parser_trace()
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
