

def get_dynasties(file,cur):
    # read until we hit the dynasties
    line = file.readline()
    while(line):
        line = file.readline()
        if line=='\t':
            cur.execute('INSERT INTO ')
        
        if line=='\t}': break