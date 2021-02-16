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


# keys: command for help
# values: string with associated information on how the command works
COMM_HELP_STRING = {
    'dynasty': """\

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
dynasties by their prestige.\n """,

'title': """\

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
- to find the current holder of a given title         title current k_france\n""",

'person': """\

    The 'person' command allows you to explore different characters
within the game.
----------------------------------------------------------------------
The command 'person' alone will display characters (up to a set limit,
which can be chagned with the 'num_results' command) within the game.
To narrow down your query, you can use the following:

    'dynasty <keyw_1> <keyw_1 arg> ... <keyw_n> <keyw_n arg>'

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
- Are in a dynasty with the substring 'de'.\n""",

'bio': """\

    The 'bio' command will list all info there is to know about a
character.
----------------------------------------------------------------------
The command 'bio' requires 1 argument:

    'bio <person ID>'

You can get character IDs from the 'person' command.
----------------------------------------------------------------------
Specifically, the 'bio' command displays:
- The name of a character
- Their date of birth
- Their date of death (if they have one)
- Their parents (if stored in game)
- Their spouce (if they have one)
- Their sex
- Their religion
- Their culture
- Their attributes
- Their traits
- The titles that they hold (if they hold any)
- The claims that they hold (if they hold any)\n""",

'religion': """\

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
largest to smallest.\n""",

'culture': """\

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
largest to smallest.\n""",

'bloodline': """\

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
    'bloodline bloodlinename parthian'\n""",

'bloodline_members': """\

    The 'bloodline_members' command lists members of a bloodline.
----------------------------------------------------------------------
The 'bloodline_members' command requres 1 argument:

    'bloodline_members <bloodline ID>'

You can get bloodline IDs from the 'bloodline' command. Note that the
number of results will be limited by the 'num_results' command.\n""",

'tree': """\

    The 'tree' command allows you to see a tree of either the 
descendants of a character or the vassals of a title, such as the 
Kingdom of France, or 'k_france'.
----------------------------------------------------------------------
To search for descendants, you can either type:
    'tree descendant <search query>' 
            or 
    'tree descendant <person id>'
If multiple people fit the search query, the command will show a
table of potential people that fit the query and their id alongside. 

For example, you can enter:
    'tree descendant arnold karling' 
            or 
    'tree descendant 190412'
----------------------------------------------------------------------
To search for the vassals of a title, type:
    'tree vassals <title id>'

For example, type:
    'tree vassals k_france'\n """,

'help': """\

    The 'help' command (attempts) to display helpful information about 
how to use this application.
----------------------------------------------------------------------
'help' on its own displays the commands that the user can use.
'help <cmd>' displays information on how to use the command 'cmd'.\n""",

'num_results': """\
    The 'num_results' command is used to restrict the number of results
that a command can return.
----------------------------------------------------------------------
The 'num_results' command requires 1 argument:

    'num_results <integer>'

For example:
    'num_results 10'
Will restrict the number of rows from future commands to 10.\n""",

'load': """\

    The 'load' command is used to load in new data from a save file.
----------------------------------------------------------------------
The 'load' command requires 1 argument:

    'load <file name>'

For example, 
    'load Leon1067_02_12.ck2' 
Will use the data from that save game.\n""",

'quit': """\

Exits the program. Can also use 'q' or 'exit'.\n"""

}
