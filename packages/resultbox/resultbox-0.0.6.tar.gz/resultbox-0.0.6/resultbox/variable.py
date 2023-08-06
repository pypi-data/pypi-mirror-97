# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:27:27 2019

@author: Reuben

Variables help resultbox know how to interpret and display data. Sometimes,
variables have different components, like x, y, and z coordinates. They
often have units, such as meters. 

The idea is that we define a variable just once. Whenever we add in some
data for that variable to a Box, we also pass in that variable. Then, we
can let resultbox take care of the rest. 

"""

import pandas as pd
from difflib import SequenceMatcher
from . import utils

def _expand_single(key, val, store, specified=None):
    ''' Expand a value into its components 
    
    Args:
        key (Variable): The variable key
        val: The data for that variable
        store (Store): The variable store
        
    Returns:
        dict: A dictionary of keys and values. If the variables has components,
        the dictionary contains the component keys and component values.
    '''
    if isinstance(val, dict):
        r = expand(val, store)
        return {key: r}
    else:
        if key in store:
            if specified is not None and key not in specified:
                return {key, val}
            if store[key].subkeys is not None:
                subkeys = store[key].subkeys
                if len(val) == len(subkeys):
                    out = {}
                    for subkey, v in zip(subkeys, val):
                        out[subkey] = v
                    return out
        return {key: val}

def expand(source, store, specified=None):
    ''' Expand variable components within a list or dictionary recursively 
    
    Args:
        source (list or dict): The source list (of dictionaries) or dictionary.
        The keys must exist in the store.
        store (Store): The corresponding Store instance.
        
    Returns:
        list or dict: The expanded list or dictionary.
    '''
    if isinstance(source, list):
        out = []
        for val in source:
            r = expand(val, store)
            out.append(r)
    elif isinstance(source, dict):
        out = {}
        for key, val in source.items():
            out.update( _expand_single(key, val, store, specified))
    return out


class Store(dict):
    ''' A store is a container for Variables  '''
    
    def __init__(self, name=None):
        self.name = name
        self._id_dct = {}
    
    def new(self, name, doc=None, unit=None, components=None, sep=' - ',
            category=None, tags=None, safe=True, identifier=None):
        ''' Create a new variable 
        
        Args:
            name (str): The variable name
            doc (str): A documentation string. Defaults to None.
            unit (str): The units of the variable (usually abbreviated).
            Defaults to None.
            components (list[str]): A list of names for each
            component. Defaults to None.
            sep (str): The separator between the name and any component names.
            category (str): An optional category
            tags (list[str]): Optional tags
            
        Returns:
            Variable: The new variable
            
        Note:
            The 'add' method is a copy of this method.
        '''
        new = Variable(name, doc, unit, components=components, sep=sep,
                       category=category, tags=tags, identifier=identifier)
        if new.key in self and safe:
            raise KeyError('Key "' + str(name) + '" already exists. Names '
                          + 'must be unique.')
        elif new.key in self and not safe:
            return self[new.key]
        self[new.key] = new
        if identifier is not None:
            self._id_dct[identifier] = new.key
        return new
    
    def id_starts_with(self, s):
        """ Returns a list of variables with identifies matching a suffix 
        
        Args:
            s (str): The string at the start of the identifiers.
        
        Returns:
            list: List of matching variables. If no variables match, the
            list will be empty.
        """
        d = self._id_dct
        return [v for k, v in d.items() if k.startswith(s)]
    
    def nearest(self, key):
        ''' Return the variable that best best-matches the input string
        
        Args:
            key (str): The input string
            
        Returns:
            Variable: The variable with the key that best matches the input
        '''
        keys = list(self.keys())
        ratios = [SequenceMatcher(None, key, k).ratio() for k in keys]
        return self[keys[ratios.index(max(ratios))]]
    
    def suffixed(self, variable, suffix):
        ''' Create or return a suffixed variable using an existing one 
        
        Args:
            variable (Variable): A variable
            suffix (str): The suffix to append to the name
            
        Returns:
            Variable: Creates a new one if needed, or returns existing.
        '''
        new_name = variable.name + suffix
        key = Variable._append_unit(new_name, variable.unit)
        if key in self:
            return self[key]
        else:
            kwargs = variable.to_dict()
            kwargs['name'] = new_name
            return self.new(**kwargs)
    
    def add_csv(self, fname, **kwargs):
        usecols = ['identifier', 'name', 'doc', 'unit', 'components',
                   'sep', 'category', 'tags']
        df = pd.read_csv(fname, usecols=usecols, **kwargs)
        records = df.to_dict(orient='rows')
        for dct in records:
            for k in dct.keys():
                if pd.isna(dct[k]):
                    dct[k] = None
            if dct['components'] is not None:
                components = dct['components'].replace(', ', ',').split(',')
                dct['components'] = components
            if dct['tags'] is not None:
                dct['tags'] = dct['tags'].replace(', ', ',').split(',')
            self.add(**dct, safe=False)
    
    def to_csv(self, fname, **kwargs):
        records = []
        for v in self.values():
            dct = v.to_dict()
            if dct['components'] is not None:
                dct['components'] = ', '.join(dct['components'])
            if dct['tags'] is not None:
                dct['tags'] = ', '.join(dct['tags'])
            records.append(dct)
        df = pd.DataFrame.from_records(records)
        df.to_csv(fname)
            
    def __getattr__(self, key):
        if key in self._id_dct:
            return self[self._id_dct[key]]
        raise AttributeError('Indentifier "' + str(key) + '" not in store.')

    def __missing__(self, key):
        if key in self._id_dct:
            return self[self._id_dct[key]]
        else:
            return super().__missing__(key)
            
    add = new


class Variable(str):
    ''' Metadata for specific data 
    
    Args:
        name (str): The name of the variable
        doc (str): A documentation string. Defaults to None.
        unit (str): The units of the variable (usually abbreviated).
        Defaults to None.
        components (list[str]): A list of names for each
        component. Defaults to None.
        sep (str): The separator between the name and any component names.
        category (str): An optional category
        tags (list[str]): Optional tags
        
    Note:
        Variables subclass `str`, so they can be used like strings. Care is
        needed when serialising and deserialising them, as otherwise their
        special attributes will be lost.
    '''
    def __new__(cls,
               name,
               doc=None,
               unit=None,
               components=None,
               sep=' - ',
               category=None,
               tags=None,
               identifier=None):
        return super().__new__(cls, cls._append_unit(name, unit))
    
    def __init__(self,
                 name,
                 doc=None,
                 unit=None,
                 components=None,
                 sep=' - ',
                 category=None,
                 tags=None,
                 identifier=None):
        self.name = name
        self.doc = doc if doc is None else doc
        self.unit = unit
        self.components = components
        self.sep = sep
        self.category = category
        self.tags = None if tags is None else utils.listify(tags)
        self.identifier = identifier
        self.key = self._append_unit(self.name, self.unit)
        
    def to_dict(self):
        ''' Create a dictionary containing the Variable attributes '''
        d = {'name': self.name,
                'doc': self.doc,
                'unit': self.unit,
                'components': self.components,
                'sep': self.sep,
                'category': self.category,
                'tags': self.tags,
                'identifier': self.identifier}
        return d
    
    @classmethod
    def from_dict(cls, dct):
        ''' Create a new Variable instance from a dictionary of attributes '''
        return cls(**dct)
    
    def to_str(self):
        ''' Create a string containing the Variable attributes '''
        dct = self.to_dict()
        return utils.dict_to_str(dct, val_sep='=', key_sep=';')
    
    @classmethod
    def from_str(cls, s):
        ''' Create a new Variable instance from a string of attributes '''
        d = utils.str_to_dict(s, val_sep='=', key_sep=';')
        return cls.from_dict(d)
    
    def __str__(self):
        return self.key

    @classmethod
    def _append_unit(cls, string, unit):
        ''' Add the unit to the string '''
        if unit is not None:
            return string + ' [' + unit + ']'
        else:
            return string
    
    def _component_name(self, component):
        ''' Get the full key for a component '''
        component_name = self.name + self.sep + component
        return self._append_unit(component_name, self.unit)
    
    @property
    def subkeys(self):
        ''' Return a list of keys for the variable components '''
        if self.components is None:
            return None
        keys = []
        for component in self.components:
            keys.append(self._component_name(component))
        return keys

    @property
    def label(self):
        ''' The variable name formatted with a trailing colon '''
        return self.name + ':'
    
    def __getitem__(self, component):
        if not isinstance(component, str):
            return super().__getitem__(component)
        if component in self.components:
            return self._component_name(component)
        else:
            return super().__getitem__(component)
    
        
class Aliases(dict):
    ''' Variables allow other keys to be used as aliases for variables 
    
    This class is a subclass of `dict`. It is designed so that each key
    is an alias, and its value is the corresponding variable. The Aliases
    instance provides methods to 'translate' (swap) aliases within standard
    data structures to be their corresponding variables.
    '''
    def __init__(self, data=None, name=None):
        data = {} if data is None else data
        self.update(data)
        self.name = name
        
    def add_csv(self,
                fname,
                store,
                identifier_col='identifier',
                alias_col='alias',
                **kwargs):
        df = pd.read_csv(fname, usecols=[identifier_col, alias_col], **kwargs)
        df = df.dropna()
        keys = df[identifier_col]
        vs = [store[k] for k in keys]
        aliases = df[alias_col]
        dct = {k: v for k, v in zip(aliases, vs)}
        self.update(dct)
        
    def __missing__(self, key):
        return key

    def translate(self, obj):
        ''' Recusively translate an object, swapping any dictionary keys '''
        if obj is None:
            return None
        if isinstance(obj, str):
            return self.translate_str(obj)
        elif isinstance(obj, list):
            return self.translate_list(obj)
        elif isinstance(obj, dict):
            return self.translate_dict(obj)
        else:
            return obj

    def translate_str(self, s):
        ''' Translate a string '''
        return self[s]

    def translate_dict_vals(self, dct):
        ''' Translate the values in a dictionary '''
        return {k: self.translate(v) for k, v in dct.items()}
        
    def translate_dict(self, dct):
        ''' Translate the keys in a dictionary '''
        return {self[k]: self.translate(v) for k, v in dct.items()}

    def translate_list(self, lst):
        ''' Translate the objects in a list '''
        return [self.translate(k) for k in lst]
    
    def inverse(self):
        ''' Return an inverse dictionary of self 
        
        Note:
            Values must be unique.
        '''
        return {v: k for k, v in self.items()}

