from commands.command import Command, table_print

class ReligionComm(Command):
    COMM_STR = "religion"
    HELP_STR = """\

The 'religion' command allows you to explore general statistics
for all religions.
----------------------------------------------------------------------
The 'religion' command on its own lists the religions (up to a set
limit, which can be changed with the 'num_results' command) in the
game lexicographically.

We have three choices for an optional argument:
   'religion allmembers'
This sorts religions by how many characters (throughout history) have
this relgion, from largest to to smallest.

    'religion alivemembers'
This sorts religions by how many living characters have this religion,
from largest to smallest.

    'religion provinces'
This sorts religions by how many on-map provinces they have, from
largest to smallest.\n"""

    def doCommand(data,args):
        query_result = None
        headings = None
        if len(args) == 0:
            headings = ['Religion']
            query_result = data.query_religion()
        elif len(args) == 1:
            headings = ['Religion', 'Number']
            valid_args = {'allmembers','alivemembers','provinces'}
            if args[0] not in valid_args:
                print('Invalid argument. Try one of:')
                print(valid_args)
                return
            query_result = data.query_religion(args[0])
        else:
            print('ERROR: Too many arguments.')
            return
        table_print(query_result, headings)
