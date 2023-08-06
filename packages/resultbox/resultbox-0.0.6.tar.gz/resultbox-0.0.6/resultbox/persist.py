# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:22:35 2019

@author: Reuben

The persist module helps the user save and load Box instances. It is
able to be extended for use with any handler.

The module instantiates a Manager class and copies its load and save methods 
to the module level, for easier usage by client code.

"""

import json
import zlib
import numpy as np

from .box import Box
from . import adapters, variable, constants


def serialise_vars(box):
    ''' Turn all the variables in a Box into a list of strings '''
    keys = box.keys(dependent=True, independent=True)
    lst = [k.to_str() for k in keys if isinstance(k, variable.Variable)]
    lst.sort()
    return lst

def deserialise_vars(lst):
    ''' Turn a list of Variable strings into a dictionary of Variables '''
    variables = [variable.Variable.from_str(s) for s in lst]
    return {v.key: v for v in variables}

def make_pack(box):
    ''' Prepare a box for persistance by including Variable data '''
    return {'data': list(box),
            'vars': serialise_vars(box)}

def unpack(pack):
    ''' Recreate a box from persistance, including Variables as keys '''
    box_data = pack['data']
    if 'vars' not in pack: 
        pack['vars'] = []
    var_dict = deserialise_vars(pack['vars'])
    aliases = variable.Aliases(var_dict)
    return aliases.translate(box_data)


class Manager():
    ''' The manager looks after different classes that can process Box data.
    
    It provides two key methods - load and save.
    '''
    
    default_handler = 'cbox'
    
    def __init__(self, default_enabled=True):
        self.handlers = {'box': JSON(),
                         'cbox': CJSON(),
                         'npz': NPZ()}
        self.specified = None
        self.default_enabled = True
        
    def add_handler(self, key, handler):
        ''' Add a handler 
        
        Args:
            key (str): The unique name of the handler.
            handler (Handler): A Handler subclass.
        '''
        self.handlers[key] = handler
        
    def del_handler(self, key):
        ''' Delete a handler 
        
        Args:
            key (str): The unique name of the handler
        '''
        
    def specify(self, key):
        ''' Specify the handler to use 
        
        Args:
            key (str): The unique name of the handler.
        '''
        self.specified = key
        
    def _load(self, source, handler=None, **kwargs):
        h = handler if handler is not None else None
        if h is None and self.specified is not None:
            h = self.specified
        if h is None:
            for name, handler in self.handlers.items():
                if handler.suitable(source, **kwargs):
                    h = name
        if h is None and self.default_enabled:
            h = self.default_handler
            source += '.cbox'
        if h is None:
            raise ValueError('No valid handler found for source: ' +
                             str(source))
        return self.handlers[h].load(source, **kwargs)

    def load(self, source, handler=None, as_box=True, **kwargs):
        ''' Return a new Box by reading the source 
        
        Args:
            source (str): The source to load from
            handler (str): Optional key specifying which handler to use
            as_box (bool): If true (the default), return a Box, otherwise
            return just the raw data.
            kwargs: Other keyword arguments passed to the handler.
        '''
        pack = self._load(source, handler, **kwargs)
        ret = unpack(pack)
        if as_box:
            return Box(ret)
        else:
            return ret

    def save(self, box, target, handler=None, **kwargs):
        ''' Save the Box data to the target 
        
        Args:
            box (Box): The Box instance.
            target (str): A string specifying the target
            handler (str): Optional key specifying which handler to use
            kwargs: Other keyword arguments passed to the handler.
        '''
        pack = make_pack(box)
        h = handler if handler is not None else None
        if h is None and self.specified is not None:
            h = self.specified
        if h is None:
            for name, handler in self.handlers.items():
                if handler.suitable(target, **kwargs):
                    h = name
        if h is None and self.default_enabled:
            h = self.default_handler
            target += '.cbox'
        if h is None:
            raise ValueError('No valid handler found for target: ' +
                             str(target))
        return self.handlers[h].save(pack, target, **kwargs)


class Handler():
    ''' A handler that can load or save Box data '''
    
    def suitable(self, s, **kwargs):
        ''' Return true the handler suits the target/source string, s '''
        raise NotImplementedError

    def save(self, box, fname, **kwargs):
        ''' Save the box '''
        raise NotImplementedError
    
    def load(self, fname, **kwargs):
        ''' Load a box 
        
        Returns:
            list: The raw data for the Box
        '''
        raise NotImplementedError
        

class JSONEncoder(json.JSONEncoder):
    ''' A custom encoder to encode numpy arrays '''
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return {'__ndarray__': obj.tolist(), 'dtype': str(obj.dtype)}
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def np_decode(dct):
    ''' A custom decoder to handle numpy arrays '''
    if '__ndarray__' in dct:
        return np.array(dct['__ndarray__'], dtype=dct['dtype'])
    return dct
    

class JSON(Handler):
    ''' Load and save in JSON format '''
    def suitable(self, fname, **kwargs):
        if fname.endswith('.box'):
            return True
        
    def save(self, box, fname, **kwargs):
        ''' Save a Box to a file 
        
        Args:
            box (Box): The Box instance.
            fname (str): A string specifying the full filename
        '''
        jsn = json.dumps(box, cls=JSONEncoder)
        with open(fname, mode='w') as f:
            f.write(jsn)
    
    def load(self, fname, **kwargs):
        ''' Return box data by reading the source 
        
        Args:
            fname (str): The file to load from
            
        Returns:
            list: A list of box data
        '''
        with open(fname, mode='r') as f:
            jsn = f.read()
        lst = json.loads(jsn, object_hook=np_decode)
        return lst


class CJSON(Handler):
    ''' Load and save in compressed JSON format '''
    def suitable(self, fname, **kwargs):
        if fname.endswith('.cbox'):
            return True
        
    def save(self, box, fname, **kwargs):
        ''' Save a Box to a file 
        
        Args:
            box (Box): The Box instance.
            fname (str): A string specifying the full filename
        '''
        jsn = json.dumps(box, cls=JSONEncoder)
        compressed = zlib.compress(jsn.encode(), level=9)
        with open(fname, mode='wb') as f:
            f.write(compressed)
    
    def load(self, fname, **kwargs):
        ''' Return box data by reading the source 
        
        Args:
            fname (str): The file to load from
            
        Returns:
            list: A list of box data
        '''
        with open(fname, mode='rb') as f:
            compressed = f.read()
        jsn = zlib.decompress(compressed).decode()
        lst = json.loads(jsn, object_hook=np_decode)
        return lst


class NPZ(Handler):
    ''' Load and save in compressed JSON format '''
    def suitable(self, fname, **kwargs):
        if fname.endswith('.npz'):
            return True
        
    def save(self, box, fname, **kwargs):
        ''' Save a Box to a file 
        
        Args:
            box (Box): The Box instance.
            fname (str): A string specifying the full filename
        '''
        flat = adapters.flat_dict(box)
        np.savez_compressed(fname, **flat, **kwargs)
    
    def load(self, fname, **kwargs):
        ''' Return box data by reading the source 
        
        Args:
            fname (str): The file to load from
            
        Returns:
            list: A list of box data
        '''
        def itemise_scalars(obj):
            if obj.ndim==0:
                return obj.item()
            return obj
        
        flat = {}
        with np.load(fname, **kwargs) as data:
            for key in list(data.keys()):
                flat[key] = itemise_scalars(data[key])
        
        composed = adapters.compose(flat)
        for row in composed['data']:
            for k in [constants.DEP, constants.INDEP]:
                if k not in row:
                    row[k] = {}
        return composed
            
            
manager = Manager()
load = manager.load
save = manager.save
