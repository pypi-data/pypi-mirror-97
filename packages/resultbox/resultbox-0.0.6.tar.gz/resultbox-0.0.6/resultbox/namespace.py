# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:14:59 2019

@author: Reuben
"""

from .variable import Store, Aliases

class Name_Space(dict):
    def __init__(self, obj_cls=Store):
        self.i = 0
        self.obj_cls = obj_cls
        self._active = None
    
    def __missing__(self, key):
        return self.create(key)
    
    def create(self, key):
        new = self.obj_cls(name=key)
        self[key] = new
        return new
    
    def get(self, key=None):
        if key is None:
            key = self.i
            self.i += 1
        if key not in self:
            return self.create(key)
        return self[key]

    def set_active(self, key):
        if key in self or key is None:
            self._active_container = key
        else:
            raise KeyError(key + ' not found in name space.')
    
    def active(self):
        return self[self._active]
    
    def duplicate(self, key, new_key):
        self[new_key] = self[key].copy()
        return self[new_key]


stores = Name_Space(Store)
aliases = Name_Space(Aliases)

def get_store(name=None):
    return stores.get(name)

def get_aliases(name=None):
    return aliases.get(name)