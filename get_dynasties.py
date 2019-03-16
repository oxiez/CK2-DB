

def get_dynasties(file,cur):
    # The following code adds in-game dynasties to the game
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
                #get the name
                line = file.readline()
                line = file.readline()
                name = line[9:len(line)-2]
                #historical dynasties are missing information: name appears as f_arms
                if name=='f_arms':
                    name = None
                #add to the database
                cur.execute('INSERT INTO dynasty Values(%s,%s)',[i,name])
                #ignore the next lines until end of dynasty
                while(line!='\t\t}\n'):
                    line = file.readline()
                # the next line is either a new dynasty or the end of the file
                line = file.readline()
            done = True
    
    # add information for existant historical dynasties
    with open('00_dynasties.txt') as f:
        line = f.readline()
        while(line!='}'):
            #line is currently an id
            index = line.find('=')
            i = line[0:index]
            #get missing name   
            while(line[1:5]!='name'):
                line = f.readline()
            name = line[7:len(line)-2]
            #move until end of parse block
            while(line!='}\n' and line!='}'):
                line = f.readline()
            #add the name to the table
            cur.execute('UPDATE dynasty SET name = %s WHERE id=%s',[name,i])
            #move pointer to next integer entry
            line = f.readline()
            #end of file when nextline is nothing
            if len(line)==0:
                break
            #ignore whitespace
            while line=='\n' or line[0]=='#':
                line = f.readline()
            