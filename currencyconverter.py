#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib2
import re

"""
CURRENCY CONVERSION SCRIPT
Version: Python 2.7

EXAMPLE USAGE:
        import currencyconverter
        string = "this is a string containing values like $100 million"
        p = currencyconverter.Parser()
        c = currencyconverter.Converter()
        detected_currency = p.parse_string(string)
        for currency in detected_currency:
            print c.convert(currency)
            
>>>100000000USD=>6714400.0GBP=>91996000.0EUR

"""

# API calls to fixer.io for exchange rates
class Fixer:
    def load_rates(self, currencies, base):
        self.base = base
        self.url = "https://api.fixer.io/latest?base=" + base + "&symbols="
        #append currency types to GET parameters in URL
        self.url += ",".join(currencies)
        self.url = urllib2.urlopen(self.url)
        # return the data as a JSON object
        return json.load(self.url)
        
class Converter:
    def __init__(self):
        # List of currencies to convert. Edit if more are needed.
        self.convert_between = ["GBP","USD","EUR"]
    # accepts an object of currency type and returns a string containing
    # converted values
    def get_symbol(self, type):
        symbols = {
                    "USD": "$", 
                    "JPY": "¥", 
                    "GBP": "£", 
                    "EUR": "€",
                  }
        return symbols[type]
    def convert(self, money):
        self.output = str(money.value) + " " + money.type
        self.data = Fixer().load_rates(self.convert_between, money.type)
        for currency_type in self.convert_between:
            # skip base value, no need to convert
            if currency_type == money.type:
                continue
            else:
                # fetch exchange rate from JSON object, use it to make conversion
                converted_amount = round(self.data['rates'][currency_type] * money.value, 2)
            self.output += "=>" + self.get_symbol(currency_type) + str(converted_amount)
        return self.output
class Money:
    def __init__(self, value, symbol, magnitude):
        self.value = value
        # magnitude: string such as "million", "billion" etc. indicating the actual amount of currency
        self.magnitude = magnitude
        self.symbol = symbol
        self.type = self.get_type()
        # get true numerical value after factoring in magnitude
        self.value = self.convert_value_magnitude()
    def get_type(self):
        ordinals = {
                         36: "USD", 
                        172: "EUR", 
                        163: "GBP",
                        165: "JPY"
                    }
        try:
            return ordinals[ord(self.symbol)]
        except ValueError:
            print "Could not get type from '" + self.symbol + "': ord value not recognized"
    
        
    def convert_value_magnitude(self):
        if self.magnitude == "billion" or self.magnitude == "b":
            self.value *= 1000000000
        if self.magnitude == "million" or self.magnitude == "m":
            self.value *= 1000000
        if self.magnitude == "thousand" or self.magnitude == "k":
            self.value *= 1000
        return self.value
class Parser:
    # input: string to be analyzed
    # returns: list of detected currency values
    def parse_string(self, string):
        symbols = r'([\$£¥€])'
        number = r'([\d+.,]+)'
        amounts = r'((million|m|billion|b|k|thousand)?(\s|\.|\,|$))?'
        matcher = re.compile(symbols+number+r"[\s]*"+amounts, re.UNICODE | re.IGNORECASE)
        matches = re.findall(matcher, string)
        detected_currency = []
        for match in matches:
            # each match is a tuple containing the symbol, value, and magnitude of the currency
            symbol    = match[0]
            value     = match[1] 
            magnitude = match[3]
            try:
                value = value.replace(",","")
                value = float(value)
                detected_currency.append(Money(value, symbol, magnitude))
            except:
                print "Possible currency detected - could not parse due to errors:"
                print "Symbol: " + symbol
                print "value: " + value
        return detected_currency
