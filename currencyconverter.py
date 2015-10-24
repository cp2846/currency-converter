#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib2
import re

#conversion script. Takes two arguments: mode and val
#mode is the type of currency e.g. '£', '$' or '€'
#val is the amount of currency, e.g. '400000', '93.34', '0.39'
def convert(mode, val):

	val = float(val)
	#Make API call to fixer.io, load JSON data for exchange rates
	url = urllib2.urlopen('http://api.fixer.io/latest?symbols=USD,GBP')
	data = json.load(url)
	USD = data['rates']['USD']
	GBP = data['rates']['GBP']
	EUR = 1.00

	converted_GBP = converted_USD = converted_EUR = 0
	
	if mode == "$":
		converted_EUR = EUR / USD * val
		converted_GBP = converted_EUR * GBP
		#format output with commas as thousands separators, round to two decimal places
		converted_EUR = "{:,}".format(round(converted_EUR,2))
		converted_GBP = "{:,}".format(round(converted_GBP,2))
		val = "{:,}".format(val)
		
		return "$"+val+" => £"+converted_GBP+" or €"+converted_EUR
		
	elif mode == "£":
		converted_EUR = EUR / GBP * val
		converted_USD = converted_EUR * USD
		converted_EUR = "{:,}".format(round(converted_EUR,2))
		converted_USD = "{:,}".format(round(converted_USD,2))
		val = "{:,}".format(val)
		return "£"+val+" => $"+converted_USD+" or €"+converted_EUR
		
	else:
		converted_GBP = GBP * val 
		converted_USD = val * USD
		converted_USD = "{:,}".format(round(converted_USD,2))
		converted_GBP = "{:,}".format(round(converted_GBP,2))
		val = "{:,}".format(val)
		return "€"+val+" => £"+converted_GBP+"or $"+converted_USD

		

def parseString(string):
	
	#hack to get some regexes to register correctly when term is at end of string
	string += " "
	#REGEX PARAMETERS
	type = r'([\$£€])'
	number = r'([\d+.,]+)'
	amounts = r'((million)?(m[\.\,\s])?(k[\.\,\s])?(thousand)?(billion)?(b[\.\,\s])?)'
	matcher = re.compile(type+number+r"[\s]*"+amounts, re.UNICODE | re.IGNORECASE)
	matches = re.findall(matcher, string)
	
	detected_currency = []
	
	for match in matches:
		type = match[0]
		value = match[1]
		magnitude = match[2]
		
		if __checkValid(value):
			value = __checkMagnitude(value,magnitude)
			detected_currency.append([type,value])
	
	return detected_currency
	

	
def __checkValid(val):

	if val.count(".") >= 2:
		return False
		
	return True
	
def __checkMagnitude(val,string):
	string = __stripChars(string)
	val = str(val)
	val = val.replace(",", "")
	val = float(val)
	
	if string == "billion" or string == "b":
		val *= 1000000000
	
	if string == "million" or string == "m":
		val *= 1000000
		
	elif string == "thousand" or string == "k":
		val *= 1000
	
	return val

#strips characters like " ", ".", etc. from "million,", "thousand " etc.
def __stripChars(string):
	string = string.replace(",","")
	string = string.replace(" ","")
	string = string.replace("."," ")
	
	return string
	
