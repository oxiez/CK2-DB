import io
import ck2_parser


dynasty_regex = {'^name':None,'^culture':None,'^religion':None}

def get_dynasties(file,cur):
	#read in historical dynasties first 
	'''
	with io.open('00_dynasties.txt',encoding="cp1252") as f:
		obj = ck2_parser.getCK2Obj(f,dynasty_regex)  
		while obj != None:
			name = None
			cultureID = None
			religionID = None
			dntID = obj.get('tag')
			if 'name' in obj:
				name = obj['name']
			if 'culture' in obj:
				cur.execute('SELECT cultureID FROM culture WHERE cultureName=%s',[obj['culture'].strip().strip('"')])
				cultureID = cur.fetchone()[0]
			if 'religion' in obj: 
				cur.execute('SELECT religionID FROM religion WHERE religionName=%s',[obj['religion'].strip().strip('"')])
				religionID = cur.fetchone()[0]
			cur.execute('INSERT INTO dynasty Values(%s,%s,%s,%s)',[dntID,name,cultureID,religionID])
			print(dntID,name,cultureID,religionID)
			obj = ck2_parser.getCK2Obj(f,dynasty_regex)
	'''
	
	with io.open('00_dynasties.txt',encoding="cp1252") as f:
		line = ' '
		while line:
			line = f.readline()
			if line == '\n' or line[0]=='#': continue
			dntID = line[0:line.find('=')].strip()
			line = f.readline()
			name = None
			cultureID = None
			religionID = None
			while line != '}\n':
				line = line.strip()
				index = line.find('=')
				if index != -1:
					key = line[0:index].strip()
					value = line[index+1:]
					if '#' in value: value = value[0:value.index('#')]
					value = value.strip().strip('"').rstrip().rstrip('"')
					if key=='name':
						name = value
					if key=='culture':
						cur.execute('SELECT cultureID FROM culture WHERE cultureName=%s',[value])
						cultureID = cur.fetchone()[0]
					if key=='religion' and '}' not in value:
						cur.execute('SELECT religionID FROM religion WHERE religionName=%s',[value])
						religionID = cur.fetchone()[0]					
				line = f.readline()
			#add this dynasty to the table
			#NOTE: dynastyID 1061019 corresponds to two dynasties!!! von Hanover and Tiversti
			if dntID=='1061019' or dntID=='105946' or dntID=='1059971': continue
			#print(dntID,name,cultureID,religionID)
			cur.execute('INSERT INTO dynasty Values(%s,%s,%s,%s)',[dntID,name,cultureID,religionID])
		
	#read in the save game dynasties 
	ck2_parser.jumpTo(file, "^dynasties=")
	obj = ck2_parser.getCK2Obj(file, dynasty_regex)  
	while obj != None:
		name = None
		cultureID = None
		religionID = None	
		dntID = obj.get('tag')
		if 'name' in obj:
			name = obj['name'].strip().strip('"')
		if 'culture' in obj:
			cur.execute('SELECT cultureID FROM culture WHERE cultureName=%s',[obj['culture'].strip().strip('"')])
			cultureID = cur.fetchone()[0]
		if 'religion' in obj: 
			cur.execute('SELECT religionID FROM religion WHERE religionName=%s',[obj['religion'].strip().strip('"')])
			religionID = cur.fetchone()[0]
		cur.execute('SELECT COUNT(*) FROM dynasty WHERE dynastyID=%s',[dntID])
		count = cur.fetchone()[0]
		if count > 0:
			if name != None: cur.execute('UPDATE dynasty SET dynastyname=%s WHERE dynastyID=%s',[name])
			if cultureID != None: cur.execute('UPDATE dynasty SET dynastyname=%s WHERE dynastyID=%s',[cultureID])
			if religionID != None: cur.execute('UPDATE dynasty SET dynastyname=%s WHERE dynastyID=%s',[religionID])
		else:
			cur.execute('INSERT INTO dynasty Values(%s,%s,%s,%s)',[dntID,name,cultureID,religionID])
		obj = ck2_parser.getCK2Obj(file,dynasty_regex)
		
		

#original spaghetti. In a worst case scenario, use this
def old_get_dynasties(file,cur):
    # The following code adds in-game dynasties to the game
    # read until we hit the dynasties
    line = file.readline()
    done = False
    while(not done):
        line = file.readline()
        #beginning of dynasties data
        if line=='\tdynasties=\n':
            line = file.readline() #get rid of '\t{\n'
            line = file.readline()
            #while not the end of the data '\t}\n'
            while line!='\t}\n':
                #parse this dynasty
                line = line.strip()
                #get the id
                i = line[0:len(line)-1]
                #get the name
                line = file.readline()
                line = file.readline()
                #historical dynasties are missing information: name appears as f_arms
                name = None         
                cul = None
                rel = None
                if 'name' in line:
                    #difficulties in finding and removing " symbols as well as comments (denoted by #)
                    #  :(
                    index = line.find('"')
                    if index==-1:
                        index = line.find('=')
                    name = line[index+1:]
                    name = name.strip()                    
                    name = name.strip('"')
                    name = name.rstrip('"')
                    name = name.strip()
                    index = name.find('"')
                    if index!=-1:
                        name = name[0:index-1]
                    index = name.find('#')
                    if index!=-1:
                        name = name[0:index-2]
                    #next two lines are culture and religion
                    line = file.readline()
                    cul = line.split('=')[1]
                    cul = cul.strip()
                    cul = cul.strip('"')
                    cur.execute('SELECT cultureID FROM culture WHERE cultureName=%s',[cul])
                    cul = cur.fetchone()[0]
                    line = file.readline()
                    rel = line.split('=')[1]
                    rel = rel.strip()
                    rel = rel.strip('"')
                    cur.execute('SELECT religionID FROM religion WHERE religionName=%s',[rel])
                    rel = cur.fetchone()[0]
                #add to the database
                cur.execute('INSERT INTO dynasty Values(%s,%s,%s,%s)',[i,name,cul,rel])
                #ignore the next lines until end of dynasty
                while(line!='\t\t}\n'):
                    line = file.readline()
                # the next line is either a new dynasty or the end of the file
                line = file.readline()
            done = True
    
    # add information for existant historical dynasties
    with io.open('00_dynasties.txt',encoding="cp1252") as f:
        line = f.readline()
        while(line!='}'):
            #line is currently an id
            index = line.find('=')
            i = line[0:index]
            #get missing name   
            while(line[1:5]!='name'):
                line = f.readline()
            index = line.find('"')
            if index==-1:
                index = line.find('=')
            name = line[index+1:]
            name = name.strip()
            name = name.strip('"')
            name = name.rstrip('"')
            name = name.strip()
            index = name.find('"')
            if index!=-1:
                name = name[0:index-1]
            index = name.find('#')
            if index!=-1:
                name = name[0:index-2]                
            #move until end of parse block
            while(line!='}\n' and line!='}'):
                line = f.readline()
            #add the name to the table
            cur.execute('UPDATE dynasty SET dynastyName = %s WHERE dynastyID=%s',[name,i])
            #move pointer to next integer entry
            line = f.readline()
            #end of file when nextline is nothing
            if len(line)==0:
                break
            #ignore whitespace
            while line=='\n' or line[0]=='#':
                line = f.readline()
            