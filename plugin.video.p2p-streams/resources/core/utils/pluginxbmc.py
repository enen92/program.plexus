# -*- coding: utf-8 -*-

""" p2p-streams
    2014 enen92 fightnight"""
    
import xbmc,xbmcplugin,xbmcgui,xbmcaddon

versao = '0.3.6'
addon_id = 'plugin.video.p2p-streams'
art = '/resources/art/'
settings = xbmcaddon.Addon(id=addon_id)
addonpath = settings.getAddonInfo('path').decode('utf-8')
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
iconpequeno=addonpath + art + 'iconpq.jpg'
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
MainURL = 'https://code.google.com/p/p2p-strm/'

def traducao(texto):
      return settings.getLocalizedString(texto).encode('utf-8')

