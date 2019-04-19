import database
import sys

def load_file(file_name,database):
    print('Opening the file '+file_name)
    database.setup(file_name)
    print('\n')


#main function
if __name__=='__main__':
    #object that maintains connection to database and performs queries
    database = database.Data()
    
    #load data
    print('\nWelcome to the Database Systems Project\n')
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        load_file(file_name,database)
    
    # main program loop (take commands until quitting)
    print("Type 'help' for help with commands, and 'quit' to exit.")
    command = ''
    while command not in {'q','quit','exit'}:
        command = input(' : ')     
        if(len(command) == 0):
            continue 
        words = command.lower().split()

        if words[0] == 'help':
            print('Commands:')
            print(' : help [displays this text]')
            print(' : load <FILENAME> [loads a file]')
            print(' : quit [exits the program]')  
        elif words[0] == 'load' :
            if(len(words[1]) != 2):
                print('ERROR load takes one argument and one argument only')
            else:
                load_file(words[1]) 
        elif words[0]=='dynasty':
            if len(words) > 3:
                print('Too many arguments')
            elif len(words)==1:
                for i,d in enumerate(database.query_dynasties()):
                    if i > 40: break
                    print(i,d[1])
            else:
                orderby = words[1]
                if orderby not in {'wealth','prestige','piety','count'}:
                    print('invalid argument')
                else:
                    for i,d in enumerate(database.query_dynasties(orderby)):
                        if i > 40: break
                        print(i,d[1],d[2])
        
        elif words[0]=='title':
            if len(words) > 1:
                print('Too many arguments')
                continue
            elif len(words)==1:
                for i,d in enumerate(database.query_title()):
                    if i > 40: break
                    print(d[0],d[1],d[2])
        elif words[0]=='person':
            if(len(words) %2 != 1):
                print('ERROR: Please have one argument for each command')
                continue
            else:
                query_args = []
                query_arg_vals = []
                i = 1
                allowed_args = {'name', 'dynasty', 'is_male', 'birthday', 'deathday', 'father', 'real_father', 'mother', 'religion', 'culture'}
                while i < len(words):
                    if(words[i] in allowed_args):
                        query_args.append(words[i])
                        query_arg_valss.append(words[i+1])
                    else:
                        print('ERROR: ' + words[i] + ' is not a valid condition, please use one of the following values:')
                        print(allowed_args)
                    i += 2
        else:
            print('ERROR: Unknown command!')
            piety('For a list of commands, please enter \'help\'')
                        
                    