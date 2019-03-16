

def get_dynasties(file,cur):
    # read until we hit the dynasties
    line = file.readline()
    while(line):
        line = file.readline()
        
        #beginning of dynasties data
        if line=='\tdynasties\n':
            #every dynasty has 14 lines of information
            i = line[2:len(line-1)]
            cur.execute('INSERT INTO dynasty Values(%s,%s)',[i,name])
        
        #end of dynasties data
        if line=='\t}': break