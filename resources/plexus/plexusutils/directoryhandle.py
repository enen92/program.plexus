# -*- coding: utf-8 -*-

""" Plexus  (c)  2015 enen92

    This file contains the functions for xbmc addon directory handle

    Functions:

    addLink(name,url,iconimage,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path")) -> Addlink function used in the 'whole' addon
    addDir(name,url,mode,iconimage,total,pasta,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path"),parser=None,parserfunction=None) -> AddDir function used in the whole addon

"""

import xbmc
import xbmcgui
import xbmcvfs
import xbmcplugin
import os
import urllib
import sys
import hashlib
from pluginxbmc import *

"""

Common addDir functions for main addon

"""

def addLink(name,url,iconimage,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path")):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', fan_art)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path"),parser=None,parserfunction=None):
    if "plugin://" in sys.argv[0]: u = sys.argv[0]; sysargv = sys.argv[0]
    else: u = 'plugin://plugin.video.p2p-streams/'; sysargv = 'plugin://plugin.video.p2p-streams/'
    u += "?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    try: u += "&parser="+urllib.quote_plus(parser)
    except: pass
    try: u += "&parserfunction="+urllib.quote_plus(parserfunction)
    except: pass
    contextmen = []
    liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty('fanart_image', fan_art)
    if mode == 1 or mode == 2:
        fic = hashlib.md5(name + '|' + url).hexdigest() + '.txt'
        if os.path.exists(os.path.join(mystrm_folder,fic)):
            contextmen.append((translate(30025), 'XBMC.RunPlugin(%s?mode=13&url=%s&name=%s&iconimage=%s)' % (sysargv, urllib.quote_plus(url),name,iconimage)))
        else:
            contextmen.append((translate(30026), 'XBMC.RunPlugin(%s?mode=12&url=%s&name=%s&iconimage=%s)' % (sysargv,urllib.quote_plus(url),name,iconimage)))
    liz.addContextMenuItems(contextmen,replaceItems=False)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
