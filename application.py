import database
import sys
import texttable
from app_docs import INTRO_STRING, HELP_STRING, COMM_HELP_STRING

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
title_level = {'k': 'Kingdom',
               'e': 'Empire',
               'd': 'Duchy',
               'c': 'County',
               'b': 'Barony'}
    
#main function
if __name__=='__main__':
    #object that maintains connection to database and performs queries
    data = database.Data()
    
    #load data
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        load_file(file_name,data)
    
    # main program loop (take commands until quitting)
    print(INTRO_STRING)
    command = ''
    query_result = []
    while command not in {'q','quit','exit'}:
        command = input(' : ')     
        if(len(command) == 0):
            continue 
        words = command.lower().split()

        if words[0] == 'help':
            if len(words)==1:
                print(HELP_STRING)
            elif len(words) > 2:
                print("Too many arguments. Try 'help' or 'help <arg>' for more information on a type of command.")
            else:
                #help with a specific argument type
                comm = words[1]

                if comm in COMM_HELP_STRING:
                    print(COMM_HELP_STRING[comm])
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
                    load_file(command.split()[1],data)
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
            allowed_args = {'bloodlinename', 'founderid'}
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
            commands = ["descendant", "vassals"]
            command = 0
            for i in range(len(commands)):
                if(words[1] == commands[i]):
                    command = i
                    break
            else:
                print("ERROR: \"" + words[1] + "\" is not a valid tree command. Please use:")
                for com in commands:
                    print("- " + com)
                continue
            args = ""
            info = []
            dag = {}
            if(command == 0):
                args = " ".join(words[2:])
                info, dag = data.descendant_tree(args)
            elif(command == 1):
                if(len(words) > 3):
                    print("ERROR: 'vassals' command only takes a titleid, which is formatted like 'k_france'")
                    continue
                args = words[2]
                info, dag = data.title_tree(args)

            if(isinstance(info, list)):
                if(len(info) > 1):
                    display = True
                    if(len(info) > 10):
                        confirm = input("WARN: {} results found for \"{}\". Display? (y/N): ".format(len(info), args))
                        if(not confirm.lower() == 'y'):
                             display = False
                    if(display):
                        table = texttable.Texttable(max_width=210)
                        table.header(("ID", "Name"))
                        table.add_rows(info, header=False)
                        print(table.draw())
                        print("WARN: {} results found. Please rerun this command with an id from above".format(len(info)))
                else:
                    if(command == 0):
                        print("INFO: No person matched with {}, try again.".format(args))
                        continue
                    elif(command == 1):
                        print("INFO: No title has the titleid {}, try again.".format(args))
                        continue
            else: # Can only be a dict
                if(len(dag) == 0):
                    if(command == 0):
                        print("No descendants found for {}: {}".format(info[0][0], info[0][1]))
                    else:
                        name = info["start"][1]
                        name = name[0].upper() + name[1:]
                        print("No vassals for The {} of {}".format(title_level[info["start"][2]], name))
                else:
                    stack = []
                    stack_above = []
                    if(command == 0):
                        print("Printing descendants of {}: {}".format(info[0][0], info[0][1]))
                        print("{}: {}".format(info[0][0], info[0][1]))
                        stack = [dag[info[0][0]]]
                        # Keep track of whose child it is
                        stack_above = [info[0][0]]
                    else:
                        name = info["start"][1]
                        name = name[0].upper() + name[1:]
                        print("Printing vassals of The {} of {}".format(title_level[info["start"][2]], name))
                        print("The {} of {}".format(title_level[info["start"][2]], name))
                        stack = [dag[info["start"][0]]]
                        stack_above  = [info["start"][0]]
                    while(len(stack) > 0):
                        id = stack[-1].pop()
                        tree_spacer(stack)
                        if(command == 0):
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
                        else:
                            print("\u2502")
                            tree_spacer(stack)
                            
                        if(len(stack[-1]) > 0):
                            print("\u251C", end="")
                        else:
                            print("\u2514", end="")

                        if(command == 0):
                            print("\u2500\u2500\u2500{}: {}".format(info[id][0], info[id][1]))
                        else:
                            name = info[id][2]
                            name = name[0].upper() + name[1:]
                            print("\u2500\u2500\u2500The {} of {}".format(title_level[info[id][3]], name))
                            
                        if(id in dag): # Has children
                            stack += [dag[id]]
                            stack_above.append(id)
                        while(len(stack) > 0 and len(stack[-1]) == 0):
                            stack.pop()
                            stack_above.pop()

        else:
            print('ERROR: Unknown command!')
            print("For a list of commands, please enter 'help'")                        
                    
