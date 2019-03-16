

def get_dynasties(file,cur):
    # read until we hit the dynasties
    line = file.readline()
    done = False
    while(not done):
        line = file.readline()
        #beginning of dynasties data
        if line=='\tdynasties\n':
            #while not the end of the data
            while line!='\t}':
                #parse 14 lines 
                line = line.readline()
                #get the id
                i = line[2:len(line-1)]
                line = f.readline()
                #get the name
                name = line[2:len(line-1)]
                #add to the database
                cur.execute('INSERT INTO dynasty Values(%s,%s)',[i,name])
                #ignore the next 12 lines
                for i in range(12):
                    line = line.readline()
            done = True