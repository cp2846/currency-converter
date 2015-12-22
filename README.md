# Currency Converter
Python module that parses input strings and uses exchange rate values from the fixer.io API to convert between GBP, USD, and EUR. This is what is used to detect and convert currency values in the [Reddit Currency Bot](https://github.com/cp2846/reddit-currency-bot).


# Usage
This file can be imported into another project, i.e.:

    import currencyconverter

Create string parser and converter objects:
    
    p = Parser()
    c = Converter()
    
Example usage:
    
    string = "This is an example string containing currency values like $4.43 million and £400,000"
    detected_currency = p.parse_string(string)
    
This would return a list containing "Money" class objects with value, symbol, and type fields.
    
Call the convert method to convert them to other types of currency:
    for found in detected_currency:
        print c.convert(found)
        
    >> USD4,430,000 => GBP2,860,000 => EUR3,900,000
    
    >> GBP400,000 => USD618,770.4 => EUR544,069.64

#TODO
* Add support for more currencies
* detect more obscure ways of formatting currency values, e.g. when formatted as a text string ("one hundred dollars", etc.)
* update Reddit conversion bot to use new version of currencyconverter
