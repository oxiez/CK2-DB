		# Person(INT id, VARCHAR(63) birthName, INT dynasty, BOOLEAN isMale, DATE birthday, DATE deathday, INT fatherID,
		# INT real_fatherID, INT motherID, INT spouseID, INT religionID, INT cultureID, FLOAT fertility, FLOAT health, FLOAT wealth,
		# INT hostID, FLOAT prestige, FLOAT piety, INT provinceLocationID, INT employerID, INT martial, INT diplomacy, INT stewardship,
		 # INT intrigue, INT learning)


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
		if line == '{':
			num_brace += 1
			continue
		elif line == '}':
			if(num_brace > 1):
				# PUSH
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
		else:
			if line[0:2] == "bn=":
				birthName = line[3:-1]
			elif line[0:3] = "dnt="
				birthName = int(line[3:])
