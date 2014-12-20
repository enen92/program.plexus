# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains the livestream addon engine. It is mostly based on divingmule work on livestreams addon!

    Functions:

    xml_lists_menu() -> main menu for the xml list category
    addlista() -> add a new list. It'll ask for local or remote and processes the given input
    remove_list(name) -> Remove a list

    get_groups(url) -> First regex function to parse a given list. Sopcast type list
    get_channels(name,url) -> Second regex function to parse a given list. Used to general livestreams xml type lists
    getData(url,fanart) -> Get the item data such as iconimage, fanart, etc
    getChannelItems(name,url,fanart) -> Function to grab the channel items
    getItems(items,fanart) -> Function to grab the items from the xml
    removeNonAscii(s) -> Function to remove non-ascii characters from the list
    getSoup(url) -> uses beautifulsoup to parse a remote xml
    addon_log(string) -> Simple log/print function
    getRegexParsed(regexs, url) -> parse the regex expression
    list_type(url) -> Checks if the list is xml or m3u
    parse_m3u(url) -> Parses a m3u type list



"""

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,time,datetime,os,xbmcvfs,sys
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
from peertopeerutils.pluginxbmc import *
from peertopeerutils.webutils import *
from peertopeerutils.directoryhandle import *
from peertopeerutils.iofile import *

"""

Main Menu

"""

def xml_lists_menu():
    if settings.getSetting('sopcast-oficial') == "true":
        addDir(translate(40116),"http://sopcast.org/chlist.xml",101,addonpath + art + 'xml_list_sopcast.png',2,True)
    try:
        if os.path.exists(os.path.join(pastaperfil,"Lists")):
            dirs, files = xbmcvfs.listdir(os.path.join(pastaperfil,"Lists"))
            for file in files:
                f = open(os.path.join(pastaperfil,"Lists",file), "r")
                string = f.read()
                if xbmcvfs.exists(os.path.join(pastaperfil,"Lists-fanart",file.replace('.txt','.jpg'))):addDir("[B][COLOR orange]" + file.replace(".txt","") + "[/B][/COLOR]",string,101,addonpath + art + 'xml_lists.png',2,True,fan_art=os.path.join(pastaperfil,"Lists-fanart",file.replace('.txt','.jpg')))
                else: addDir("[B][COLOR orange]" + file.replace(".txt","") + "[/B][/COLOR]",string,101,addonpath + art + 'xml_lists.png',2,True)
    except: pass
    addDir(translate(40121),MainURL,107,addonpath + art + 'plus-menu.png',2,False)
    #xbmc.executebuiltin("Container.SetViewMode(51)")

"""

Add a new list function

"""

def addlista():
    opcao= xbmcgui.Dialog().yesno(translate(40000), translate(40123),"","",translate(40124),translate(40125))
    if opcao:
        dialog = xbmcgui.Dialog()
        lista_xml = dialog.browse(int(1), translate(40186), 'myprograms','.xml|.m3u')
        keybdois = xbmc.Keyboard("", translate(40130))
        keybdois.doModal()
        if (keybdois.isConfirmed()):
            searchname = keybdois.getText()
            if searchname=='': sys.exit(0)
            encode=urllib.quote(searchname)
            if xbmcvfs.exists(os.path.join(pastaperfil,"Lists")): pass
            else: xbmcvfs.mkdir(os.path.join(pastaperfil,"Lists"))
            txt_name = searchname + ".txt"
            save(os.path.join(pastaperfil,"Lists",txt_name),lista_xml)
            mensagemok(translate(40000),translate(40129))
            xbmc.executebuiltin("XBMC.Container.Refresh")
    else:
        keyb = xbmc.Keyboard("", translate(40127))
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            if "dropbox" in search and not "?dl=1" in search: search = search + '?dl=1'
            if "xml" not in search.split(".")[-1] and "m3u" not in search.split(".")[-1]: mensagemok(translate(40000),translate(40128)); sys.exit(0)
            else:
                try:
                    code = get_page_source(search)
                except:
                    mensagemok(translate(40000),translate(40128))
                    sys.exit(0)
            keybdois = xbmc.Keyboard("", translate(40130))
            keybdois.doModal()
            if (keybdois.isConfirmed()):
                searchname = keybdois.getText()
                if searchname=='': sys.exit(0)
                encode=urllib.quote(searchname)
                if os.path.exists(os.path.join(pastaperfil,"Lists")): pass
                else: xbmcvfs.mkdir(os.path.join(pastaperfil,"Lists"))
                txt_name = searchname + ".txt"
                save(os.path.join(pastaperfil,"Lists",txt_name),search)
                mensagemok(translate(40000),translate(40129))
                xbmc.executebuiltin("XBMC.Container.Refresh")

"""

Remove a List

"""

def remove_list(name):
    xbmcvfs.delete(name)
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(40150), 1,addonpath+"/icon.png"))
    xbmc.executebuiltin("Container.Refresh")

"""

