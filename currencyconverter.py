#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib2

#conversion script. Takes two arguments: mode and val
#mode is the type of currency e.g. £, $ or €
#val is the amount of currency, e.g. 400,000, 93.34, 0.39
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
		return "$"+str(val)+" USD is £"+converted_GBP+", €"+converted_EUR
		
	elif mode == u"£":
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
def parseString(str):
	
	str = str.decode('utf-8')
	detected_currency = []
	started = False
	i = 0
	
	for ch in str:
		if started:
			#check ordinal value of character to see whether or not it's a digit
			if ord(ch) >= 48 and ord(ch) <= 57:
				detected_currency[i][1] += ch

			elif ch == ".":
				#If there's already a demical point in this index in the result, assume it is a period and move on
				if not "." in detected_currency[i][1]:
					detected_currency[i][1] += "."

			#ignore commas e.g. $3,830 <- don't want this to be interpreted as $3
			elif ch == ",":
				continue
						
			else:
				started = False
				
		elif ch == "$":
			started = True
			__addNewItem(detected_currency,"$")
			i = len(detected_currency)-1
			
		elif ch == u"€":
			started = True
			__addNewItem(detected_currency,u"€")
			i = len(detected_currency)-1
			
		elif ch == u"£":
			started = True
			__addNewItem(detected_currency,u"£")
			i = len(detected_currency)-1
		
	__removeEmpty(detected_currency)
			
	return detected_currency

#clean up list - remove empty sublists
def __removeEmpty(currency_list):
	current = len(currency_list)-1
	while current >= 0:
		if currency_list[current][1] == "":
			currency_list.pop(current)
		current -= 1
	return currency_list
	
#currency found, add sublist to list		
def __addNewItem(currency_list,currency_type):
	currency_list.append(["",""])
	i = len(currency_list)-1
	currency_list[i][0] = currency_type
			
