# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains the the code for favourites used in the addon
    
    Functions:
    
	addon_favourites() -> Main menu. It parses the userdata/Favourites folder for items and lists them
	manual_add_to_favourites() -> Add a favourite to list manually
	add_to_addon_favourites(name,url,iconimage) -> Add an item to the addon favourites. Receives the name of the channel, the url and the iconimage
	remove_addon_favourites(url) -> Remove from addon favourites
    

"""
    
import xbmc,xbmcgui,xbmcplugin,xbmcvfs,sys,os
from peertopeerutils.pluginxbmc import *
from peertopeerutils.iofile import *
from peertopeerutils.directoryhandle import addDir
from random import randint

def addon_favourites():
	if os.path.exists(os.path.join(pastaperfil,"Favourites")):
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
	addDir('[B]' + translate(70022) + '[/B]',MainURL,203,addonpath + art + 'plus-menu.png',2,False)	
	xbmc.executebuiltin("Container.SetViewMode(51)")

def manual_add_to_favourites():
	keyb = xbmc.Keyboard("", translate(70023))
	keyb.doModal()
	if (keyb.isConfirmed()):
		favourite_url = keyb.getText()
		if ('acestream://' in favourite_url) or ('sop://' in favourite_url) or ('.acelive' in favourite_url) or ('.torrent' in favourite_url):
			keyb = xbmc.Keyboard("", translate(70024))
			keyb.doModal()
			if (keyb.isConfirmed()):
				favourite_name = keyb.getText()
				if favourite_name: pass
				else: favourite_name = 'p2p-streams ' + str(randint(1,100))
				add_to_addon_favourites(favourite_name,favourite_url,'')
		else:
			mensagemok(translate(40000),translate(40128))
			
def add_to_addon_favourites(name,url,iconimage):
	name = name.replace("[b]","").replace("[/b]","").replace("[color orange]","").replace("[/color]","").replace("[B]","").replace("[/B]","")
	if "runplugin" in url:
		match = re.compile("url=(.+?)&mode=(.+?)&").findall(url.replace(";",""))
		for url,mode in match:
			favourite_text = str(name) + " (" + str(url) + ")|" + str(mode) + "|" + str(url) + '|' + str(iconimage)
			favouritetxt = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
			if not xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")): xbmcvfs.mkdir(os.path.join(pastaperfil,"Favourites"))
			save(favouritetxt, favourite_text)
			xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(40148), 1,addonpath+"/icon.png"))
	else:
		if "sop://" in url:
			tipo = "sopcast"
			if not iconimage: iconimage = os.path.join(addonpath,'resources','art','sopcast_logo.jpg')
		elif "acestream://" in url:
			tipo = "acestream"
			if not iconimage: iconimage = os.path.join(addonpath,'resources','art','acelogofull.jpg')
		elif ".torrent" in url:
			tipo = "acestream"
			if not iconimage: iconimage = os.path.join(addonpath,'resources','art','acelogofull.jpg')
		elif ".acelive" in url:
			tipo = "acestream"
			if not iconimage: iconimage = os.path.join(addonpath,'resources','art','acelogofull.jpg')		
		else:
			if len(url) < 30: tipo = "sopcast"
			else: tipo = "acestream"
		if tipo == "sopcast":
			favourite_text = str(name) + " (" + str(url) + ")|" + str(2) + "|" + str(url) + '|' + str(iconimage)
		elif tipo == "acestream":
			favourite_text = str(name) + " (" + str(url) + ")|" + str(1) + "|" + str(url) + '|' + str(iconimage) 
		favouritetxt = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
		if not xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")): xbmcvfs.mkdir(os.path.join(pastaperfil,"Favourites"))
		save(favouritetxt, favourite_text)
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(40148), 1,addonpath+"/icon.png"))
		xbmc.executebuiltin("Container.Refresh")
			
def remove_addon_favourites(url):
	if "runplugin" in url:
		match = re.compile("url=(.+?)&mode").findall(url.replace(";",""))
		if match: ficheiro = os.path.join(pastaperfil,"Favourites",match[0].replace("/","").replace(":","") + ".txt")
	else:
		ficheiro = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
	xbmcvfs.delete(ficheiro)
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(40147), 1,addonpath+"/icon.png"))
	xbmc.executebuiltin("Container.Refresh")

