# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:27:38 2019

@author: Reuben

Sometimes it's useful not to have to pass around a dictionary or other object
to accumulate data (e.g. key-value pairs). To that end, this module provides
singleton-like access to a set of dictionaries. A call to the `get_dict`
method with the same name will always return the same dictionary.

This approach can be useful in complex classes where multiple methods all
inpput data into a resultbox entry.

"""
    
class Dict_Container(dict):
    ''' A dictionary to contain dictionaries '''
    def __missing__(self, key):
        self[key] = {}
        return self[key]

dict_container = Dict_Container()

def get_dict(name):
    ''' Return the named dictionary 
    
    Args:
        name (str): The name of the dictionary
        
    Returns:
        dict: The dictionary
    '''
    return dict_container[name]