Parsing functions

"""
def list_type(url):
    ltype = url.split('.')[-1]
    if 'xml' in ltype: get_groups(url)
    elif 'm3u' in ltype: parse_m3u(url)
    else: pass

def parse_m3u(url):
    if "http" in url: content = get_page_source(url)
    else: content = readfile(url)
    match = re.compile('#EXTINF:.+?,(.*?)\n(.*?)(?:\r|\n)').findall(content)
    for channel_name,stream_url in match:
        if 'plugin://' in stream_url:
            stream_url = 'XBMC.RunPlugin('+stream_url+')'
            addDir(channel_name,stream_url,106,'',1,False)
        elif 'sop://' in stream_url:
            addDir(channel_name,stream_url,2,'',1,False)
        elif ('acestream://' in stream_url) or ('.acelive' in stream_url) or ('.torrent' in stream_url):
            addDir(channel_name,stream_url,1,'',1,False)
        else: addLink(channel_name,stream_url,'')


def get_groups(url):
    from xml.etree import ElementTree
    try:
        print("Sopcast xml-type list detected")
        if "http" in url:
            source = get_page_source(url)
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
                addDir_livestreams_common(group_name,url,102,addonpath + art + 'xml_list_sopcast.png',True)
            except: pass
        #xbmc.executebuiltin("Container.SetViewMode(51)")
    except:
        print("Other type of xml list")
        getData(url,"")

def get_channels(name,url):
    from xml.etree import ElementTree
    if url.startswith('http://'):
        source = get_page_source(url)
    else:
        source = readfile(url)
    save(os.path.join(pastaperfil,"working.xml"),source)
    chlist_tree = ElementTree.parse(os.path.join(pastaperfil,"working.xml"))
    LANGUAGE = "en"
    groups = ElementTree.parse(os.path.join(pastaperfil,"working.xml")).findall('.//group')
    for group in groups:
        if group.attrib[LANGUAGE].encode('utf-8') == name:
            channels = group.findall('.//channel')
            for channel in channels:
                try:
                    try:
                        title = channel.find('.//name').attrib['en'].encode('utf-8')
                    except: title = ''
                    if not title: 
                        try: title = channel.find('.//name').attrib['cn'].encode('utf-8')
                        except: title = ''
                    if not title:
                        try: title = channel.find('.//name').text
                        except: title = ''
                    tipo = channel.find('.//stream_type').text
                    sop_address = channel.find('.//item').text
                    if not tipo: tipo = "N/A"
                    if not title: title = "N/A"
                    thumbnail = ""
                    try:
                        thumbnail = channel.find('.//thumbnail').text
                    except: pass
                    if sop_address:
                        if thumbnail == "": thumbnail = addonpath + art + 'sopcast_link.png'
                        try: addDir_livestreams_common('[B][COLOR orange]' + title + ' [/B][/COLOR](' + tipo +')',sop_address,2,thumbnail,False)
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
                addDir_livestreams(name.encode('utf-8', 'ignore'),url.encode('utf-8'),103,thumbnail,fanArt,desc,genre,date,credits,True)
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
                    addDir_livestreams(name.encode('utf-8', 'ignore'),url[0],106,thumbnail,fanArt,desc,genre,"credits",date)
                except:
                    match = re.compile("&name=(.+?)\)").findall(url[0].replace(";",""))
                    if match:
                        try:
                            addDir_livestreams(name.encode('utf-8', 'ignore'),removeNonAscii(url[0]),106,thumbnail,fanArt,desc,genre,credits,date)
                        except:
                            try:
                                addDir_livestreams(removeNonAscii(name.encode('utf-8', 'ignore')),removeNonAscii(url[0].replace(";","")),106,thumbnail,fanArt,desc,genre,credits,date)
                            except:
                                addon_log('There was a problem adding item - '+name.encode('utf-8', 'ignore'))
                    else:
                        addon_log('There was a problem adding item - '+name.encode('utf-8', 'ignore'))

            else:
                if ('acestream://' in url[0]) or ('.acelive' in url[0]) or ('.torrent' in url[0]):
                    if 'plugin://' not in url[0]:
                        addDir_livestreams(name.encode('utf-8', 'ignore'),url[0],1,thumbnail,fanArt,desc,genre,"credits",date)
                    else:
                        addLink_livestreams(url[0].replace(';',''),name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,None,regexs,total)
                elif 'sop://' in url[0]:
                    if 'plugin://' not in url[0]:
                        addDir_livestreams(name.encode('utf-8', 'ignore'),url[0],2,thumbnail,fanArt,desc,genre,"credits",date)
                    else:
                        addLink_livestreams(url[0].replace(';',''),name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,None,regexs,total)
                else: addLink_livestreams(url[0].replace(';',''),name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,None,regexs,total)
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
    print(string)

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
