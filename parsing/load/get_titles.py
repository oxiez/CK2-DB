import io
import re
from .get_chars import make_date

def get_titles(data,cur):
    for title in data:
        obj = data[title]
        level = title[0]
        name = title[2:]
        
        if(isinstance(obj.get("liege"), dict)):
            obj["liege"] = obj["liege"]["base_title"] # liege id
        
        if(isinstance(obj.get("de_jure_liege"), dict)):
            obj["de_jure_liege"] = obj["de_jure_liege"]["base_title"]

        cur.execute("INSERT INTO title VALUES(?, ?, ?, ?, ?, ?)",
                    [title,
                     obj.get("holder"),
                     name,
                     level,
                     obj.get("liege"),
                     obj.get("de_jure_liege")]
        )

        if(obj.get("holder")):
            cur.execute("INSERT INTO rulers VALUES(?, ?)",
                        [obj.get("holder"),
                         obj.get("tag")]
            )
        
        hist = obj.get("history")
        if hist is not None:
            for date in hist:
                holder = hist.get(date)
                # sometimes succession entries are listed twice
                if isinstance(holder,list):
                    holder = holder[-1]
                holder = holder.get('holder')
                # sometimes two people inherit on the same day
                # probably a ruler receiving a title then granting it away on the same day
                if isinstance(holder,list):
                    holder = holder[-1]
                # somtimes the holder information comes with info on how they inherited
                if isinstance(holder,dict):
                    holder = holder.get('who')
                # case where title goes out of existence: holder == "0"
                cur.execute("INSERT INTO titlehistory VALUES(?, ?, ?)",
                            [title, holder, make_date(date)])
