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
    #
    command = ''
    while command not in {'q','quit','exit'}:
        command = input(' : ')
        if command == 'help':
            print('Commands:')
            print(' : help [displays this text]')
            print(' : quit [exits the program]')            
        else:
            pass