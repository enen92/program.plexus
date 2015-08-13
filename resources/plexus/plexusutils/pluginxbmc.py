# -*- coding: utf-8 -*-

""" Plexus  (c)  2015 enen92

    This file contains the common variables used by the addon
    
    Functions:
    
    translate(text) -> Translate a string based on the addon language strings
   	
"""
    
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import os

linkwiki="http://bit.ly/1r5uGQT"
addon_id = 'program.plexus'
art = os.path.join('resources','art')
settings = xbmcaddon.Addon(id=addon_id)
addonpath = settings.getAddonInfo('path').decode('utf-8')
versao = settings.getAddonInfo('version')
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
MainURL = 'https://code.google.com/p/p2p-strm/'
addon_icon    = settings.getAddonInfo('icon')
mystrm_folder = os.path.join(pastaperfil,'streams')
      
def translate(text):
      return settings.getLocalizedString(text).encode('utf-8')

