
import psycopg2
import io
import sys

import get_dynasties
import get_chars
import get_provs
import get_titles
import get_religion
import get_culture
import get_traits

# connect and get a cursor
conn = psycopg2.connect("dbname=ck2 user=charles password=frank")
cur = conn.cursor()

# create the tables
with open("ck2_make_table.sql") as f:
    cur.execute(f.read())

#read in religion and culture
get_religion.get_religion(cur)
get_culture.get_culture(cur)
get_traits.get_traits(cur)

file_name = "Leon1067_02_12.ck2"

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    
with io.open(file_name, "rb") as f:
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
with io.open(file_name, encoding="cp1252") as f:
	get_dynasties.get_dynasties(f, cur)
	get_chars.get_chars(f, cur)
	#get_religion.get_heresies(f, cur)
	get_provs.get_provs(f, cur)
	#get_titles.get_titles(f, cur)

# commit changes made and disconnect from database
conn.commit()
cur.close()
conn.close()

print("All done!")
