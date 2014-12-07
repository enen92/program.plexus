# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains web utilities
    
    Classes:
    
    download_tools() -> Contains a downloader, a extraction function and a remove function
    
    Functions:
    
    get_page_source -> Get a webpage source code through urllib2
    mechanize_browser(url) -> Get a webpage source code through mechanize module. To avoid DDOS protections.
    makeRequest(url, headers=None) -> check if a page is up and retrieve its source code
    clean(text) -> Remove specific characters from the page source
    url_isup(url, headers=None) -> Check if url is up. Returns True or False.
   	
"""
    
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,urllib2,tarfile,os,sys,re
from pluginxbmc import *

user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'

class download_tools():
	def Downloader(self,url,dest,description,heading):
		dp = xbmcgui.DialogProgress()
		dp.create(heading,description,'')
		dp.update(0)
		urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: self._pbhook(nb,bs,fs,dp))
		
	def _pbhook(self,numblocks, blocksize, filesize,dp=None):
		try:
			percent = int((int(numblocks)*int(blocksize)*100)/int(filesize))
			dp.update(percent)
		except:
			percent = 100
			dp.update(percent)
		if dp.iscanceled(): 
			dp.close()
	
	def extract(self,file_tar,destination):
		dp = xbmcgui.DialogProgress()
		dp.create(translate(40000),translate(40044))
		tar = tarfile.open(file_tar)
		tar.extractall(destination)
		dp.update(100)
		tar.close()
		dp.close()
		
	def remove(self,file_):
		dp = xbmcgui.DialogProgress()
		dp.create(translate(40000),translate(40045))
		os.remove(file_)
		dp.update(100)
		dp.close()

def get_page_source(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def mechanize_browser(url):
	import mechanize
	br = mechanize.Browser()
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	r = br.open(url)
	html = r.read()
	html_source= br.response().read()
	return html_source
	
def makeRequest(url, headers=None):
	try:
		if not headers:
			headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
		req = urllib2.Request(url,None,headers)
		response = urllib2.urlopen(req)
		data = response.read()
		response.close()
		return data
	except:
		mensagemok(translate(40000),translate(40122))
		sys.exit(0)
		
def url_isup(url, headers=None):
	try:
		if not headers:
			headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
		req = urllib2.Request(url,None,headers)
		response = urllib2.urlopen(req)
		data = response.read()
		response.close()
		return True
	except: return False
		
def clean(text):
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&#039;':'','&#39;':"'",'&#227;':'ã','&170;':'ª','&#233;':'é','&#231;':'ç','&#243;':'ó','&#226;':'â','&ntilde;':'ñ','&#225;':'á','&#237;':'í','&#245;':'õ','&#201;':'É','&#250;':'ú','&amp;':'&','&#193;':'Á','&#195;':'Ã','&#202;':'Ê','&#199;':'Ç','&#211;':'Ó','&#213;':'Õ','&#212;':'Ó','&#218;':'Ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)
