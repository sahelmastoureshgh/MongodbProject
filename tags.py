#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data model
and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with problematic characters.

"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Find and count number od k elements which are in above regular expression
def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k'] # find attribute K of tag "tag"
        if lower.findall(k):    # find  k in lower regular expression
            keys["lower"]+= 1   # count number of k which are in lower regular expression
        elif lower_colon.search(k):  # find  k in lower_colon regular expression
            keys["lower_colon"]+= 1  # count number of k which are in lower_colon re
        elif problemchars.search(k):
            keys["problemchars"]+= 1  # find  k in problemchars regular expression
        else:
            keys["other"]+= 1      # find  k in any other type 
        
    return keys


#Create a dictionary called keys which its key intiated with 0
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys


# Create a test case with example.osm 4.4MB dataset
def test():
    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5850, 'lower_colon': 1125, 'other': 226, 'problemchars': 0}


if __name__ == "__main__":
    test()