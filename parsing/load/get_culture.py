import io
from ..lark_parser import parse

def get_culture(cur):
    with io.open('data/00_cultures.txt',encoding="cp1252") as f:
        data = parse(f.read())
        cul_id = 1
        for cul_group in data:
            cul_obj = data[cul_group]
            if not isinstance(cul_obj, dict):
                continue
            for cul_name in cul_obj:
                obj = cul_obj[cul_name]
                if not isinstance(obj, dict):
                    continue
                # every culture has a male_names parameter
                if 'male_names' not in obj:
                    continue

                cur.execute('INSERT INTO culture Values(?,?,?)',
                        [cul_id,cul_name,cul_group]
                )
                cul_id += 1
