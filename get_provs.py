import io
import re

import ck2_parser as parser

barony_regex = {"type" : None}

province_regex = {"culture" : None,
				  "religion" : None,
				  "name" : None,
				  "._" : barony_regex}

def get_provs(file, cur):
	parser.jumpTo(file, "^provinces=")

	obj = parser.getCK2Obj(file, province_regex)
	while(not obj == None):
		try:
			id = int(obj.get("tag"))
		except ValueError:
			raise Exception("ERROR: Province ID is not an int!")
		
		if("name" in obj):
			obj["name"] = obj["name"].replace("\"", "")

		cur.execute("INSERT INTO province VALUES(%s,%s,%s,%s,%s)",
					[id,
					 obj.get("name"),
					 None,
					 obj.get("culture"),
					 obj.get("religion")]
		)

		for key in obj.keys():
			if(not re.match("._", key) == None):
				name = key[2].upper() + key[3:len(key)]
				cur.execute("INSERT INTO barony VALUES(%s, %s, %s)",
							[name,
							 id,
							 obj[key]["type"]])
				
		obj = parser.getCK2Obj(file, province_regex)

