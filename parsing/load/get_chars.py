        # Person(INT id, VARCHAR(63) birthName, INT dynasty, BOOLEAN isMale, DATE birthday, DATE deathday, INT fatherID,
        # INT real_fatherID, INT motherID, INT spouseID, INT religionID, INT cultureID, FLOAT fertility, FLOAT health, FLOAT wealth,
        # INT hostID, FLOAT prestige, FLOAT piety, INT provinceLocationID, INT employerID, INT martial, INT diplomacy, INT stewardship,
         # INT intrigue, INT learning)

import datetime

claim_title_regex = {"^title" : None}

claim_regex = {"title" : claim_title_regex,
               "pressed" : None,
               "weak" : None
}

person_regex = {"^bn" : None,
                "^dnt" : None,
                "^fem" : None,
                "^b_d" : None,
                "^d_d" : None,
                "^fat" : None, # The default for rfat if none specificed
                "^rfat" : None,
                "^mot" : None,
                "^spouse" : None,
                "^rel" : None,
                "^cul" : None,
                "^fer" : None,
                "^health" : None,
                "^wealth" : None,
                "^prs" : None,
                "^piety" : None,
                "^emp" : None,
                "^host" : None,
                "^oh" : None,
                "^att" : None, # This needs to be broken up manually
                "^tr" : None, # This needs to be broken up manually
                "^claim" : claim_regex # Repeated
}


def make_date(str):
    dt_arr = str.split('.')
    year = int(dt_arr[0])
    month = int(dt_arr[1])
    day = int(dt_arr[2])

    result_date = datetime.date(year, month, day)
    return result_date

def get_cul_ID(cur,name):
    cur.execute("SELECT cultureid FROM culture WHERE culturename=?",[name])
    cultureID = cur.fetchone()
    if cultureID!=None: cultureID=cultureID[0]
    return cultureID

def get_rel_ID(cur,name):
    cur.execute("SELECT religionid FROM religion WHERE religionname=?",[name])
    religionID = cur.fetchone()
    if religionID!=None: religionID=religionID[0]
    return religionID

def get_chars(data, cur):
    for charID in data:
        obj = data[charID]
        religionID = None
        cultureID = None
        isMale = True
        attributes = {}
        traits = []
        
        # Integer conversions and list truncation
        try:
            charID = int(charID) # Person id
            if("dnt" in  obj): obj["dnt"] = int(obj["dnt"])
            if("fat" in obj): obj["fat"] = int(obj["fat"])
            if("rfat" in obj): obj["rfat"] = int(obj["rfat"])
            else: obj["rfat"] = obj.get("fat")
            if("mot" in obj): obj["mot"] = int(obj["mot"]) 
            if("emp" in obj): obj["emp"] = int(obj["emp"])
            if("host" in obj): obj["host"] = int(obj["host"])
            
            if("fer" in obj): obj["fer"] = float(obj["fer"])
            if("health" in obj): obj["health"] = float(obj["health"])
            if("wealth" in obj): obj["wealth"] = float(obj["wealth"])
            if("prs" in obj): obj["prs"] = float(obj["prs"])
            if("piety" in obj): obj["piety"] = float(obj["piety"])

            # TODO: for some reason martial comes before diplomacy in our table
            #       we need to unswap these at some point
            if("att" in obj):
                attributes = [int(a) for a in obj.get('att')]
                attributes[0],attributes[1] = attributes[1], attributes[0]

            if("tr" in obj):
                traits = [int(t) for t in obj.get("tr")]
        except ValueError:
            raise Exception("ERROR: One of the person attributes is not a number!")

        if("rel" in obj): religionID = get_rel_ID(cur,obj["rel"])
        if("cul" in obj): cultureID = get_cul_ID(cur,obj["cul"])
        if("bn" in obj): obj["bn"] = obj["bn"]
        if("b_d" in obj): obj["b_d"] = make_date(obj["b_d"])
        if("d_d" in obj): obj["d_d"] = make_date(obj["d_d"])
        if("fem" in obj): isMale = False
        
        #if religion or culture is missing, default to dynasty religion and culture
        if obj.get('dnt')!=None:
            if ('rel' not in obj):
                cur.execute("SELECT religionID FROM dynasty WHERE dynastyID=?",[obj.get('dnt')])
                religionID = cur.fetchone()
                if religionID!=None: religionID=religionID[0]
            if ('cul' not in obj):
                cur.execute("SELECT cultureID FROM dynasty WHERE dynastyID=?",[obj.get('dnt')])
                cultureID = cur.fetchone()
                if cultureID!=None: cultureID=cultureID[0]
        
        cur.execute(
            'INSERT INTO Person Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            [charID, obj.get("bn"), obj.get("dnt"), isMale, obj.get("b_d"), obj.get("d_d"), obj.get("fat"),
             obj.get("rfat"), obj.get("mot"), religionID, cultureID, obj.get("fer"),
             obj.get("health"), obj.get("wealth"), obj.get("prs"), obj.get("piety"),
             obj.get("host"), obj.get("emp")] + attributes)

        if(isinstance(obj.get("oh"), list)):
            for title_id in (obj["oh"]):
                if title_id != '---':
                    cur.execute("INSERT INTO rulers VALUES(?, ?)", [charID, title_id])
        elif obj.get("oh"):
            title_id = obj["oh"]
            cur.execute("INSERT INTO rulers VALUES(?, ?)", [charID, title_id])

        for tr in traits:
            cur.execute("INSERT INTO trait Values(?, ?)", [charID, int(tr)])

        if("spouse" in obj):
            if(isinstance(obj["spouse"], list)):
                for s in obj["spouse"]:
                    cur.execute("INSERT INTO marriage Values(?, ?)",
                                [charID, s])
            else:
                cur.execute("INSERT INTO marriage Values(?, ?)",
                            [charID, obj["spouse"]])
        

        # Parse claims
        if("claim" in obj):
            if(isinstance(obj["claim"], list)):
                for claim in obj["claim"]:
                    if(isinstance(claim.get("title"), dict)):
                        claim["title"] = claim["title"]["title"]
                    cur.execute("INSERT INTO claim Values(?, ?, ?, ?)",
                                [charID, claim.get("title"),
                                 "pressed" in claim,
                                 "weak" in claim])
            else:
                claim = obj["claim"]
                if(isinstance(claim.get("title"), dict)):
                        claim["title"] = claim["title"]["title"]
                cur.execute("INSERT INTO claim Values(?, ?, ?, ?)",
                            [charID,
                             claim.get("title"),
                             "pressed" in claim,
                             "weak" in claim])
