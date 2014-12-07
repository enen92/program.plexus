# -*- coding: utf-8 -*-

""" p2p-streams  (c)  2014 enen92 fightnight

    This file contains functions related to time manipulation
    
    Functions:
    
    translate_months(month) -> Receives the month name in english and returns an integer corresponding to the month number. Used in parsers.
   	
"""

def translate_months(month):
	if month == "January": return 1
	elif month == "February": return 2
	elif month == "March": return 3
	elif month == "April": return 4
	elif month == "May": return 5
	elif month == "June": return 6
	elif month == "July": return 7
	elif month == "August": return 8
	elif month == "September": return 9
	elif month == "October": return 10
	elif month == "November": return 11
	elif month == "December": return 12
	else: return
