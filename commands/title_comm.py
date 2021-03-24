from commands.command import Command, table_print

class TitleComm(Command):
    COMM_STR = "title"
    HELP_STR = """\

The 'title' command allows you to look into characters that are
associated with a title (such as past holders and current holders)
----------------------------------------------------------------------
The title command with either take a character's ID, or a specifier
(either 'rulers' or 'current') with a title ID. Title IDs are formatted
as follows:
    [k/e/d/c/b]_[name]
Where the first letter represents which level (in a heirarchy) that
the title is in:

    +-------+---------+
    |Label  |Level    |
    +-------+---------+
    |e      |Empire   |
    +-------+---------+
    |k      |Kingdom  |
    +-------+---------+
    |d      |Duchy    |
    +-------+---------+
    |c      |County   |
    +-------+---------+
    |b      |Barony   |
    +-------+---------+

----------------------------------------------------------------------
Examples:                                             e.g.
- to find the titles owned by a specific character    title 6392
- to find the history of rulers of a given title      title rulers k_france
- to find the current holder of a given title         title current k_france\n"""

    def doCommand(data,args):
        query_result = None
        headings = None
        # title on its own returns ???
        if len(args)==0:
            print('Title queries should be of the form : title personid or title rulers titleid or title current titleid')
            return
        # title id returns all titles of the given personid
        elif len(args)==1:
            query_result = data.query_title(args[0])
            headings = ['Title ID']
        # we are looking for personID(s) given a certain title
        elif len(args)==2:
            #rulers
            if args[0]=='rulers':
                query_result = data.query_rulers(args[1])
                headings = ['personid', 'Name', 'Dynasty', 'Date of Birth', 'Date of Death', 'Start of Rule']
            #current
            elif args[0]=='current':
                query_result = data.query_ruler(args[1])
                headings = ['personid','Name','Dynasty']
            else:
                print("Queries should be of the form 'title (rulers|current) titleid.'")
                return
        else:
            print('Title queries should be of the form : title personid or title rulers titleid or title current titleid')
            return
        table_print(query_result,headings)
