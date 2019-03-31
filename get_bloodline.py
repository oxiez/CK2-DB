def get_bloodlines(file, cur):
	# we should start in the right place
	#print(line) #character=

	founder_ID = None
	bloodline_ID = None
	bloodline_name = None
	holder_ID = None

	line = file.readline()
	while line.strip() != "bloodline=":
		line = file.readline()
		if(not line):
			return
	num_brace = 0
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
				cur.execute('INSERT INTO BloodLines Values(%s, %s, %s)', [bloodline_ID, bloodline_name, founder_ID])
				founder_ID = None
				bloodline_ID = None
				bloodline_name = None
				holder_ID = None
				# PUSH
			num_brace -= 1
			continue
		if (num_brace == 1):
			bloodline_ID = int(line[0:-1])
			continue
		elif (num_brace > 2):
			continue
		else:
			if line[0:4] == "type=":
				bloodline_name = line[5:-1]
			elif line[0:6] == "owner=":
				founder_ID = int(line[6:])
			elif line[0:6] == "member=":
				holder_ID = line[6:]
				cur.execute('INSERT INTO trait BloodLineOwners(%s,%s)',[holder_ID,bloodline_ID])
