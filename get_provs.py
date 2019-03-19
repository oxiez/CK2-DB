import io
import re

import parser

barony_regex = {"type" : None}

province_regex = {"culture" : None,
                  "religion" : None,
                  "name" : None,
                  "._" : barony_regex}

def get_provs(file, cur):
    # Jump to beginning of provinces
    parser.jumpTo(file, "^provinces=")
    x = file.readline()
    parsed = x.strip()

    while(x and not parsed == "}"):
        if(not "=" in x):
            x = file.readline()
            parsed = x.strip()
            continue
        try:
            id = int(parsed[0:-1])
        except ValueError:
            raise Exception("ERROR: Province ID is not an int!")

        province = parser.getAttr(file, province_regex, x)
        province["id"] = id

        if("name" in province): # Because we need to apply an operation on it
            province["name"] = province["name"].replace("\"","")

        # Insert the province first
        cur.execute("INSERT INTO province VALUES(%s,%s,%s,%s,%s)",
                    [province.get("id"),
                     province.get("name"),
                     None,
                     province.get("culture"),
                     province.get("religion")]
        )

        for key in province.keys():
            if(not re.match("._", key) == None):
                name = key[2].upper() + key[3:len(key)]
                cur.execute("INSERT INTO barony VALUES(%s, %s, %s)",
                            [name,
                             id,
                             province[key]["type"]])
  
        x = file.readline()
        parsed = x.strip()
            
    if(not x):
        raise Exception("ERROR: No closing bracket for Provinces!")


