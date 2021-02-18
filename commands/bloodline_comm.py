from commands.command import Command, table_print

class BloodlineComm(Command):
    COMM_STR = "bloodline"
    HELP_STR = """\

    The 'bloodline' command allows you to see which bloodlines
exist in the game and get who their founders are.
----------------------------------------------------------------------
The 'bloodline' command on its own lists the bloodlines (up to a set
limit, which can be changed with the 'num_results' command) in the game
by their ID. To see members of a specific bloodline, use the
'bloodline_members' command instead.

Optional arguments can be added for
- bloodlinename      [limits to names that match the string of the type]
- founderID          [limits to bloodlines founded by that person ID].

For example:
    'bloodline bloodlinename parthian'\n"""

    def doCommand(data,args):
        query_result = None
        headings = None

        query_args = []
        if(len(args)%2 != 0):
            print('ERROR: Please have one argument for each command')
            return
        query_arg_vals = []
        i = 0
        allowed_args = {'bloodlinename', 'founderid'}
        valid = True
        while i < len(args):
            if(args[i] in allowed_args):
                query_args.append(args[i])
                query_arg_vals.append(args[i+1])
            else:
                print('ERROR: ' + args[i] + ' is not a valid condition, please use one of the following values:')
                print(allowed_args)
                valid = False
            i += 2
        if valid:
            headings = ['ID', 'Type', 'Founder']
            query_result = data.query_bloodline(query_args,query_arg_vals)
            table_print(query_result,headings)

