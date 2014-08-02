# -*- coding: utf-8 -*-
""" p2p-streams (c) 2014 enen92 fightnight

This file handles all the website parsers addon engine

Functions:

	addon_parsers_menu() -> Lists all installed parsers
	add_new_parser() -> Function to add a new parser
	remove_parser(iconimage) -> Remove a parser
	sync_parser() -> Syncs the parser code with remote repository
	runscript() -> Executes a remote python script 

"""


import os,sys,xbmc,xbmcgui,xbmcvfs,re,datetime,time
base_dir =  os.path.dirname(os.path.realpath(__file__))
core_dir =  os.path.dirname(os.path.realpath(__file__)).replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.directoryhandle import addDir,addLink
from utils.pluginxbmc import *
from utils.iofile import *

parser_folder = os.path.join(pastaperfil,'parsers')
parser_core_folder = os.path.join(addonpath,'resources','core','parsers')

def addon_parsers_menu():
	dirs,files = xbmcvfs.listdir(base_dir)
	if not dirs:
		dirsuserdata,files = xbmcvfs.listdir(parser_folder)
		for fich in files:
			dictionary_module = eval(readfile(os.path.join(parser_folder,fich)))
			if "url" in dictionary_module.keys():
				add_new_parser(dictionary_module["url"])
	dirs,files = xbmcvfs.listdir(base_dir)
	parser_dict = {}
	for module in dirs:
		module_dir = os.path.join(base_dir,module)
		module_cfg = os.path.join(module_dir,"module.cfg")
		module_icon = os.path.join(module_dir,"icon.png")
		module_fanart = os.path.join(module_dir,"fanart.jpg")
		if xbmcvfs.exists(module_icon): thumbnail = module_icon
		else: thumbnail = 'os.path.join(module_dir,"")'
		if xbmcvfs.exists(module_fanart): fanart = module_fanart
		else: fanart = ''
		if xbmcvfs.exists(module_cfg):
			cfg = readfile(module_cfg)
			try: 
				cfg = eval(cfg)
				module_name = cfg['name']
			except: module_name = None
			if module_name:
				parser_dict[module_name] = [module,thumbnail,fanart]
	total_parsers = len(parser_dict.keys())
	if settings.getSetting('parser_sync') == "true":
		try:t1 = datetime.datetime.strptime(settings.getSetting("parsers_last_sync"), "%Y-%m-%d %H:%M:%S.%f")
		except:t1 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(settings.getSetting("parsers_last_sync"), "%Y-%m-%d %H:%M:%S.%f")))
		t2 = datetime.datetime.now()
		hoursList = [10, 15, 20, 24]
		interval = int(settings.getSetting("parser_sync_cron"))
		update = abs(t2 - t1) > datetime.timedelta(hours=hoursList[interval])
		if update:
			sync_parser()
			settings.setSetting('parsers_last_sync',value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
		
	for key in sorted(parser_dict.keys()):
		addDir(key,MainURL,401,parser_dict[key][1],total_parsers,True,parser=parser_dict[key][0])
	addDir(traducao(400011),MainURL,402,addonpath + art + 'plus-menu.png',2,False)

def add_new_parser(url):
	if not url:
		opcao= xbmcgui.Dialog().yesno(traducao(40000),traducao(400012),"","",traducao(40124),traducao(40125))
		if opcao:
			dialog = xbmcgui.Dialog()
			parser_tball = dialog.browse(int(1), traducao(400013), 'myprograms','.tar.gz')
			if '.tar.gz' in parser_tball:
				parser_name = parser_tball.split('/')
				if not parser_name: parser_name = parser_tball.split('\\')
				parser_name=parser_name[-1].replace('.tar.gz','')	
				print("the list is: " + parser_tball,parser_name)
				future_parser_tball = os.path.join(parser_folder,parser_name+'.tar.gz')
				xbmcvfs.copy(parser_tball,future_parser_tball)
				import tarfile
				if tarfile.is_tarfile(future_parser_tball):
					download_tools().extract(future_parser_tball,parser_core_folder)
					xbmc.sleep(500)
					download_tools().remove(future_parser_tball)
				module_file = os.path.join(parser_folder,parser_name + '.txt')
				text = str({})
				save(module_file,str(text))
				xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(400014),1,addonpath+"/icon.png"))
				xbmc.executebuiltin("Container.Refresh")
			else:
				mensagemok(traducao(40000),traducao(400015))
				sys.exit(0) 			
		else:
			keyb = xbmc.Keyboard("", traducao(400016))
			keyb.doModal()
			if (keyb.isConfirmed()):
				search = keyb.getText()
				if search=='': sys.exit(0)
				if '.tar.gz' not in search: mensagemok(traducao(40000),traducao(400017)); sys.exit(0)
				else: 
					md5checksum = search.replace('.tar.gz','.md5')
					modulename = search.split('/')[-1].replace('.tar.gz','').replace('?raw=true','')
					md5_up=url_isup(md5checksum)
					module_up=url_isup(search)
					if not xbmcvfs.exists(parser_folder): xbmcvfs.mkdir(parser_folder)
					text = {}
					if module_up: text['url'] = search
					if md5_up: text['md5'] = get_page_source(md5checksum)
					if text:
						try:
							module_file = os.path.join(parser_folder,modulename + '.txt')
							module_tar_location = os.path.join(parser_core_folder,modulename+'tar.gz')
							save(module_file,str(text))
							download_tools().Downloader(search,module_tar_location,traducao(400018),traducao(40000))
							import tarfile            
							if tarfile.is_tarfile(module_tar_location):
								download_tools().extract(module_tar_location,parser_core_folder)
								xbmc.sleep(500)
								download_tools().remove(module_tar_location)
							xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000),traducao(400014),1,addonpath+"/icon.png"))
							xbmc.executebuiltin("Container.Refresh")
						except: mensagemok(traducao(40000),traducao(400024))
					else:
						mensagemok(traducao(40000),traducao(400015))
						sys.exit(0)
	else:
		md5checksum = url.replace('.tar.gz','.md5')
		modulename = url.split('/')[-1].replace('.tar.gz','').replace('?raw=true','')
		md5_up=url_isup(md5checksum)
		module_up=url_isup(url)
		if not xbmcvfs.exists(parser_folder): xbmcvfs.mkdir(parser_folder)
		text = {}
		if module_up: text['url'] = url
		if md5_up: text['md5'] = get_page_source(md5checksum)
		if text:
			module_file = os.path.join(parser_folder,modulename + '.txt')
			module_tar_location = os.path.join(parser_core_folder,modulename+'.tar.gz')
			save(module_file,str(text))
			download_tools().Downloader(url,module_tar_location,traducao(400018),traducao(40000))
			import tarfile 
			if tarfile.is_tarfile(module_tar_location):
				download_tools().extract(module_tar_location,parser_core_folder)
				xbmc.sleep(500)
				download_tools().remove(module_tar_location)
				print(str(modulename) + " : Module installed sucessfully")
				return
	
