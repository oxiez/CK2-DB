from lark import Lark, Transformer
from multiprocessing import Pool

import re

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
def lark_parse(string):
    return parser.parse(string)

list_re = r'''{\s*([^{}\[\]=<>#"\t\n ]+|"[^"]*")(\s+([^{}\[\]=<>#"\t\n ]+|"[^"]*"))*\s*}'''
bracket_prog = re.compile(list_re)
comment_re = r'''#.+\n'''
comment_prog = re.compile(comment_re)

# delete comments, replace lists { ... } as [ ... ] so our lalr grammar is well-defined
def preprocess(save_string):
    return bracket_prog.sub(
            lambda matchobj: "["+matchobj.group(0)[1:-1]+"]",
            comment_prog.sub(lambda x: "\n", save_string)
    )

# given an assignment list, extract out only the top-level assignments of interest
def extract_key_strings(save_string,keywords):
    substrings = []
    depth = 0
    kstart = 0
    key = ""
    for i,c in enumerate(save_string): 
        if c == '{':
            if depth == 0:
                key = None
                kend = i
                while not save_string[kend].isalnum(): kend -= 1
                kstart = kend
                while save_string[kstart].isalnum() or save_string[kstart] == '_': kstart -= 1
                kstart += 1
                key = save_string[kstart:kend+1]
            depth += 1
        if c == '}':
            depth -= 1 
            if depth == 0 and key in keywords:
                substrings.append(save_string[kstart:i+1])
    return substrings

def parse(save_string):
    return lark_parse(preprocess(save_string))

def parse_character(character_string):
    chunks = []
    depth = 0
    kstart = 0
    # parallelize the parsing of individual characters
    # we can do this because we know that characterID is actually a unique identifier
    for i,c in enumerate(character_string): 
        if c == '{':
            if depth == 1:
                kend = i
                while not character_string[kend].isalnum(): kend -= 1
                kstart = kend
                while character_string[kstart].isalnum() or character_string[kstart] == '_': kstart -= 1
                kstart += 1
            depth += 1
        if c == '}':
            depth -= 1 
            if depth == 1:
                chunks.append(character_string[kstart:i+1])
    parsed_chunks = None
    with Pool() as p:
        parsed_chunks = p.map(lark_parse, chunks)
    res =  ('character', dict(parsed_chunks))
    return res

# returns a dictionary representing the relevant sections of the save file
def parse_save(save_string):
    strings = extract_key_strings(
            preprocess(save_string[8:save_string.rfind("}")]), # save data starts with "CK2txt" and ends with the trailing '''}\nchecksum="..."'''
            keywords=["dynasties", "character", "religion", "provinces", "bloodline", "title"]
    )
    character = strings.pop(1)
    # take advantage of multiprocessing and parse in parallel
    parsed_vals = None
    with Pool() as p:
        parsed_vals = p.map(lark_parse, strings)
    # parse character with multiprocessing separately
    parsed_vals.append(parse_character(character))
    return dict(parsed_vals) 
