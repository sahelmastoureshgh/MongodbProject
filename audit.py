"""

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
# there are three type of street name in my dataset St, St., ST
mapping = { "St":   "Street",
            "St.":  "Street",
            "ST":   "Street",
            "Rd.":  "Road",
            "N.":   "North",
            "Ave":  "Avenue"
            }

# find the one which are not in expcted name 
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# find if arrtib k vakue is addr: street
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# for the addr:street check name of street to be correct
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

#update name of street which has problems
def update_name(name, mapping):

    auditKeys=mapping.keys()
    for key in auditKeys:
        if name.find(key)>-1: # if problemtic street name is in the name of street
            name=name.replace(key,mapping[key]) # replace problemtic part with value of map dictionary
            break       

    return name

# Creat test case
def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 8
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "Newton ST":
                assert better_name == "Newton Street"
            if name == "Banks St.":
                assert better_name == "Banks Street"


if __name__ == '__main__':
    test()