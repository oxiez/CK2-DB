import io
from ..lark_parser import parse

#read in historical dynasties first 
def get_hist_dynasties(cur):
    with io.open('data/00_dynasties.txt',encoding="cp1252") as f:
        data = parse(f.read())
        for dntID in data:
            obj = data.get(dntID)
            # NOTE: some dynasties have duplicate dynastyIDs e.g.  1061019, 1061019, 105946, 1059971, 1062442, 1062594
            # handle collisions by using the dynasty object furthest down the file
            if isinstance(obj,list):
                obj = obj[-1]
            name = obj.get('name')
            cultureID = None
            religionID = None
            if 'culture' in obj:
                cur.execute('SELECT cultureID FROM culture WHERE cultureName=?',[obj.get('culture')])
                cultureID = cur.fetchone()[0]
            if 'religion' in obj:
                cur.execute('SELECT religionID FROM religion WHERE religionName=?',[obj.get('religion')])
                religionID = cur.fetchone()[0]                    
            cur.execute('INSERT INTO dynasty Values(?,?,?,?)',[dntID,name,cultureID,religionID])
        
#read in the save game dynasties 
def get_dynasties(data, cur):
    for dntID in data:
        name = None
        cultureID = None
        religionID = None    
        obj = data[dntID]
        if 'name' in obj:
            name = obj['name']
        if 'culture' in obj:
            cur.execute('SELECT cultureID FROM culture WHERE cultureName=?',[obj['culture']])
            cultureID = cur.fetchone()[0]
        if 'religion' in obj: 
            cur.execute('SELECT religionID FROM religion WHERE religionName=?',[obj['religion']])
            religionID = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM dynasty WHERE dynastyID=?',[dntID])
        count = cur.fetchone()[0]
        if count > 0:
            if name != None: cur.execute('UPDATE dynasty SET dynastyname=? WHERE dynastyID=?',[name])
            if cultureID != None: cur.execute('UPDATE dynasty SET dynastyname=? WHERE dynastyID=?',[cultureID])
            if religionID != None: cur.execute('UPDATE dynasty SET dynastyname=? WHERE dynastyID=?',[religionID])
        else:
            cur.execute('INSERT INTO dynasty Values(?,?,?,?)',[dntID,name,cultureID,religionID])
