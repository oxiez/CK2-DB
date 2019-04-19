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


# query for dynasties, sorted by optional parameter (default alphabetically)
def query_dynasties(orderby='dynastyname'):
    conn = psycopg2.connect("dbname=ck2 user=charles password=frank")
    cur = conn.cursor()
    
    if orderby=='dynastyname':
        cur.execute('SELECT dynastyname FROM dynasty WHERE dynastyname IS NOT NULL ORDER BY dynastyname')
    elif orderby=='wealth':
        cur.execute('SELECT dynastyname,sum FROM (SELECT dynastyid,SUM(wealth) FROM person WHERE wealth IS NOT NULL GROUP BY dynastyid) summation NATURAL JOIN dynasty ORDER BY sum DESC')
    elif orderby=='prestige':
        cur.execute('SELECT dynastyname,sum FROM (SELECT dynastyid,SUM(prestige) FROM person WHERE prestige IS NOT NULL GROUP BY dynastyid) summation NATURAL JOIN dynasty ORDER BY sum DESC')
    elif orderby=='piety':
        cur.execute('SELECT dynastyname,sum FROM (SELECT dynastyid,SUM(piety) FROM person WHERE piety IS NOT NULL GROUP BY dynastyid) summation NATURAL JOIN dynasty ORDER BY sum DESC')
    
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


# query for relating people to titles
def query_title():
    conn = psycopg2.connect("dbname=ck2 user=charles password=frank")
    cur = conn.cursor()
    
    cur.execute('SELECT birthname,dynastyname,name FROM (SELECT personid as holderid,birthname,dynastyid FROM person) ppl NATURAL JOIN dynasty NATURAL JOIN title')
    
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result