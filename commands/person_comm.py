from commands.command import Command, table_print

class PersonComm(Command):
    COMM_STR = "person"
    HELP_STR = """\

The 'person' command allows you to explore different characters
within the game.
----------------------------------------------------------------------
The command 'person' alone will display characters (up to a set limit,
which can be chagned with the 'num_results' command) within the game.
To narrow down your query, you can use the following:

    'person <keyw_1> <keyw_1 arg> ... <keyw_n> <keyw_n arg>'

Keywords can be any of the following (in any order):
- name            [limit to characters with a similar name]
- dynasty         [limit to characters with a similar dynasty name]
- religion        [limit to characters with a similar religion name]
- culture         [limit to characters with a similar culture name]
- fertility       [limit to characters with a higher fertility value]
- health          [limit to characters with a higher health value]
- prestige        [limit to characters with a higher prestige value]
- piety           [limit to characters with a higher piety value]

For example:
    'person name will dynasty de health 1 prestige 100'
Will find characters that:
- Have 1 or more health
- Have 100 or more prestige
- Have a name like 'will'
- Are in a dynasty with the substring 'de'.\n"""

    def doCommand(data,args):
        if(len(args)%2 != 0):
            print('ERROR: Please have one argument for each command')
            return
        query_args = []
        query_arg_vals = []
        i = 0
        allowed_args = {'name', 'dynasty', 'ismale', 'birthday', 'deathday', 'father', 'real_father', 'mother', 'religion', 'culture', 'fertility', 'health', 'wealth', 'prestige', 'piety'}
        valid = True
        while i < len(args):
            if(args[i] in allowed_args):
                query_args.append(args[i])
                query_arg_vals.append(args[i+1])
            else:
                print('ERROR: ' + args[i] + ' is not a valid condition, please use one of the following values:')
                print(allowed_args)
                return
            i += 2
        #get person with these conditions
        headings = ['ID', 'Name', 'Dynasty', 'is Male', 'Birthday', 'Deathday', 'Father', 'Real Father', 'Mother', 'Religion', 'Culture', 'Fertility', 'Health', 'Wealth', 'Prestige', 'Piety']
        query_result = data.query_person(query_args,query_arg_vals)
        table_print(query_result,headings)
