# -*- coding: utf-8 -*-

""" Plexus (c) 2015 enen92
   
   This file contains the main menu and the addon directory tree.
   All the necessary modules are present in ~/resources/plexus directory
    
"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time,subprocess,xbmcvfs,socket
from resources.plexus.plexusutils.pluginxbmc import *
from resources.plexus import acestream as ace
from resources.plexus import sopcast as sop
from resources.plexus.autoconf import *
from resources.plexus.plexusutils.directoryhandle import addLink,addDir
from resources.plexus.advancedfunctions import *
from resources.plexus.resolver import go_to_id
from resources.plexus.acecore import stop_aceengine
from resources.plexus.history import *
from resources.plexus.mystreams import *
                                                                                                                                                                                                                                                                  
def main_menu():
      addDir('[B]'+translate(30001)+'[/B]',MainURL,10,os.path.join(addonpath,art,'mystreams.png'),2,True)
      if settings.getSetting('addon_history') == "true":
      	addDir('[B]'+translate(30002)+'[/B]',MainURL,8,os.path.join(addonpath,art,'history.png'),2,True)
      	if "confluence" in xbmc.getSkinDir(): addLink('','','plexus')

      addDir('[B][COLOR maroon]'+translate(30003)+'[/COLOR][/B]' + translate(30005),MainURL,4,os.path.join(addonpath,art,'acestream-menu-item.png'),1,False)
      addDir('[B][COLOR maroon]'+translate(30003)+'[/COLOR][/B]' + translate(30006),MainURL,6,os.path.join(addonpath,art,'acestream-menu-item.png'),1,False)

      addDir('[B][COLOR maroon]'+translate(30004)+'[/COLOR][/B]' + translate(30007),MainURL,3,os.path.join(addonpath,art,'sopcast-menu-item.png'),1,False)
      addDir('[B][COLOR maroon]'+translate(30004)+'[/COLOR][/B]' + translate(30008),MainURL,5,os.path.join(addonpath,art,'sopcast-menu-item.png'),1,False)

      #if "confluence" in xbmc.getSkinDir(): addLink('','','plexus')
      #addDir('[B][COLOR maroon]' + translate(40057) + '[/COLOR][/B]',MainURL,300,os.path.join(addonpath,art,'settings.png'),2,True)       
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
      main_menu()
elif mode==1: ace.acestreams(name,iconimage,url)
elif mode==2: sop.sopstreams(name,iconimage,url)
elif mode==3: go_to_id('sop_id')
elif mode==4: go_to_id('ace')
elif mode==5: go_to_id('sop_url')
elif mode==6: ace.load_local_torrent()
elif mode==7: stop_aceengine()
elif mode==8: list_history()
elif mode==9: remove_history()
elif mode==10: my_streams_menu()
elif mode==11: add_stream()
elif mode==12: add_stream(name,url,iconimage)
elif mode==13: remove_stream(name,url)
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
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
