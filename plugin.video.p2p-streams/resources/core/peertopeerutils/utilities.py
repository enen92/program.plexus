# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains common utilites
    
    Functions:
    
    handle_wait(time_to_wait,title,text,segunda='') -> Timer with dialog progress capabilities
    clean_text(text) -> Function to remove specific characters from a string
    getDirectorySize(directory) -> returns a directory size recursively
    recursive_overwrite(src, dest, ignore=None) -> Copy and replace an entire directory recursively
   	
"""
    
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,re,os,shutil
from pluginxbmc import *

def handle_wait(time_to_wait,title,text,segunda=''):
        ret = mensagemprogresso.create(' '+title)
        secs=0
        percent=0
        increment = int(100 / time_to_wait)
        cancelled = False
        while secs < time_to_wait:
                secs = secs + 1
                percent = increment*secs
                secs_left = str((time_to_wait - secs))
                if segunda=='': remaining_display = translate(40188) + str(secs_left) + translate(40189)
                else: remaining_display=segunda
                mensagemprogresso.update(percent,text,remaining_display)
                xbmc.sleep(1000)
                if (mensagemprogresso.iscanceled()):
                        cancelled = True
                        break
        if cancelled == True:
                return False
        else:
                mensagemprogresso.close()
                return False

def clean_text(text):
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&#039;':'','&#39;':"'",'&#227;':'ã','&170;':'ª','&#233;':'é','&#231;':'ç','&#243;':'ó','&#226;':'â','&ntilde;':'ñ','&#225;':'á','&#237;':'í','&#245;':'õ','&#201;':'É','&#250;':'ú','&amp;':'&','&#193;':'Á','&#195;':'Ã','&#202;':'Ê','&#199;':'Ç','&#211;':'Ó','&#213;':'Õ','&#212;':'Ó','&#218;':'Ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)
      
def getDirectorySize(directory):
	dir_size = 0
	for (path, dirs, files) in os.walk(directory):
		for file in files:
			filename = os.path.join(path, file)
			dir_size += os.path.getsize(filename)
	return dir_size
	
def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)
    return
