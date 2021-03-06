import io

def get_provs(data, cur):
    province_id_dict = {}
    with io.open(r'data/province_id to county_id.txt') as f:
        for line in f:
            line = line.split("\n")[0]
            l = line.split(" ")
            province_id_dict[int(l[0])] = l[1]

    for provID in data:
        obj = data[provID]
        provID = int(provID)
        
        if(provID not in province_id_dict):
            province_id_dict[provID] = None
        
        cur.execute("INSERT INTO province VALUES(?,?,?,?,?)",
                    [provID,
                     obj.get("name"),
                     province_id_dict[provID],
                     obj.get("culture"),
                     obj.get("religion")]
        )

        for key in obj.keys():
            if key[:2] == "b_":
                name = key[2].upper() + key[3:len(key)]
                cur.execute("INSERT INTO barony VALUES(?, ?, ?)",
                            [name,
                             provID,
                             obj[key]["type"]])
