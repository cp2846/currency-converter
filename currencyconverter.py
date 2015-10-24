#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib2
import re


def convert(base, val):

	val = float(val)
	#Make API call to fixer.io, load JSON data for exchange rates
	url = urllib2.urlopen('http://api.fixer.io/latest?symbols=USD,GBP')
	data = json.load(url)
	USD = data['rates']['USD']
	GBP = data['rates']['GBP']
	EUR = base_rate = 1.00

	convert_between = [
					['£',GBP],
					['$',USD],
					['€',EUR]
				]
	
	for type in convert_between:
		if type[0] == base:
			base_rate = type[1]
	
	output = base+"{:,}".format(val)
	
	for type in convert_between:
		if type[1] == base_rate:
			continue
		else:
			converted_amount =  round(type[1] / base_rate * val,2)
			converted_amount = "{:,}".format(converted_amount)
		output += " => "+type[0]+str(converted_amount)
		
	return output

def parseString(string):
	#REGEX PARAMETERS
	type = r'([\$£€])'
	number = r'([(\d+),]+(\.\d{2})?)'
	amounts = r'((million|m|billion|b|k|thousand)?(\s|\.|\,|$))?'
	matcher = re.compile(type+number+r"[\s]*"+amounts, re.UNICODE | re.IGNORECASE)
	matches = re.findall(matcher, string)
	
	detected_currency = []
	
	for match in matches:
		type = match[0]
		value = match[1]
		magnitude = match[4]
		
		if __checkValid(value):
			value = __checkMagnitude(value,magnitude)
			detected_currency.append([type,value])
	
	return detected_currency
	
def __checkValid(val):
	val = val.replace(",","")
	try:
		val = float(val)
		return True
	except:
		return False
	
def __checkMagnitude(val,string):
	val = val.replace(",", "")
	val = float(val)
	
	if string == "billion" or string == "b":
		val *= 1000000000
	if string == "million" or string == "m":
		val *= 1000000
	if string == "thousand" or string == "k":
		val *= 1000
	return val

