# -*- coding: utf-8 -*-

""" Plexus  (c)  2015 enen92

    This file contains the functions for file handling
    
    Functions:
    
    readfile(filename) -> Function to read text files given the full path
    savefile(filename, contents) -> Function to write/save text files given the text file name
    save(filename,contents) -> Function to write/save text to a file given the text file full path
   	
"""
    
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
		print("Could not write to: %s" % filename)
		return
    
def save(filename,contents):
	fh = open(filename, 'w')
	fh.write(contents)
	fh.close()
	return
