# Currency Converter
Python module that parses input strings and uses exchange rate values from the fixer.io API to convert between GBP, USD, and EUR. This is what is used to detect and convert currency values in the [Reddit Currency Bot](https://github.com/cp2846/reddit-currency-bot).


# Usage
This file can be imported into another project, i.e.:

    import currencyconverter

Inside the file are defined two methods:
    
    parseString(str)
    convert(mode, val)
    
Example usage:
    
    string = "This is an example string containing currency values like $4.43 million and £400,000"
    results = currencyconverter.parseString(string)
    
This would return a list containing sublists of the type of currency and their values:
    
    results = [['$',4430000],['£',400000]]
    
Which can be converted by calling on the convert method:

    for result in results:
        print currencyconverter.convert(result[0],result[1])
        
    >> $4,430,000 => £2,860,000 => €3,900,000
    >> £400,000 => $618,770.4 => €544,069.64

