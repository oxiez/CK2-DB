
import psycopg2
import get_dynasties.py
import get_chars.py
import get_provs.py
import get_titles.py

# connect and get a cursor
conn = psycopg2.connect("dbname=postgres user=postgres password=superuser")
cur = conn.cursor()

# create the tables
with open("ck2_make_table.sql") as f:
    cur.execute(f.read())

# parse the file and fill the tables with data
with open("Leon1067_02_12.ck2") as f:
	get_dynasties(f, cur)
	get_chars(f, cur)
	get_provs(f, cur)
	get_titles(f, cur)

# parse in culture


# parse in religion


# commit changes made and disconnect from database
conn.commit()
cur.close()
conn.close()
