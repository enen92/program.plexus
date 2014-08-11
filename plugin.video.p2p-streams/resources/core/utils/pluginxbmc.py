# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains the common variables used by the addon
    
    Functions:
    
    translate(text) -> Translate a string based on the addon language strings
   	
"""
    
import xbmc,xbmcplugin,xbmcgui,xbmcaddon

linkwiki="http://bit.ly/1r5uGQT"
addon_id = 'plugin.video.p2p-streams'
art = '/resources/art/'
settings = xbmcaddon.Addon(id=addon_id)
addonpath = settings.getAddonInfo('path').decode('utf-8')
versao = settings.getAddonInfo('version')
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
iconpequeno=addonpath + art + 'iconpq.jpg'
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
MainURL = 'https://code.google.com/p/p2p-strm/'
addon_icon    = settings.getAddonInfo('icon')
      
def translate(text):
      return settings.getLocalizedString(text).encode('utf-8')

