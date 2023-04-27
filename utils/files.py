import re

def filename_normal(filename):
    s2 = []
    for c1 in filename:
        if re.match('[a-zA-Zа-яА-Я0-9]', c1):
            s2.append(c1)
        else:
            s2.append('_')
    return ''.join(s2)        
    
