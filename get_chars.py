		# Person(INT id, VARCHAR(63) birthName, INT dynasty, BOOLEAN isMale, DATE birthday, DATE deathday, INT fatherID,
		# INT real_fatherID, INT motherID, INT spouseID, INT religionID, INT cultureID, FLOAT fertility, FLOAT health, FLOAT wealth,
		# INT hostID, FLOAT prestige, FLOAT piety, INT provinceLocationID, INT employerID, INT martial, INT diplomacy, INT stewardship,
		 # INT intrigue, INT learning)

import datetime
import ck2_parser as parser
		 
claim_regex = {"title" : None,
			   "pressed" : None,
			   "weak" : None
}

person_regex = {"^bn" : None,
				"^dnt" : None,
				"^fem" : None,
				"^b_d" : None,
				"^d_d" : None,
				"^fat" : None, # The default for rfat if none specificed
				"^rfat" : None,
				"^mot" : None,
				"^spouse" : None,
				"^rel" : None,
				"^cul" : None,
				"^fer" : None,
				"^health" : None,
				"^wealth" : None,
				"^prs" : None,
				"^piety" : None,
				"^emp" : None,
				"^host" : None,
				"^att" : None, # This needs to be broken up manually
				"^tr" : None, # This needs to be broken up manually
				"^claim" : claim_regex # Repeated
}

def make_person_attributes(att):
	attr_list = att[1:-1].strip().split() # Remove brackets
	attributes = {"diplomacy" : int(attr_list[0]),
				  "martial" : int(attr_list[1]),
				  "steward" : int(attr_list[2]),
				  "intrigue" : int(attr_list[3]),
				  "learning" : int(attr_list[4])
	}
	return attributes

def make_traits(tr):
	return tr[1:-1].strip().split()

def make_date(str):
	dt_arr = str.split('.')
	year = int(dt_arr[0])
	month = int(dt_arr[1])
	day = int(dt_arr[2])

	result_date = datetime.date(year, month, day)
	return result_date

def get_cul_ID(cur,name):
	cur.execute("SELECT cultureid FROM culture WHERE culturename=%s",[name])
	return cur.fetchone()

def get_rel_ID(cur,name):
	cur.execute("SELECT religionid FROM religion WHERE religionname=%s",[name])
	return cur.fetchone()

def get_chars(file, cur):
	parser.jumpTo(file, "^character=")

	obj = parser.getCK2Obj(file, person_regex)
	while(not obj == None):
		religionID = None
		cultureID = None
		isMale = True
		attributes = {}
		traits = []
		
		# Integer conversions and list truncation
		try:
			id = int(obj.get("tag")) # Person id
			if("dnt" in  obj): obj["dnt"] = int(obj["dnt"])
			if("fat" in obj): obj["fat"] = int(obj["fat"])
			if("rfat" in obj): obj["rfat"] = int(obj["rfat"])
			else: obj["rfat"] = obj.get("fat")
			if("mot" in obj): obj["mot"] = int(obj["mot"]) 
			if("emp" in obj): obj["emp"] = int(obj["emp"])
			if("host" in obj): obj["host"] = int(obj["host"])
			
			if("fer" in obj): obj["fer"] = float(obj["fer"])
			if("health" in obj): obj["health"] = float(obj["health"])
			if("wealth" in obj): obj["wealth"] = float(obj["wealth"])
			if("prs" in obj): obj["prs"] = float(obj["prs"])
			if("piety" in obj): obj["piety"] = float(obj["piety"])

			if("att" in obj):
				attributes = make_person_attributes(obj["att"])

			if("tr" in obj):
				traits = make_traits(obj["tr"])
		except ValueError:
			raise Exception("ERROR: One of the person attributes is not a number!")

		if("rel" in obj): religionID = get_rel_ID(cur,obj["rel"].replace("\"", ""))
		if("cul" in obj): cultureID = get_cul_ID(cur,obj["cul"].replace("\"", ""))
		if("bn" in obj): obj["bn"] = obj["bn"].replace("\"", "")
		if("b_d" in obj): obj["b_d"] = make_date(obj["b_d"].replace("\"", ""))
		if("d_d" in obj): obj["d_d"] = make_date(obj["d_d"].replace("\"", ""))
		if("fem" in obj): isMale = False

		cur.execute(
			'INSERT INTO Person Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
			[id, obj.get("bn"), obj.get("dnt"), isMale, obj.get("b_d"), obj.get("d_d"), obj.get("fat"),
			 obj.get("rfat"), obj.get("mot"), religionID, cultureID, obj.get("fer"),
			 obj.get("health"), obj.get("wealth"), obj.get("host"), obj.get("prs"), obj.get("piety"),
			 obj.get("emp"), attributes.get("martial"), attributes.get("diplomacy"),
			 attributes.get("steward"), attributes.get("intrigue"), attributes.get("learning")
		])

		for tr in traits:
			cur.execute("INSERT INTO trait Values(%s, %s)", [id, int(tr)])

		if("spouse" in obj):
			if(isinstance(obj["spouse"], list)):
				for s in obj["spouse"]:
					cur.execute("INSERT INTO marriage Values(%s, %s)",
								[id, s])
			else:
				cur.execute("INSERT INTO marriage Values(%s, %s)",
							[id, obj["spouse"]])
		
		# Parse claims
		if("claim" in obj):
			if(isinstance(obj["claim"], list)):
				for d in obj["claim"]:
					cur.execute("INSERT INTO claim Values(%s, %s, %s, %s)",
								[id, d.get("title"),
								 "pressed" in d,
								 "weak" in d])
			else:
				cur.execute("INSERT INTO claim Values(%s, %s, %s, %s)",
							[id,
							 obj["claim"].get("title"),
							 "pressed" in obj["claim"],
							 "weak" in obj["claim"]])

		obj = parser.getCK2Obj(file, person_regex);

