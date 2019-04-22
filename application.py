import database
import sys
import texttable

# loads the given file name using a database object
def load_file(file_name,data):
    print('Opening the file '+file_name)
    data.setup(file_name)
    print('\n')

#how many rows every query will return
ROW_COUNT = 40

# helper function for printing tables of data
def table_print(data,headings=None):
    table = texttable.Texttable()
    if headings!=None:
        table.header(headings)
    table.set_max_width(210)
    for i,v in enumerate(query_result):
        if i >= ROW_COUNT: break
        row = []
        row = row + [str(x) for x in v]
        table.add_row(row)
    t = table.draw()
    print(t)    

def tree_spacer(stack):
    level = len(stack) - 1
    for i in range(0,level):
        if(len(stack[i]) > 0):
            print("\u2502   ", end="")
        else:
            print("    ", end="")

help_string = """
Welcome to the Crusader Kings 2 Database Project!
----------------------------------------------------------------------
In this application, you can learn about the details of the world 
stored within save files from the game Crusader Kings 2. 
----------------------------------------------------------------------
Some things you can do:
- You can get bios for any character containing
  - Date of birth and death
  - Their statistics
  - Religion
- Get all members of a religion/culture
- See the largest religion/culture (province wise)
- List all descendants of a character
- And much more...

Type 'help' for all the commands you can insert. Type 'help <command>' 
for more information about a command. You can also exit the 
application with 'quit'
"""
    
