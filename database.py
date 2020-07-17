import sqlite3
import io
import sys
import load_data


class Data:
    def __init__(self):
        self.conn = sqlite3.connect("ck2-db.db")

    # use load_data to fill the database with info from this game
    def setup(self,filename):
        self.conn.close()
        load_data.load_data(filename)
        self.conn = sqlite3.connect("ck2-db.db")
        self.conn.row_factory = sqlite3.Row

    #find a specific person by their personid
    def query_personid(self,ID):
        cur = self.conn.cursor()
        cur.execute('SELECT personid,birthname,dynastyname,ismale,birthday,deathday,fatherid,real_fatherid,motherid,religionname,culturename,fertility,health,wealth,hostid,prestige,piety,employerid,martial,diplomacy,stewardship,intrigue,learning FROM person NATURAL JOIN culture NATURAL JOIN religion LEFT OUTER JOIN dynasty ON person.dynastyid=dynasty.dynastyid WHERE personid=?',[ID])
        result = cur.fetchall()
        cur.close()
        return result

   
    # 1) check arguments (done in application.py)
    # 2) WHERE 1 (i.e. true)
    # 3) For Each arg
    #   a) and ARG = / LIKE ?,
    #   b) add arg_val to list
    # 4) execute
    
    # returns a list of dictionaries (easier to deal with than indexing huge list of values)
    def query_person(self, args, arg_vals):
        ex_string = "SELECT personid,birthname,dynastyname,ismale,birthday,deathday,fatherid,real_fatherid,motherid,religionname,culturename,fertility,health,wealth,prestige,piety FROM person NATURAL JOIN culture NATURAL JOIN religion LEFT OUTER JOIN dynasty ON person.dynastyid=dynasty.dynastyid WHERE 1"
        like_args = {'name','dynasty','religion', 'culture'}
        geq_args = {'fertility','health','wealth','prestige','piety'}
        for i,(a,v) in enumerate(zip(args,arg_vals)):
            if a in like_args:
                #convert user input to columns of relation
                if a=='dynasty': a = 'dynastyname'
                if a=='name': a = 'birthname'
                if a=='culture': a = 'culturename'
                if a== 'religion': a= 'religionname'
                arg_vals[i] = '%'+v+'%'
                ex_string = ex_string + ' AND ' + a + ' LIKE ?'
            elif a in geq_args:
                ex_string = ex_string + ' AND ' + a + ' >= ?'
            else:
                ex_string = ex_string + ' AND ' + a + '=?'
        cur = self.conn.cursor()
        cur.execute(ex_string, arg_vals)
        result = cur.fetchall()
        cur.close()
        return result
    
    
    #query for getting the spouseIDs of a given person
    def query_spouse(self,personID):
        cur = self.conn.cursor()
        cur.execute("SELECT spouseID FROM marriage WHERE personID=?",[personID])
        result = cur.fetchall()
        cur.close()
        return result
    
    
    # query for everyone in a specific dynasty
    def query_dynastyid(self,ID,orderby='name'):
        cur = self.conn.cursor()
        if orderby=='name':
            cur.execute("SELECT personid,birthname FROM person NATURAL JOIN dynasty WHERE dynastyid=? ORDER BY birthname",[ID])
        elif orderby in {'wealth','prestige','piety'}:
            cur.execute('SELECT personid,birthname,'+orderby+' FROM person NATURAL JOIN dynasty WHERE dynastyid=? ORDER BY '+orderby,[ID])
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
            ex_string = ex_string + "(SELECT dynastyid,SUM("+orderby+") AS sum FROM person WHERE "+orderby+" IS NOT NULL GROUP BY dynastyid) summation NATURAL JOIN "
        if orderby in orderby_count_vals:
            ex_string = ex_string + "(SELECT dynastyid,COUNT(*) AS count FROM person GROUP BY dynastyid) summation NATURAL JOIN "
        ex_string = ex_string + 'dynasty NATURAL JOIN religion NATURAL JOIN culture WHERE 1'      
        for i,(a,v) in enumerate(zip(args,arg_vals)):
            if a in like_args:
                #convert user input to columns of relation
                if a=='name': a = 'dynastyname'
                else: a+='name'
                arg_vals[i] = '%'+v+'%'
                ex_string = ex_string + ' AND ' + a + ' LIKE ?'
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
    
    
    
    # return set of religions ordered by (name,members,provinces)
    def query_religion(self,orderby='name'):
        cur = self.conn.cursor()
        #alphabetical
        if orderby=='name':
            cur.execute('SELECT religionname FROM religion ORDER BY religionname')
        #total member count
        elif orderby=='allmembers':
            cur.execute('SELECT religionname,count FROM (SELECT religionid,COUNT(*) AS count FROM person GROUP BY religionid) ppl NATURAL JOIN religion ORDER BY count DESC')
        #living member count
        elif orderby=='alivemembers':
            cur.execute('SELECT religionname,count FROM (SELECT religionid,COUNT(*) AS count FROM person WHERE deathday IS NULL GROUP BY religionid) ppl NATURAL JOIN religion ORDER BY count DESC')
        #province count
        else:
            cur.execute('SELECT religion,COUNT(*) AS count FROM province GROUP BY religion ORDER BY count DESC')
        result = cur.fetchall()
        cur.close()
        return result        
    
    
    #return set of cultures ordered somehow
    def query_culture(self,orderby='name'):
        cur = self.conn.cursor()
        #alphabetical
        if orderby=='name':
            cur.execute('SELECT culturename FROM culture ORDER BY culturename')
        #total member count
        elif orderby=='allmembers':
            cur.execute('SELECT culturename,count FROM (SELECT cultureid,COUNT(*) AS count FROM person GROUP BY cultureid) ppl NATURAL JOIN culture ORDER BY count DESC')
        #living member count
        elif orderby=='alivemembers':
            cur.execute('SELECT culturename,count FROM (SELECT cultureid,COUNT(*) AS count FROM person WHERE deathday IS NULL GROUP BY cultureid) ppl NATURAL JOIN culture ORDER BY count DESC')        
        #province count
        else:
            cur.execute('SELECT culture,COUNT(*) AS count FROM province GROUP BY culture ORDER BY count DESC')
        result = cur.fetchall()
        cur.close()
        return result            


    # query for relating people to titles
    def query_title(self,personID):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT rlr.personid,birthname,dynastyname,name,rlr.titleid
            FROM (SELECT personid,birthname,dynastyname,titleid
            FROM (SELECT personid AS holderid,birthname,dynastyid FROM person WHERE personid=?) ppl
            LEFT OUTER JOIN dynasty ON ppl.dynastyid=dynasty.dynastyid NATURAL JOIN rulers)
            rlr LEFT OUTER JOIN title ON rlr.titleID=title.titleID WHERE personid=?
            """, [personID, personID])
        result = cur.fetchall()
        cur.close()
        return result
    
    
    # query for getting the claims of someone
    def query_claim(self,personID):
        cur = self.conn.cursor()
        cur.execute("SELECT titleid FROM claim WHERE personid=?",[personID])
        result = cur.fetchall()
        cur.close()
        return result
    
    
    # query returning all of the past rulers of a given title
    def query_rulers(self,titleID):
        cur = self.conn.cursor()
        #returns personid,name,dynasty,birthdate,deathdate of every historical ruler of the title
        cur.execute(
            """
            SELECT rul.holderid,birthname,dynastyname,birthday,deathday,succession
            FROM (SELECT personid AS holderid,titleid,birthname,dynastyname,birthday,deathday,succession
                FROM titlehistory NATURAL JOIN person LEFT OUTER JOIN dynasty ON person.dynastyid=dynasty.dynastyid)
            rul LEFT JOIN title ON title.titleid=rul.titleid WHERE title.titleid=?
            ORDER BY succession
            """
            ,[titleID])
        result = cur.fetchall()
        cur.close()
        return result
    
    
    #query returning the current ruler of a given title
    def query_ruler(self,titleID):
        cur = self.conn.cursor()
        cur.execute('SELECT holderid,birthname,dynastyname FROM (SELECT personid AS holderid,birthname,dynastyname FROM person LEFT OUTER JOIN dynasty ON person.dynastyid=dynasty.dynastyid) ppl NATURAL JOIN title WHERE titleid=?',[titleID])
        result = cur.fetchall()
        cur.close()
        return result
  
    
    #returns a list of the direct vassals for a given title
    def query_direct_vassals(self,titleID):
        cur = self.conn.cursor()
        cur.execute('SELECT titleid FROM title WHERE defactoleige=?',[titleID])
        result = cur.fetchall()
        cur.close()
        return result
        
    
    
    #query for getting all of the traits of a specific person
    def query_traits(self,personID):
        cur = self.conn.cursor()
        cur.execute('SELECT traitname FROM person NATURAL JOIN trait NATURAL JOIN traitlookup WHERE personid=?',[personID])
        result = cur.fetchall()
        cur.close()
        return result
    
    
    #queries for getting bloodlines
    def query_bloodline_members(self, b_id):
        cur = self.conn.cursor()
        cur.execute("SELECT birthname, dynastyname FROM person NATURAL JOIN dynasty NATURAL JOIN BloodLineMembers where bloodLineID = ?", [b_id])
        result = cur.fetchall()
        cur.close()
        return result
    
    
    def query_bloodline(self, args, arg_vals):
        ex_string = "SELECT bloodlineID, bloodlineName, founderID FROM BloodLines WHERE 1"
        for i,(a,v) in enumerate(zip(args,arg_vals)):
            ex_string = ex_string + ' AND ' + a + '=?'
        cur = self.conn.cursor()
        cur.execute(ex_string, arg_vals)
        result = cur.fetchall()
        cur.close()
        return result

    def title_tree(self, titleid):
        cur = self.conn.cursor()
        cur.execute("SELECT titleid, name, level FROM title WHERE titleid = ?", [titleid])

        tup = None
        if(cur.rowcount < 1):
            return [], None # invalid titleid
        else:
            tup = cur.fetchone()

        cur.execute(
            """ WITH RECURSIVE vassal AS (
            SELECT t.titleid, p.birthname || COALESCE( ' ' || d.dynastyname, ''), t.name, 
            t.level, t.defactoleige
            FROM title t LEFT JOIN person p ON t.holderid = p.personid 
            LEFT JOIN dynasty d ON p.dynastyid = d.dynastyid
            WHERE t.defactoleige = ?
            UNION
            SELECT t.titleid, p.birthname || COALESCE( ' ' || d.dynastyname, ''), t.name, 
            t.level, t.defactoleige
            FROM title t LEFT JOIN person p ON t.holderid = p.personid 
            LEFT JOIN dynasty d ON p.dynastyid = d.dynastyid
            INNER JOIN vassal s ON t.defactoleige = s.titleid
            )
            SELECT * FROM vassal """, [titleid])

        result = cur.fetchall()
        cur.close()
        
        info = {"start" : tup}
        dag = {}

        for t in result:
            info[t[0]] = t
            if(t[4] is not None):
                if(t[4] in dag):
                    dag[t[4]].append(t[0])
                else:
                    dag[t[4]] = [t[0]]

        return info, dag

    # Uses CTEs to query multiple times
    def descendant_tree(self, person, levels=0):
        cur = self.conn.cursor()
        is_id = False
        
        try:
            person = int(person)
            is_id = True
        except ValueError:
            person = "%" + "%".join(person.split()) + "%"

        personid = None
        name = None

        if not is_id:
            cur.execute(
                """ SELECT personid, birthname || COALESCE( ' ' || dynastyname, '')
                FROM person LEFT JOIN dynasty ON person.dynastyid = dynasty.dynastyid
                WHERE birthname || COALESCE( ' ' || dynastyname, '')
                LIKE ? """, [person])
            result = cur.fetchall()
            if(len(result) > 1 or len(result) == 0):
                return result, None # Prompt user to choose person by id, and show choices
            personid = result[0][0]
            name = result[0][1]
        else:
            cur.execute(
                """ SELECT personid, birthname || COALESCE( ' ' || dynastyname, '') 
                FROM person LEFT JOIN dynasty ON person.dynastyid = dynasty.dynastyid 
                WHERE personid = ? """, [person])
            result = cur.fetchone()
            if(result == None):
                return [], None
            personid = result[0]
            name = result[1]

        # Start the recursive query!
        cur.execute(
            """ WITH RECURSIVE children AS (
            SELECT p.personid, p.birthname || COALESCE( ' ' || d.dynastyname, '' ), 
            p.motherid, mot.birthname || COALESCE( ' ' || mot_d.dynastyname, '' ), 
            p.real_fatherid, dad.birthname || COALESCE( ' ' || dad_d.dynastyname, '' )
            FROM person p
            LEFT JOIN person mot ON mot.personid = p.motherid LEFT JOIN dynasty mot_d ON mot.dynastyid = mot_d.dynastyid
            LEFT JOIN person dad ON dad.personid = p.real_fatherid LEFT JOIN dynasty dad_d ON dad.dynastyid = dad_d.dynastyid
            LEFT JOIN dynasty d ON p.dynastyid = d.dynastyid
            WHERE (p.motherid = ? OR p.real_fatherid = ?)
            UNION
            SELECT p.personid,  p.birthname || COALESCE( ' ' || d.dynastyname, '' ), 
            p.motherid, mot.birthname || COALESCE( ' ' || mot_d.dynastyname, '' ), 
            p.real_fatherid, dad.birthname || COALESCE( ' ' || dad_d.dynastyname, '' )
            FROM person p
            LEFT JOIN person mot ON mot.personid = p.motherid LEFT JOIN dynasty mot_d ON mot.dynastyid = mot_d.dynastyid
            LEFT JOIN person dad ON dad.personid = p.real_fatherid LEFT JOIN dynasty dad_d ON dad.dynastyid = dad_d.dynastyid
            LEFT JOIN dynasty d ON p.dynastyid = d.dynastyid
            INNER JOIN children c ON (c.personid = p.motherid OR c.personid = p.real_fatherid)
            )
            SELECT * FROM children """, [personid, personid])

        result = cur.fetchall()

        cur.close()
        
        dag = {}
        tbl = {}

        tbl[0] = (personid, name)
        tbl[personid] = (personid, name)

        for t in result:
            tbl[int(t[0])] = t
            if(not t[2] == None): # Mot
                if(t[2] in dag):
                    dag[t[2]].append(t[0])
                else:
                    dag[t[2]] = [t[0]]
            if(not t[4] == None): # Fat
                if(t[4] in dag):
                    dag[t[4]].append(t[0])
                else:
                    dag[t[4]] = [t[0]]

        return tbl, dag
