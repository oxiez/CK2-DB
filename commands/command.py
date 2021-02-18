import texttable

row_count = 10

# helper function for printing tables of data
def table_print(query_result,headings=None):
    table = texttable.Texttable()
    if headings!=None:
        table.header(headings)
        table.set_max_width(210)
    for i,v in enumerate(query_result):
        if i >= row_count: break
        row = []
        row = row + [str(x) for x in v]
        table.add_row(row)
    t = table.draw()
    print(t)


class Command:
    COMM_STR = None
    HELP_STR = """PLACEHOLDER HELP STRING"""

    def doCommand(data,args):
        pass