#main function
if __name__=='__main__':
    #object that maintains connection to database and performs queries
    data = database.Data()
    
    #load data
    #print('\nWelcome to the Database Systems Project\n')
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        load_file(file_name,data)
    
    # main program loop (take commands until quitting)
    print(help_string)
    command = ''
    query_result = []
    while command not in {'q','quit','exit'}:
        command = input(' : ')     
        if(len(command) == 0):
            continue 
        words = command.lower().split()

        if words[0] == 'help':
            if len(words)==1:
                print('Commands:')
                print(' - dynasty <args> [displays information on dynasties]')
                print(' - title <args> [displays information on titles]')
                print(' - person <args> [displays information on characters]')
                print(' - bio <ID> [displays information on the character with the given ID]')
                print(' - religion <arg> [displays information on religions]')
                print(' - culture <arg> [displays information on cultures]')
                print(' - bloodline <arg> [displays information on bloodlines]')
                print(' - bloodline_members <ID> [displays characters with bloodline of ID]')
                print(' - tree descendant <name/ID> [displays family tree beginning with the given person]')
                print(' - help <command> [displays this text, or with an argument, explains a command]')
                print(' - num_results <NUM> [changes the number of results displayed to NUM]')
                print(' - load <FILENAME> [loads a file]')
                print(' - quit [exits the program]')
            elif len(words) > 2:
                print("Too many arguments. Try 'help' or 'help <arg>' for more information on a type of command.")
            else:
                #help with a specific argument type
                comm = words[1]
                if comm=='dynasty':
                    print(
"""The dynasty command is used to explore the different dynsaties of the game.
On its own, the command 'dynasty' will list some of the dynasties in the game.
Optionally, we can add arguments to match the name, religion, or culture.
For example, if we wanted to find catholic, frankish dynasties,
we can enter 'dynasty religion catholic culture frankish'.
The 'orderby' argument can be followed by one of prestige, piety, wealth, and count (number of members).
This will sort the results of the search by this term, descending from greatest to least.
To build on our previous example, if we wanted to sort by prestige, we can write
'dynasty orderby prestige religion catholic culture frankish'."""
                    )
                elif comm=='title':
                    print("""\
The title command can be used in three ways:            e.g.
 - to find the titles owned by a specific character     title 6392
 - to find the history of rulers of a given title       title ruler k_france
 - to find the current holder of a given title          title current k_france"""
                        )
                elif comm=='person':
                    print("""\
The person command on its own lists characters stored in the save file.
Optionally, we can add argument/value pairs to find people with a name, dynasty, religion or culture similar to a given string.
Also, we can specify a number for fertility, health, wealth, prestige or piety, which will restrict the results to characters
that have a value greater than or equal to the amount specified.
For example, the command 'person name will dynasty de health 1 prestige 100'
will find characters with 1 or more health and 100 or more prestige who have a name like 'will' and are in a dynasty with the substring 'de'."""
                          )
                elif comm=='bio':
                    print("""\
The bio command requires a single argument: the ID of a person. You can find a personID by using
person commands. The bio command prints information about the given character, such as name, date of birth, date of death,
sex, religion, culture, attributes, traits, titles, claims, and so on."""
                          )
                elif comm=='religion':
                    print("""\
The 'religion' command on its own lists the religions in the game lexicographically.
We have three choices for an optional argument:
 - 'religion allmembers'   sorts religions by how many characters (throughout history) have this relgion
 - 'religion alivemembers' sorts religions by how many living characters have this religion
 - 'religion provinces'    sorts religions by how many on-map provinces they have"""
                          )
                elif comm=='culture':
                    print("""\
The 'culture' command on its own lists the cultures in the game lexicographically.
We have three choices for an optional argument:
 - 'culture allmembers'   sorts cultures by how many characters (throughout history) have this culture
 - 'culture alivemembers' sorts cultures by how many living characters have this culture
 - 'culture provinces'    sorts cultures by how many on-map provinces they have"""
                          )
                elif comm=='bloodline':
                    print("""\
The 'bloodline' command on its own lists the bloodlines in the game by their ID.
Optional arguments can be added for 'bloodlinename' (to match the string of the type)
and for 'founderID' (being the personID of the founder of the bloodline)."""
                          )
                elif comm=='bloodline_members':
                    print("""\
The 'bloodline_members' command takes one argument, being the ID of the bloodline.
It then prints all of the members of the bloodline."""
                          )
                elif comm=='tree':
                    print("""\
The 'tree' command prints a family tree. To generate the family tree of a person
with a specific id, enter 'tree descendant ID'. If you are looking someone with a
certain name, you can enter 'tree descendant name', and then options will come up
for you to choose from."""
                          )
                elif comm=='help':
                    print("""\
The help command (attempts) to display helpful information about how to use this application.
'help' on its own displays the commands that the user can use.
'help cmd' displays information on how to use the command 'cmd'."""
                          )
                elif comm=='num_results':
                    print("""\
The num_results command is used to restrict the number of results that a command can return.
For example, if we wanted to restrict the number of rows from future commands to ten,
we can enter the command 'num_results 10'."""
                          )
                elif comm=='load':
                    print("""\
The load command is used to load in data from a save file.
For example, 'load leon1067_02_12.ck2' will use the data from that save game."""
                          )
                elif comm=='quit':
                    print("""\
Exits the program. Can also use 'q' or 'exit'.""")
                else:
                    print("Did not recognize command '" + comm + "'. Type help to see the list of commands.")
                
                
                
                                                
        elif words[0] in {'q','quit','exit'}:
            break

        #load data from another file
        elif words[0] == 'load' :
            if(len(words) != 2):
                print('ERROR load takes one argument and one argument only')
            else:
                #attempt at error handling here could be improved
                try:
                    load_file(words[1],data)
                except:
                    print('ERROR: issue loading file ' + words[1]+'.')
                    data = database.Data()
        #set number of rows
        elif words[0] == 'num_results' :
            if(len(words) != 2):
                print('ERROR num_results takes one argument and one argument only')
            else:
                try:
                    ROW_COUNT = int(words[1])
                    print('Number of rows set to ' + str(ROW_COUNT))
                except:
                    print("ERROR: num_results must take a number as its argument")
        
        #dynasty queries  
        elif words[0]=='dynasty':
            if(len(words) %2 != 1):
                print('ERROR: Please have one argument for each command')
                continue            
            query_args = []
            query_arg_vals = []
            i = 1
            allowed_args = {'name', 'orderby', 'religion', 'culture'}
            valid = True
            has_orderby = False
            while i < len(words):
                if(words[i] in allowed_args):
                    valid_vals = {'prestige','piety','wealth','count'}
                    if words[i]=='orderby':
                        if has_orderby:
                            valid = False
                            print('ERROR: Query contained a second orderby term. Queries should contain zero or one orderby term.')
                            break
                        has_orderby = True
                        if words[i+1] not in valid_vals:
                            print('ERROR: ' + words[i+1] + ' is not a valid value to order by. Please use one of:')
                            print(valid_vals)
                            valid = False
                    if valid:
                        query_args.append(words[i])
                        query_arg_vals.append(words[i+1])
                else:
                    print('ERROR: ' + words[i] + ' is not a valid condition, please use one of the following values:')
                    print(allowed_args)
                    valid = False
                i += 2
            #get person with these conditions
            if valid:
                query_result = data.query_dynasty(query_args,query_arg_vals)
                table = texttable.Texttable()
                table.set_max_width(210)
                table_print(query_result)
        
        #title queries
        elif words[0]=='title':
            headings = None
            # title on its own returns ???
            if len(words)==1:
                print('Title queries should be of the form : title personid or title rulers titleid or title current titleid')
                continue
 
            # title id returns all titles of the given personid
            elif len(words)==2:
                query_result = data.query_title(words[1])
                headings = ['Person ID', 'Name', 'Dynasty', 'Title Name', 'Title ID']
            # we are looking for personID(s) given a certain title
            elif len(words)==3:
                #rulers
                if words[1]=='rulers':
                    query_result = data.query_rulers(words[2])
                    headings = ['personid', 'Name', 'Dynasty', 'Date of Birth', 'Date of Death', 'Start of Rule']
                #current
                elif words[1]=='current':
                    query_result = data.query_ruler(words[2])
                    headings = ['personid','Name','Dynasty']
                else:
                    print("Queries should be of the form 'title (rulers|current) titleid.'")
                    continue
            else:
                print('Title queries should be of the form : title personid or title rulers titleid or title current titleid')
                continue            
            table_print(query_result,headings)
        
        #person queries
        elif words[0]=='person':
            if(len(words) %2 != 1):
                print('ERROR: Please have one argument for each command')
                continue
            query_args = []
            query_arg_vals = []
            i = 1
            allowed_args = {'name', 'dynasty', 'ismale', 'birthday', 'deathday', 'father', 'real_father', 'mother', 'religion', 'culture', 'fertility', 'health', 'wealth', 'prestige', 'piety'}
            valid = True
            while i < len(words):
                if(words[i] in allowed_args):
                    query_args.append(words[i])
                    query_arg_vals.append(words[i+1])
                else:
                    print('ERROR: ' + words[i] + ' is not a valid condition, please use one of the following values:')
                    print(allowed_args)
                    valid = False
                i += 2
            #get person with these conditions
            if valid:
                table = texttable.Texttable()
                headings = ['ID', 'Name', 'Dynasty', 'is Male', 'Birthday', 'Deathday', 'Father', 'Real Father', 'Mother', 'Religion', 'Culture', 'Fertility', 'Health', 'Wealth', 'Prestige', 'Piety']
                query_result = data.query_person(query_args,query_arg_vals)
                table_print(query_result,headings)
        
        #bio query: gets the full information on a person
        elif words[0]=='bio':
            if len(words)!=2:
                print('ERROR: query should be of the form bio personID.')
                continue
            query_result = data.query_personid(words[1])
            if len(query_result)==0:
                print('Could not find person with personID ' + words[1])
            else:
                personid,birthname,dynastyname,ismale,birthday,deathday,fatherid,real_fatherid,motherid,religionname,culturename,fertility,health,wealth,hostid,prestige,piety,employerid,martial,diplomacy,stewardship,intrigue,learning = query_result[0]
                #full name
                print(birthname + (' ' + dynastyname if dynastyname != None else ''))
                #dates
                print('Born: ' + str(birthday) + ('' if deathday == None else '    Died: '+str(deathday)))
                # parents
                if fatherid!=None:
                    father_query = data.query_personid(fatherid)[0]
                    print('Father: ' + str(father_query[1]) + ' ' + ('' if father_query[2] == None else str(father_query[2])+' ') + str(fatherid))
                if fatherid!=real_fatherid:
                    father_query = data.query_personid(real_fatherid)[0]
                    print('Real Father: ' + str(father_query[1]) + ' ' + ('' if father_query[2] == None else str(father_query[2])+' ') + str(real_fatherid))
                if motherid!=None:
                    mother_query = data.query_personid(motherid)[0]
                    print('Mother: '  + str(mother_query[1]) + ' ' + ('' if mother_query[2] == None else str(mother_query[2])+ ' ') + str(motherid))
                #spouse
                spouses = data.query_spouse(personid)
                for s in spouses:
                    spouseid = s[0]
                    spouse_query = data.query_personid(spouseid)[0]
                    print('Spouse: '  + str(spouse_query[1]) + ' ' + ('' if spouse_query[2] == None else str(spouse_query[2])+ ' ') + str(spouseid))
                #titles
                titles = data.query_title(personid)
                if len(titles)!=0:
                    print('Titles: ' + ', '.join([x[4] for x in titles]))
                #claims
                claims = data.query_claim(personid)
                if len(claims)!=0:
                    print('Claims: ' + ', '.join([x[0] for x in claims]))
                #personal info
                print('Sex: ' + ('M' if ismale else 'F') + '    Religion: ' + religionname + '    Culture: ' + culturename)
                if deathday == None:
                    print('Prestige: ' + str(prestige) + '    Piety: ' + str(piety) + '    Health: ' + str(health) + '    Wealth: ' + str(wealth) + '    Fertility: ' + str(fertility))
                print('Attributes: martial ' + str(martial) + ', diplomacy ' + str(diplomacy) + ', stewardship ' + str(stewardship) + ', intrigue ' + str(intrigue) + ', learning ' + str(learning))
                print('Traits: ' + ', '.join([x[0] for x in data.query_traits(words[1])]))
                
        #religion
        elif words[0]=='religion':
            if len(words) == 1:
                headings = ['Religion']
                query_result = data.query_religion()
            elif len(words) == 2:
                headings = ['Religion', 'Number']
                valid_args = {'allmembers','alivemembers','provinces'}
                if words[1] not in valid_args:
                    print('Invalid argument. Try one of:')
                    print(valid_args)
                    continue
                query_result = data.query_religion(words[1])
            else:
                print('ERROR: Too many arguments.')
                continue
            table = texttable.Texttable()
            table_print(query_result, headings)
        
        #culture
        elif words[0]=='culture':
            if len(words) == 1:
                headings = ['Culture']
                query_result = data.query_culture()
            elif len(words) == 2:
                headings = ['Culture', 'Number']
                valid_args = {'allmembers','alivemembers','provinces'}
                if words[1] not in valid_args:
                    print('Invalid argument. Try one of:')
                    print(valid_args)
                    continue
                query_result = data.query_culture(words[1])
            else:
                print('ERROR: Too many arguments.')
                continue
            table_print(query_result, headings)

        #bloodlines
        elif words[0]=='bloodline':
            query_args = []
            if(len(words) %2 != 1):
                print('ERROR: Please have one argument for each command')
                continue
            query_arg_vals = []
            i = 1
            allowed_args = {'bloodlinename', 'founderID'}
            valid = True
            while i < len(words):
                if(words[i] in allowed_args):
                    query_args.append(words[i])
                    query_arg_vals.append(words[i+1])
                else:
                    print('ERROR: ' + words[i] + ' is not a valid condition, please use one of the following values:')
                    print(allowed_args)
                    valid = False
                i += 2
            if valid:
                headings = ['ID', 'Type', 'Founder']
                query_result = data.query_bloodline(query_args,query_arg_vals)
                table_print(query_result,headings)

        elif words[0]=='bloodline_members':
            if(len(words) != 2):
                print('ERROR bloodline_members takes one argument (the id of the bloodline) and one argument only')
            else:
                headings = ['Name', 'Dynasty']
                query_result = data.query_bloodline_members(words[1])
                table_print(query_result,headings)

        elif words[0]=="tree":
            if(len(words) < 3):
                print("ERROR: Please format the tree command like so:\ntree <descendant> <person name/id>")
                continue
            commands = ["descendant"]
            command = ""
            if(words[1] in commands):
                command = words[1]
            else:
                print("ERROR: \"" + words[1] + "\" is not a valid tree command. Please use:")
                for com in commands:
                    print("- " + com)
                continue
            
            args = " ".join(words[2:])
            info, dag = data.descendant_tree(args)

            if(isinstance(info, list)):
                if(len(info) > 1):
                    display = True
                    if(len(info) > 10):
                        confirm = input("INFO: {} results found for \"{}\". Display? (y/N): ".format(len(info), args))
                        if(not confirm.lower() == 'y'):
                             display = False
                    if(display):
                        table = texttable.Texttable(max_width=210)
                        table.header(("ID", "Name"))
                        table.add_rows(info, header=False)
                        print(table.draw())
                        print("INFO: {} results found. Please rerun this command with an id from above".format(len(info)))
                else:
                    print("INFO: No person matched with {}, try again.".format(args))
            else: # Can only be a dict
                if(len(dag) == 0):
                    print("No descendants found for {}: {}".format(info[0][0], info[0][1]))
                else:
                    print("Printing descendants of {}: {}".format(info[0][0], info[0][1]))
                    print("{}: {}".format(info[0][0], info[0][1]))
                    stack = [dag[info[0][0]]]
                    # Keep track of whose child it is
                    stack_above = [info[0][0]]
                    while(len(stack) > 0):
                        id = stack[-1].pop()
                        tree_spacer(stack)
                        if(stack_above[-1] == info[id][2] and info[id][4]):
                            print("\u2502   ")
                            tree_spacer(stack)
                            print("\u2502   Father: ({}: {})".format(info[id][4], info[id][5]))
                        elif(stack_above[-1] == info[id][4] and info[id][2]):
                            print("\u2502   ")
                            tree_spacer(stack)
                            print("\u2502   Mother: ({}: {})".format(info[id][2], info[id][3]))
                        else:
                            print("\u2502")
                        tree_spacer(stack)
                        if(len(stack[-1]) > 0):
                            print("\u251C", end="")
                        else:
                            print("\u2514", end="")
                        print("\u2500\u2500\u2500{}: {}".format(info[id][0], info[id][1])) 
                        
                        if(id in dag): # Has children
                            stack += [dag[id]]
                            stack_above.append(id)
                        while(len(stack) > 0 and len(stack[-1]) == 0):
                            stack.pop()
                            stack_above.pop()

        else:
            print('ERROR: Unknown command!')
            print("For a list of commands, please enter 'help'")                        
                    
