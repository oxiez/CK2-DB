
def get_traits(cur):
    trait_files = ['00_traits.txt','01_traits.txt',
                   '02_traits.txt','03_traits.txt']
    trait_id = 1
    for file in trait_files:
        trait_id = add_traits(file,cur,trait_id)


def add_traits(file,cur,trait_id):
    #open the file and add traits to the traitlookup relation
    with open(file) as f:
        for line in f.readlines():
            if line.find('=')!=-1 and line.find('{')!=-1 and line[0]!='\t':
                name = line[0:line.find('=')-1]
                if name.find('#')!=-1: continue
                cur.execute('INSERT INTO traitlookup Values(%s,%s)',[trait_id,name])
                trait_id += 1
    return trait_id