# -*- coding: utf-8 -*-

""" P2P-STREAMS XBMC ADDON

Arenavision.in module parser

"""
import sys,os
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.pluginxbmc import *
from utils.directoryhandle import *
import acestream as ace
import sopcast as sop

base_url = "http://go.arenavision.in/"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: arenavision_menu()
	elif parserfunction == "arenavision_streams": arenavision_streams(name,url)
	elif parserfunction == "arenavision_schedule": arenavision_schedule(url)

def arenavision_menu():
	try:
		source = abrir_url(base_url)
	except: source="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile("<li><a href='(.+?)'>(.+?)</a></li>").findall(source)
		for link,name in match:
			if "Agenda" in name:
				addDir("[B][COLOR orange]Agenda/Schedule[/COLOR][/B]",link,54,os.path.join(current_dir,"icon.png"),1,True,parser="arenavision",parserfunction="arenavision_schedule")
			if "AV" in name:
				addDir(name,link,54,os.path.join(current_dir,"icon.png"),1,False,parser="arenavision",parserfunction="arenavision_streams")
			else: pass


def arenavision_streams(name,url):
	try:
		source = abrir_url(url)
	except: source="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.compile('sop://(.+?)"').findall(source)
		if match: sop.sopstreams(name,os.path.join(current_dir,"icon.png"),"sop://" + match[0])
		else:
			match = re.compile('this.loadPlayer\("(.+?)"').findall(source)
			if match: ace.acestreams(name,os.path.join(current_dir,"icon.png"),match[0])
			else: mensagemok(traducao(40000),traducao(40022))

def arenavision_schedule(url):
	try:
		source = abrir_url(url)
	except: source="";mensagemok(traducao(40000),traducao(40128))
	if source:
		match = re.findall("<br />(.*?)<div class='post-footer'>", source, re.DOTALL)
		for event in match:
			eventmatch = re.compile('(.+?)/(.+?)/(.+?) (.+?):(.+?) CET (.+?)<').findall(event)
			for dia,mes,year,hour,minute,evento in eventmatch:
				try:
					import datetime
					from utils import pytzimp
					d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2000 + int(year), int(mes), int(dia), hour=int(hour), minute=int(minute)))
					timezona= settings.getSetting('timezone_new')
                                        lisboa=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                                        convertido=d.astimezone(lisboa)
                                        fmt = "%d-%m-%y %H:%M"
                                        time=convertido.strftime(fmt)
					addLink('[B][COLOR orange]' + time + '[/B][/COLOR] ' + evento,'',os.path.join(current_dir,"icon.png"))
				except:
					addLink(evento.replace("&nbsp;",""),'',os.path.join(current_dir,"icon.png"))
	xbmc.executebuiltin("Container.SetViewMode(51)")
