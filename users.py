#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Find out how many unique users
have contributed to the map in this particular area!
The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return

#Return a set of user with uid 
def process_map(filename):
    users = set() # create a set of users
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib:          # find where uid is tag attribute 
             users.add(element.attrib['uid'])
        pass

    return users

#Create a test case
def test():
    users = process_map('example.osm')
    pprint.pprint(users)
    assert len(users) == 87

if __name__ == "__main__":
    test()