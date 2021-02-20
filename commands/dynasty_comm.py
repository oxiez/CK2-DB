from commands.command import Command, table_print

class DynastyComm(Command):
    COMM_STR = "dynasty"
    HELP_STR = """\

    The 'dynasty' command allow you to explore the different
dynasties, or sets of characters considered to be within the same
family.
----------------------------------------------------------------------
The commmand 'dynasty' alone will display dyanasties (up to a set
limit, which can be changed with 'num_results' command) within the
game. Each dynasty has it's own religion and culture associated with
it, so you can limit your search with the following:

    'dynasty <keyw_1> <keyw_1 arg> ... <keyw_n> <keyw_n arg>'

Keywords can be any of the following (in any order):
- name            [limit to dynasties with a similar name]
- religion        [limit to dynasties with a similar religion name]
- culture         [limit to dynasties with a similar culture name]
- orderby         [explained in the next section]

For example:
    'dynasty religion Catholic culture Frankish'
Which will return a list of dynasties associated with the Catholic
religion and Frankish culture.
----------------------------------------------------------------------
The 'dynasty' command also has the option to order the the output from
the greatest to the least. There are several statistics that you can
order the output by:
- prestige
- piety
- wealth
- count           [member count]

For example:
    'dynasty orderby prestige religion Catholic culture Frankish'
Will take the output of the previous section's example and order the
dynasties by their prestige.\n """


    def doCommand(data,args):
        if(len(args) % 2 != 0):
            print('ERROR: Please have one argument for each command')
            return            
        query_args = []
        query_arg_vals = []
        i = 0
        allowed_args = {'name', 'orderby', 'religion', 'culture'}
        valid = True
        has_orderby = False
        while i < len(args):
            if(args[i] in allowed_args):
                valid_vals = {'prestige','piety','wealth','count'}
                if args[i]=='orderby':
                    if has_orderby:
                        valid = False
                        print('ERROR: Query contained a second orderby term. Queries should contain zero or one orderby term.')
                        break
                    has_orderby = True
                    if args[i+1] not in valid_vals:
                        print('ERROR: ' + args[i+1] + ' is not a valid value to order by. Please use one of:')
                        print(valid_vals)
                        valid = False
                if valid:
                    query_args.append(args[i])
                    query_arg_vals.append(args[i+1])
            else:
                print('ERROR: ' + args[i] + ' is not a valid condition, please use one of the following values:')
                print(allowed_args)
                valid = False
            i += 2
        #get person with these conditions
        if valid:
            query_result = data.query_dynasty(query_args,query_arg_vals)
            table_print(query_result)
