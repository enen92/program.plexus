P2P-Streams XBMC Addon
================

About the addon
----------
p2p-streams is an XBMC addon for watching peer-to-peer streams in XBMC without the need for external players. Peer-to-peer (P2P) computing or networking is a distributed application architecture that partitions tasks or workloads between peers. Peers are equally privileged, equipotent participants in the application. They are said to form a peer-to-peer network of nodes.

The addon currently supports SopCast and AceStream and several platforms:
* Windows
* OSX
* Android
* Linux
  * Armv6 (Raspberry PI including OpenELEC)
  * Armv7 (OpenELEC,Xbian,MXLinux)
  * i386 (including OpenELEC)
  * x86_64 (including OpenELEC)
  
Installation & configuration
----------
###Addon installation

Please install the repository in XBMC (System → settings → addons → install from zip file)

[Repository Download](http://p2p-strm.googlecode.com/svn/addons/repository.p2p-streams.xbmc/repository.p2p-streams.xbmc-1.0.3.zip)

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
  * [Armv7 (OpenELEC,Xbian,MXLinux)](https://github.com/enen92/P2P-Streams-XBMC/wiki/Linux-Armv7-Configuration)
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
* **Parser plugins** - Built-in plugin engine that lets you create simple pure python plugins for website scrapping. Installing, removing and syncing code with remote repositories for a given parser. More information on the plugin structure and how to create your parser can be found here: Coiso. No piracy related sites discussion or support!
* **Lists** - You can easily add and remove local or remote (internet) lists. The addon supports sopcast based lists (like: http://sopcast.org/chlist.xml) or general livestreams addon lists. Also, it supports general m3u lists. No sharing or discussion of lists containing piracy content!
* **Favourites** - Easily add channels from parsers or lists to the addon favourites.
* **Advanced tools** - Easily import recommended advancedsettings.xml files that are known to provide the best behaviour, backup advancedsettings.xml configuration or remove them. Change AcestreamEngine settings in platforms where a gui is not available.

FAQ
----------
####Are the devs related to acestream.org or sopcast.org?
No, we are not affiliated with any of them. We do this addon in our free time. Hence, we do not provide support for possible errors or issues in both technologies. 

####Why does the addon come with just one list and no parsers? There are plenty of sop and ace links out there...
The plugin goal is to extend xbmc functionality and to make peer-to-peer streams playable in XBMC. Website parsers are difficult to maintain and can provide non-legal content. So, for obvious reasons we do not provide any support nor include any of them in the core addon. Also we want to keep updates at a minimum level.

####Am I allowed to discuss and share websites containg sopcast and acestream links?
If the content is legal yes. If not, please don't. You're messages will be either deleted or ignored if that's the case. 

####Is it available for iOS or atv2? I get a “not available for your os message”
Sopcast or Acestream are closed source applications that are not available for ios and atv (and might never be). You might want to consider [this option](https://github.com/enen92/P2P-Streams-XBMC/wiki/Using-an-acestream-engine-running-on-a-different-location)

####Why do I need to run xbmc as administrator in Windows when doing the initial configuration?
Sopcast in windows is complete gui package. It doesn't have any CLI executable or any possible way of integration. For the addon to play sopcast links a windows service is created (using the srvany microsoft tool) that makes sopcast.exe to run headless in your system. To create and modify the service permissions you need administration previledges.

####If the executables the addon uses are available from the official sites of both technologies why do you host and ship those .exe or .apk's from your repo?
To simplify the configuration, make it easier for the average user and to have better control of the files the addon needs. You're free to get those executables from the official channels and also compare the checksums with the ones downloaded from the addon (to confirm they are exactly the same). Also, you can check the addon code on github to understand what the addon is doing.

####Sopcast in OSX only lasts 3 seconds...
Unfortunately since xbmc gotham beta 3 this behaviour started to happen. Frodo and gotham versions till beta 3 seem to handle the streams fine. 

####Sometimes I get the message “Channel initialization failed” in Sopcast. Why?
Either the sopcast executable failed to login, the channel is offline or has been removed by SopCast because of proprietary content. Either the reason, there's nothing we can do to avoid this. 

####I'm kicked out of AceStreams after 'x' time...
There are several aditional configurations you might have to do to improve acestreams behaviour and... most of them fall out of the bounds of this addon.  Try to limit the cache in XBMC by importing one of the recommended advancedsettings.xml (advanced tools menu). Port forward port 8621 and change the acestream-engine settings. This site has some usefull information: [acestream buffer guide](http://acestreamguide.com/buffering/) . If these don't improve the behaviour your ISP is probably throttling your traffic.
Again, we are not affiliated with acestream.org and we can't do anything about it.

####Some acestreams play fine in windows but not on Android, Raspberry Pi and Linux (Torrent unavailable).
The AcestreamEngine for windows is several versions above the others and seems to receive much more support and development by acestream developers. Streams created in the windows 2.2 version of acestream engine (and above) are not supported in older versions (which are used in all the other platforms). For linux (x86_64 only) you can check the [Acestream-Engine Alpha 3.0 ](http://wiki.acestream.org/wiki/index.php/AceStream_3.0.0_alpha/en).

####Can I run the engine on a different computer?
Yes. [Read this](https://github.com/enen92/P2P-Streams-XBMC/wiki/Using-an-acestream-engine-running-on-a-different-location)

####Can I stream normal torrents with this plugin? 
The Acestream-Engine provided by acestream.org can stream normal .torrent files. Since this addon is nothing more than the implementation of its public API...it can play them in XBMC as well.
However in our opinion there are better alternatives to do this. Check XBMCtorrent or Pulsar.

Authors
----------
enen92 and fightnight

Credits
----------
This addon would not be possible without the help and first work of some developers:

* **Nouismons** – First version of tsengine plugin
* **Cristi-Atlanta** – Xsopcast plugin
* **Divingmule** – Livestreams addon
* **Marquerite** – Addon art
* **Tarasian666** – Alternative version of the acestreamengine written in python (which was tweaked to work on linux arm and mac osx)

Contribute
----------
* [**Source code**](https://github.com/enen92/P2P-Streams-XBMC/tree/master/plugin.video.p2p-streams)
* [**External modules**](https://github.com/enen92/P2P-Streams-XBMC--Modules-)
* [**Translations**](https://github.com/enen92/P2P-Streams-XBMC/blob/master/plugin.video.p2p-streams/resources/language/English/strings.xml)
* [**Issues or feature requests**](https://github.com/enen92/P2P-Streams-XBMC/issues)
