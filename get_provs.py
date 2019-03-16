province_tags = set(["id",
                    "name",
                    "culture",
                    "religion"])
barony_tags = set(["type"])

def get_provs(file, cur):
    # Jump to beginning of procinces
    x = file.readline().strip()
    while (x and x != "provinces="): # Read until provinces= or EOF
        x = file.readline()

    x = file.readline().strip()
    if(x != "{"):
        raise Exception("ERROR: No opening bracket for Provinces!")
    
    # Start reading provinces until we get to the same level enclosing bracket or EOF
    provinces = set()
    baronies = set()
    
    x = file.readline().strip()
    while(x):
        province = {}
        baronies = set()
        try:
            province["id"] = int(x[0:-1])
        except ValueError:
            raise Exception("ERROR: Province ID is not an int!")
        get_prov_tags(province, baronies)

        provinces.insert(province)

    for province in provinces:
        print(province)
        
def get_prov_tags(file, province, baronies):
    x = file.readline().strip()
    while(x and x != "}"):
        statement = x.split("=", 1) # Split up to first =        
        if(statement[0] in province_tags): # If tag
            province[statement[0]] = statement[1]
        elif(statement[0] == "name"): # If name (parse the quotations)
            province["name"] = statement[1].replace("\"", "")
        elif(len[statement[1] == ""]): # Multiline attribute
            parse_multiline_attr(file, province, baronies, statement[0], 1)
        x = file.readline().strip()

# level: 0 = unknown, 1 = barony
def parse_multiline_attr(file, province, baronies, tag, level):
    x = file.readline().strip()
    if(x and x != "{" and level == 0):
        raise Exception("ERROR: No opening bracket for a multiline attributes!")
    
    if(len(tag) > 2 and tag[0][1] == "_"): # If barony
        barony_name = tag[2:]
        barony_name[0] = barony_name[0].upper()
        barony = {"name" : barony_name,
                  "province" : province["id"]
        }

        while(x and x != "}"):
            statement = x.split("=", 1) # Split up to first =
            if(statement[0] in barony_tags):
                barony[statement[0]] = statement[1]
            elif(statement[1] == ""):
                parse_multiline_attr(file, province, baronies, statement[0], 0)
        
        baronies.insert(barony)
    else:
        while(x and x != "}"):
            if(x == "{"):
                parse_multiline_attr(file, province, baronies, statement[0], 0)
            x = readline().strip()
    
