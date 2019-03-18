"""General Parser for ck2 files. Uses regex."""

import re

# File, regex dict, line of the attribute that we want to read, i.e. provinces=
# (where { is on the this/next line) or culture=norweigan.
def getAttr(file, regex, attr_line):
    """Takes a file object and a dict of regex rules (one for each possible tag(s)) 
    to determine which rules to store. The value for each regex rule should either
    be None or another regex dict which indicates the value is made up of multiple attributes.
    Returns a dict that contains tag-value pairs. If a tag results in a multiline attribute,
    the value for that tag is a dictionary of tags and values, and this continues on. Otherwise,
    returns a string.

    Note that single line multiattributes are considered single attributes (i.e. 
    tag={a...b..c})"""

    # Determine if multiline or single attribute
    pair = attr_line.split("=", 1)
    tag = pair[0]
    val = ""
    if(len(pair > 1)): val = pair[1].strip()
    if(not val == "" and not val == "{"): # single attribute check
        if("}" in pair[1] and not "{" in pair[1]):
            raise Exception("ERROR: No opening bracket for corresponding closing bracket!")
        return pair[1]

    # Multiline attributes
    # At this point, we assume that } is on a separate line
    x = val
    while(x and not x == "{"): # Skip everything until opening bracket
        # { must be on the first line or a newline by itself
        x = file.readline().strip()
    if(not x):
        raise Exception("ERROR: No opening bracket for attribute {}".format(tag))

    results = {} # We can start parsing the tags now
    x = file.readline().strip()
    while(x and not x == "}"):
        if(x == ""): # empty line
            x = file.readline().strip()
            continue

        # If regex == None, take all attributes
        pair = x.split("=", 1)
        if(not regex == None):
            for key in regex.keys():
                if(not re.match(key, pair[0]) == None):
                    results[pair[0]] = getAttr(file, regex[key], x)
        else:
            results[pair[0]] = getAttr(file, None, x)
        x = file.readline().strip()
             
    if(not x == "}"):
        raise Exception("ERROR: No closing bracket for attribute {}".format(tag))

    return results
