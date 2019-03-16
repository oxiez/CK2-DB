
import psycopg2
import get_dynasties
import get_chars
import get_provs
import get_titles
import get_religion
import get_culture

# connect and get a cursor
conn = psycopg2.connect("dbname=postgres user=postgres password=superuser")
cur = conn.cursor()

# create the tables
with open("ck2_make_table.sql") as f:
    cur.execute(f.read())

#read in religion and culture
get_religion.get_religion(cur)
get_culture.get_culture(cur)

# parse the file and fill the tables with data
with open("Leon1067_02_12.ck2") as f:
	get_dynasties.get_dynasties(f, cur)
	#get_chars.get_chars(f, cur)
	#get_provs.get_provs(f, cur)
	#get_titles.get_titles(f, cur)

#read in culture

# commit changes made and disconnect from database
conn.commit()
cur.close()
conn.close()

print("All done!")