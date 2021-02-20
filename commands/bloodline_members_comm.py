from commands.command import Command, table_print

class BloodlineMembersCommand(Command):
    COMM_STR = "bloodline_members"
    HELP_STR = """\

    The 'bloodline_members' command lists members of a bloodline.
----------------------------------------------------------------------
The 'bloodline_members' command requres 1 argument:

    'bloodline_members <bloodline ID>'

You can get bloodline IDs from the 'bloodline' command. Note that the
number of results will be limited by the 'num_results' command.\n"""

    def doCommand(data,args):
        if(len(args) != 1):
            print('ERROR: bloodline_members takes one argument (the id of the bloodline) and one argument only')
        else:
            headings = ['Name','Dynasty']
            query_result = data.query_bloodline_members(args[0])
            table_print(query_result,headings)
