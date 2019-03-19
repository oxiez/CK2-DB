import io

#level_id
title_regex = {"holder" : None,
               "^liege" : None, # Dejure Liege
               "de_facto_liege" : None}

def get_titles(file,cur):
    x = file.readline()
    while(x):
        x = file.readline()
