		# Person(INT id, VARCHAR(63) birthName, INT dynasty, BOOLEAN isMale, DATE birthday, DATE deathday, INT fatherID,
		# INT real_fatherID, INT motherID, INT spouseID, INT religionID, INT cultureID, FLOAT fertility, FLOAT health, FLOAT wealth,
		# INT hostID, FLOAT prestige, FLOAT piety, INT provinceLocationID, INT employerID, INT martial, INT diplomacy, INT stewardship,
		 # INT intrigue, INT learning)

def make_date(str):
	dt_arr = str.split('.')
	year = int(dt_arr[0])
	month = int(dt_arr[1])
	date = int(dt_arr[2])

	result_date = datetime.date(year, month, day)
	return result_date

def get_cul_ID(str):
	return 0

def get_rel_ID(str):
	return 0

def get_chars(file, cur):
	# we should start in the right place
	line = file.readline()
	print(line) #character=

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
		print(num_brace)
		print(line)
		if line == '{':
			num_brace += 1
			continue
		elif line == '}':
			if(num_brace == 2):
				print('pushing ' + str(birthName))
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
				birthName = int(line[4:])
			elif line == "fem=yes":
				isMale = False
			elif line[0:4] == "b_d=":
				birthday = make_date(line[5:-1])
			elif line[0:4] == "d_d=":
				deathday = make_date(line[5:-1])
			elif line[0:4] == "fat=":
				fatherID = int(line[5:])
				real_fatherID = int(line[5:])
			elif line[0:5] == "rfat=":
				real_fatherID = int(line[6:])
			elif line[0:4] == "mot=":
				motherID = int(line[5:])
			elif line[0:6] == "spouse=":
				spouseID = int(line[7:])
			elif line[0:3] == "rel=":
				religionID = get_rel_ID(line[5:-1])
			elif line[0:3] == "cul=":
				cultureID = get_cul_ID(line[5:-1]) 
			elif line[0:3] == "fer=":
				fertility = float(line[4:]) 
			elif line[0:6] == "health=":
				health = float(line[7:]) 
			elif line[0:6] == "wealth=":
				wealth = float(line[7:])
			elif line[0:3] == "prs=":
				prestige = float(line[4:]) 
			elif line[0:5] == "piety=":
				piety = float(line[6:])
			elif line[0:3] == "emp=":
				employerID = int(line[4:])
			elif line[0:4] == "host=":
				hostID = int(line[5:])
			elif line[0:4 == "att="]:
				att = line[4:-1]
				attributes = att.split()

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