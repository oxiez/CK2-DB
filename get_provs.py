province_tags = set(["id",
                    "culture",
                    "religion"])
barony_tags = set(["type"])

def get_provs(file, cur):
    # Jump to beginning of procinces
    x = file.readline().strip()
    while (x != "provinces="): # Read until provinces= or EOF
        x = file.readline().strip()

    x = file.readline().strip()
    if(x != "{"):
        raise Exception("ERROR: No opening bracket for Provinces!")
    
    # Start reading provinces until we get to the same level enclosing bracket or EOF
    
    x = file.readline().strip()
    while(x and x != "}"):
        province = {}
        baronies = []
        try:
            province["id"] = int(x[0:-1])
        except ValueError:
            raise Exception("ERROR: Province ID is not an int!")
        get_prov_tags(file, province, baronies)
        x = file.readline().strip()

        # Insert the province first
        cur.execute("INSERT INTO province VALUES(%s,%s,%s,%s,%s)",
                    [province.get("id"),
                     province.get("name"),
                     None,
                     province.get("culture"),
                     province.get("religion")]
        )

        # Insert all baronies
        for barony in baronies:
            cur.execute("INSERT INTO barony VALUES(%s,%s,%s)",
                        [barony.get("name"),
                         barony.get("province"),
                         barony.get("type")]
            )
        
def get_prov_tags(file, province, baronies):
    x = file.readline().strip()
    while(x and x != "}"):
        statement = x.split("=", 1) # Split up to first =        
        if(statement[0] in province_tags): # If tag
            province[statement[0]] = statement[1]
        elif(statement[0] == "name"): # If name (parse the quotations)
            province["name"] = statement[1].replace("\"", "")
        elif(len(statement) > 1 and len(statement[1]) == 0): # Multiline attribute
            parse_multiline_attr(file, province, baronies, statement[0], 1)
        x = file.readline().strip()

# level: 0 = unknown, 1 = province_attr
def parse_multiline_attr(file, province, baronies, tag, level):
    x = file.readline().strip()
    if(x and x != "{"):
        raise Exception("ERROR: No opening bracket for a multiline attributes!")
    
    if(len(tag) > 2 and tag[1] == "_" and level == 1): # If barony
        barony_name = tag[2:]
        barony_name = barony_name[0].upper() + barony_name[1:]
        barony = {"name" : barony_name,
                  "province" : province["id"]
        }

        while(x and x != "}"):
            statement = x.split("=", 1) # Split up to first =
            if(statement[0] in barony_tags):
                barony[statement[0]] = statement[1]
            elif(len(statement) > 1 and statement[1] == ""):
                parse_multiline_attr(file, province, baronies, statement[0], 0)
            x = file.readline().strip()
        
        baronies.append(barony)
    else:
        while(x and x != "}"):
            statement = x.split("=", 1) # Split up to first =
            if(len(statement) > 1 and statement[1] == ""):
                parse_multiline_attr(file, province, baronies, "", 0)
            x = file.readline().strip()
    
