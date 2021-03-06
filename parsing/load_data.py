import io
import sys

from .load import *
from .lark_parser import parse

import sqlite3

def load_data(filename):
    # connect and get a cursor
    conn = sqlite3.connect('../ck2-db.db')
    cur = conn.cursor()

    # create the tables
    with open("ck2_make_table.sql") as f:
        cur.executescript(f.read())

    #read in religion and culture
    print('Preloading religion...')
    get_religion.get_religion(cur)
    print('Preloading culture...')
    get_culture.get_culture(cur)
    print('Preloading traits...')
    get_traits.get_traits(cur)

    with io.open(filename, "rb") as f:
        label = f.read(2) # Get byte object
        if label == b"PK": # I don't know if the beginning is just PK or PK3
            print("This file is a zip-compressed file, exiting...")
            quit()
        elif label == b"CK": # If PK3, then we should check CK2
            print("Reading CK2 file...")
        else: # Ironman mode files???
            print("Unknown file type, exiting...")
            quit()

    # parse the file and fill the tables with data
    with io.open(filename, encoding="cp1252") as f:
        data = parse(f.read())

    with io.open(filename, encoding="cp1252") as f:
        print('Getting dynasties...')
        get_dynasties.get_dynasties(data['dynasties'], cur)
        print('Getting characters...')
        get_chars.get_chars(data['character'], cur)
        print('Getting religions...')
        get_religion.get_heresies(data['religion'], cur)
        print('Getting provinces...')
        get_provs.get_provs(f, cur)
        # Handle case for no dlc?
        print("Getting bloodlines...")
        get_bloodline.get_bloodlines(f, cur) # order matters because we don't rewind the file in each separate parser
        print("Getting titles...")
        get_titles.get_titles(f, cur)

    # commit changes made and disconnect from database
    conn.commit()
    cur.close()
    conn.close()
    
    print("All done!")


if __name__=='__main__':
    file_name = "Leon1067_02_12.ck2"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    load_data(file_name)
