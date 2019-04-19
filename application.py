import database
import sys



#main function
if __name__=='__main__':
    print('\nWelcome to the Database Systems Project\n')
    file_name = "Leon1067_02_12.ck2"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    print('Opening the file '+file_name)
    database.setup(file_name)
    print('\n')
    
    print("Type 'help' for help with commands, and 'quit' to exit.")
    
    # main program loop (take commands until quitting)
    command = ''
    while command not in {'q','quit','exit'}:
        command = input(' : ')
        if command == 'help':
            print('Commands:')
            print(' : help [displays this text]')
            print(' : quit [exits the program]')            
        else:
            words = command.split()
            if words[0]=='dynasty':
                if len(words) > 3:
                    print('Too many arguments')
                elif len(words)==1:
                    for i,d in enumerate(database.query_dynasty()):
                        if i > 40: break
                        print(d[0])
                else:
                    orderby = words[1]
                    if orderby not in {'wealth','prestige','piety'}:
                        print('invalid argument')
                    else:
                        for i,d in enumerate(database.query_dynasty(orderby)):
                            if i > 40: break
                            print(d[0],d[1])
                        
                    