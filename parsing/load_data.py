import io
import sys

from .load import *
from .lark_parser import parse_save

import sqlite3

def load_data(filename):
    # connect and get a cursor
    conn = sqlite3.connect('./ck2-db.db')
    cur = conn.cursor()

    # create the tables
    with open("ck2_make_table.sql") as f:
        cur.executescript(f.read())

    # preload default game files
    print('Preloading religion...')
    get_religion.get_religion(cur)
    print('Preloading culture...')
    get_culture.get_culture(cur)
    print('Preloading traits...')
    get_traits.get_traits(cur)
    print('Preloading historical dynasties...')
    get_dynasties.get_hist_dynasties(cur)

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
    print('Parsing file- this may take a minute...')
    data = None
    with io.open(filename, encoding="cp1252") as f:
        data = parse_save(f.read())

    print('Loading dynasties...')
    get_dynasties.get_dynasties(data['dynasties'], cur)
    print('Loading characters...')
    get_chars.get_chars(data['character'], cur)
    print('Loading religions...')
    get_religion.get_heresies(data['religion'], cur)
    print('Loading provinces...')
    get_provs.get_provs(data['provinces'], cur)
    # Not all save files have bloodlines (part of Holy Fury DLC)
    if 'bloodline' in data:
        print("Loading bloodlines...")
        get_bloodline.get_bloodlines(data['bloodline'], cur)
    else:
        print("No bloodlines found in save, continuing...")
    print("Loading titles...")
    get_titles.get_titles(data['title'], cur)

    # commit changes made and disconnect from database
    conn.commit()
    cur.close()
    conn.close()
    
    print("All done!")
