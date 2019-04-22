import io
import re
from get_chars import make_date

import ck2_parser as parser

# odd_case where liege is a CK2 Obj (See c_auxerre)
liege_regex = {"base_title" : None}

hist_sub_regex = {"^holder" : None}

history_regex = {"^\d+\.\d+\.\d+" : hist_sub_regex}

#level_id
title_regex = {"holder" : None,
               "^liege" : liege_regex, # Defacto Liege
               "^previous" : None, # This needs to be broken up manually
               "de_jure_liege" : None,
               "^history" : history_regex}

def get_titles(file,cur):
    parser.jumpTo(file, "^title=")

    obj = parser.getCK2Obj(file, title_regex)
    while(not obj == None):
        level = obj.get("tag")[0]
        name = obj.get("tag")[2:]
        previous = []
        
        if(isinstance(obj.get("liege"), dict)):
            obj["liege"] = obj["liege"]["base_title"] # liege id
        
        cur.execute("INSERT INTO title VALUES(%s, %s, %s, %s, %s, %s)",
                    [obj.get("tag"),
                     obj.get("holder"),
                     name,
                     level,
                     obj.get("liege"),
                     obj.get("de_jure_liege")]
        )
        if("previous" in obj):
            for p in obj.get("previous"):
                cur.execute("INSERT INTO rulers Values(%s, %s)", [int(p), obj.get("tag")])

        hist = obj.get("history")
        if(not hist == None):
            for key in hist.keys():
                if(not re.match("^\d+\.\d+\.\d+", key) == None):
                    day = make_date(key)
                    holder = None
                    try:
                        # There's an odd case for c_modena (but also many more)
                        if(isinstance(hist[key], list)):
                            holder = int(hist[key][-1].get("holder"))
                        else:
                            holder = int(hist[key].get("holder"))
                    except ValueError: # If holder tag is something like "0"
                        holder = None
                    except TypeError: # If no holder tag
                        holder = None
                    cur.execute("INSERT INTO titlehistory VALUES(%s, %s, %s)",
                                [obj.get("tag"),
                                 holder,
                                 day])
                    
        obj = parser.getCK2Obj(file, title_regex)
