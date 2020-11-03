import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

osm_file = open("FullVelaux.osm", "r", encoding='utf-8')

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) 
street_types = defaultdict(set)

# All terms in French
expected = ["Rue", "Allée" "Avenue", 
            "Impasse", "Route", "Lotissement", "Montée"]

# this fonction's lokking for type and name of streets
def audit_street_type(street_types, street_name, problem_chars=problemchars):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# this function makes the display of the result more attractive
def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    
    for k in keys:
        v = d[k]
        print ("%s: %d" % (k, v)) 

# return all attributs "k" for "name" values
def is_street_name(elem):
    return (elem.attrib['k'] == "name")

# This is the parsing function
def audit(osm_file):
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v']) 
    pprint.pprint(dict(street_types))
    
if __name__ == '__main__':
    audit(osm_file)