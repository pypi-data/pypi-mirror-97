GDAPI Is a simple geometry dash api.

Examples:
    from gdapi import *
    zodiac = search('zodiac', 0, 'id')
    song = getSong(zodiac, 'name')
    song
    
    Result:
    Creo - Sphere

    from gdapi import *
    tlr = level(55520)
    name = tlr.getz('name')
    name

    Result:
        THE LIGHTNING ROAD
        
Commands:
    getSong() - Get Info About A Level's Song
    Parameters:
        id2=idoflevelorvar, mode='id'/'name'/'link'
    search() - Find levels by name
    Parameters:
        name, specificresult, specificproperty
    level() - Get info about a level by id
    Parameters:
        id2, specificproperty
        
    
        
    
        
