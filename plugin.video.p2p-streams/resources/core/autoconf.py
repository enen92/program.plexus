# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains a single function. It's a function that will run on the addon first boot to download and configure the system for acestream/sopcast. The platform will be automatically detected and the necessary files downloaded and extracted to the userdata. 
    This function will run if and only the setting "Download modules" on boot is enabled.
    
    Functions:
    
   	check_for_updates() -> Look for module updates between versions, force download them
   	firstconf() -> Configuration function, detects the platform, saves to settings, run configure sopcast/acestream functions
   	configure_sopcast() -> Configure Sopcast
   	configure_acestream() -> Configure Acestream

"""
     
import xbmc,xbmcgui,xbmcplugin,xbmcvfs
import tarfile,os,re,sys,subprocess
from peertopeerutils.pluginxbmc import *
from peertopeerutils.webutils import download_tools,get_page_source
from peertopeerutils.utilities import *

""" Platform dependent files downloaded during the addon configuration"""

#Linux Armv6 (Raspberry PI)
sopcast_raspberry = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/sopcast-raspberry.tar.gz"
acestream_generic_raspberry = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/raspberry-acestream.tar.gz"
acestream_openelec_raspberry = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/openelec-acestream.tar.gz"
#Linux Armv7 packages
sopcast_jynxbox = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Armv7/sopcast-jynxbox_purelinux.tar.gz"
acestream_mxlinux = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Armv7/mxlinux/mxlinux_armv7_acestream.tar.gz"
acestream_armv7_openelec = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Armv7/openelec/openelec-acestream.tar.gz"
acestream_armv7_xbian = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Armv7/xbian/xbian_acestream.tar.gz"
#Linux i386 and x86_64 (including openelec)
sopcast_linux_generico =  "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Sopcastx86_64i386/sopcast_linux.tar.gz"
openelecx86_64_sopcast = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/x86_64/Openelec/sopcast_openelec64.tar.gz"
openeelcx86_64_acestream = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/x86_64/Openelec/acestream_openelec64_3051.tar.gz"
openelecxi386_sopcast = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/i386/openelec/sopcast_openeleci386.tar.gz"
openeelcxi386_acestream = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/i386/openelec/acestream_openeleci386_303fix.tar.gz"
#gen linux
acestream_linux_x64_generic = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/x86_64/acestream-linux-x86_64_3051.tar.gz"
acestream_linux_i386_generic = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/i386/acestream-linux-i386_303.tar.gz"
#Android
sopcast_apk = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/SopCast.apk.tar.gz"
acestreamengine_apk_arm = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/AceStream-3.0.6-2in1.apk.tar.gz"
acestreamengine_apk_x86 = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/AceStream-3.0.6-2in1.apk.tar.gz"
android_aceengine_arm = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/org.acestream.engine-arm-3.0.6.tar.gz"
android_aceengine_x86 = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/org.acestream.engine_x86.tar.gz"
android_aceplayer_arm = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/AcePlayer-3.0.6-2in1.apk.tar.gz"
android_aceplayer_x86 = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/AcePlayer-3.0.6-2in1.apk.tar.gz"
#Mac OSX
osx_i386_sopcast = "http://p2p-strm.googlecode.com/svn/trunk/Modules/MacOsx/i386/sopcast_osxi386.tar.gz"
osx_i386_acestream = "http://p2p-strm.googlecode.com/svn/trunk/Modules/MacOsx/AceStreamWineOSX.zip"
osx_x64_sopcast = "http://p2p-strm.googlecode.com/svn/trunk/Modules/MacOsx/x86_64/sopcast_osx64.tar.gz"
osx_x64_acestream = "http://p2p-strm.googlecode.com/svn/trunk/Modules/MacOsx/AceStreamWineOSX.zip"
#Windows Files
acestream_windows = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Windows/acewindows-aceengine3.0.4.tar.gz"
srvany_executable = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Windows/srvany.tar.gz"
srvany_permissions = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Windows/sopcastp2p-permissions.txt"

def check_for_updates():
	try:
		version_source = get_page_source("http://p2p-strm.googlecode.com/svn/trunk/ModuleVersions/versions.info")
	except: version_source = ""
	if version_source:
		version_source = eval(version_source)
		if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android') and not settings.getSetting('force_android') == "true":
			if os.uname()[4] == "armv6l":
				if settings.getSetting('openelecarm6') == "true": platf = "openelec_arm6"
				else: platf = "raspberrypi"
			elif os.uname()[4] == "armv7l":
				if settings.getSetting('openelecarm7') == "true": platf = "openelec_armv7"
				elif settings.getSetting('mxlinuxarm7') == "true": platf = "mxlinux_armv7"
				elif settings.getSetting('xbianarm7') == "true": platf = "xbian_armv7"
				elif settings.getSetting('jynxbox_arm7') == "true": platf = "jynxbox_armv7"
			elif os.uname()[4] == "i386" or os.uname()[4] == "i686":
				if settings.getSetting('openeleci386') == "true": platf = "openeleci386"
				else: platf = "linuxi386"
			elif os.uname()[4] == "x86_64": 
				if settings.getSetting('openelecx86_64') == "true": platf = "openelecx64"
				else: platf = "linux_x86_64"
		elif xbmc.getCondVisibility('system.platform.windows'): platf = "windows"
		elif xbmc.getCondVisibility('system.platform.Android') or settings.getSetting('force_android') == "true": platf = "android"
		elif xbmc.getCondVisibility('System.Platform.OSX'):
			if os.uname()[4] == "i386" or os.uname()[4] == "i686": platf = "osx32"
			elif os.uname()[4] == "x86_64": platf = "osx64"
		try:
			if version_source["sopcast"][platf] != settings.getSetting('sopcast_version'): configure_sopcast(version_source["sopcast"][platf])
			sopcast_update = True
		except: sopcast_update = False
		try:
			if version_source["acestream"][platf] != settings.getSetting('acestream_version'): configure_acestream(version_source["acestream"][platf])
			acestream_update = True
		except: acestream_update = False
		if acestream_update and sopcast_update: settings.setSetting('last_version_check',value=versao)
		return
		
				
		
			
def first_conf():
	settings.setSetting('last_version_check',value='')
	settings.setSetting('sopcast_version',value='')
	settings.setSetting('acestream_version',value='')
	if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android') and not settings.getSetting('force_android') == "true":
		if os.uname()[4] == "armv6l":
			if re.search(os.uname()[1],"openelec",re.IGNORECASE): settings.setSetting('openelecarm6',value='true')
			elif re.search(os.uname()[1],"raspbmc",re.IGNORECASE): settings.setSetting('raspberrypi',value='true')
			elif os.path.isfile("/etc/xbian_version"): acestream_rpi = settings.setSetting('raspberrypi',value='true')
			elif "ARCH" in os.uname()[2]:
				settings.setSetting('raspberrypi',value='true')
				settings.setSetting('python_cmd',value='python2')
			else:
				mensagemok(translate(40000),translate(400007),translate(400008))
				OS_list = ["OpenELEC","Raspbmc","Xbian","Pipplware","Arch Linux Arm"]
				OS_Rpi_choose = xbmcgui.Dialog().select
				choose=OS_Rpi_choose('Select your OS',OS_list)
				if choose > -1:
					if OS_list[choose] == "OpenELEC": settings.setSetting('openelecarm6',value='true')
					elif OS_list[choose] == "Arch Linux Arm": settings.setSetting('raspberrypi',value='true');settings.setSetting('python_cmd',value='python2')
					else: settings.setSetting('raspberrypi',value='true')
			check_for_updates()
		elif os.uname()[4] == "armv7l":
			if re.search(os.uname()[1],"openelec",re.IGNORECASE):
				settings.setSetting('openelecarm7',value='true')
			elif os.path.isfile("/etc/xbian_version"):
				settings.setSetting('xbianarm7',value='true')
			else:
                		mensagemok(translate(40000),translate(40109),translate(40110))
                		OS_list = ["MXLinux","OpenELEC","Xbian","Jynxbox Pure Linux"]
                		choose=xbmcgui.Dialog().select('Select your OS',OS_list)
                		if choose > -1:
                			OS_Choose= OS_list[choose]
                			if OS_Choose == "OpenELEC": settings.setSetting('openelecarm7',value='true')
                			elif OS_Choose == "Xbian": settings.setSetting('xbianarm7',value='true')
                			elif OS_Choose == "MXLinux": settings.setSetting('mxlinuxarm7',value='true')
                			elif OS_Choose == "Jynxbox Pure Linux": settings.setSetting('jynxbox_arm7',value='true')
			check_for_updates()
		else:
			#32bit and 64bit
			if os.uname()[4] == "x86_64":
				if re.search(os.uname()[1],"openelec",re.IGNORECASE):
					settings.setSetting('openelecx86_64',value='true')
				else:
					opcao= xbmcgui.Dialog().yesno(translate(40000), translate(40113))
					if opcao: 
						settings.setSetting('openelecx86_64',value='true')
			elif os.uname()[4] == "i386" or os.uname()[4] == "i686":
				if re.search(os.uname()[1],"openelec",re.IGNORECASE):	
					settings.setSetting('openeleci386',value='true')
				else:
					opcao= xbmcgui.Dialog().yesno(translate(40000), translate(600023))
					if opcao: 
						settings.setSetting('openeleci386',value='true')
			check_for_updates()
			
	elif xbmc.getCondVisibility('system.platform.windows'):
		check_for_updates()

	elif xbmc.getCondVisibility('system.platform.Android'):
		check_for_updates()
		
	elif xbmc.getCondVisibility('System.Platform.OSX'):
		check_for_updates()
		
	settings.setSetting('autoconfig',value="false")
		

	
def configure_sopcast(latest_version):
	#Configuration for LINUX 
	if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android') and not settings.getSetting('force_android') == "true":
		print("Detected OS: Linux")
		#Linux Armv6
		if os.uname()[4] == "armv6l":
			print("Detected linux armv6 - possible Raspberry PI")
			#Sop
			SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
			download_tools().Downloader(sopcast_raspberry,SPSC_KIT,translate(40025),translate(40000))
			import tarfile            
			if tarfile.is_tarfile(SPSC_KIT):
				path_libraries = os.path.join(pastaperfil,"sopcast")
				download_tools().extract(SPSC_KIT,path_libraries)
				xbmc.sleep(500)
				download_tools().remove(SPSC_KIT)
			if latest_version: settings.setSetting('sopcast_version',value=latest_version)
			return

		elif os.uname()[4] == "armv7l":
			if settings.getSetting('jynxbox_arm7') == "true":
				SPSC_KIT = os.path.join(addonpath,sopcast_jynxbox.split("/")[-1])
				download_tools().Downloader(sopcast_jynxbox,SPSC_KIT,translate(40025),translate(40000))
				import tarfile
				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil)
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
				if latest_version: settings.setSetting('sopcast_version',value=latest_version)
				return
			else:
				SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
				download_tools().Downloader(sopcast_raspberry,SPSC_KIT,translate(40025),translate(40000))
				import tarfile
				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"sopcast")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
				if latest_version: settings.setSetting('sopcast_version',value=latest_version)
				return

		elif os.uname()[4] == "x86_64":
			generic = False
			if settings.getSetting('openelecx86_64') == "true":
				print("Detected OpenELEC x86_64")
				SPSC_KIT = os.path.join(addonpath,openelecx86_64_sopcast.split("/")[-1])
				download_tools().Downloader(openelecx86_64_sopcast,SPSC_KIT,translate(40025),translate(40000))
				import tarfile
				if tarfile.is_tarfile(SPSC_KIT):
					download_tools().extract(SPSC_KIT,pastaperfil)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
				if latest_version: settings.setSetting('sopcast_version',value=latest_version)
				return
			else: generic = True
		elif os.uname()[4] == "i386" or os.uname()[4] == "i686":
			generic = False
			if settings.getSetting('openeleci386') == "true":
				SPSC_KIT = os.path.join(addonpath,openelecxi386_sopcast.split("/")[-1])
				download_tools().Downloader(openelecxi386_sopcast,SPSC_KIT,translate(40025),translate(40000))
				import tarfile
				if tarfile.is_tarfile(SPSC_KIT):
					download_tools().extract(SPSC_KIT,pastaperfil)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
				if latest_version: settings.setSetting('sopcast_version',value=latest_version)
				return
			else: generic = True
		if generic == True:
			SPSC_KIT = os.path.join(addonpath,sopcast_linux_generico.split("/")[-1])
			download_tools().Downloader(sopcast_linux_generico,SPSC_KIT,translate(40025),translate(40000))
			import tarfile
			if tarfile.is_tarfile(SPSC_KIT):
				path_libraries = os.path.join(pastaperfil,"sopcast")
				download_tools().extract(SPSC_KIT,path_libraries)
				xbmc.sleep(500)
				download_tools().remove(SPSC_KIT)
			#set every single file from the bundle as executable
			path_libraries = os.path.join(pastaperfil,"sopcast")
			dirs, files = xbmcvfs.listdir(path_libraries)
			for ficheiro in files:
				binary_path = os.path.join(path_libraries,ficheiro)
				st = os.stat(binary_path)
				import stat
				os.chmod(binary_path, st.st_mode | stat.S_IEXEC)
			path_libraries = os.path.join(path_libraries,"lib")
			dirs, files = xbmcvfs.listdir(path_libraries)
			for ficheiro in files:
				binary_path = os.path.join(path_libraries,ficheiro)
				st = os.stat(binary_path)
				import stat
				os.chmod(binary_path, st.st_mode | stat.S_IEXEC)
			if latest_version: settings.setSetting('sopcast_version',value=latest_version)
			return


	elif xbmc.getCondVisibility('system.platform.windows'):
		print("Detected OS: Windows")
		if not xbmcvfs.exists(pastaperfil): xbmcvfs.mkdir(pastaperfil)
        	#Sop
		import ctypes
                is_admin=ctypes.windll.shell32.IsUserAnAdmin() != 0
                if is_admin == False:
                    mensagemok(translate(40000),translate(40158),translate(40159))
                else:
		    import subprocess
                    cmd = ['sc','delete','sopcastp2p']
                    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                    for line in proc.stdout:
                        print("cmd out: " + line.rstrip())
                    xbmc.sleep(1000)
                    ret = mensagemprogresso.create(translate(40000),translate(40000))
                    mensagemprogresso.update(0,translate(40160),"  ")
                    xbmc.sleep(1000)
                    import _winreg
                    aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                    try:
                        aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
                        name, value, type = _winreg.EnumValue(aKey, 0)
                        sopcast_executable = value
                        print("Installation executable of sopcast was found: " + sopcast_executable)
                        _winreg.CloseKey(aKey)
                        mensagemprogresso.update(10,translate(40160),translate(40161))
                    except:
                        sopcast_executable = ""
                        mensagemok(translate(40000),translate(40162),translate(40163))
                    if not sopcast_executable: pass
                    else:
                        xbmc.sleep(1000)
                        mensagemprogresso.update(20,translate(40164),"  ")
                        xbmc.sleep(1000)
                        print ("Getting windows users IDS")
                        aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                        aKey = _winreg.OpenKey(aReg, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList')
                        users = []
                        for i in range(1024):
                            try:
                                asubkey=_winreg.EnumKey(aKey,i)
                                print(asubkey)
                                aKeydois = _winreg.OpenKey(aReg, os.path.join('SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList',asubkey))
                                val=_winreg.QueryValueEx(aKeydois, "ProfileImagePath")
                                try:
                                    print(val[0])
                                except:
                                    print("Notice: User with strange characters, print cmd ignored.")
                                if "Windows" in val[0] or "%systemroot%" in val[0]:
                                    pass
                                else:
                                    users.append(asubkey)
                            except:
                                pass
                        if not users:
                            mensagemok(translate(40000),translate(40165))
                        else:
                            mensagemprogresso.update(30,translate(40164),translate(40161))
                            xbmc.sleep(200)
                            mensagemprogresso.update(30,translate(40166),"   ")
                            xbmc.sleep(1000)
                            print("System Users", users)
                            srvany_final_location = os.path.join(sopcast_executable.replace("SopCast.exe",""),"srvany.exe")
                            srvany_download_location = os.path.join(addonpath,"srvany.exe")
                            srvanytgz_download_location = os.path.join(addonpath,"srvany.tar.gz")                            
                            download_tools().Downloader(srvany_executable,srvanytgz_download_location,translate(40167),translate(40000)) 
                            xbmc.sleep(1000)
                            import tarfile
                            if tarfile.is_tarfile(srvanytgz_download_location):
                                path_libraries = addonpath
                                download_tools().extract(srvanytgz_download_location,path_libraries)
                                xbmcvfs.copy(srvany_download_location,srvany_final_location)
                                download_tools().remove(srvanytgz_download_location)
                                download_tools().remove(srvany_download_location)
                            xbmc.sleep(1000)
                            ret = mensagemprogresso.create(translate(40000),translate(40000))
                            xbmc.sleep(200)
                            mensagemprogresso.update(35,translate(40168),"  ")
                            xbmc.sleep(1000)
                            import subprocess
                            cmd = ['sc','create','sopcastp2p','binpath=',os.path.join(os.path.join(sopcast_executable.replace("SopCast.exe","")),'srvany.exe')]
                            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                            servicecreator = False
                            for line in proc.stdout:
                                print ("cmd out: " + line.rstrip())
                                servicecreator = True
                            if servicecreator == False:
                                mensagemok(translate(40000),translate(40169))
                            else:
                                mensagemprogresso.update(40,translate(40168),translate(40161))
                                xbmc.sleep(1000)
                                mensagemprogresso.update(45,translate(40170),"  ")
                                xbmc.sleep(1000)
                                print("Trying to modify regedit....")
                                try:
                                    aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                                    key = _winreg.CreateKey(aReg, r'SYSTEM\CurrentControlSet\Services\sopcastp2p\Parameters')
                                    _winreg.SetValueEx(key, 'AppDirectory', 0, _winreg.REG_SZ, os.path.join(sopcast_executable.replace("SopCast.exe","")))
                                    _winreg.SetValueEx(key, 'Application', 0, _winreg.REG_SZ, os.path.join(os.path.join(sopcast_executable.replace("SopCast.exe","")),"SopCast.exe"))
                                    _winreg.SetValueEx(key, 'AppParameters', 0, _winreg.REG_SZ, "sop://")
                                    mensagemprogresso.update(50,translate(40170), translate(40161))
                                    regedit = True
                                except:
                                    mensagemok(translate(40000),translate(40171))
                                    regedit = False
                                if regedit == False: pass
                                else:
                                    xbmc.sleep(1000)
                                    mensagemprogresso.update(50,translate(40172), "   ")
                                    cmd = ['sc','sdshow','sopcastp2p']
                                    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                                    lines = []
                                    for line in proc.stdout:
					print(line.rstrip())
                                        if line.rstrip() != "" and "(" in line.rstrip(): lines.append(line.rstrip())
                                        else: pass
                                    if len(lines) != 1: mensagemok(translate(40000),translate(40173))
                                    else:
                                        linha_arr = []
                                        for user in users:
                                            linha_arr.append('(A;;RPWPCR;;;' + user + ')')
                                        linha_add = ''
                                        for linha in linha_arr:
                                            linha_add += linha
                                        print("line peace to add: " + linha_add)
                                        linha_final = lines[0].replace("S:(",linha_add + "S:(")
                                        print("Final line: " + linha_final)
                                        permissions = False
                                        xbmc.sleep(500)
                                        mensagemprogresso.update(60,translate(40172), translate(40161))
                                        xbmc.sleep(500)
                                        mensagemprogresso.update(60,translate(40174), "   ")
                                        cmd = ['sc','sdset','sopcastp2p',linha_final]
                                        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                                        for line in proc.stdout:
                                            print(line.rstrip())
                                            permissions = True
                                        if permissions == False: mensagemok(translate(40000),translate(40175))
                                        else:
                                            mensagemprogresso.update(70,translate(40174), translate(40161))
                                            xbmc.sleep(1000)
                                            mensagemprogresso.update(70,translate(40176), "   ")
                                            print("Trying to set sopcastp2p service regedit permissions...")
                                            download_tools().Downloader(srvany_permissions,os.path.join(pastaperfil,"sopcastp2p-permissions.txt"),translate(40177),translate(40000))
                                            xbmc.sleep(500)
                                            ret = mensagemprogresso.create(translate(40000),translate(40000))
                                            xbmc.sleep(500)
                                            mensagemprogresso.update(80,translate(40178), "   ")
                                            xbmc.sleep(1000)
                                            cmd = ['regini',os.path.join(pastaperfil,"sopcastp2p-permissions.txt")]
                                            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                                            for line in proc.stdout:
                                                print(line.rstrip())
                                            mensagemprogresso.update(90,translate(40178), translate(40178))
                                            mensagemprogresso.update(100,translate(40179), "   ")
                                            xbmc.sleep(2000)
                                            mensagemprogresso.close()
                                            if latest_version: settings.setSetting('sopcast_version',value=latest_version)
                                            return
    
	elif xbmc.getCondVisibility('System.Platform.OSX'):
		print("Detected OS: Mac OSX")
		available = False
		if os.uname()[-1] == "x86_64":
			mac_package = osx_x64_sopcast
			available = True
		elif os.uname()[-1] == "i386":
			mac_package = osx_i386_sopcast
			available = True
		else:
			available = False
		if available == True:		
			if not os.path.exists(pastaperfil):
				xbmcvfs.mkdir(pastaperfil)		
			MAC_KIT = os.path.join(addonpath,mac_package.split("/")[-1])
			download_tools().Downloader(mac_package,MAC_KIT,translate(40025),translate(40000))
			import tarfile
			if tarfile.is_tarfile(MAC_KIT):
				path_libraries = os.path.join(pastaperfil)
				download_tools().extract(MAC_KIT,pastaperfil)
				download_tools().remove(MAC_KIT)
				sp_sc_auth = os.path.join(pastaperfil,"sopcast","sp-sc-auth")
				st = os.stat(sp_sc_auth)
				import stat
				os.chmod(sp_sc_auth, st.st_mode | stat.S_IEXEC)
			if latest_version: settings.setSetting('sopcast_version',value=latest_version)
			return
		else:
			mensagemok(translate(40000),translate(600014))
			return
				
	elif xbmc.getCondVisibility('System.Platform.Android') or settings.getSetting('force_android') == "true":

		print("Detected OS: Android")
		#Sopcast configuration
		print("Starting SopCast Configuration")

		#Moving sopclient to ext4 hack - tks steeve from xbmctorrent

		sopclient_builtin_location = os.path.join(addonpath,"resources","binaries","sopclient")

		#Hack to get current xbmc app id
		xbmcfolder=xbmc.translatePath(addonpath).split("/")

		i = 0
		found = False
		sopcast_installed = False
		
		for folder in xbmcfolder:
			if folder.count('.') >= 2 and folder != addon_id :
				found = True
				break
			else:
				i+=1

		if found == True:
			uid = os.getuid()
			app_id = xbmcfolder[i]
			xbmc_data_path = os.path.join("/data", "data", app_id)
			if os.path.exists(xbmc_data_path) and uid == os.stat(xbmc_data_path).st_uid:
				android_binary_dir = os.path.join(xbmc_data_path, "files", "plugin.video.p2p-streams")
				if not os.path.exists(android_binary_dir):
            				os.makedirs(android_binary_dir)
				android_binary_path = os.path.join(android_binary_dir, "sopclient")
		        	if not os.path.exists(android_binary_path) or os.path.getsize(android_binary_path) != os.path.getsize(sopclient_builtin_location):
					import shutil
					shutil.copy2(sopclient_builtin_location, android_binary_path)
				binary_path = android_binary_path
				st = os.stat(binary_path)
				import stat
				os.chmod(binary_path, st.st_mode | stat.S_IEXEC)
				settings.setSetting('android_sopclient',value=binary_path)
				opcao= xbmcgui.Dialog().yesno(translate(40000), translate(50011),translate(50012))
				if not opcao:
					settings.setSetting('external-sopcast',value='1')
					settings.setSetting('force_android',value='true')
					sopcast_installed = True
					mensagemok(translate(40000),translate(50014))
				else:
					mensagemok(translate(40000),translate(50013))
					if os.path.exists(os.path.join("sdcard","Download")):
						pasta = os.path.join("sdcard","Download")
						sopfile = os.path.join("sdcard","Download",sopcast_apk.split("/")[-1])
					else:
						dialog = xbmcgui.Dialog()
						pasta = dialog.browse(int(0), translate(40190), 'myprograms')
						sopfile = os.path.join(pasta,sopcast_apk.split("/")[-1])
					download_tools().Downloader(sopcast_apk,sopfile,translate(40073),translate(40000))
					import tarfile
					if tarfile.is_tarfile(sopfile):
						download_tools().extract(sopfile,pasta)
						download_tools().remove(sopfile)
					mensagemok(translate(40000),translate(50015),pasta,translate(50016))
					sopcast_installed = True
					settings.setSetting('external-sopcast',value='0')
					mensagemok(translate(40000),translate(50014))
				if latest_version: settings.setSetting('sopcast_version',value=latest_version)
				return

		else:
			mensagemok(translate(40000),translate(50017))
			return
			
			
			
def configure_acestream(latest_version):
	#Configuration for LINUX 
	if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android') and not settings.getSetting('force_android') == "true":
		print("Detected OS: Linux")
		#Linux Armv6
		if os.uname()[4] == "armv6l":
			print("Detected linux armv6 - possible Raspberry PI")
			if settings.getSetting('openelecarm6') == "true": acestream_rpi = acestream_openelec_raspberry
			else: acestream_rpi = acestream_generic_raspberry
			ACE_KIT = os.path.join(addonpath,acestream_rpi.split("/")[-1])
			download_tools().Downloader(acestream_rpi,ACE_KIT,translate(40026),translate(40000))
			import tarfile            
			if tarfile.is_tarfile(ACE_KIT):
				path_libraries = os.path.join(pastaperfil,"acestream")
				download_tools().extract(ACE_KIT,path_libraries)
				xbmc.sleep(500)
				download_tools().remove(ACE_KIT)
			if latest_version: settings.setSetting('acestream_version',value=latest_version)
			return
		#Linux Armv7
		elif os.uname()[4] == "armv7l":
			if settings.getSetting('openelecarm7') == "true": acestream_package = acestream_armv7_openelec
			elif settings.getSetting('xbianarm7') == "true": acestream_package = acestream_armv7_xbian
			elif settings.getSetting('mxlinuxarm7') == "true" or settings.getSetting('jynxbox_arm7') == "true": acestream_package = acestream_mxlinux
		
			ACE_KIT = os.path.join(addonpath,acestream_package.split("/")[-1])
			download_tools().Downloader(acestream_package,ACE_KIT,translate(40026),translate(40000))
			import tarfile
			if tarfile.is_tarfile(ACE_KIT):
				path_libraries = os.path.join(pastaperfil,"acestream")
				download_tools().extract(ACE_KIT,path_libraries)
				xbmc.sleep(500)
				download_tools().remove(ACE_KIT)
			if latest_version: settings.setSetting('acestream_version',value=latest_version)
			return

		elif os.uname()[4] == "x86_64":
			if settings.getSetting('openelecx86_64') == "true":
				print("OpenELEC x86_64 Acestream configuration")
				ACE_KIT = os.path.join(addonpath,openeelcx86_64_acestream.split("/")[-1])
				download_tools().Downloader(openeelcx86_64_acestream ,ACE_KIT,translate(40026),translate(40000))
				import tarfile
				if tarfile.is_tarfile(ACE_KIT):
					download_tools().extract(ACE_KIT,pastaperfil)
					xbmc.sleep(500)
					download_tools().remove(ACE_KIT)
				if latest_version: settings.setSetting('acestream_version',value=latest_version)
				return

			else:
				print("64 bit Linux Disto Acestream Configuration")
				ACE_KIT = os.path.join(addonpath,acestream_linux_x64_generic.split("/")[-1])
				download_tools().Downloader(acestream_linux_x64_generic,ACE_KIT,translate(40026),translate(40000))
				import tarfile
				if tarfile.is_tarfile(ACE_KIT):
					download_tools().extract(ACE_KIT,pastaperfil)
					xbmc.sleep(500)
					download_tools().remove(ACE_KIT)
				if latest_version: settings.setSetting('acestream_version',value=latest_version)
				return

		elif os.uname()[4] == "i386" or os.uname()[4] == "i686":
			if settings.getSetting('openeleci386') == "true":
				print("32 bit Openelec Acestream Configuration")
				ACE_KIT = os.path.join(addonpath,openeelcxi386_acestream.split("/")[-1])
				download_tools().Downloader(openeelcxi386_acestream,ACE_KIT,translate(40026),translate(40000))
				import tarfile
				if tarfile.is_tarfile(ACE_KIT):
					download_tools().extract(ACE_KIT,pastaperfil)
					xbmc.sleep(500)
					download_tools().remove(ACE_KIT)
				if latest_version: settings.setSetting('acestream_version',value=latest_version)
				return
			else:
				print("32 bit Linux general distro Acestream Configuration")
				ACE_KIT = os.path.join(addonpath,acestream_linux_i386_generic.split("/")[-1])
				download_tools().Downloader(acestream_linux_i386_generic,ACE_KIT,translate(40026),translate(40000))
				import tarfile
				if tarfile.is_tarfile(ACE_KIT):
					download_tools().extract(ACE_KIT,pastaperfil)
					xbmc.sleep(500)
					download_tools().remove(ACE_KIT)
				if latest_version: settings.setSetting('acestream_version',value=latest_version)
				return

	elif xbmc.getCondVisibility('system.platform.windows'):
		print("Detected OS: Windows")
		if not os.path.exists(pastaperfil): xbmcvfs.mkdir(pastaperfil)
          #Ace
		SPSC_KIT = os.path.join(addonpath,acestream_windows.split("/")[-1])
		download_tools().Downloader(acestream_windows,SPSC_KIT,translate(40026),translate(40000))
		import shutil
		if os.path.exists(os.path.join(pastaperfil,"acestream")):
			shutil.rmtree(os.path.join(pastaperfil,"acestream"))
		if os.path.exists(os.path.join(pastaperfil,"player")):
			shutil.rmtree(os.path.join(pastaperfil,"player"))
		import tarfile
		if tarfile.is_tarfile(SPSC_KIT):
			path_libraries = os.path.join(pastaperfil)
			download_tools().extract(SPSC_KIT,path_libraries)
			download_tools().remove(SPSC_KIT)
		if latest_version: settings.setSetting('acestream_version',value=latest_version)
		return
    
	elif xbmc.getCondVisibility('System.Platform.OSX'):
		print("Detected OS: Mac OSX")
		available = False
		if os.uname()[-1] == "x86_64":
			mac_package = osx_x64_acestream
			available = True
		elif os.uname()[-1] == "i386":
			mac_package = osx_i386_acestream
			available = True
		else:
			available = False
		if available == True:			
			MAC_KIT = os.path.join('/Applications',mac_package.split("/")[-1])
			if not xbmcvfs.exists(os.path.join('/Applications','Ace Stream.app')):
				download_tools().Downloader(mac_package,MAC_KIT,translate(40026),translate(40000))
				if xbmcvfs.exists(MAC_KIT):
					xbmc.sleep(1000)
					cmd = 'unzip /Applications/AceStreamWineOSX.zip'
					zipa = subprocess.Popen(cmd,shell=True)
					cmd = 'chmod -R 755 /Applications/Ace\ Stream.app'
					print cmd
					chmod = subprocess.Popen(cmd,shell=True)
					try: os.remove(MAC_KIT)
					except: pass
			if latest_version: settings.setSetting('acestream_version',value=latest_version)
			return
		else:
			mensagemok(translate(40000),translate(600014))
			return
			
				
	elif xbmc.getCondVisibility('System.Platform.Android') or settings.getSetting('force_android') == "true":

		print("Detected OS: Android")
		print("Starting Acestream Configuration")
		#acestream config for android
		if not os.path.exists(pastaperfil): xbmcvfs.mkdir(pastaperfil)
		#Hack to get xbmc app id
		xbmcfolder=xbmc.translatePath(addonpath).split("/")
		
		i = 0
		found = False
		sopcast_installed = False
		
		for folder in xbmcfolder:
			if folder.count('.') >= 2 and folder != addon_id :
				found = True
				break
			else:
				i+=1

		if found == True:
			uid = os.getuid()
			app_id = xbmcfolder[i]
			settings.setSetting('app_id',app_id)
			#Acestreamconfiguration for android starts here
			if "arm" in os.uname()[4]:
				acebundle = os.path.join(pastaperfil,android_aceengine_arm.split("/")[-1])
				download_tools().Downloader(android_aceengine_arm,acebundle,translate(70014),translate(40000))
			else:
				acebundle = os.path.join(pastaperfil,android_aceengine_x86.split("/")[-1])
				download_tools().Downloader(android_aceengine_x86,acebundle,translate(70014),translate(40000))
			import tarfile
			if tarfile.is_tarfile(acebundle):
				download_tools().extract(acebundle,pastaperfil)
				download_tools().remove(acebundle)
			orgacestreamenginefolder = os.path.join(pastaperfil,"org.acestream.engine")
			xbmc_data_path = os.path.join("/data", "data", app_id)
			if os.path.exists(xbmc_data_path) and uid == os.stat(xbmc_data_path).st_uid:
				android_binary_dir = os.path.join(xbmc_data_path, "files", "plugin.video.p2p-streams")
				if not os.path.exists(android_binary_dir): os.makedirs(android_binary_dir)
            		android_acestream_folder = os.path.join(android_binary_dir,"org.acestream.engine")
            		if not os.path.exists(android_acestream_folder): os.makedirs(android_acestream_folder)
            		else:
            			#clean install for android - delete old folder
            			print android_acestream_folder
            			try:
            				os.system("chmod -R 777 "+android_acestream_folder+"/*")
            				os.system("rm -r '"+android_acestream_folder+"'")
            			except: pass
            			try: os.makedirs(android_acestream_folder)
            			except: pass
            		xbmc.sleep(200)
            		#clean install in android - remove /sdcard/.ACEStream folder if it exists (to be enabled between versions if we need to remove older settings
            		#if os.path.exists(os.path.join('/sdcard','.ACEStream')):
				#	try:
				#		hidden_ace = os.path.join('/sdcard','.ACEStream')
				#		os.system("chmod -R 777 "+hidden_ace+"/*")
				#		os.system("rm -r '"+hidden_ace+"'")
				#	except: pass
            		recursive_overwrite(orgacestreamenginefolder, android_acestream_folder, ignore=None)
            		pythonbin = os.path.join(android_acestream_folder,"files","python","bin","python")
            		st = os.stat(pythonbin)
            		import stat
            		os.chmod(pythonbin, st.st_mode | stat.S_IEXEC)
            		if os.path.exists(orgacestreamenginefolder):
					try:
						os.system("chmod -R 777 "+orgacestreamenginefolder+"/*")
						os.system("rm -r '"+orgacestreamenginefolder+"'")
					except: pass
            		try: xbmcvfs.mkdir(os.path.join('/sdcard','org.acestream.engine'))
            		except: pass
			opcao= xbmcgui.Dialog().yesno(translate(40000), translate(70015),translate(70016))
			if not opcao:
				settings.setSetting('engine_app','0')
			else:
				mensagemok(translate(40000),translate(50018),translate(50019),translate(50020))
				if os.path.exists(os.path.join("sdcard","Download")):
					pasta = os.path.join("sdcard","Download")
					if "arm" in os.uname()[4]: acefile = os.path.join("sdcard","Download",acestreamengine_apk_arm.split("/")[-1])
					else: acefile = os.path.join("sdcard","Download",acestreamengine_apk_x86.split("/")[-1])
				else:
					dialog = xbmcgui.Dialog()
					pasta = dialog.browse(int(0), translate(40190), 'myprograms')
					if "arm" in os.uname()[4]: acefile = os.path.join(pasta,acestreamengine_apk_arm.split("/")[-1])
					else: acefile = os.path.join(pasta,acestreamengine_apk_x86.split("/")[-1])
				if "arm" in os.uname()[4]: download_tools().Downloader(acestreamengine_apk_arm,acefile,translate(40072),translate(40000))
				else: download_tools().Downloader(acestreamengine_apk_x86,acefile,translate(40072),translate(40000))
				import tarfile
				if tarfile.is_tarfile(acefile):
					download_tools().extract(acefile,pasta)
					download_tools().remove(acefile)
				xbmc.sleep(2000)
				mensagemok(translate(40000),translate(50021),pasta,translate(50016))
				mensagemok(translate(40000),translate(50023),translate(50024),translate(50025))
				settings.setSetting('engine_app','1')
			opcao= xbmcgui.Dialog().yesno(translate(40000), translate(70017),translate(70018))
			if opcao:
				if os.path.exists(os.path.join("sdcard","Download")):
					pasta = os.path.join("sdcard","Download")
					if "arm" in os.uname()[4]: acefile = os.path.join("sdcard","Download",android_aceplayer_arm.split("/")[-1])
					else: os.path.join("sdcard","Download",android_aceplayer_x86.split("/")[-1])
				else:
					dialog = xbmcgui.Dialog()
					pasta = dialog.browse(int(0), translate(40190), 'myprograms')
					if "arm" in os.uname()[4]: acefile = os.path.join(pasta,acestreamengine_apk_arm.split("/")[-1])
					else: acefile = os.path.join(pasta,acestreamengine_apk_x86.split("/")[-1])
				if "arm" in os.uname()[4]: download_tools().Downloader(android_aceplayer_arm,acefile,translate(70019),translate(40000))
				else: download_tools().Downloader(android_aceplayer_x86,acefile,translate(70019),translate(40000))
				import tarfile
				if tarfile.is_tarfile(acefile):
					download_tools().extract(acefile,pasta)
					download_tools().remove(acefile)
				xbmc.sleep(2000)
				mensagemok(translate(40000),translate(70020),pasta,translate(50016))
				opcao= xbmcgui.Dialog().yesno(translate(40000), translate(70021))
				if opcao:
					settings.setSetting('engine_app','2')							
			if latest_version: settings.setSetting('acestream_version',value=latest_version)
			mensagemok(translate(40000),translate(50022))
			return			
		else:
			mensagemok(translate(40000),translate(50017))
			return
