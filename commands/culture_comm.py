from commands.command import Command, table_print

class CultureComm(Command):
    COMM_STR = "culture"
    HELP_STR = """\

    The 'culture' command allows you to explore general statistics
for all cultures.
----------------------------------------------------------------------
The 'culture' command on its own lists the cultures (up to a set
limit, which can be changed with the 'num_results' command) in the
game lexicographically.

We have three choices for an optional argument:

    'culture allmembers'
Which sorts cultures by how many characters (throughout history) have
had this culture, from largest to smallest.

    'culture alivemembers'
 Which sorts cultures by how many currently alive characters have this
 culture, from largest to smallest.

    'culture provinces'
 Which sorts cultures by how many on-map provinces they have, from
 largest to smallest.\n"""
    
    def doCommand(data,args):
        query_result = None
        headings = None
        if len(args) == 0:
            headings = ['Culture']
            query_result = data.query_culture()
        elif len(args) == 1:
            headings = ['Culture', 'Number']
            valid_args = {'allmembers','alivemembers','provinces'}
            if args[0] not in valid_args:
                print('Invalid argument. Try one of:')
                print(valid_args)
                return
            query_result = data.query_culture(args[0])
        else:
            print('ERROR: Too many arguments.')
            return
        table_print(query_result, headings)
