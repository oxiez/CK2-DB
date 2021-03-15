from lark import Lark, Transformer

ck2_grammar = """
    ?start: a+

    ?a: var _w ("="|"<"|">"|">="|"<=") _w val _w

    _w: WS*

    ?var: /[^\\{ \\} \\[ \\] = < > # " \\t \\n \\ ]+/    -> var_var

    ?esc_var: "\\"" [/[^"]+/] "\\""

    ?val: "{" _w a+ "}"         -> dict
        | "{" _w objlist "}"
        | "[" _w ((var|esc_var) _w)+ "]"  -> list
        | "{" _w "}"            -> nothing
        | var                   -> val_var
        | esc_var               -> esc_var

    objlist: ( "{" _w a+ "}" _w )+

    %import common.WS
    %import common.SH_COMMENT

    %ignore WS
    %ignore SH_COMMENT
"""

class TreeToDict(Transformer):
    def start(self, lst):
        return dict(lst)

    def a(self,key_value):
        k,v = key_value
        return k, v

    def val_var(self,token):
        (token,)=token
        return str(token)
 
    def var_var(self,token):
        return self.val_var(token)

    def esc_var(self,lst):
        return "".join(lst)

    def string(self,esc_string):
        (esc_string,)=esc_string
        return str(esc_string)

    def objlist(self,stuff):
        return dict(stuff)

    def nothing(self,stuff):
        return dict()

    def dict(self,pair_lst):
        # sometimes ck2 files just re-use the same key (e.g. bloodline member=)
        # if this is the case, then make d[key] a list with entries for each assigned value
        d = dict()
        for k,v in pair_lst:
            if k not in d:
                d[k] = v
            else:
                if isinstance(d[k], list):
                    d[k].append(v)
                else:
                    d[k] = [d[k],v]
        return d

    list = list

parser = Lark(ck2_grammar,parser="lalr",transformer=TreeToDict())

def parse(save_string, keywords=None):
    # preprocessing
    # if { ... } is a list of primitives, rewrite it as [ ... ]
    # if keywords is specified, only parse the top-level assignments we care about
    processed_string = [c for c in save_string]
    substrings = dict()

    stack = []
    skip = False
    comment = False
    for i,c in enumerate(save_string):
        if c == '#':
            comment = True

        if comment:
            if c == '\n':
                comment = False
            continue

        if c == '{':
            key = None
            if len(stack) == 0:
                kend = i
                while not save_string[kend].isalnum(): kend -= 1
                kstart = kend
                while save_string[kstart].isalnum() or save_string[kstart] == '_': kstart -= 1
                kstart += 1
                key = save_string[kstart:kend+1]
            stack.append((key,i))
            skip = False

        if c == '}':
            if len(stack) == 0:
                break
            key, start = stack.pop()
            end = i
            if skip:
                continue
            substr = save_string[start+1:end]
            lst = substr.split()
            # empty object
            if len(lst) == 0:
                skip = True
                continue
            # list of non-assignments
            flag = True
            for token in lst:
                if '=' in token:
                    flag = False
                    break
            if flag: # the object { ... } is really a list
                processed_string[start] = '['
                processed_string[end] = ']'
            if len(stack)==0 and key is not None and (keywords is None or key in keywords): #and (str(key) not in blacklist):
                substrings[key] = key+"="+"".join(processed_string[start:end+1])

    data = parser.parse("".join(substrings.values()))
    return data 

# returns a dictionary representing the relevant sections of the save file
def parse_save(save_string):
    keys = ["dynasties", "character", "religion", "provinces", "bloodline", "title"]
    return parse(save_string, keywords=keys)
