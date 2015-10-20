# currency-converter
Python script that parses input strings and uses exchange rate values from the fixer.io API to convert between GBP, USD, and EUR. This is a WIP version of a script that I plan on using in a bigger, later project.


# Usage
This file can be imported into another project, i.e.:

    import currencyconverter

Inside the file are defined two methods:
    
    parseString(str)
    convert(mode, val)
    
Example usage:
    
    string = "This is an example string containing currency values like $4.43 and £400,000"
    results = currencyconverter.parseString(string)
    
This would return a list containing sublists of the type of currency and their values:
    
    results = [['$','4.43'],['£','400000']]
    
Which can be converted by calling on the convert method:

    for result in results:
        print currencyconverter.convert(result[0],result[1])
        
    >> $4.43 is £2.86, €3.9
    >> £400000 is $618770.4, €544069.64
