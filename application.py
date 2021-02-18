import database
import sys
import texttable
from app_docs import *
from commands import *

#main function
if __name__=='__main__':

    # lookup table of command strings to Command implementations
    command_map = {c.COMM_STR : c for c in command.Command.__subclasses__()}
    
    #object that maintains connection to database and performs queries
    data = database.Data()
    
    #load data
    if len(sys.argv) > 1:
        load_comm.load_file(sys.argv[1],data)
    
    # main program loop (take commands until quitting)
    print(INTRO_STRING)

    while True:
        user_input = input(' : ')     
        if(len(user_input) == 0):
            continue 
        words = user_input.lower().split()
        comm = words[0]
        args = words[1:]

        if comm in {'q','quit','exit'}:
            break

        elif comm == 'help':
            if len(words)==1:
                print(HELP_STRING)
            elif len(words) > 2:
                print("Too many arguments. Try 'help' or 'help <arg>' for more information on a type of command.")
            else:
                # help with a specific argument type
                comm_help = args[0]
                if comm_help == "help":
                    print(HELP_HELP)
                elif comm_help == "quit":
                    print(QUIT_HELP)
                elif comm_help == "num_results":
                    print(NUM_RESULTS_HELP)
                elif comm_help in command_map:
                    print(command_map[comm_help].HELP_STR)
                else:
                    print("Did not recognize command '" + comm_help + "'. Type help to see the list of commands.")

        #set number of rows
        elif comm == 'num_results' :
            if(len(words) != 2):
                print('ERROR num_results takes one argument and one argument only')
            else:
                try:
                    command.row_count = int(args[0])
                    print('Number of rows set to ' + str(command.row_count))
                except:
                    print("ERROR: num_results must take a number as its argument")

        elif comm in command_map:
            command_map[comm].doCommand(data,args)

        else:
            print('ERROR: Unknown command!')
            print("For a list of commands, please enter 'help'")                        
                    
