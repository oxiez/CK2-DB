from commands.command import Command

def tree_spacer(stack):
    level = len(stack) - 1
    for i in range(0,level):
        if(len(stack[i]) > 0):
            print("\u2502   ", end="")
        else:
            print("    ", end="")

title_level = { 'k': 'Kingdom',
                'e': 'Empire',
                'd': 'Duchy',
                'c': 'County',
                'b': 'Barony'}

class TreeComm(Command):
    COMM_STR = "tree"
    HELP_STR = """\

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
    'tree vassals k_france'\n """


    def doCommand(data,args):
        if(len(args) < 2):
            print("ERROR: Please format the tree command like so:\ntree <descendant> <person name/id>")
            return
        commands = ["descendant", "vassals"]
        command = 0
        for i in range(len(commands)):
            if(args[0] == commands[i]):
                command = i
                break
        else:
            print("ERROR: \"" + args[0] + "\" is not a valid tree command. Please use:")
            for com in commands:
                print("- " + com)
            return
        # args = ""
        info = []
        dag = {}
        if(command == 0):
            args = " ".join(args[1:])
            info, dag = data.descendant_tree(args)
        elif(command == 1):
            if(len(args) > 2):
                print("ERROR: 'vassals' command only takes a titleid, which is formatted like 'k_france'")
                return
            args = args[1]
            info, dag = data.title_tree(args)

        if(isinstance(info, list)):
            if(len(info) > 1):
                display = True
                if(len(info) > 10):
                    confirm = input("WARN: {} results found for \"{}\". Display? (y/N): ".format(len(info), args))
                    if(not confirm.lower() == 'y'):
                         display = False
                if(display):
                    table = texttable.Texttable(max_width=210)
                    table.header(("ID", "Name"))
                    table.add_rows(info, header=False)
                    print(table.draw())
                    print("WARN: {} results found. Please rerun this command with an id from above".format(len(info)))
            else:
                if(command == 0):
                    print("INFO: No person matched with {}, try again.".format(args))
                    return
                elif(command == 1):
                    print("INFO: No title has the titleid {}, try again.".format(args))
                    return
        else: # Can only be a dict
            if(len(dag) == 0):
                if(command == 0):
                    print("No descendants found for {}: {}".format(info[0][0], info[0][1]))
                else:
                    name = info["start"][1]
                    name = name[0].upper() + name[1:]
                    print("No vassals for The {} of {}".format(title_level[info["start"][2]], name))
            else:
                stack = []
                stack_above = []
                if(command == 0):
                    print("Printing descendants of {}: {}".format(info[0][0], info[0][1]))
                    print("{}: {}".format(info[0][0], info[0][1]))
                    stack = [dag[info[0][0]]]
                    # Keep track of whose child it is
                    stack_above = [info[0][0]]
                else:
                    name = info["start"][1]
                    name = name[0].upper() + name[1:]
                    print("Printing vassals of The {} of {}".format(title_level[info["start"][2]], name))
                    print("The {} of {}".format(title_level[info["start"][2]], name))
                    stack = [dag[info["start"][0]]]
                    stack_above  = [info["start"][0]]
                while(len(stack) > 0):
                    id = stack[-1].pop()
                    tree_spacer(stack)
                    if(command == 0):
                        if(stack_above[-1] == info[id][2] and info[id][4]):
                            print("\u2502   ")
                            tree_spacer(stack)
                            print("\u2502   Father: ({}: {})".format(info[id][4], info[id][5]))
                        elif(stack_above[-1] == info[id][4] and info[id][2]):
                            print("\u2502   ")
                            tree_spacer(stack)
                            print("\u2502   Mother: ({}: {})".format(info[id][2], info[id][3]))
                        else:
                            print("\u2502")
                        tree_spacer(stack)
                    else:
                        print("\u2502")
                        tree_spacer(stack)
                        
                    if(len(stack[-1]) > 0):
                        print("\u251C", end="")
                    else:
                        print("\u2514", end="")

                    if(command == 0):
                        print("\u2500\u2500\u2500{}: {}".format(info[id][0], info[id][1]))
                    else:
                        name = info[id][2]
                        name = name[0].upper() + name[1:]
                        print("\u2500\u2500\u2500The {} of {}".format(title_level[info[id][3]], name))
                        
                    if(id in dag): # Has children
                        stack += [dag[id]]
                        stack_above.append(id)
                    while(len(stack) > 0 and len(stack[-1]) == 0):
                        stack.pop()
                        stack_above.pop()
