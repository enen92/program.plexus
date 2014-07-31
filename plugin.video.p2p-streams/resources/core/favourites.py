# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains the the code for favourites used in the addon
    
    Functions:
    
	addon_favourites() -> Main menu. It parses the userdata/Favourites folder for items and lists them
	add_to_addon_favourites(name,url,iconimage) -> Add an item to the addon favourites. Receives the name of the channel, the url and the iconimage
	remove_addon_favourites(url) -> Remove from addon favourites
    

"""
    
import xbmc,xbmcgui,xbmcplugin,xbmcvfs,sys,os
from utils.pluginxbmc import *
from utils.iofile import *
from utils.directoryhandle import addDir

def addon_favourites():
	if xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")):
		dirs, files = xbmcvfs.listdir(os.path.join(pastaperfil,"Favourites"))
		if files:
			for file in files:
				string = readfile(os.path.join(pastaperfil,"Favourites",file))
				match = string.split("|")
				try: iconimage = match[3]
				except:
					if 'acestream' in file: iconimage = addonpath + art + 'acelogofull.png'
					elif 'sop' in file: iconimage = addonpath + art + 'sopcast_logo.jpg'
					else: iconimage = ''
				addDir("[B][COLOR orange]" + match[0] + "[/B][/COLOR]",match[2],int(match[1]),iconimage,1,False)
			xbmc.executebuiltin("Container.SetViewMode(51)")
		else:
			mensagemok(traducao(40000),traducao(40145));sys.exit(0)
			
def add_to_addon_favourites(name,url,iconimage):
	name = name.replace("[b]","").replace("[/b]","").replace("[color orange]","").replace("[/color]","").replace("[B]","").replace("[/B]","")
	if "runplugin" in url:
		match = re.compile("url=(.+?)&mode=(.+?)&").findall(url.replace(";",""))
		for url,mode in match:
			favourite_text = name + " (" + url + ")|" + str(mode) + "|" + url + '|' + iconimage
			favouritetxt = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
			if not xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")): xbmcvfs.mkdir(os.path.join(pastaperfil,"Favourites"))
			save(favouritetxt, favourite_text)
			xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40148), 1,addonpath+"/icon.png"))
	else:
		if "sop://" in url:
			tipo = "sopcast"
		elif "acestream://" in url:
			tipo = "acestream"
		else:
			if len(url) < 30: tipo = "sopcast"
			else: tipo = "acestream"
		if tipo == "sopcast":
			favourite_text = name + " (" + url + ")|" + str(2) + "|" + url + '|' + iconimage
		elif tipo == "acestream":
			favourite_text = name + " (" + url + ")|" + str(1) + "|" + url + '|' + iconimage 
		favouritetxt = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
		if not xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")): xbmcvfs.mkdir(os.path.join(pastaperfil,"Favourites"))
		save(favouritetxt, favourite_text)
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40148), 1,addonpath+"/icon.png"))
		xbmc.executebuiltin("Container.Refresh")
			
def remove_addon_favourites(url):
	if "runplugin" in url:
		match = re.compile("url=(.+?)&mode").findall(url.replace(";",""))
		if match: ficheiro = os.path.join(pastaperfil,"Favourites",match[0].replace("/","").replace(":","") + ".txt")
	else:
		ficheiro = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
	xbmcvfs.delete(ficheiro)
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40147), 1,addonpath+"/icon.png"))
	xbmc.executebuiltin("Container.Refresh")    

