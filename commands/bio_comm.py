from commands.command import Command, table_print

class BioComm(Command):
    COMM_STR = "bio"
    HELP_STR = """\

The 'bio' command will list all info there is to know about a
character.
----------------------------------------------------------------------
The command 'bio' requires 1 argument:

    'bio <person ID>'

You can get character IDs from the 'person' command.
----------------------------------------------------------------------
Specifically, the 'bio' command displays:
- The name of a character
- Their date of birth
- Their date of death (if they have one)
- Their parents (if stored in game)
- Their spouce (if they have one)
- Their sex
- Their religion
- Their culture
- Their attributes
- Their traits
- The titles that they hold (if they hold any)
- The claims that they hold (if they hold any)\n"""

    def doCommand(data,args):
        if len(args)!=1:
            print('ERROR: query should be of the form bio personID.')
            return
        personid = args[0]
        query_result = data.query_personid(personid)
        if len(query_result)==0:
            print('Could not find person with personID ' + personid)
        else:
            personid,birthname,dynastyname,ismale,birthday,deathday,fatherid,real_fatherid,motherid,religionname,culturename,fertility,health,wealth,hostid,prestige,piety,employerid,martial,diplomacy,stewardship,intrigue,learning = query_result[0]
            #full name
            print(birthname + (' ' + dynastyname if dynastyname != None else ''))
            #dates
            print('Born: ' + str(birthday) + ('' if deathday == None else '    Died: '+str(deathday)))
            # parents
            if fatherid!=None:
                father_query = data.query_personid(fatherid)[0]
                print('Father: ' + str(father_query[1]) + ' ' + ('' if father_query[2] == None else str(father_query[2])+' ') + str(fatherid))
            if fatherid!=real_fatherid:
                father_query = data.query_personid(real_fatherid)[0]
                print('Real Father: ' + str(father_query[1]) + ' ' + ('' if father_query[2] == None else str(father_query[2])+' ') + str(real_fatherid))
            
            if motherid!=None:
                mother_query = data.query_personid(motherid)[0]
                print('Mother: '  + str(mother_query[1]) + ' ' + ('' if mother_query[2] == None else str(mother_query[2])+ ' ') + str(motherid))
            #spouse
            spouses = data.query_spouse(personid)
            for s in spouses:
                spouseid = s[0]
                spouse_query = data.query_personid(spouseid)[0]
                print('Spouse: '  + str(spouse_query[1]) + ' ' + ('' if spouse_query[2] == None else str(spouse_query[2])+ ' ') + str(spouseid))
            #titles
            titles = data.query_title(personid)
            if len(titles)!=0:
                print('Titles: ' + ', '.join([x[4] for x in titles]))
            #claims
            claims = data.query_claim(personid)
            if len(claims)!=0:
                print('Claims: ' + ', '.join([x[0] for x in claims]))
            #personal info
            print('Sex: ' + ('M' if ismale else 'F') + '    Religion: ' + religionname + '    Culture: ' + culturename)
            if deathday == None:
                print('Prestige: ' + str(prestige) + '    Piety: ' + str(piety) + '    Health: ' + str(health) + '    Wealth: ' + str(wealth) + '    Fertility: ' + str(fertility))
                print('Attributes: martial ' + str(martial) + ', diplomacy ' + str(diplomacy) + ', stewardship ' + str(stewardship) + ', intrigue ' + str(intrigue) + ', learning ' + str(learning))
                print('Traits: ' + ', '.join([x[0] for x in data.query_traits(personid)]))
