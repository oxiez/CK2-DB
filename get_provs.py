import io
import re

import ck2_parser as parser

barony_regex = {"type" : None}

province_regex = {"culture" : None,
				  "religion" : None,
				  "name" : None,
				  "._" : barony_regex}

def get_provs(file, cur):
	province_id_dict = {}
	with io.open(r'data/province_id to county_id.txt') as f:
		for line in f:
			line = line.split("\n")[0]
			l = line.split(" ")
			province_id_dict[int(l[0])] = l[1]
	parser.jumpTo(file, "^provinces=")

	obj = parser.getCK2Obj(file, province_regex)
	while(not obj == None):
		try:
			id = int(obj.get("tag"))
		except ValueError:
			raise Exception("ERROR: Province ID is not an int!")
		
		if("name" in obj):
			obj["name"] = obj["name"].replace("\"", "")
		
		if(id not in province_id_dict):
			province_id_dict[id] = None
		
		cur.execute("INSERT INTO province VALUES(?,?,?,?,?)",
					[id,
					 obj.get("name"),
					 province_id_dict[id],
					 obj.get("culture"),
					 obj.get("religion")]
		)

		for key in obj.keys():
			if(not re.match("._", key) == None):
				name = key[2].upper() + key[3:len(key)]
				cur.execute("INSERT INTO barony VALUES(?, ?, ?)",
							[name,
							 id,
							 obj[key]["type"]])
				
		obj = parser.getCK2Obj(file, province_regex)

