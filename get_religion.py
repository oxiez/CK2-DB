
def get_religion(cur):
    return None
    with open('00_religion.txt') as f:
        #setup
        line = None
        for i in range(13):
            line = f.readline()
        #variable initialization
        rel_id = 1
        rel_name = None
        rel_group = None 
        # loop until the end of the file
        while True:
            #find the next religious group      
            line = f.readline()
            if len(line)==0: break
            if line.find('#')!=-1: continue
            
            index = line.find('=')
            rel_group = line[0:index-1]

            #find the next religion in this group            
            while line != '}\n':
                line = f.readline()
                if line.find('#')!=-1: continue
                
                
                
                #determine if it is a heresy
                
                #insert tuple <id,name,heresy,religiongroup>
                break
            
        
        
        
        #find the next religion
        
        #record is_heresy, moral_authority
        
        
        
        