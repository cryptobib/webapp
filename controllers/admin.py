# -*- coding: utf-8 -*-

def reload():
    """ Reload the cache (e.g., after an update of the database). Can only be called from localhost """
    if request.is_local:
        cache.ram.clear()
        cache.disk.clear()
        
        return dict()
    else:
        raise HTTP(404)
        
