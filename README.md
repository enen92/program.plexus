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
We currently keep the distribution versions in googlecode and use github only for development. Please install the repository in XBMC (System → settings → addons → install from zip file)

[Repository Download](http://p2p-strm.googlecode.com/svn/addons/repository.p2p-streams.xbmc/repository.p2p-streams.xbmc-1.0.3.zip)

After doing this, install the addon from the repository:

System → settings → addons → get addons → p2p-streams repository → p2p-streams → install

###Platform specific configuration instructions:
The addon includes a configuration function which tries to make the configuration really easy. However it is platform dependent. Please check the specific FAQ's for your platform.

* [Windows](coiso)
* [OSX](coiso)
* [Android](coiso)
* Linux
  * [Armv6 (Raspberry PI including OpenELEC)](ciso)
  * [Armv7 (OpenELEC,Xbian,MXLinux)](coiso)
  * [i386 (including OpenELEC)](coiso)
  * [x86_64 (including OpenELEC)](coiso)
  
About the technologies (and addon integration)
----------
###SopCast

SopCast is a simple, free way to broadcast video and audio or watch the video and listen to radio on the Internet. Adopting P2P(Peer-to-Peer) technology, It is very efficient and easy to use. Let anyone become a broadcaster without the costs of a powerful server and vast bandwidth. SoP is the abbreviation for Streaming over P2P. Sopcast is a Streaming Direct Broadcasting System based on P2P. The core is the communication protocol produced by Sopcast Team, which is named sop://, or SoP technology. More at: [sopcast.org](http://sopcast.org)

The addon can accept sop url or id's as following:

`plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=title+sopcast`
`plugin://plugin.video.p2p-streams/?url=11265&mode=2&name=title+sopcast`

###AceStream
Acestream (formerly known as TorrentStream) is a recent peer-to-peer technology based on bittorrent which will take you to a new high-quality level of multimedia space on the Internet. It's used for VOD and Live content. More at: [acestream.org](http://acestream.org)
The addon can accept general acestream:// based url, .torrent urls, local .torrent files, .acelive urls or just acestream hashes. Eg:

`plugin://plugin.video.p2p-streams/?url=_some_hash&mode=1&name=acestream+title`
`plugin://plugin.video.p2p-streams/?url=acestream://_some_hash&mode=1&name=acestream+title`
`plugin://plugin.video.p2p-streams/?url=http://something.torrent&mode=1&name=acestream+title`
`plugin://plugin.video.p2p-streams/?url=http://something.acelive&mode=1&name=acestream+title`

Addon aditional functionalities
----------

