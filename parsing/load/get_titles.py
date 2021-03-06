import io
import re
from .get_chars import make_date

from .ck2_parser import ck2_parser as parser

# odd_case where liege is a CK2 Obj (See c_auxerre)
liege_regex = {"base_title" : None}
de_jure_liege_regex = {"base_title" : None}

hist_sub_regex = {"^holder" : None}

history_regex = {"^\d+\.\d+\.\d+" : hist_sub_regex}

#level_id
title_regex = {"holder" : None,
               "^liege" : liege_regex, # Defacto Liege
               "de_jure_liege" : de_jure_liege_regex,
               "^history" : history_regex}

def get_titles(file,cur):
    parser.jumpTo(file, "^bloodline=")
    parser.jumpTo(file, "^title=")

    obj = parser.getCK2Obj(file, title_regex)
    while(not obj == None):
        level = obj.get("tag")[0]
        name = obj.get("tag")[2:]
        
        if(isinstance(obj.get("liege"), dict)):
            obj["liege"] = obj["liege"]["base_title"] # liege id
        
        if(isinstance(obj.get("de_jure_liege"), dict)):
            obj["de_jure_liege"] = obj["de_jure_liege"]["base_title"]

        cur.execute("INSERT INTO title VALUES(?, ?, ?, ?, ?, ?)",
                    [obj.get("tag"),
                     obj.get("holder"),
                     name,
                     level,
                     obj.get("liege"),
                     obj.get("de_jure_liege")]
        )

        if(obj.get("holder")):
            cur.execute("INSERT INTO rulers VALUES(?, ?)",
                        [obj.get("holder"),
                         obj.get("tag")]
            )
        
        hist = obj.get("history")
        if(not hist == None):
            for key in hist.keys():
                if(not re.match("^\d+\.\d+\.\d+", key) == None):
                    day = make_date(key)
                    holder = None
                    # There's an odd case for c_modena (but also many more)
                    if(isinstance(hist[key], list)):
                        for i in range(len(hist[key])):
                            try:
                                holder = int(hist[key][i].get("holder"))
                            except ValueError: # If holder tag is something like "0"
                                continue
                            except TypeError: # If no holder tag
                                continue
                            if (i > 0 and (hist[key][i].get("holder") == hist[key][i-1].get("holder"))):
                                continue
                            cur.execute("INSERT INTO titlehistory VALUES(?, ?, ?)",
                                        [obj.get("tag"),
                                         holder,
                                         day])
                    else:
                        try:
                            holder = int(hist[key].get("holder"))
                        except ValueError: # If holder tag is something like "0"
                            continue
                        except TypeError: # If no holder tag
                            continue
                        cur.execute("INSERT INTO titlehistory VALUES(?, ?, ?)",
                                    [obj.get("tag"),
                                     holder,
                                     day])
                    
        obj = parser.getCK2Obj(file, title_regex)
