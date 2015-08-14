# -*- coding: utf-8 -*-

""" Plexus  (c)  2015 enen92

    This file contains the functions for xbmc addon directory handle

    Functions:

    addLink(name,url,iconimage,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path")) -> Addlink function used in the 'whole' addon
    addDir(name,url,mode,iconimage,total,pasta,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path"),parser=None,parserfunction=None) -> AddDir function used in the whole addon
    addDir_livestreams_common(name,url,mode,iconimage,folder,fannart=None) -> AddDir function used only by the livestreams module of the addon
    addLink_livestreams(url,name,iconimage,fanart,description,genre,date,showcontext,playlist,regexs,total) -> AddLink function used only by the livestreams module of the addon


"""

import xbmc,xbmcgui,xbmcvfs,xbmcplugin,os,urllib,sys
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
        try:
            dirs, files = xbmcvfs.listdir(os.path.join(pastaperfil,"Favourites"))
            if url.replace(":","").replace("/","") + ".txt" in files: contextmen.append((translate(40146), 'XBMC.RunPlugin(%s?mode=202&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], urllib.quote_plus(url),name,iconimage)))
            else: contextmen.append((translate(40143), 'XBMC.RunPlugin(%s?mode=201&url=%s&name=%s&iconimage=%s)' % (sysargv, urllib.quote_plus(url),name,iconimage)))
        except: pass
    elif mode == 101:
        try:
            ficheiro = os.path.join(pastaperfil,"Lists",name.replace("[B][COLOR orange]","").replace("[/B][/COLOR]","") + ".txt")
            if xbmcvfs.exists(ficheiro):
                contextmen.append((translate(40149), 'XBMC.RunPlugin(%s?mode=108&url=%s&name=%s&iconimage=%s)' % (sysargv, urllib.quote_plus(url),ficheiro,iconimage)))
        except: pass
    elif mode == 401 and parser and not parserfunction:
        contextmen.append((translate(400009), 'XBMC.RunPlugin(%s?mode=403&url=%s&name=%s&iconimage=%s)' % (sysargv, urllib.quote_plus(url),name,iconimage)))
        contextmen.append((translate(400010), 'XBMC.RunPlugin(%s?mode=407&url=%s&name=%s&iconimage=%s&parser=%s)' % (sysargv, urllib.quote_plus(url),name,iconimage,parser)))
    liz.addContextMenuItems(contextmen,replaceItems=False)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
