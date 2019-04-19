import psycopg2
from psycopg2.extras import DictCursor
import io
import sys
import load_data


class Data:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=ck2 user=charles password=frank")

    # use load_data to fill the database with info from this game
    def setup(self,filename):
        load_data.load_data(filename)


   
    # 1) check arguments (done in application.py)
    # 2) WHERE true
    # 3) For Each arg
    #   a) and ARG = / LIKE %s,
    #   b) add arg_val to list
    # 4) execute
    
    # returns a list of dictionaries (easier to deal with than indexing huge list of values)
    def query_person(self, args, arg_vals):
        ex_string = "SELECT * FROM person NATURAL JOIN culture NATURAL JOIN religion WHERE TRUE"   # TODO: Make this a join with dynasty and make it select only interesting things (no dynasty id)
        like_args = {'name','dynasty','religion', 'culture'}
        geq_args = {'culture','fertility','health','wealth','prestige','piety'}
        for i,(a,v) in enumerate(zip(args,arg_vals)):
            if a in like_args:    # Strings TODO: add dynasty to this (via a join)
                #convert user input to columns of relation
                if a=='dynasty': a = 'dynastyname'
                if a=='name': a = 'birthname'
                if a=='culture': a = 'culturename'
                if a== 'religion': a= 'religionname'
                arg_vals[i] = '%'+v+'%'
                ex_string = ex_string + ' AND ' + a + ' ILIKE %s'
            elif a in geq_args:
                ex_string = ex_string + ' AND ' + a + ' >= %s'
            else:
                ex_string = ex_string + ' AND ' + a + '=%s'
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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
    
    
    # similar to query person; ONLY ALLOW ONE ORDERBY TERM (code is built on that assumption)
    def query_dynasty(self,args,arg_vals):
        cur = self.conn.cursor()
        like_args = {'name','religion', 'culture'}
        orderby_sum_vals = {'wealth','prestige','piety'}
        orderby_count_vals = {'count'}
        ex_string = 'SELECT dynastyid,dynastyname'
        for a in args:
            if a!='name' and a in like_args:
                ex_string = ex_string + ','+a+'name'
        #if we are ordering by something, we want to present that
        orderby = None
        for a,v in zip(args,arg_vals):
            if a=='orderby':
                orderby = v
                if orderby in orderby_sum_vals:
                    ex_string = ex_string + ',sum'
                else:
                    ex_string = ex_string + ',count'
        ex_string = ex_string + ' FROM '
        if orderby in orderby_sum_vals:
            ex_string = ex_string + "(SELECT dynastyid,SUM("+orderby+") FROM person WHERE "+orderby+" IS NOT NULL GROUP BY dynastyid) summation NATURAL JOIN "
        if orderby in orderby_count_vals:
            ex_string = ex_string + "(SELECT dynastyid,COUNT(*) FROM person GROUP BY dynastyid) summation NATURAL JOIN "
        ex_string = ex_string + 'dynasty NATURAL JOIN religion NATURAL JOIN culture WHERE TRUE'      
        for i,(a,v) in enumerate(zip(args,arg_vals)):
            if a in like_args:
                #convert user input to columns of relation
                if a=='name': a = 'dynastyname'
                else: a+='name'
                arg_vals[i] = '%'+v+'%'
                ex_string = ex_string + ' AND ' + a + ' ILIKE %s'
        #add the order by term
        if orderby in orderby_sum_vals:
            ex_string = ex_string + ' ORDER BY sum DESC'
        if orderby in orderby_count_vals:
            ex_string = ex_string + ' ORDER BY count DESC'
        #remove the orderby from the argvals
        for i in range(len(arg_vals)):
            if arg_vals[i]==orderby:
                arg_vals.pop(i)
                break
        cur.execute(ex_string,arg_vals)
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
    