INTRO_STRING = """
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

HELP_STRING = """\

Commands:
 - dynasty <args>            [displays information on dynasties]
 - title <args>              [displays information on titles]
 - person <args>             [displays information on characters]
 - bio <ID>                  [displays information on the character with the given ID]
 - religion <arg>            [displays information on religions]
 - culture <arg>             [displays information on cultures]
 - bloodline <arg>           [displays information on bloodlines]
 - bloodline_members <ID>    [displays characters with bloodline of ID]
 - tree <cmd> <cmd args>     [displays various info in a tree-based format]
 - help <command>            [displays this text, or with an argument, explains a command]
 - num_results <NUM>         [changes the number of results displayed to NUM]
 - load <FILENAME>           [loads a file]
 - quit                      [exits the program]

If you are confused about a command, type 'help <command>' for a more specific list of 
things that command can do.\n"""

HELP_HELP = """\

    The 'help' command (attempts) to display helpful information about 
how to use this application.
----------------------------------------------------------------------
'help' on its own displays the commands that the user can use.
'help <cmd>' displays information on how to use the command 'cmd'.\n"""

NUM_RESULTS_HELP =  """\
    The 'num_results' command is used to restrict the number of results
that a command can return.
----------------------------------------------------------------------
The 'num_results' command requires 1 argument:

    'num_results <integer>'

For example:
    'num_results 10'
Will restrict the number of rows from future commands to 10.\n"""

QUIT_HELP= """\

Exits the program. Can also use 'q' or 'exit'.\n"""
