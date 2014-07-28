# -*- coding: utf-8 -*-

""" p2p-streams
    2014 enen92 fightnight"""
    
import xbmc,xbmcgui,xbmcplugin,xbmcvfs,sys,os
from utils.pluginxbmc import *
from utils.iofile import *

def addon_favourites():
	if xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")):
		dirs, files = xbmcvfs.listdir(os.path.join(pastaperfil,"Favourites"))
		if files:
			for file in files:
				f = open(os.path.join(pastaperfil,"Favourites",file), "r")
				string = f.read()
				match = string.split("|")
				addDir("[B][COLOR orange]" + match[0] + "[/B][/COLOR]",match[2],int(match[1]),'',1,False)
			xbmc.executebuiltin("Container.SetViewMode(51)")
		else:
			mensagemok(traducao(40000),traducao(40145));sys.exit(0)
			
def add_to_addon_favourites(name,url):
	name = name.replace("[b]","").replace("[/b]","").replace("[color orange]","").replace("[/color]","")
	if "runplugin" in url:
		print "Existe Runplugin"
		match = re.compile("url=(.+?)&mode=(.+?)&").findall(url.replace(";",""))
		for url,mode in match:
			favourite_text = name + " (" + url + ")|" + str(mode) + "|" + url
			favouritetxt = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
			if not xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")): xbmcvfs.mkdir(os.path.join(pastaperfil,"Favourites"))
			print favouritetxt
			savefile(favouritetxt, favourite_text)
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
			favourite_text = name + " (" + url + ")|" + str(2) + "|" + url  
		elif tipo == "acestream":
			favourite_text = name + " (" + url + ")|" + str(1) + "|" + url  
		favouritetxt = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
		if not xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")): xbmcvfs.mkdir(os.path.join(pastaperfil,"Favourites"))
		savefile(favouritetxt, favourite_text)
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40148), 1,addonpath+"/icon.png"))
		xbmc.executebuiltin("Container.Refresh")
			
def remove_addon_favourites(url):
	print url
	if "runplugin" in url:
		match = re.compile("url=(.+?)&mode").findall(url.replace(";",""))
		if match: ficheiro = os.path.join(pastaperfil,"Favourites",match[0].replace("/","").replace(":","") + ".txt")
	else:
		ficheiro = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
	xbmcvfs.delete(ficheiro)
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(40147), 1,addonpath+"/icon.png"))
	xbmc.executebuiltin("Container.Refresh")    

