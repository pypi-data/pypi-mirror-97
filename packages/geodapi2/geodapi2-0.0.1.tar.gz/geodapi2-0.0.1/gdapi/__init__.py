from urllib.request import urlopen
from json import load
def level(id2, select=''):
    t = load(urlopen(f'https://gdbrowser.com/api/level/{id2}'))
    if select == '':
        return t
    elif select != '':
        return t.get(select)
def search(query, result='', spec=''):
    t = load(urlopen(f'https://gdbrowser.com/api/search/{query}'))
    if result == '' and spec =='':
        return t
    elif result != '' and spec == '':
        return t[result]
    elif result != '' and spec != '':
        return t[result][spec]
def getSong(varid, mode):
    t = load(urlopen(f'https://gdbrowser.com/api/level/{varid}'))
    if mode == 'name':
        return t['songName']
    elif mode == 'id':
        return t['songID']
    elif mode == 'link':
        return t['songLink']
        
