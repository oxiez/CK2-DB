

def get_dynasties(file,cur):
    # read until we hit the dynasties
    line = file.readline()
    done = False
    while(not done):
        line = file.readline()
        #beginning of dynasties data
        if line=='\tdynasties=\n':
            line = file.readline() #get rid of '\t{\n'
            line = file.readline()
            #while not the end of the data '\t}\n'
            while line!='\t}\n':
                #parse this dynasty
                #get the id
                i = line[2:len(line)-2]
                # 1 is bad news ''
                if i == '1': break
                #get the name
                line = file.readline()
                line = file.readline()
                name = line[9:len(line)-2]
                #add to the database
                cur.execute('INSERT INTO dynasty Values(%s,%s)',[i,name])
                print(i,name)
                #ignore the next lines until end of dynasty
                while(line!='\t\t}\n'):
                    line = file.readline()
                # the next line is either a new dynasty or the end of the file
                line = file.readline()
            done = True