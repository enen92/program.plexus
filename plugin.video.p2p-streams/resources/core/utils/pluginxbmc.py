# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains the common variables used by the addon
    
    Functions:
    
    traducao(texto) -> Translate a string
   	
"""
    
import xbmc,xbmcplugin,xbmcgui,xbmcaddon

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

#to be removed
def traducao(texto):
      return settings.getLocalizedString(texto).encode('utf-8')
      
def translate(text):
	return traducao(text)

