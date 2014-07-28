# -*- coding: utf-8 -*-

""" p2p-streams
    2014 enen92 fightnight"""
    
import os

def readfile(filename):
	f = open(filename, "r")
	string = f.read()
	return string
	
def savefile(filename, contents):
	try:
		destination = os.path.join(pastaperfil, filename)
		fh = open(destination, 'wb')
		fh.write(contents)  
		fh.close()
		return
	except:
		print "Could not write to: %s" % filename
		return
    
def save(filename,contents):
	fh = open(filename, 'w')
	fh.write(contents)
	fh.close()
	return
