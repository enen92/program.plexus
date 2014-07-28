""" p2p-streams
    2014 enen92 fightnight"""


import os,sys,xbmc,xbmcgui,xbmcvfs,re
base_dir =  os.path.dirname(os.path.realpath(__file__))
core_dir =  os.path.dirname(os.path.realpath(__file__)).replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.directoryhandle import addDir,addLink
from utils.pluginxbmc import *
from utils.iofile import *

def addon_parsers_menu():
	dirs,files = xbmcvfs.listdir(base_dir)
	parser_dict = {}
	for module in dirs:
		module_dir = os.path.join(base_dir,module)
		module_cfg = os.path.join(module_dir,"module.cfg")
		module_icon = os.path.join(module_dir,"icon.png")
		module_fanart = os.path.join(module_dir,"fanart.jpg")
		if xbmcvfs.exists(module_icon): thumbnail = module_icon
		else: thumbnail = ''
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
	for key in sorted(parser_dict.keys()):
		addDir(key,MainURL,401,parser_dict[key][1],total_parsers,True,parser=parser_dict[key][0])
	addDir(traducao(40121),MainURL,34,addonpath + art + 'plus-menu.png',2,False)
	xbmc.executebuiltin("Container.SetViewMode(51)")
	

