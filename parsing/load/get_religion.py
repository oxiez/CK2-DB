import io

#fills the religion table with entries of id,name,group
# IMPORTANT NOTE: we need to look at the save file to determine heresies
def get_religion(cur):
    with io.open('data/00_religions.txt',encoding="cp1252") as f:
        #setup
        line = None
        for i in range(13):
            line = f.readline()
        #variable initialization
        rel_id = 1
        rel_name = None
        rel_group = None 
        # loop until the end of the file
        while True:
            #find the next religious group      
            line = f.readline()
            if not line: break
            line = line.strip()
            # we want something like 'group = {'
            if '{' not in line:
                continue
            index = line.find('=')
            rel_group = line[0:index-1]
            brace_depth = 1
            #find the next religion in this group            
            while brace_depth > 0:
                line = f.readline()
                line.strip()
                if '{' in line:
                    brace_depth += 1
                    index = line.find('=')
                    if index != -1 and brace_depth==2:
                        rel_name = line[0:index-1]
                        rel_name = rel_name.strip()
                        #make sure this isnt some other parameter
                        if not rel_name in ['male_names','female_names','color','god_names','evil_god_names','alternate_start','interface_skin','unit_modifier','unit_home_modifier']:
                            # insert tuple<id, name,heresy,religiongroup>                          
                            cur.execute('INSERT INTO religion Values(?,?,NULL,NULL,?)',
                                    [rel_id,rel_name,rel_group])
                            rel_id += 1
                if '}' in line:
                    brace_depth -= 1

# finds religion={ in the main save file and determines which ones are heresies
def get_heresies(file,cur):
    line = file.readline()
    line = line.strip()
    while line!='religion=':
        line = file.readline()
        line = line.strip()
    line = file.readline()
    brace_depth = 1
    rel_name = None
    while brace_depth != 0:
        line = file.readline()
        line = line.strip()
        if line=='{':
            brace_depth += 1
        elif line=='}':
            brace_depth -= 1
        #read in religion name
        elif brace_depth==1:
            rel_name = line[0:-1]
        #read in religion parent
        elif brace_depth==2:
            index = line.find('=')
            #parent attribute
            if line[0:index]=='parent':
                parent = line[index+1:]
                parent = parent.strip('"')
                heresy = True
                if parent=='noreligion':
                    heresy = False
                cur.execute('UPDATE religion SET heresy=? WHERE religionname=?',
                            [heresy,rel_name])
                cur.execute('UPDATE religion SET parent=? WHERE religionname=?',
                            [parent,rel_name])
            
