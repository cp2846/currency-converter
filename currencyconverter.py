#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib2
import re

#conversion script. Takes two arguments: mode and val
#mode is the type of currency e.g. '£', '$' or '€'
#val is the amount of currency, e.g. '400,000', '93.34', '0.39'
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
		converted_EUR = str(round(converted_EUR,2)) 
		converted_GBP = str(round(converted_GBP,2))
		return "$"+str(val)+" is £"+converted_GBP+", €"+converted_EUR
		
	elif mode == "£":
		converted_EUR = EUR / GBP * val
		converted_USD = converted_EUR * USD
		converted_EUR = str(round(converted_EUR,2))
		converted_USD = str(round(converted_USD,2))
		return "£"+str(val)+"  is $"+converted_USD+", €"+converted_EUR
		
	else:
		converted_GBP = GBP * val 
		converted_USD = val * USD
		converted_USD = str(round(converted_USD,2))
		converted_GBP = str(round(converted_GBP,2))
		return "€"+str(val)+" is £"+converted_GBP+", $"+converted_USD

		
#STRING PARSING ALGORITHM
def parseString(string):

	string = string.lower()
	
	detected_currency = []
	
	#get currency type, USD, GBP, or EUR
	type = r'([\$£€]{1})'
	#Get digits, commas allowed
	number = r'([\d+.,]+)'
	#qualifiers such as "thousand", "million", "m", "k", etc
	amounts = r'((million)?(m[\.\,\s])?(k[\.\,\s])?(thousand)?)'

	matcher = re.compile(type+number+r"[\s]*"+amounts)
	
	matches = re.findall(matcher, string)
	
	
	for i in matches:
		type = i[0]
		value = i[1]
		if __checkValid(value):
			value = __checkIfThousandsOrMillions(i[1],i[2])
			detected_currency.append([type,value])
	
	return detected_currency
			
def __checkValid(val):
	if val.count(".") >= 2:
		return False
	if val == "":
		return False
	return True

def __checkIfThousandsOrMillions(val,string):
	
	string = string.replace(",","")
	string = string.replace(" ","")
	string = string.replace("."," ")
	
	val = str(val)
	
	val = val.replace(",", "")
	
	if val.count(".") >= 2:
		pass
		
	val = float(val)
	if string == "million" or string == "m":
		val *= 1000000
	elif string == "thousand" or string == "k":
		val *= 1000
	
	return val



