import psycopg2
import io
import sys
import load_data

# use load_data to fill the database with info from this game
def setup(filename):
    load_data.load_data(filename)


# query for specific person
def query_person(name):
    conn = psycopg2.connect("dbname=ck2 user=charles password=frank")
    cur = conn.cursor()
    
    #code here
    
    cur.close()
    conn.close()    