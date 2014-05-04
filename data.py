#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
"""
Wrangle the data and transform the shape of the data
into the below model . The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_ref": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {} # creta a dictionary to save json type which we want to create
    node["created"]={}
    node["address"]={}
    node["pos"]=[]
    refs=[]
    
    
    if element.tag == "node" or element.tag == "way" :
        #id type visible attribute
        if "id" in element.attrib:
            node["id"]=element.attrib["id"]
        #type is what we create and it is tag name    
        node["type"]=element.tag 
        
        if "visible" in element.attrib:
            node["visible"]=element.attrib["visible"]
            
        #For each elemet in CREATED list    
        for elem in CREATED: 
            if elem in element.attrib:
                node["created"][elem]=element.attrib[elem] # create nested dictionary
        #attributes for latitude and longitude should be added to a "pos" array        
        if "lat" in element.attrib:
            node["pos"].append(float(element.attrib["lat"]))
        if "lon" in element.attrib:
            node["pos"].append(float(element.attrib["lon"]))    
        
        for tag in element.iter("tag"):
            # if second level tag "k" value contains problematic characters, it should be ignored
            if not(problemchars.search(tag.attrib['k'])):
            #if second level tag "k" value starts with "addr:", 
            #it should be added to a dictionary "address"
            # houseadrees, postalcode,street

                if tag.attrib['k'] == "addr:housenumber":
                    node["address"]["housenumber"]=tag.attrib['v']
                if tag.attrib['k'] == "addr:postcode":
                    node["address"]["postcode"]=tag.attrib['v']    
                if tag.attrib['k'] == "addr:street":
                    node["address"]["street"]=tag.attrib['v']    
                # all other attribute which dont have addr
                if tag.attrib['k'].find("addr")==-1:
                    node[tag.attrib['k']]=tag.attrib['v']
         #for not tag name in second level way
        for nd in element.iter("nd"):     
             refs.append(nd.attrib["ref"])
        # remove empty address        
        if node["address"] =={}:
            node.pop("address", None) 
        # add to the dictionary if it is not null           
        if refs != []:    
           node["node_refs"]=refs #"node_ref": ["305896090", "1719825889"]
        return node
    else:
        return None

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el :
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
                  
    return data

def test():

    data = process_map('example.osm', pretty = False)
    assert data[0] ==  {'created': {'changeset': '457421',
                                    'timestamp': '2009-02-15T17:26:02Z',
                                    'uid': '1034',
                                    'user': 'crschmidt',
                                    'version': '5'},
                        'id': '61170995',
                        'pos': [42.37869, -71.096112],
                        'type': 'node',
                        'visible': 'true'}


if __name__ == "__main__":
    test()