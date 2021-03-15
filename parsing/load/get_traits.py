import io
from ..lark_parser import parse

def get_traits(cur):
    trait_files = ['data/00_traits.txt', 'data/01_traits.txt',
                   'data/02_traits.txt', 'data/03_traits.txt']
    trait_id = 1
    for t_file in trait_files:
        with io.open(t_file,encoding="cp1252") as f:
            data = parse(f.read())
            # if a traits file has only one trait, it comes back as a tuple (trait_name, trait_data_dict)
            if isinstance(data,tuple):
                data = [data[0]]
            for trait_name in data:
                cur.execute('INSERT INTO traitlookup Values(?,?)',[trait_id,trait_name])
                trait_id += 1
