import io
from ..lark_parser import parse

#fills the religion table with entries of id,name,group
# IMPORTANT NOTE: we need to look at the save file to determine heresies
def get_religion(cur):
    with io.open('data/00_religions.txt',encoding="cp1252") as f:
        data = parse(f.read())
        rel_id = 1
        for rel_group in data:
            rel_obj = data[rel_group]
            if not isinstance(rel_obj, dict):
                continue
            for rel_name in rel_obj:
                obj = rel_obj[rel_name]
                if not isinstance(obj, dict):
                    continue
                # insert tuple<id, name,heresy,religiongroup>                          
                cur.execute('INSERT INTO religion Values(?,?,NULL,NULL,?)',
                    [rel_id,rel_name,rel_group]
                )
                rel_id += 1

# determines which religions are heresies according to the main save file
def get_heresies(data,cur):
    for rel_name in data:
        obj = data[rel_name]
        if 'parent' in obj:
            parent = obj.get('parent')
            heresy = True
            if parent=='noreligion':
                heresy = False
            cur.execute('UPDATE religion SET heresy=? WHERE religionname=?', [heresy, rel_name])
            cur.execute('UPDATE religion SET parent=? WHERE religionname=?', [parent, rel_name])
            
