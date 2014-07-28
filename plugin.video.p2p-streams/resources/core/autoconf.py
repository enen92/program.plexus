# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    Sopcast and Acestream modules setup - Addon first boot

"""
     
import xbmc,xbmcgui,xbmcplugin
import tarfile,os,re,sys,subprocess
from utils.pluginxbmc import *
from utils.webutils import download_tools


""" Platform dependent files downloaded during the addon configuration"""

#Linux Armv6 (Raspberry PI)
sopcast_raspberry = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/sopcast-raspberry.tar.gz"
acestream_generic_raspberry = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/acestream-raspberry.tar.gz"
acestream_openelec_raspberry = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/RaspberryPi/openelec-acestream.tar.gz"
#Linux Armv7 packages
acestream_mxlinux = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Armv7/mxlinux/mxlinux_armv7_acestream.tar.gz"
acestream_armv7_openelec = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Armv7/openelec/openelec-acestream.tar.gz"
acestream_armv7_xbian = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Armv7/xbian/xbian_acestream.tar.gz"
#Linux i386 and x86_64 (including openelec
sopcast_linux_generico =  "https://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/Sopcastx86_64i386/sopcast_linux.tar.gz"
openelecx86_64_package = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/x86_64/Openelec/openelec_x86_64_userdata.tar.gz"
openeleci386_package = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Linux/i386/openelec/openeleci386-acestream-sopcast.tar.gz"
#Android
sopcast_apk = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/SopCast.apk.tar.gz"
acestreamengine_apk = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Android/acestream-2.1.11.apk.tar.gz"
#Mac OSX
osx_x86_64 = "https://p2p-strm.googlecode.com/svn/trunk/Modules/MacOsx/MacOSX_x86_64_ace_and_sop.tar.gz"
osx_i386 = "http://p2p-strm.googlecode.com/svn/trunk/Modules/MacOsx/MacOSX_i386_ace_and_sop.tar.gz"
#Windows Files
acestream_windows = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Windows/windows-aceengine2-3.tar.gz"
srvany_executable = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Windows/srvany.tar.gz"
srvany_permissions = "http://p2p-strm.googlecode.com/svn/trunk/Modules/Windows/sopcastp2p-permissions.txt"


def autoconf():
	#Configuration for LINUX 
	if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android') and not settings.getSetting('force_android') == "true":
		print "Detected OS: Linux"
		#Linux Armv6
		if os.uname()[4] == "armv6l":
			try:
				if re.search(os.uname()[1],"openelec",re.IGNORECASE): acestream_rpi = acestream_openelec_raspberry
				elif re.search(os.uname()[1],"raspbmc",re.IGNORECASE): acestream_rpi = acestream_generic_raspberry
				elif os.path.isfile("/etc/xbian_version"): acestream_rpi = acestream_generic_raspberry
				elif "ARCH" in os.uname()[2]:
					acestream_rpi = acestream_generic_raspberry
					settings.setSetting('python_cmd',value='python2')
				else:
					mensagemok(traducao(40000),"Sorry could not detect your OS.","Select it from the next list")
					OS_list = ["OpenELEC","Raspbmc","Xbian","Pipplware","Arch Linux Arm"]
					url_packagerpi_list = [acestream_openelec_raspberry, acestream_generic_raspberry, acestream_generic_raspberry,acestream_generic_raspberry, acestream_generic_raspberry]
					OS_Rpi_choose = xbmcgui.Dialog().select
					choose=OS_Rpi_choose('Select your OS',OS_list)
					if choose > -1:
						acestream_rpi= url_packagerpi_list[choose]
						if OS_list[choose] == "Arch Linux Arm": settings.setSetting('python_cmd',value='python2')
			except: acestream_rpi = "" #da erro de script no windows, workaround porque diferente rpi
			print "Detected Platform Raspberry PI"
			#Sop

			SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
			download_tools().Downloader(sopcast_raspberry,SPSC_KIT,traducao(40025),traducao(40000))
            
			if tarfile.is_tarfile(SPSC_KIT):
				path_libraries = os.path.join(pastaperfil,"sopcast")
				download_tools().extract(SPSC_KIT,path_libraries)
				xbmc.sleep(500)
				download_tools().remove(SPSC_KIT)

            		#Ace
			SPSC_KIT = os.path.join(addonpath,acestream_rpi.split("/")[-1])
			download_tools().Downloader(acestream_rpi,SPSC_KIT,traducao(40026),traducao(40000))
        
			if tarfile.is_tarfile(SPSC_KIT):
				path_libraries = os.path.join(pastaperfil,"acestream")
				download_tools().extract(SPSC_KIT,path_libraries)
				xbmc.sleep(500)
				download_tools().remove(SPSC_KIT)

			settings.setSetting('autoconfig',value='false')


                elif os.uname()[4] == "armv7l":
			if re.search(os.uname()[1],"openelec",re.IGNORECASE):
				OS_Choose = "OpenELEC"
			elif os.path.isfile("/etc/xbian_version"):
				OS_Choose = "Xbian"
			else:
                		mensagemok(traducao(40000),traducao(40109),traducao(40110))
                		OS_list = ["MXLinux","OpenELEC","Xbian"]
                		choose=xbmcgui.Dialog().select('Select your OS',OS_list)
                		if choose > -1:
                			OS_Choose= OS_list[choose]

			#Linux armv7 configuration according to platform

			#MXLINUX

                	if OS_Choose == "MXLinux":
				acestream_installed = False
				sopcast_installed = False
               			print "MXLinux"
               			SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
               			download_tools().Downloader(sopcast_raspberry,SPSC_KIT,traducao(40025),traducao(40000))
				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"sopcast")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					sopcast_installed = True

				SPSC_KIT = os.path.join(addonpath,acestream_mxlinux.split("/")[-1])
				download_tools().Downloader(acestream_mxlinux,SPSC_KIT,traducao(40026),traducao(40000))
        			if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"acestream")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					acestream_installed = True
				if acestream_installed and sopcast_installed:
					settings.setSetting('autoconfig',value='false')	

			#OPENELEC

                	if OS_Choose == "OpenELEC":
				acestream_installed = False
				sopcast_installed = False
                		print "Openelec armv7 platform detected"
                		SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
                		download_tools().Downloader(sopcast_raspberry,SPSC_KIT,traducao(40025),traducao(40000))
				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"sopcast")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					sopcast_installed = True
				SPSC_KIT = os.path.join(addonpath,acestream_armv7_openelec.split("/")[-1])
				download_tools().Downloader(acestream_armv7_openelec,SPSC_KIT,traducao(40026),traducao(40000))
        			if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"acestream")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					acestream_installed = True
				if acestream_installed and sopcast_installed:
					settings.setSetting('autoconfig',value='false')	

			#XBIAN
               		if OS_Choose == "Xbian":
				acestream_installed = False
				sopcast_installed = False
               			print "Xbian armv7 platform detected"
               			SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
               			download_tools().Downloader(sopcast_raspberry,SPSC_KIT,traducao(40025),traducao(40000))
				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"sopcast")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					sopcast_installed = True
				SPSC_KIT = os.path.join(addonpath,acestream_armv7_xbian.split("/")[-1])
				download_tools().Downloader(acestream_armv7_xbian,SPSC_KIT,traducao(40026),traducao(40000))
       				if tarfile.is_tarfile(SPSC_KIT):
					path_libraries = os.path.join(pastaperfil,"acestream")
					download_tools().extract(SPSC_KIT,path_libraries)
					xbmc.sleep(500)
					download_tools().remove(SPSC_KIT)
					acestream_installed = True
				if acestream_installed and sopcast_installed:
					settings.setSetting('autoconfig',value='false')	


			
		elif (os.uname()[4] == "x86_64" and re.search(os.uname()[1],"openelec",re.IGNORECASE)) or settings.getSetting('openelecx86_64') == "true":
			settings.setSetting('openelecx86_64',value='true')
			print "Detected OpenELEC x86_64"
			SPSC_KIT = os.path.join(addonpath,openelecx86_64_package.split("/")[-1])
			download_tools().Downloader(openelecx86_64_package,SPSC_KIT,traducao(40112),traducao(40000))
			import tarfile
			if tarfile.is_tarfile(SPSC_KIT):
				download_tools().extract(SPSC_KIT,pastaperfil)
				xbmc.sleep(500)
				download_tools().remove(SPSC_KIT)
			settings.setSetting('autoconfig',value='false')

		elif (os.uname()[4] == "i386" and re.search(os.uname()[1],"openelec",re.IGNORECASE)) or (os.uname()[4] == "i686" and re.search(os.uname()[1],"openelec",re.IGNORECASE)) or settings.getSetting('openeleci386') == "true":
			settings.setSetting('openeleci386',value='true')
			print "Detected OpenELEC i386"
			SPSC_KIT = os.path.join(addonpath,openeleci386_package.split("/")[-1])
			download_tools().Downloader(openeleci386_package,SPSC_KIT,traducao(40112),traducao(40000))
			import tarfile
			if tarfile.is_tarfile(SPSC_KIT):
				download_tools().extract(SPSC_KIT,pastaperfil)
				xbmc.sleep(500)
				download_tools().remove(SPSC_KIT)
			settings.setSetting('autoconfig',value='false')		
	
		else:
			if os.uname()[4] == "x86_64":
				opcao= xbmcgui.Dialog().yesno(traducao(40000), traducao(40113))
				if opcao: 
					settings.setSetting('openelecx86_64',value='true')
					autoconf()
			elif os.uname()[4] == "i386" or os.uname()[4] == "i686":
				opcao= xbmcgui.Dialog().yesno(traducao(40000), traducao(600023))
				if opcao: 
					settings.setSetting('openeleci386',value='true')
					autoconf()

			else: mensagemok(traducao(40000),traducao(40056))
			

			#Linux but not openelec i386 nor openelec x86_64 - General Linux platforms configuration
			
			if settings.getSetting('openeleci386') == "false" and settings.getSetting('openelecx86_64') == "false":

				print "Detected Other Linux Plataform"

            		#Sop
            		#Download and extract sopcast-bundle
				SPSC_KIT = os.path.join(addonpath,sopcast_linux_generico.split("/")[-1])
				download_tools().Downloader(sopcast_linux_generico,SPSC_KIT,traducao(40025),traducao(40000))
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
	   		 
	   		 #Ace
	   		 
				import subprocess
				proc_response = []
				proc = subprocess.Popen(['whereis','acestreamengine'],stdout=subprocess.PIPE)
				for line in proc.stdout:
					print "Output of acestream subprocess check",line.rstrip()
					proc_response.append(line.rstrip())
					if "acestreamengine: /" in str(proc_response):
						print "Acestream engine is already installed"
						try:
							proc.kill()
							proc.wait()
						except:pass
					else:
						mensagemok(traducao(40031),traducao(40027),traducao(40028) + linkwiki,traducao(40029))
						sys.exit(0)
				settings.setSetting('autoconfig',value='false')


	elif xbmc.getCondVisibility('system.platform.windows'):
		print "Detected OS: Windows"
		if not xbmcvfs.exists(pastaperfil): xbmcvfs.mkdir(pastaperfil)
        	#Sop
		import ctypes
                is_admin=ctypes.windll.shell32.IsUserAnAdmin() != 0
                if is_admin == False:
                    mensagemok(traducao(40000),traducao(40158),traducao(40159))
                else:
		    import subprocess
                    cmd = ['sc','delete','sopcastp2p']
                    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                    for line in proc.stdout:
                        print "linha " + line.rstrip()
                    xbmc.sleep(1000)
                    ret = mensagemprogresso.create(traducao(40000),traducao(40000))
                    mensagemprogresso.update(0,traducao(40160),"  ")
                    xbmc.sleep(1000)
                    import _winreg
                    aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                    try:
                        aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
                        name, value, type = _winreg.EnumValue(aKey, 0)
                        sopcast_executable = value
                        print "Installation executable of sopcast was found: " + sopcast_executable
                        _winreg.CloseKey(aKey)
                        mensagemprogresso.update(10,traducao(40160),traducao(40161))
                    except:
                        sopcast_executable = ""
                        mensagemok(traducao(40000),traducao(40162),traducao(40163))
                    if not sopcast_executable: pass
                    else:
                        xbmc.sleep(1000)
                        mensagemprogresso.update(20,traducao(40164),"  ")
                        xbmc.sleep(1000)
                        print "Getting windows users IDS"
                        aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                        aKey = _winreg.OpenKey(aReg, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList')
                        users = []
                        for i in range(1024):
                            try:
                                asubkey=_winreg.EnumKey(aKey,i)
                                print asubkey
                                aKeydois = _winreg.OpenKey(aReg, os.path.join('SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList',asubkey))
                                val=_winreg.QueryValueEx(aKeydois, "ProfileImagePath")
                                try:
                                    print val[0]
                                except:
                                    print "Notice: User with strange characters, print cmd ignored."
                                if "Windows" in val[0] or "%systemroot%" in val[0]:
                                    pass
                                else:
                                    users.append(asubkey)
                            except:
                                pass
                        if not users:
                            mensagemok(traducao(40000),traducao(40165))
                        else:
                            mensagemprogresso.update(30,traducao(40164),traducao(40161))
                            xbmc.sleep(200)
                            mensagemprogresso.update(30,traducao(40166),"   ")
                            xbmc.sleep(1000)
                            print "System Users", users
			    srvanytargz = os.path.join(sopcast_executable.replace("SopCast.exe",""),"srvany.tar.gz")                               
                            download_tools().Downloader(srvany_executable,srvanytargz,traducao(40167),traducao(40000)) 
                            xbmc.sleep(1000)
                            import tarfile
                            if tarfile.is_tarfile(srvanytargz):
                                path_libraries = sopcast_executable.replace("SopCast.exe","")
                                download_tools().extract(srvanytargz,path_libraries)
                                download_tools().remove(srvanytargz)
                            xbmc.sleep(1000)
                            ret = mensagemprogresso.create(traducao(40000),traducao(40000))
                            xbmc.sleep(200)
                            mensagemprogresso.update(35,traducao(40168),"  ")
                            xbmc.sleep(1000)
                            import subprocess
                            cmd = ['sc','create','sopcastp2p','binpath=',os.path.join(os.path.join(sopcast_executable.replace("SopCast.exe","")),'srvany.exe')]
                            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                            servicecreator = False
                            for line in proc.stdout:
                                print "linha " + line.rstrip()
                                servicecreator = True
                            if servicecreator == False:
                                mensagemok(traducao(40000),traducao(40169))
                            else:
                                mensagemprogresso.update(40,traducao(40168),traducao(40161))
                                xbmc.sleep(1000)
                                mensagemprogresso.update(45,traducao(40170),"  ")
                                xbmc.sleep(1000)
                                print "Trying to modify regedit...."
                                try:
                                    aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
                                    key = _winreg.CreateKey(aReg, r'SYSTEM\CurrentControlSet\Services\sopcastp2p\Parameters')
                                    _winreg.SetValueEx(key, 'AppDirectory', 0, _winreg.REG_SZ, os.path.join(sopcast_executable.replace("SopCast.exe","")))
                                    _winreg.SetValueEx(key, 'Application', 0, _winreg.REG_SZ, os.path.join(os.path.join(sopcast_executable.replace("SopCast.exe","")),"SopCast.exe"))
                                    _winreg.SetValueEx(key, 'AppParameters', 0, _winreg.REG_SZ, "sop://")
                                    mensagemprogresso.update(50,traducao(40170), traducao(40161))
                                    regedit = True
                                except:
                                    mensagemok(traducao(40000),traducao(40171))
                                    regedit = False
                                if regedit == False: pass
                                else:
                                    xbmc.sleep(1000)
                                    mensagemprogresso.update(50,traducao(40172), "   ")
                                    cmd = ['sc','sdshow','sopcastp2p']
                                    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                                    lines = []
                                    for line in proc.stdout:
					print line.rstrip()
                                        if line.rstrip() != "" and "(" in line.rstrip(): lines.append(line.rstrip())
                                        else: pass
				    print lines
				    print len(lines)
                                    if len(lines) != 1: mensagemok(traducao(40000),traducao(40173))
                                    else:
                                        linha_arr = []
                                        for user in users:
                                            linha_arr.append('(A;;RPWPCR;;;' + user + ')')
                                        linha_add = ''
                                        for linha in linha_arr:
                                            linha_add += linha
                                        print "line peace to add: " + linha_add
                                        linha_final = lines[0].replace("S:(",linha_add + "S:(")
                                        print "Final line: " + linha_final
                                        permissions = False
                                        xbmc.sleep(500)
                                        mensagemprogresso.update(60,traducao(40172), traducao(40161))
                                        xbmc.sleep(500)
                                        mensagemprogresso.update(60,traducao(40174), "   ")
                                        cmd = ['sc','sdset','sopcastp2p',linha_final]
                                        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                                        for line in proc.stdout:
                                            print line.rstrip()
                                            permissions = True
                                        if permissions == False: mensagemok(traducao(40000),traducao(40175))
                                        else:
                                            mensagemprogresso.update(70,traducao(40174), traducao(40161))
                                            xbmc.sleep(1000)
                                            mensagemprogresso.update(70,traducao(40176), "   ")
                                            print "Trying to set sopcastp2p service regedit permissions..."
                                            download_tools().Downloader(srvany_permissions,os.path.join(pastaperfil,"sopcastp2p-permissions.txt"),traducao(40177),traducao(40000))
                                            xbmc.sleep(500)
                                            ret = mensagemprogresso.create(traducao(40000),traducao(40000))
                                            xbmc.sleep(500)
                                            mensagemprogresso.update(80,traducao(40178), "   ")
                                            xbmc.sleep(1000)
                                            cmd = ['regini',os.path.join(pastaperfil,"sopcastp2p-permissions.txt")]
                                            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                                            for line in proc.stdout:
                                                print line.rstrip()
                                            mensagemprogresso.update(90,traducao(40178), traducao(40178))
                                            mensagemprogresso.update(100,traducao(40179), "   ")
                                            xbmc.sleep(2000)
                                            mensagemprogresso.close()
        #Ace
		SPSC_KIT = os.path.join(addonpath,acestream_windows.split("/")[-1])
		download_tools().Downloader(acestream_windows,SPSC_KIT,traducao(40026),traducao(40000))
		import tarfile
		if tarfile.is_tarfile(SPSC_KIT):
			path_libraries = os.path.join(pastaperfil)
			download_tools().extract(SPSC_KIT,path_libraries)
			download_tools().remove(SPSC_KIT)
		settings.setSetting('autoconfig',value='false')
    
	elif xbmc.getCondVisibility('System.Platform.OSX'):
		print "Detected OS: Mac OSX"
		available = False
		if os.uname()[-1] == "x86_64":
			mac_package = osx_x86_64
			available = True
		elif os.uname()[-1] == "i386":
			mac_package = osx_i386
			available = True
		else:
			available = False
		if available == True:		
			if not xbmcvfs.exists(pastaperfil):
				xbmcvfs.mkdir(pastaperfil)		
			MAC_KIT = os.path.join(addonpath,mac_package.split("/")[-1])
			download_tools().Downloader(mac_package,MAC_KIT,traducao(40112),traducao(40000))
			import tarfile
			if tarfile.is_tarfile(MAC_KIT):
				path_libraries = os.path.join(pastaperfil)
				download_tools().extract(MAC_KIT,pastaperfil)
				download_tools().remove(MAC_KIT)
				sp_sc_auth = os.path.join(pastaperfil,"sopcast","sp-sc-auth")
				st = os.stat(sp_sc_auth)
				import stat
				os.chmod(sp_sc_auth, st.st_mode | stat.S_IEXEC)
				settings.setSetting('autoconfig',value='false')
		else:
			mensagemok(traducao(40000),traducao(600014))
			sys.exit(0)
				
	elif xbmc.getCondVisibility('System.Platform.Android') or settings.getSetting('force_android') == "true":

		print "Detected OS: Android"
		#Sopcast configuration
		print "Starting SopCast Configuration"

		#Moving sopclient to ext4 hack - tks steeve from xbmctorrent

		sopclient_builtin_location = os.path.join(addonpath,"resources","binaries","sopclient")

		#Hack to get current xbmc app id
		xbmcfolder=xbmc.translatePath(addonpath).split("/")
		print "XBMC folder",xbmcfolder

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
			print i
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
				opcao= xbmcgui.Dialog().yesno(traducao(40000), traducao(50011),traducao(50012))
				if not opcao:
					settings.setSetting('external_sopcast',value='1')
					settings.setSetting('force_android',value='true')
					sopcast_installed = True
					mensagemok(traducao(40000),traducao(50014))
				else:
					mensagemok(traducao(40000),traducao(50013))
					if xbmcvfs.exists(os.path.join("sdcard","Download")):
						pasta = os.path.join("sdcard","Download")
						sopfile = os.path.join("sdcard","Download",sopcast_apk.split("/")[-1])
					else:
						dialog = xbmcgui.Dialog()
						pasta = dialog.browse(int(0), traducao(40190), 'myprograms')
						sopfile = os.path.join(pasta,sopcast_apk.split("/")[-1])
					download_tools().Downloader(sopcast_apk,sopfile,traducao(40073),traducao(40000))
					if tarfile.is_tarfile(sopfile):
						download_tools().extract(sopfile,pasta)
						download_tools().remove(sopfile)
					mensagemok(traducao(40000),traducao(50015),pasta,traducao(50016))
					sopcast_installed = True
					settings.setSetting('external_sopcast',value='0')
					mensagemok(traducao(40000),traducao(50014))

		else:
			mensagemok(traducao(40000),traducao(50017))

		#acestream config for android

		if sopcast_installed == True:
			mensagemok(traducao(40000),traducao(50018),traducao(50019),traducao(50020))
			if xbmcvfs.exists(os.path.join("sdcard","Download")):
				pasta = os.path.join("sdcard","Download")
				acefile = os.path.join("sdcard","Download",acestreamengine_apk.split("/")[-1])
			else:
				dialog = xbmcgui.Dialog()
				pasta = dialog.browse(int(0), traducao(40190), 'myprograms')
				acefile = os.path.join(pasta,acestreamengine_apk.split("/")[-1])
			download_tools().Downloader(acestreamengine_apk,acefile,traducao(40072),traducao(40000))
			if tarfile.is_tarfile(acefile):
				download_tools().extract(acefile,pasta)
				download_tools().remove(acefile)
			xbmc.sleep(2000)
			mensagemok(traducao(40000),traducao(50021),pasta,traducao(50016))
			mensagemok(traducao(40000),traducao(50022))
			mensagemok(traducao(40000),traducao(50023),traducao(50024),traducao(50025))
			settings.setSetting('autoconfig',value='false')	
