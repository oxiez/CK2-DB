import texttable

row_count = 20

# helper function for printing tables of data
def table_print(query_result,headings=None):
    table = texttable.Texttable()
    if headings!=None:
        table.header(headings)
        table.set_max_width(210)
    trunc_flag = False
    for i,v in enumerate(query_result):
        if i >= row_count:
            trunc_flag=True
            break
        row = []
        row = row + [str(x) for x in v]
        table.add_row(row)
    t = table.draw()
    print(t)
    if trunc_flag:
        print("Results truncated to %i rows." % row_count,
        "To see more or less, modify the number of rows to retreive with the `num_results` command.", sep="\n")
    print("%i rows retreived." % len(query_result))


class Command:
    COMM_STR = None
    HELP_STR = """PLACEHOLDER HELP STRING"""

    def doCommand(data,args):
        pass