def get_chars_old(file, cur):
	# we should start in the right place
	line = file.readline()
	#print(line) #character=

	char_id = None
	birthName = None
	dynasty = None
	isMale = True
	birthday = None
	deathday = None
	fatherID = None
	real_fatherID = None
	motherID = None
	spouseID = None
	religionID = None
	cultureID = None
	fertility = None
	health = None
	wealth = None
	hostID = None
	prestige = None
	piety = None
	provinceLocationID = None
	employerID = None
	martial = None
	diplomacy = None
	stewardship = None
	intrigue = None
	learning = None

	line = file.readline()
	num_brace = 1
	while num_brace > 0:	#make sure we are still in the characters

		line = file.readline()
		line = line.strip()
		#print(num_brace)
		#print(line)
		if line == '{' or (line.find('{')!=-1 and line.find('}')==-1):
			num_brace += 1
			continue
		elif line == '}':
			if(num_brace == 2):
				#print('pushing ' + str(birthName))
				cur.execute('INSERT INTO Person Values(%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [char_id, birthName, dynasty, isMale, birthday, deathday, fatherID, real_fatherID, motherID, spouseID, religionID, cultureID, fertility, health, wealth, hostID, prestige, piety, provinceLocationID, employerID, martial, diplomacy, stewardship, intrigue, learning])
				char_id = None
				birthName = None
				dynasty = None
				isMale = True
				birthday = None
				deathday = None
				fatherID = None
				real_fatherID = None
				motherID = None
				spouseID = None
				religionID = None
				cultureID = None
				fertility = None
				health = None
				wealth = None
				hostID = None
				prestige = None
				piety = None
				provinceLocationID = None
				employerID = None
				martial = None
				diplomacy = None
				stewardship = None
				intrigue = None
				learning = None
				# PUSH
			num_brace -= 1
			continue
		if (num_brace == 1):
			char_id = int(line[0:-1])
			continue
		elif (num_brace > 2):
			continue
		else:
			if line[0:3] == "bn=":
				birthName = line[4:-1]
			elif line[0:4] == "dnt=":
				dynasty = int(line[4:])
			elif line == "fem=yes":
				isMale = False
			elif line[0:4] == "b_d=":
				birthday = make_date(line[5:-1])
			elif line[0:4] == "d_d=":
				deathday = make_date(line[5:-1])
			elif line[0:4] == "fat=":
				fatherID = int(line[4:])
				real_fatherID = int(line[4:])
			elif line[0:5] == "rfat=":
				real_fatherID = int(line[5:])
			elif line[0:4] == "mot=":
				motherID = int(line[4:])
			elif line[0:7] == "spouse=":
				spouseID = int(line[7:])
			elif line[0:4] == "rel=":
				religionID = get_rel_ID(line[5:-1])
			elif line[0:4] == "cul=":
				cultureID = get_cul_ID(line[5:-1]) 
			elif line[0:4] == "fer=":
				fertility = float(line[4:]) 
			elif line[0:7] == "health=":
				health = float(line[7:]) 
			elif line[0:7] == "wealth=":
				wealth = float(line[7:])
			elif line[0:4] == "prs=":
				prestige = float(line[4:]) 
			elif line[0:6] == "piety=":
				piety = float(line[6:])
			elif line[0:4] == "emp=":
				employerID = int(line[4:])
			elif line[0:5] == "host=":
				hostID = int(line[5:])
			elif line[0:4] == "att=":
				att = line[4:-1]
				attributes = ''.join(att.split('{')).split()
				diplomacy = int(attributes[0])
				martial = int(attributes[1])
				stewardship = int(attributes[2])
				intrigue = int(attributes[3])
				learning = int(attributes[4])
			elif line[0:3] == "tr=":
				tr = line[4:-1]
				traits = tr.split()

				for t in traits:
					cur.execute('INSERT INTO trait Values(%s,%s)',[char_id,int(t)])
