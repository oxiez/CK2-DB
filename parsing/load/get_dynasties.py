import io
from .ck2_parser import ck2_parser


dynasty_regex = {'^name':None,'^culture':None,'^religion':None}

def get_dynasties(file,cur):
    #read in historical dynasties first 
    '''
    with io.open('data/00_dynasties.txt',encoding="cp1252") as f:
        obj = ck2_parser.getCK2Obj(f,dynasty_regex)  
        while obj != None:
            name = None
            cultureID = None
            religionID = None
            dntID = obj.get('tag')
            if 'name' in obj:
                name = obj['name']
            if 'culture' in obj:
                cur.execute('SELECT cultureID FROM culture WHERE cultureName=?',[obj['culture'].strip().strip('"')])
                cultureID = cur.fetchone()[0]
            if 'religion' in obj: 
                cur.execute('SELECT religionID FROM religion WHERE religionName=?',[obj['religion'].strip().strip('"')])
                religionID = cur.fetchone()[0]
            cur.execute('INSERT INTO dynasty Values(?,?,?,?)',[dntID,name,cultureID,religionID])
            print(dntID,name,cultureID,religionID)
            obj = ck2_parser.getCK2Obj(f,dynasty_regex)
    '''
    
    with io.open('data/00_dynasties.txt',encoding="cp1252") as f:
        line = ' '
        while line:
            #print(line)
            line = f.readline()
            if len(line)==0: break
            if line == '\n' or line[0]=='#': continue
            dntID = line[0:line.find('=')].strip()
            line = f.readline()
            name = None
            cultureID = None
            religionID = None
            while line != '}\n' and line != '}':
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
                        cur.execute('SELECT cultureID FROM culture WHERE cultureName=?',[value])
                        cultureID = cur.fetchone()[0]
                    if key=='religion' and religionID==None and '}' not in value:
                        cur.execute('SELECT religionID FROM religion WHERE religionName=?',[value])
                        religionID = cur.fetchone()[0]                    
                line = f.readline()
            #add this dynasty to the table
            #NOTE: dynastyID 1061019 corresponds to two dynasties!!! von Hanover and Tiversti
            if dntID in ['1061019', '105946', '1059971', '1062442', '1062594']: continue
            #print(dntID,name,cultureID,religionID)
            cur.execute('INSERT INTO dynasty Values(?,?,?,?)',[dntID,name,cultureID,religionID])
        
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
            cur.execute('SELECT cultureID FROM culture WHERE cultureName=?',[obj['culture'].strip().strip('"')])
            cultureID = cur.fetchone()[0]
        if 'religion' in obj: 
            cur.execute('SELECT religionID FROM religion WHERE religionName=?',[obj['religion'].strip().strip('"')])
            religionID = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM dynasty WHERE dynastyID=?',[dntID])
        count = cur.fetchone()[0]
        if count > 0:
            if name != None: cur.execute('UPDATE dynasty SET dynastyname=? WHERE dynastyID=?',[name])
            if cultureID != None: cur.execute('UPDATE dynasty SET dynastyname=? WHERE dynastyID=?',[cultureID])
            if religionID != None: cur.execute('UPDATE dynasty SET dynastyname=? WHERE dynastyID=?',[religionID])
        else:
            cur.execute('INSERT INTO dynasty Values(?,?,?,?)',[dntID,name,cultureID,religionID])
        obj = ck2_parser.getCK2Obj(file,dynasty_regex)
