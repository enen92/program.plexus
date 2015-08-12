This addon is not being supported. Another project (Plexus) is under development.
================


P2P-Streams addon for Kodi
================

[![screenshot1](http://t.imgbox.com/DtEF1B3b)](http://i.imgbox.com/DtEF1B3b.png)
[![screenshot2](http://t.imgbox.com/QtmPKURK)](http://i.imgbox.com/QtmPKURK.png)
[![screenshot3](http://t.imgbox.com/UMa9SpHi)](http://i.imgbox.com/UMa9SpHi.png)
[![screenshot4](http://t.imgbox.com/PN8YALYm)](http://i.imgbox.com/PN8YALYm.png)
[![screenshot5](http://t.imgbox.com/5L4R9PrT)](http://i.imgbox.com/5L4R9PrT.png)
[![screenshot6](http://t.imgbox.com/9wYcPmNp)](http://i.imgbox.com/9wYcPmNp.png)
[![screenshot7](http://t.imgbox.com/Pg0q8R6u)](http://i.imgbox.com/Pg0q8R6u.png)
[![screenshot8](http://t.imgbox.com/aUSDYYma)](http://i.imgbox.com/aUSDYYma.png)

About the addon
----------
p2p-streams is a video Kodi addon for watching peer-to-peer streams without the need for external players. Peer-to-peer (P2P) computing or networking is a distributed application architecture that partitions tasks or workloads between peers. Peers are equally privileged, equipotent participants in the application. They are said to form a peer-to-peer network of nodes.

The addon currently supports SopCast and AceStream and several platforms:
* Windows
* OSX
* Android
* Linux
  * Armv6 (Raspberry PI including OpenELEC) - AceStream 2.0 protocol only
  * Armv7 (OpenELEC,Xbian,MXLinux,Jynxbox Pure Linux) - AceStream 2.0 protocol only
  * i386 (including OpenELEC)
  * x86_64 (including OpenELEC)
  
Installation & configuration
----------
###Addon installation

Please install the repository in Kodi (System → settings → addons → install from zip file)

[Repository Download](http://p2p-strm.googlecode.com/svn/addons/repository.p2p-streams.xbmc/repository.p2p-streams.xbmc-1.0.4.zip)

After, get the addon from the installed repository:

System → settings → addons → get addons → p2p-streams repository → p2p-streams → install

###Platform specific configuration instructions:
Although we try to make the configuration as simple as possible it is platform dependent. Please check the specific detailed instructions for your platform/operating system.

* [Windows](https://github.com/enen92/P2P-Streams-XBMC/wiki/Windows-configuration)
* [Mac OSX](https://github.com/enen92/P2P-Streams-XBMC/wiki/Mac-OSX-configuration)
* [Android](https://github.com/enen92/P2P-Streams-XBMC/wiki/Android-Configuration)
* Linux
  * [OpenELEC](https://github.com/enen92/P2P-Streams-XBMC/wiki/OpenELEC-configuration)
  * [Armv6 (Raspberry PI)](https://github.com/enen92/P2P-Streams-XBMC/wiki/Linux-Armv6-Configuration)
  * [Armv7 (OpenELEC,Xbian,MXLinux,Jynxbox Pure Linux)](https://github.com/enen92/P2P-Streams-XBMC/wiki/Linux-Armv7-Configuration)
  * [i386 (Debian,Ubuntu,Arch...)](https://github.com/enen92/P2P-Streams-XBMC/wiki/Linux-(i386-and-x86_64)-configuration)
  * [x86_64 (Debian,Ubuntu,Arch)](https://github.com/enen92/P2P-Streams-XBMC/wiki/Linux-(i386-and-x86_64)-configuration)
  
About the technologies (and addon integration)
----------
###SopCast

SopCast is a simple, free way to broadcast video and audio or watch the video and listen to radio on the Internet. Adopting P2P(Peer-to-Peer) technology, It is very efficient and easy to use. Let anyone become a broadcaster without the costs of a powerful server and vast bandwidth. SoP is the abbreviation for Streaming over P2P. Sopcast is a Streaming Direct Broadcasting System based on P2P. The core is the communication protocol produced by Sopcast Team, which is named sop://, or SoP technology. More info at: [sopcast.org](http://sopcast.org)

The addon can accept `sop://` url's or simple id's (e.g.:`sop://broker.sopcast.org:3912/1234`) as following:

`plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=title+sopcast`

`plugin://plugin.video.p2p-streams/?url=1234&mode=2&name=title+sopcast`

###AceStream
Acestream (formerly known as TorrentStream) is a recent peer-to-peer technology based on the bittorrent protocol which will take you to a new high-quality level of multimedia space on the Internet. It's used for VOD and Live content. More info at: [acestream.org](http://acestream.org)
The addon can accept general `acestream://` based url, `.torrent urls, local .torrent files, .acelive urls or just acestream hashes. Eg:

`plugin://plugin.video.p2p-streams/?url=_some_hash&mode=1&name=acestream+title`

`plugin://plugin.video.p2p-streams/?url=acestream://_some_hash&mode=1&name=acestream+title`

`plugin://plugin.video.p2p-streams/?url=http://something.torrent&mode=1&name=acestream+title`

`plugin://plugin.video.p2p-streams/?url=http://something.acelive&mode=1&name=acestream+title`

Addon aditional functionalities
----------
The addon provides aditional functionalities you can use to create your own experience:
* **Parser plugins** - Built-in plugin engine that lets you create simple pure python plugins for website scrapping. Installing, removing and syncing code with remote repositories for a given parser. More information on the plugin structure and how to create your parser can be found here: [Website-parser tutorial and reference guide](https://github.com/enen92/P2P-Streams-Kodi/wiki/Website-Parser-tutorial). _Any plugin you might find in this addon is third party, not hosted nor maintained by the plugin authors_!
  
* **Lists** - You can easily add and remove local or remote (internet) lists. The addon supports sopcast based lists, m3u livetv lists and xml livestreams addon type lists. Click [here](https://github.com/enen92/P2P-Streams-Kodi/wiki/Lists) to know more about the formats._The only list included is the sopcast.org. The authors are not responsible for any lists you may install_
  
* **Favourites** - Easily add channels from parsers or lists to the addon favourites.
  
* **Advanced tools** - Easily import recommended advancedsettings.xml files that are known to provide the best behaviour, backup advancedsettings.xml configuration or remove them. Change AcestreamEngine settings in platforms where a gui is not available.

FAQ
----------
####Are the devs related to acestream.org or sopcast.org?
No, we are not affiliated with any of them. We do this addon in our free time. Hence, we do not provide support for possible errors or issues in both technologies. 

####Why does the addon come with just one list and no parsers? There are plenty of sop and ace links out there...
The plugin goal is to extend Kodi functionality and to make peer-to-peer streams playable in Kodi (as if they were part of the software core). Website parsers are difficult to maintain and can provide non-legal content. So, for obvious reasons we do not provide any support nor include any of them in the core addon. Also we want to keep updates at a minimum level.

####Am I allowed to discuss and share websites containg sopcast and acestream links?
If the content is legal yes. If not, please don't. You're messages will be either deleted or ignored if that's the case. 

####Is it available for iOS or atv2? I get a “not available for your os message”
Sopcast or Acestream are closed source applications that are not available for ios and atv (and might never be). You might want to consider [this option](https://github.com/enen92/P2P-Streams-Kodi/wiki/Using-an-acestream-engine-running-on-a-different-location)

####Why do I need to run Kodi as administrator in Windows when doing the initial configuration?
Sopcast in windows is complete gui package. It doesn't have any CLI executable or any possible way of integration. For the addon to play sopcast links a windows service is created (using the srvany microsoft tool) that makes sopcast.exe to run headless in your system. To create and modify the service permissions you need administration previledges.

####If the executables the addon uses are available from the official sites of both technologies why do you host and ship those .exe or .apk's from your repo?
To simplify the configuration, make it easier for the average user and to have better control of the files the addon needs. You're free to get those executables from the official channels and also compare the checksums with the ones downloaded from the addon (to confirm they are exactly the same). Also, you can check the addon code on github to understand what the addon is doing.

####Sometimes I get the message “Channel initialization failed” in Sopcast. Why?
Either the sopcast executable failed to login, the channel is offline or has been removed by SopCast because of proprietary content. Either the reason, there's nothing we can do to avoid this. 

####I'm kicked out of AceStreams after 'x' time...
There are several aditional configurations you might have to do to improve acestreams behaviour and... most of them fall out of the bounds of this addon.  Try to limit the cache in Kodi by importing one of the recommended advancedsettings.xml (advanced tools menu). Port forward port 8621 and change the acestream-engine settings. This site has some usefull information: [acestream buffer guide](http://acestreamguide.com/buffering/) . If these don't improve the behaviour your ISP is probably throttling your traffic.
Again, we are not affiliated with acestream.org and we can't do anything about it.

####Some acestreams play fine in windows, linux, OSX and Android but not on the Raspberry Pi,Linux Armv7 (Torrent unavailable / Failed to load list of files).
For the platforms mentioned we are using an old "open-source" version of the acestreamengine (protocol 2.0). Streams created with the newer versions (protocol 3.0 - available only for windows, android and linux) are not supported in older versions of the engine. We can't do much about this...

####Can I run the engine on a different computer?
Yes. [Read this](https://github.com/enen92/P2P-Streams-Kodi/wiki/Using-an-acestream-engine-running-on-a-different-location)

####Can I stream normal torrents with this plugin? 
The Acestream-Engine provided by acestream.org can stream normal .torrent files. Since this addon is nothing more than the implementation of its public API...it can play them in Kodi as well.
However in our opinion there are better alternatives to do this. Check [XBMCTorrent](http://forum.xbmc.org/showthread.php?tid=174736) or [Pulsar](http://forum.xbmc.org/showthread.php?tid=200957).

Authors
----------
enen92 and fightnight

Credits
----------
This addon would not be possible without the help and first work of some developers:

* **Nouismons** – First version of tsengine plugin
* **Cristi-Atlanta** – Xsopcast plugin
* **Divingmule** – Livestreams addon
* **Takoi** - Keymap editor addon
* **Marquerite** – Addon art
* **Tarasian666** – Alternative version of the acestreamengine written in python (which was tweaked to work on linux arm)
* **IGHOR** – Mac OSX acestream app

Contribute
----------
* [**Source code**](https://github.com/enen92/P2P-Streams-Kodi/tree/master/plugin.video.p2p-streams)
* [**External modules**](https://github.com/enen92/P2P-Streams-Kodi--Modules-)
* [**Translations**](https://github.com/enen92/P2P-Streams-Kodi/blob/master/plugin.video.p2p-streams/resources/language/English/strings.xml)
* [**Issues or feature requests**](https://github.com/enen92/P2P-Streams-Kodi/issues)
