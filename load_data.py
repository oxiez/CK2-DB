
import psycopg2

# connect and get a cursor
conn = psycopg2.connect("dbname=postgres user=postgres password=superuser")
cur = conn.cursor()

# create the tables
with open("ck2_make_table.sql") as f:
    cur.execute(f.read())

# parse the file and fill the tables with data
with open("Leon1067_02_12.ck2") as f:
    x = f.readline()
    while(x):
        
        
        x = f.readline()

# parse in culture


# parse in religion


# commit changes made and disconnect from database
conn.commit()
cur.close()
conn.close()
