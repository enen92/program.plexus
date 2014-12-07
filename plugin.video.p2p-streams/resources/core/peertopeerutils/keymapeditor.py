# -*- coding: utf-8 -*-

""" p2p-streams (c) 2014 enen92 fightnight
   
   This file contains functions from the keymap editor addon by takoi
    
"""
from peertopeerutils.pluginxbmc import *
import xbmc,os,shutil
from xbmcgui import Dialog, WindowXMLDialog
from threading import Timer
import xml.etree.ElementTree as ET

default = xbmc.translatePath('special://xbmc/system/keymaps/keyboard.xml')
userdata = xbmc.translatePath('special://userdata/keymaps')
gen_file = os.path.join(userdata, 'gen.xml')


def run():
	## load mappings ##
	try:
		setup_keymap_folder()
	except Exception:
		pass

	defaultkeymap = read_keymap(default)
	userkeymap = []
	if os.path.exists(gen_file):
		try:
			userkeymap = read_keymap(gen_file)
		except Exception:
			pass
	newkey = KeyListener.record_key()
	if newkey:
		new = ('global', u'RunPlugin(plugin://plugin.video.p2p-streams/?mode=7)', newkey)
		userkeymap.append(new)
		if os.path.exists(gen_file):
			shutil.copyfile(gen_file, gen_file + ".old")
		write_keymap(userkeymap, gen_file)
		xbmc.executebuiltin("action(reloadkeymaps)")
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(600026), 1,addonpath+"/icon.png"))
		

class KeyListener(WindowXMLDialog):
    TIMEOUT = 5

    def __new__(cls):
        return super(KeyListener, cls).__new__(cls, "DialogKaiToast.xml", "")

    def __init__(self):
        self.key = None

    def onInit(self):
        try:
            self.getControl(401).addLabel(translate(70034))
            self.getControl(402).addLabel(translate(70035) % self.TIMEOUT)
        except AttributeError:
            self.getControl(401).setLabel(translate(70034))
            self.getControl(402).setLabel(translate(70035) % self.TIMEOUT)

    def onAction(self, action):
        code = action.getButtonCode()
        self.key = None if code == 0 else str(code)
        self.close()

    @staticmethod
    def record_key():
        dialog = KeyListener()
        timeout = Timer(KeyListener.TIMEOUT, dialog.close)
        timeout.start()
        dialog.doModal()
        timeout.cancel()
        key = dialog.key
        del dialog
        return key
        
def read_keymap(filename):
    ret = []
    with open(filename, 'r') as xml:
        tree = ET.iterparse(xml)
        for _, keymap in tree:
            for context in keymap:
                for device in context:
                    for mapping in device:
                        key = mapping.get('id') or mapping.tag
                        action = mapping.text
                        if action:
                            ret.append((context.tag.lower(), action.lower(), key.lower()))
    return ret
    
def setup_keymap_folder():
    if not os.path.exists(userdata):
        os.makedirs(userdata)
    else:
        #make sure there are no user defined keymaps
        for name in os.listdir(userdata):
            if name.endswith('.xml') and name != os.path.basename(gen_file):
                src = os.path.join(userdata, name)
                for i in xrange(100):
                    dst = os.path.join(userdata, "%s.bak.%d" % (name, i))
                    if os.path.exists(dst):
                        continue
                    shutil.move(src, dst)
                    #successfully renamed
                    break
                    
def write_keymap(keymap, filename):
    contexts = list(set([c for c, a, k in keymap]))
    builder = ET.TreeBuilder()
    builder.start("keymap", {})
    for context in contexts:
        builder.start(context, {})
        builder.start("keyboard", {})
        for c, a, k in keymap:
            if c == context:
                builder.start("key", {"id":k})
                builder.data(a)
                builder.end("key")
        builder.end("keyboard")
        builder.end(context)
    builder.end("keymap")
    element = builder.close()
    ET.ElementTree(element).write(filename, 'utf-8')
