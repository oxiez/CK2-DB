import psycopg2
import io
import sys
import load_data


class Data:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=ck2 user=charles password=frank")

    # use load_data to fill the database with info from this game
    def setup(self,filename):
        load_data.load_data(filename)


    # query for a person with a name similar to the given string
    def query_person(self,name):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM person WHERE birthname LIKE %s",['%'+name+'%'])
        result = cur.fetchall()
        cur.close()
        return result
    
    
    #find a specific person by their personid
    def query_personid(self,ID):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM person WHERE personid=%s',[ID])
        result = cur.fetchall()
        cur.close()
        return result
    
    
    # query for everyone in a specific dynasty
    def query_dynastyid(self,ID,orderby='name'):
        cur = self.conn.cursor()
        if orderby=='name':
            cur.execute("SELECT personid,birthname FROM person NATURAL JOIN dynasty WHERE dynastyid=%s ORDER BY birthname",[ID])
        elif orderby in {'wealth','prestige','piety'}:
            cur.execute('SELECT personid,birthname,'+orderby+' FROM person NATURAL JOIN dynasty WHERE dynastyid=%s ORDER BY '+orderby,[ID])
        result = cur.fetchall()
        cur.close()
        return result
    
    
    # search for dynasties that are similar to a string
    def query_dynastyname(self,name):
        cur = self.conn.cursor()
        cur.execute("SELECT birthname FROM person NATURAL JOIN dynasty WHERE dynastyname LIKE %s",['%'+name+'%'])
        result = cur.fetchall()
        cur.close()
        return result
        

    # query for dynasties, sorted by optional parameter (default alphabetically)
    def query_dynasties(self,orderby='dynastyname'):
        cur = self.conn.cursor()
        if orderby=='dynastyname':
            cur.execute('SELECT dynastyid,dynastyname FROM dynasty WHERE dynastyname IS NOT NULL ORDER BY dynastyname')
        elif orderby in {'wealth','prestige','piety'}:
            cur.execute('SELECT dynastyid,dynastyname,sum FROM (SELECT dynastyid,SUM('+orderby+') FROM person WHERE '+orderby+' IS NOT NULL GROUP BY dynastyid) summation NATURAL JOIN dynasty ORDER BY sum DESC')
        elif orderby=='count':
            cur.execute('SELECT dynastyid,dynastyname,count FROM (SELECT dynastyid,COUNT(*) FROM person GROUP BY dynastyid) summation NATURAL JOIN dynasty ORDER BY count DESC')
        result = cur.fetchall()
        cur.close()
        return result
    
    
    # return set of religions ordered somehow
    def query_religion(self,orderby='religionname'):
        cur = self.conn.cursor()
        
        result = cur.fetchall()
        cur.close()
        return result        


    # query for relating people to titles
    def query_title(self):
        cur = self.conn.cursor()
    
        cur.execute('SELECT birthname,dynastyname,name FROM (SELECT personid as holderid,birthname,dynastyid FROM person) ppl NATURAL JOIN dynasty NATURAL JOIN title')
    
        result = cur.fetchall()
        cur.close()
        return result
    