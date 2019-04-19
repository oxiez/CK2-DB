import io

import ck2_parser as parser

# odd_case where liege is a CK2 Obj (See c_auxerre)
liege_regex = {"base_title" : None}

#level_id
title_regex = {"holder" : None,
			   "^liege" : liege_regex, # Defacto Liege
			   "^previous" : None, # This needs to be broken up manually
			   "de_jure_liege" : None}

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
		obj = parser.getCK2Obj(file, title_regex)
