"""General Parser for ck2 files. Uses regex."""

import re

# Reads all of the first object at the same level that it was called on
# Regex is a dict
# Returns a dict where the name of the object is kept as a val to a key
# In addition, the dict contains a structure defined by the regex dict
# I don't suggest calling getCK2Obj on single attr
# Returns None if there are no more objects at this level
def getCK2Obj(file, regex, ck2_obj_key = "tag"):    
    # Jump to the first object it finds
    x = file.readline()
    parsed = x.strip()
    pair = parsed.split("=", 1)
    while(x and len(pair) < 2):
        if(parsed == "}"):
            return None
        x = file.readline()
        parsed = x.strip()
        pair = parsed.split("=", 1)
    if(not x):
        raise Exception("ERROR: No statement found!")

    results = getAttr(file, regex, parsed)
    results[ck2_obj_key] = pair[0].strip()
    
    return results
        

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
    tag = pair[0].strip()
    val = ""
    if(len(pair) > 1): val = pair[1].strip()
    if(not val == "" and not val == "{"): # single attribute check
        if("}" in pair[1] and not "{" in pair[1]):
            raise Exception("ERROR: No opening bracket for corresponding closing bracket!")
        return val

    # Multiline attributes
    # At this point, we assume that } is on a separate line
    x = "insert word here"
    parsed = val
    while(x and not parsed == "{"): # Skip everything until opening bracket
        # { must be on the first line or a newline by itself
        x = file.readline()
        parsed = x.strip()
    if(not x):
        raise Exception("ERROR: No opening bracket for attribute {}".format(tag))

    results = {} # We can start parsing the tags now
        
    x = file.readline()
    parsed = x.strip() # We need to separate the two because has newlines
    while(x and not parsed == "}"):
        # If regex == None, ignore all attributes
        pair = parsed.split("=", 1)

        if(len(pair) < 2): # No = character
            x = file.readline()
            parsed = x.strip()
            continue
        
        if(not regex == None):
            valid = False
            for key in regex.keys():
                if(not re.match(key, pair[0]) == None):
                    pair[0] = pair[0].strip()
                    results[pair[0]] = getAttr(file, regex[key], parsed)
                    valid = True
                    break
            if(not valid): # skip
                getAttr(file, None, parsed)
        else:
            getAttr(file, None, parsed)
        x = file.readline()
        parsed = x.strip()
    if(not x):
        raise Exception("ERROR: No closing bracket for attribute {}".format(tag))
    return results

# Takes file pointer and regex string
# Jumps to line of value(s) (the opening bracket if multiple values)
def jumpTo(file, regex, multi = True):
    x = file.readline()
    parsed = x.strip()
    while (x and re.match(regex, parsed) == None):
        x = file.readline()
        parsed = x.strip()
        
    if(not multi): return  
    
    # Skip to the opening bracket
    if(not "{" in parsed):
        while(x and not parsed == "{"):
            x = file.readline()
            parsed = x.strip()
        if(not x):
            raise Exception("ERROR: No opening bracket for {}".format(regex))
    
