from commands.command import Command

# loads the given file name using a database object
def load_file(filename,data):
    print('Opening the file ' + filename)
    data.setup(filename)
    print('\n')


class LoadComm(Command):
    COMM_STR = "load"
    HELP_STRING = """\

    The 'load' command is used to load in new data from a save file.
----------------------------------------------------------------------
The 'load' command requires 1 argument:

    'load <file name>'

For example,
    'load Leon1067_02_12.ck2'
Will use the data from that save game.\n"""

    def doCommand(data, args):
        if len(args) > 1 or len(args) < 1:
            print("ERROR: load takes exactly one argument, the name of the ck2 save file to load.")
            return
        filename = args[0]
        try:
            load_file(filename,data)
        except:
            print("ERROR: issue loading file " + filename)
            return
