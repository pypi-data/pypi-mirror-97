# Introduction 
Tiny python library to determine actual available Cisco AP models, and their full name, specific to the regulatory 
domain of the country you provide.
## How it works..
This module reads a spreadsheet from cisco.com, which is what is contains the data being used on:
https://www.cisco.com/c/dam/assets/prod/wireless/wireless-compliance-tool/index.html

This page is basically javascript, reading data from the spreadsheet, and then offering it in an interactive web form.
This is all nice and fine, but if you need software to pick the APs to order for Uzbekistan or some place, this library 
allows you to do just that, if you know the base model and country.

### full coverage...
So Ciscos list doesn't actually cover all countries, so to find the regulatory domain for countries
not in ciscos tool, we also use Junipers list to find the regulatory domains for undocumented countries.
This is semi-valid, since the domains are vendor agnostic - only cisco does not have any models for -W or World, but 
this way its at least indicated that a country is not matched by Cisco..

Junipers list is here: 

https://www.juniper.net/documentation/en_US/release-independent/junos/topics/reference/specifications/access-point-ax411-country-channel-support.html


# Usage

```
>>> from ciscoaplookup import *
>>> print(get_models_for('AIR-CAP1532E', 'Ukraine'))
[AIR-CAP1532E-E-K9]
# now lets try with a model not supported for Ukraine..
>>> print(get_models_for('AIR-CAP1552H', 'Ukraine'))
ValueError: Found AIR-CAP1552H for Ukraine - but no active regulatory domains?
>>> print(get_models())
['AIR-AP1800I', 'AIR-CAP1532I', 'AIR-AP1852', 'AIR-BLE-USB', 'AIR-AP1562D', 'AIR-AP3802E', 'AIR-OEAP1810', 
'AIR-AP1815W', 'AIR-CAP702W', 'AIR-AP2802I', 'AIR-AP2602', 'AIR-CAP1552S', 'AIR-AP1572EC', 'AIR-AP3602', 'AIR-AP1832', 
'AIR-AP1815T', 'AIR-AP1572IC', 'AIR-AP1815I', 'AIR-CAP702I', 'AIR-AP702I', 'AIR-RM3010L', 'AIR-SAP702I', 'AIR-CAP2702', 
'C9115AXI', 'AIR-AP1542D', 'AIR-AP1602', 'AIR-CAP3702', 'AIR-CAP1552H', 'AIR-AP3802P', 'AIR-CAP1532E', 'AIR-AP3702', 
'AIR-AP1542I', 'AIR-AP1562I', 'AIR-AP1562E', 'AIR-AP1810W', 'AIR-AP702W', 'C9117AXI', 'AIR-AP2702', 'AIR-AP3802I', 
'AIR-CAP1552WU', 'AIR-AP4800', 'AIR-AP1815M', 'AIR-AP1532', 'IW3702-2E-UXK9', 'IW3702-4E-X-K9', 'AIR-CAP3702P', 
'IW3702-4E-UXK9', 'AIR-AP1572EAC', 'AIR-AP1800S', 'IW3702-2E-X-K9', 'AIR-AP2802E', 'AIR-CAP1702']

```


# Test and Build
```
python -m unittest -v test.TestCiscoAPLookup
python setup.py sdist bdist_wheel
```
    
# Contribute
Go nuts..

# Future
Support of ISO countries would be nice - this requires a mapping as the underlying spreadsheet 
doesn't conform to iso :(
