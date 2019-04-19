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
    
    # 1) check arguments (done in application.py)
    # 2) WHERE true
    # 3) For Each arg
    #   a) and ARG = / LIKE %s,
    #   b) add arg_val to list
    # 4) execute

    def query_person(self, args, arg_vals):
        ex_string = "SELECT * FROM person WHERE TRUE"
        for a in args:
            if(a ==  'birthName'):
                ex_string = ex_string + ' AND ' + a + 'LIKE %s'
            else:
                ex_string = ex_string + ' AND ' + a + '=%s'
        cur = self.conn.cursor()
        cur.execute(ex_string, arg_vals)
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
    def query_dynasties(self,orderby='dynastyname',living):
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
    