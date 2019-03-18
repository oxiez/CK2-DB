import io

def get_culture(cur):
    with io.open('00_cultures.txt',encoding="cp1252") as f:
        #setup
        line = None
        #variable initialization
        cul_id = 1
        cul_name = None
        cul_group = None 
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
            cul_group = line[0:index-1]
            brace_depth = 1
            #find the next religion in this group            
            while brace_depth > 0:
                line = f.readline()
                line.strip()
                if '{' in line:
                    brace_depth += 1
                    index = line.find('=')
                    if index != -1 and brace_depth==2:
                        cul_name = line[0:index-1]
                        cul_name = cul_name.strip()
                        #make sure this isnt some other parameter
                        if not cul_name in ['male_names','female_names','color','alternate_start','graphical_cultures']:
                            # insert tuple<id, name,heresy,religiongroup>                          
                            cur.execute('INSERT INTO culture Values(%s,%s,%s)',
                                    [cul_id,cul_name,cul_group])
                            cul_id += 1
                if '}' in line:
                    brace_depth -= 1