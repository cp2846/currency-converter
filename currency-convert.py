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
	
	#if the mode is USD, convert USD value to GBP and EUR
	if mode == "$":
		converted_EUR = EUR / USD * val
		converted_GBP = converted_EUR * GBP
		#round to 2 decimal places and converted to string
		converted_EUR = str(round(converted_EUR,2)) 
		converted_GBP = str(round(converted_GBP,2))
		#return result
		return "$"+str(val)+" USD is £"+converted_GBP+", €"+converted_EUR
		
	#if mode is pounds, convert to USD and EUR
	elif mode == u"£":
		converted_EUR = EUR / GBP * val
		converted_USD = converted_EUR * USD
		converted_EUR = str(round(converted_EUR,2))
		converted_USD = str(round(converted_USD,2))
		return "£"+str(val)+"  is $"+converted_USD+", €"+converted_EUR
		
	#if mode is EUR, convert to USD and GBP
	else:
		converted_GBP = GBP * val 
		converted_USD = val * USD
		#round to 2 decimal places and converted to string
		converted_USD = str(round(converted_USD,2))
		converted_GBP = str(round(converted_GBP,2))
		#return result
		return "€"+str(val)+" is £"+converted_GBP+", $"+converted_USD

		
#STRING PARSING ALGORITHM
def parseString(str):
	
	#convert parsed string to unicode
	str = str.decode('utf-8')
	
	#container for all of the currency values. This is a nested list
	result = []
	
	#an array containing digits as characters
	digits = ['0','1','2','3','4','5','6','7','8','9']
	
	started = False
	
	#String parsing algorithm
	for ch in str:
		
		if started:
		
			#checks if the current character in the string is a digit, and if so, adds it to sublist
			if ch in digits:
				result[i][1] += ch

			#check to see if character in string is a decimal point
			elif ch == ".":
				
				#If there's already a demical point in this index in the result, assume it is a period and move on
				if not "." in result[i][1]:
					result[i][1] += "."
				
			#ignore commas e.g. $3,830 <- don't want this to be interpreted as $3
			elif ch == ",":
				continue
						
			#if character is not a digit or a decimal/period, move on
			else:
				started = False
				
		#new dollar value
		elif ch == "$":
			started = True
			#append new sublist to list, update i
			result.append(["",""])
			i = len(result)-1
			result[i][0] = "$"
			
		#new EUR value
		elif ch == u"€":
			started = True
			result.append(["",""])
			i = len(result)-1
			result[i][0] = u"€"
			
		#new GBP value
		elif ch == u"£":
			started = True
			result.append(["",""])
			i = len(result)-1
			result[i][0] = u"£"
		
	#clean up list - remove empty sublists
	count = len(result)-1
	while count >= 0:
		if result[count][1] == "":
			result.pop(count)
			count -= 1
		else:
			count -= 1
			
	#return results
	return result


	
	
#TESTS. IGNORE FOR NOW	
tests = ["This is a string containing a sub-string $4.43 which is a value in USD.","This is a string containing no currency value.","$400.38.3","this is some $gibberish that I don't want my script to confuse for a currency-containing string","$380 and the rest was $38","$$$$$","This is some euro right here bruh €400","£43493, this is too much for me!"]

for test in tests:
	count = 0
	output = ""
	results = parseString(test)
	if len(results) > 0:
		for result in results:
			try:
				output += convert(result[0],result[1])
				count += 1
			except:
				print "An error has occured"
	if count > 0:
		print output
	

raw_input("Press Enter")