def remove_parser(iconimage):
	parser_plugin = iconimage.split('/')
	if len(parser_plugin) == 1: 
		parser_plugin=iconimage.split("\\")
	parser_plugin = parser_plugin[-2]
	xbmcvfs.delete(os.path.join(parser_folder,parser_plugin +'.txt'))
	module_folder = os.path.join(parser_core_folder,parser_plugin)
	dirs, files = xbmcvfs.listdir(module_folder)
	for file in files:
			xbmcvfs.delete(os.path.join(module_folder,file))
	try:
		xbmcvfs.rmdir(module_folder)
	except:
		import shutil
		shutil.rmtree(module_folder)
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000), traducao(400019),1,addonpath+"/icon.png"))
	xbmc.executebuiltin("Container.Refresh")
	
def sync_parser():
	dirs, files = xbmcvfs.listdir(parser_folder)
	if files: 
		mensagemprogresso.create(traducao(40000),"Syncing parsers...","")
		mensagemprogresso.update(0,"Syncing parsers...","")
		xbmc.sleep(1000)
		number_of_files = len(files)
		i = 0
	for file in files:
		i += 1
		error = False
		mensagemprogresso.update(int(float(i)/number_of_files*100),traducao(400020),file.replace('.txt',''),traducao(400021))
		module_file = os.path.join(parser_folder,file)
		text = eval(readfile(module_file))
		if not text: pass
		else:
			if 'url' and 'md5' in text.keys():
				installed_md5 = text['md5']
				module_url = text['url']
				module_md5 = text['url'].replace('.tar.gz','.md5')
				try: current_md5 = get_page_source(module_md5)
				except: current_md5 = installed_md5; error = True
				if current_md5 != installed_md5:
					print('Module requires update ' + str(file.replace('.txt','')) + ' ' + str(installed_md5) + ' != ' + str(current_md5))
					mensagemprogresso.update(int(float(i)/number_of_files*100),traducao(400020),file.replace('.txt',''),traducao(400025))
					add_new_parser(module_url)
					mensagemprogresso.create(traducao(40000),traducao(400020),file.replace('.txt',''),traducao(400022))
				else:
					print('Module is up to date: ' + str(file.replace('.txt','')))
					if error == False: message = traducao(400023)
					else: message = traducao(400024)
					mensagemprogresso.update(int(float(i)/number_of_files*100),traducao(400020),file.replace('.txt',''),message)
		xbmc.sleep(1000)
	try:
		mensagemprogresso.update(100,"","")
		mensagemprogresso.close()
	except: pass
	settings.setSetting('parsers_last_sync',value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
	return
	
def sync_single_parser(parser):
	parser_file = os.path.join(parser_folder,parser+'.txt')
	if xbmcvfs.exists(parser_file):
		string = eval(readfile(parser_file))
		if string:
			add_new_parser(string['url'])
			xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000),traducao(400026),1,addonpath+"/icon.png"))	
	
def runscript():
	keyb = xbmc.Keyboard("", traducao(400016))
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		if search=='': sys.exit(0)
		else:
			try:
				download_tools().Downloader(search,os.path.join(pastaperfil,'rscript.py'),traducao(400027),traducao(40000))
				xbmc.executebuiltin('XBMC.RunScript('+os.path.join(pastaperfil,'rscript.py')+')')
				xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (traducao(40000),traducao(400028),1,addonpath+"/icon.png"))
			except: mensagemok(traducao(40000),traducao(40128))
			
			
	
	

