#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output should be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

"""
import xml.etree.ElementTree as ET
import pprint
# Count number of tags and put each tag in the dictionary called tags
# key is tag name , value is number of tags
def count_tags(filename):
        # create an empty dictionary
        tags={}
        osm_file = open(filename, "r") #read file
        for event,elem in ET.iterparse(osm_file): 
            if elem.tag in tags:
                tags[elem.tag]=tags[elem.tag]+1  # count number of each unique tags
            else:
                tags[elem.tag]=1
            elem.clear()    
        return tags        


# test case 
def test():
    # example.osm is 4.4 MB file from boston,MA area
    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 1227,
                     'nd': 21826,
                     'node': 18581,
                     'osm': 1,
                     'relation': 61,
                     'tag': 7201,
                     'way': 2900}

    

if __name__ == "__main__":
    test()