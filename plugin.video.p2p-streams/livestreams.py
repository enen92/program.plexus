#!/usr/bin/env python
# -*- coding: utf-8 -*-

#NOTE: This part of the addon is mostly the livestreams addon code made by Divingmule!

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,time,datetime,os,xbmcvfs,sys
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP

addon_id = 'plugin.video.p2p-streams'
settings = xbmcaddon.Addon(id=addon_id)
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
mensagemok = xbmcgui.Dialog().ok
traducaoma= settings.getLocalizedString

def traducao(texto):
      return traducaoma(texto).encode('utf-8')

def get_groups(url):
    from xml.etree import ElementTree
    try:
        print "Sopcast xml-type list detected"
	if "http" in url:
		source = abrir_url(url)
		save(os.path.join(pastaperfil,"working.xml"),source)
		workingxml = os.path.join(pastaperfil,"working.xml")
	else:
		workingxml = url
        groups = ElementTree.parse(workingxml).findall('.//group')
        unname_group_index = 1
	LANGUAGE = "en"
        for group in groups:
            if group.attrib[LANGUAGE] == "":
                group.attrib[LANGUAGE] = str(unname_group_index)
                unname_group_index = unname_group_index + 1
                if re.sub('c','e',LANGUAGE) == LANGUAGE:
                    OTHER_LANG = re.sub('e','c',LANGUAGE)
                else:
                    OTHER_LANG = re.sub('c','e',LANGUAGE)
                if LANGUAGE == "cn":
                    try:
                        if len(group.attrib[OTHER_LANG]) > 0:
                            group.attrib[LANGUAGE] = group.attrib[OTHER_LANG]
                            unname_group_index = unname_group_index - 1
                    except:
                        pass
            if (group.find('.//channel')==None): continue
            group_name=group.attrib[LANGUAGE]
            try:
	        addDir(group_name,url,29,"",True)
            except: pass
        xbmc.executebuiltin("Container.SetViewMode(51)")
    except:
	getData(url,"")

def get_channels(name,url):
        from xml.etree import ElementTree
	source = abrir_url(url)
	save(os.path.join(pastaperfil,"working.xml"),source)
	chlist_tree = ElementTree.parse(os.path.join(pastaperfil,"working.xml"))
	LANGUAGE = "en"
	groups = ElementTree.parse(os.path.join(pastaperfil,"working.xml")).findall('.//group')
	for group in groups:
		if group.attrib[LANGUAGE].encode('utf-8') == name:
			channels = group.findall('.//channel')
			for channel in channels:
				try:
					title = channel.find('.//name').attrib['en'].encode('utf-8')
					if not title: title = channel.find('.//name').attrib['cn'].encode('utf-8')
					tipo = channel.find('.//stream_type').text
					sop_address = channel.find('.//item').text
					if not tipo: tipo = "N/A"
					if not title: title = "N/A"
					thumbnail = ""
					try:
						thumbnail = channel.find('.//thumbnail').text
					except: pass
					if sop_address:
						try: addDir('[B][COLOR orange]' + title + ' [/B][/COLOR](' + tipo +')',sop_address,2,thumbnail,False)
						except:pass
					else: pass
				except: pass
		else: pass


def getData(url,fanart):
        soup = getSoup(url)
        if len(soup('channels')) > 0:
            channels = soup('channel')
            for channel in channels:
                name = channel('name')[0].string
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    thumbnail = ''

                try:
                    if not channel('fanart'):
                        if addon.getSetting('use_thumb') == "true":
                            fanArt = thumbnail
                        else:
                            fanArt = fanart
                    else:
                        fanArt = channel('fanart')[0].string
                    if fanArt == None:
                        raise
                except:
                    fanArt = fanart

                try:
                    desc = channel('info')[0].string
                    if desc == None:
                        raise
                except:
                    desc = ''

                try:
                    genre = channel('genre')[0].string
                    if genre == None:
                        raise
                except:
                    genre = ''

                try:
                    date = channel('date')[0].string
                    if date == None:
                        raise
                except:
                    date = ''

                try:
                    credits = channel('credits')[0].string
                    if credits == None:
                        raise
                except:
                    credits = ''

                try:
                    addDir_livestreams(name.encode('utf-8', 'ignore'),url.encode('utf-8'),30,thumbnail,fanArt,desc,genre,date,credits,True)
                except:
                    addon_log('There was a problem adding directory from getData(): '+name.encode('utf-8', 'ignore'))
        else:
            addon_log('No Channels: getItems')
            getItems(soup('item'),fanart)

def getChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('channel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('item')
        try:
            fanArt = channel_list('fanart')[0].string
            if fanArt == None:
                raise
        except:
            fanArt = fanart
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not channel('fanart'):
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                else:
                    fanArt = channel('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                pass
            try:
                desc = channel('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = channel('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = channel('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            try:
                credits = channel('credits')[0].string
                if credits == None:
                    raise
            except:
                credits = ''

            try:
                addDir_livestreams(name.encode('utf-8', 'ignore'),url.encode('utf-8'),3,thumbnail,fanArt,desc,genre,credits,date)
            except:
                addon_log('There was a problem adding directory - '+name.encode('utf-8', 'ignore'))
        getItems(items,fanArt)

def getItems(items,fanart):
        total = len(items)
        addon_log('Total Items: %s' %total)
        for item in items:
            try:
                name = item('title')[0].string
                if name is None:
                    name = 'unknown?'
            except:
                addon_log('Name Error')
                name = ''
            try:
                if item('epg'):
                    if item.epg_url:
                        addon_log('Get EPG Regex')
                        epg_url = item.epg_url.string
                        epg_regex = item.epg_regex.string
                        epg_name = get_epg(epg_url, epg_regex)
                        if epg_name:
                            name += ' - ' + epg_name
                    elif item('epg')[0].string > 1:
                        name += getepg(item('epg')[0].string)
                else:
                    pass
            except:
                addon_log('EPG Error')

            try:
                url = []
                for i in item('link'):
                    if not i.string == None:
                        url.append(i.string)
                if len(url) < 1:
                    raise
            except:
                addon_log('Error <link> element, Passing:'+name.encode('utf-8', 'ignore'))
                continue

            try:
                thumbnail = item('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not item('fanart'):
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                    else:
                        fanArt = fanart
                else:
                    fanArt = item('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                fanArt = fanart
            try:
                desc = item('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = item('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = item('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            regexs = None
            if item('regex'):
                try:
                    regexs = {}
                    for i in item('regex'):
                        regexs[i('name')[0].string] = {}
                        regexs[i('name')[0].string]['expre'] = i('expres')[0].string
                        regexs[i('name')[0].string]['page'] = i('page')[0].string
                        try:
                            regexs[i('name')[0].string]['refer'] = i('referer')[0].string
                        except:
                            addon_log("Regex: -- No Referer --")
                        try:
                            regexs[i('name')[0].string]['agent'] = i('agent')[0].string
                        except:
                            addon_log("Regex: -- No User Agent --")
                    regexs = urllib.quote(repr(regexs))
                except:
                    regexs = None
                    addon_log('regex Error: '+name.encode('utf-8', 'ignore'))

            try:
		    if "RunPlugin" in url[0]:
			try:
				print name,url
				addDir_livestreams(name.encode('utf-8', 'ignore'),url[0],33,thumbnail,fanArt,desc,genre,"credits",date)
			except:
				match = re.compile("&name=(.+?)\)").findall(url[0].replace(";",""))
				if match:
					try:
						addDir_livestreams(name.encode('utf-8', 'ignore'),removeNonAscii(url[0]),33,thumbnail,fanArt,desc,genre,credits,date)
					except:
						try:
							addDir_livestreams(removeNonAscii(name.encode('utf-8', 'ignore')),removeNonAscii(url[0].replace(";","")),33,thumbnail,fanArt,desc,genre,credits,date)
						except: 
							addon_log('There was a problem adding item - '+name.encode('utf-8', 'ignore'))
				else:
                			addon_log('There was a problem adding item - '+name.encode('utf-8', 'ignore'))

		    else:
                    	addLink_livestreams(url[0].replace(';',''),name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,None,regexs,total)
            except:
                addon_log('There was a problem adding item - '+name.encode('utf-8', 'ignore'))

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def getSoup(url):
        if url.startswith('http://'):
            data = makeRequest(url)
        else:
            if xbmcvfs.exists(url):
                if url.startswith("smb://") or url.startswith("nfs://"):
                    copy = xbmcvfs.copy(url, os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    if copy:
                        data = open(os.path.join(profile, 'temp', 'sorce_temp.txt'), "r").read()
                        xbmcvfs.delete(os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    else:
                        addon_log("failed to copy from smb:")
                else:
                    data = open(url, 'r').read()
            else:
                addon_log("Soup Data not found!")
                return
        return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)

def addon_log(string):
	print string

def getRegexParsed(regexs, url):
        regexs = eval(urllib.unquote(regexs))
        cachedPages = {}
        doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
        for k in doRegexs:
            if k in regexs:
                m = regexs[k]
                if m['page'] in cachedPages:
                    link = cachedPages[m['page']]
                else:
                    req = urllib2.Request(m['page'])
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
                    if 'refer' in m:
                        req.add_header('Referer', m['refer'])
                    if 'agent' in m:
                        req.add_header('User-agent', m['agent'])
                    response = urllib2.urlopen(req)
                    link = response.read()
                    response.close()
                    cachedPages[m['page']] = link
                reg = re.compile(m['expre']).search(link)
                url = url.replace("$doregex[" + k + "]", reg.group(1).strip())
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def addlista():
	opcao= xbmcgui.Dialog().yesno(traducao(40000), traducao(40123),"","",traducao(40124),traducao(40125))
	if opcao:
		print "Carreguei"
		dialog = xbmcgui.Dialog()
		lista_xml = dialog.browse(int(1), traducao(40186), 'myprograms','.xml')
		keybdois = xbmc.Keyboard("", traducao(40130))
		keybdois.doModal()
		if (keybdois.isConfirmed()):
			searchname = keybdois.getText()
			if searchname=='': sys.exit(0)
			encode=urllib.quote(searchname)
			if xbmcvfs.exists(os.path.join(pastaperfil,"Lists")): pass
			else: xbmcvfs.mkdir(os.path.join(pastaperfil,"Lists"))
			txt_name = searchname + ".txt"
			save(os.path.join(pastaperfil,"Lists",txt_name),lista_xml)
			mensagemok(traducao(40000),traducao(40129))
			xbmc.executebuiltin("XBMC.Container.Refresh")
	else:
		keyb = xbmc.Keyboard("", traducao(40127))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			encode=urllib.quote(search)
			if encode.split(".")[-1] != "xml": print "diferente de xml";mensagemok(traducao(40000),traducao(40128)); sys.exit(0)
			else:
				try:
					print encode
					code = abrir_url(search)
				except:
					mensagemok(traducao(40000),traducao(40128))
					sys.exit(0)
			keybdois = xbmc.Keyboard("", traducao(40130))
			keybdois.doModal()
			if (keybdois.isConfirmed()):
				searchname = keybdois.getText()
				if searchname=='': sys.exit(0)
				encode=urllib.quote(searchname)
				if xbmcvfs.exists(os.path.join(pastaperfil,"Lists")): pass
				else: xbmcvfs.mkdir(os.path.join(pastaperfil,"Lists"))
				txt_name = searchname + ".txt"
				save(os.path.join(pastaperfil,"Lists",txt_name),search)
				mensagemok(traducao(40000),traducao(40129))
				xbmc.executebuiltin("XBMC.Container.Refresh")

#########################################################################################

def save(filename,contents):
	fh = open(filename, 'w')
	fh.write(contents)
	fh.close()
	return

def readfile(filename):
	f = open(filename, "r")
	string = f.read()
	return string

def makeRequest(url, headers=None):
        try:
            if headers is None:
                headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
            req = urllib2.Request(url,None,headers)
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            return data
        except:
	    mensagemok(traducao(40000),traducao(40122))
	    sys.exit(0)


def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link


def addDir(name,url,mode,iconimage,folder,fannart=None):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
	contextmen = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	if fannart:
		liz.setProperty('fanart_image', fannart)
	else:
        	liz.setProperty('fanart_image', "%s/fanart.jpg"%settings.getAddonInfo("path"))
	if mode == 1 or mode == 2:
		try:
			dirs, files = xbmcvfs.listdir(os.path.join(pastaperfil,"Favourites"))
			if url.replace(":","").replace("/","") + ".txt" in files: contextmen.append((traducao(40146), 'XBMC.RunPlugin(%s?mode=48&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], urllib.quote_plus(url),name,iconimage)))
			else: contextmen.append((traducao(40143), 'XBMC.RunPlugin(%s?mode=46&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], urllib.quote_plus(url),name,iconimage)))
		except: pass
	liz.addContextMenuItems(contextmen,replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addDir_livestreams(name,url,mode,iconimage,fanart,description,genre,date,credits,showcontext=False):
	if not genre: genre='genre'
	if not credits: credits='credits'
	if not date: date = 'date'
	if not description: description = 'description'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
	contextmen = []
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        if "RunPlugin" in url: pasta = False
        else: pasta = True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	if mode == 33:
		try:
			dirs, files = xbmcvfs.listdir(os.path.join(pastaperfil,"Favourites"))
			match = re.compile("url=(.+?)&mode").findall(url.replace(";",""))
			if match:
				if match[0].replace(":","").replace("/","").replace(";","") + ".txt" in files: contextmen.append((traducao(40146), 'XBMC.RunPlugin(%s?mode=48&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], urllib.quote_plus(url),name,iconimage)))
				else: contextmen.append((traducao(40143), 'XBMC.RunPlugin(%s?mode=46&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], urllib.quote_plus(url),name,iconimage)))
		except: pass
	liz.addContextMenuItems(contextmen,replaceItems=False)		
	if fanart:
		liz.setProperty('fanart_image', fanart)
	else:
        	liz.setProperty('fanart_image', "%s/fanart.jpg"%settings.getAddonInfo("path"))
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date, "credits": credits })
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
        return ok

def addLink_livestreams(url,name,iconimage,fanart,description,genre,date,showcontext,playlist,regexs,total):
        try:
            name = name.encode('utf-8')
        except: pass
	contextmen = []
        ok = True
        if regexs: mode = '31'
        else: mode = '32'
        u=sys.argv[0]+"?"
        u += "url="+urllib.quote_plus(url)+"&mode="+mode
        if regexs:
            u += "&regexs="+regexs
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date })
	liz.addContextMenuItems(contextmen,replaceItems=False)		
	if fanart:
		liz.setProperty('fanart_image', fanart)
	else:
        	liz.setProperty('fanart_image', "%s/fanart.jpg"%settings.getAddonInfo("path"))
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,totalItems=total)
        return ok





