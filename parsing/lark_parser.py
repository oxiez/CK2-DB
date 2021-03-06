from lark import Lark, Transformer

# returns a dictionary representing the relevant sections of the save file
def parse(save_string):
    # preprocessing
    # if { ... } is a list of primitives, rewrite it as [ ... ]
    # if { } is an empty object, rewrite as < >
    # filter in the only strings we care about
    processed_string = [c for c in save_string]
    keywords = ["dynasties", "character", "religion", "provinces", "bloodline", "title"]
    substrings = dict()
    
    stack = []
    skip = False
    for i,c in enumerate(save_string):
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
            if len(lst) == 0:
                processed_string[start] = '<'
                processed_string[end] = '>'
                skip = True
                continue
            # list of numbers
            flag = True 
            for token in lst:
                try:
                    float(token)
                except:
                    flag = False
                    break
            # list of strings
            if not flag:
                flag = True
                for token in lst:
                    if '=' in token:
                        flag = False
                        break
            if flag: #if these are all numbers, or baronies
                processed_string[start] = '['
                processed_string[end] = ']'
            if len(stack)==0 and key is not None and key in keywords: #and (str(key) not in blacklist):
                substrings[key] = key+"="+"".join(processed_string[start:end+1])
    
    
    ck2_grammar = """
        ?start: a
    
        ?a: var _w "=" _w val _w
    
        _w: WS*
    
        ?var: /[A-Za-z0-9_.\-]+/    -> var_var
    
        ?val: "{" _w a+ "}"         -> dict
            | "{" _w objlist "}"
            | "[" _w (var _w)+ "]"  -> list
            | "<" _w ">"            -> nothing
            | ESCAPED_STRING        -> string
            | var                   -> val_var
    
        objlist: ( "{" _w a+ "}" _w )+
    
        %import common.ESCAPED_STRING
        %import common.WS
    
        %ignore WS
    """

    class TreeToDict(Transformer):
        def start(self, lst):
            return dict(lst[0])
    
        def a(self,key_value):
            k,v = key_value
            return k, v
    
        def val_var(self,token):
            (token,)=token
            return str(token)
     
        def var_var(self,token):
            return self.val_var(token)
    
        def string(self,esc_string):
            (esc_string,)=esc_string
            return esc_string[1:-1]
    
        def objlist(self,stuff):
            return dict(stuff)
    
        dict = dict
        list = list
    
    l = Lark(ck2_grammar,parser="lalr",transformer=TreeToDict())
    
    data = dict()
    for k in keywords:
        data[k] = l.parse(substrings[k])

    return data 
