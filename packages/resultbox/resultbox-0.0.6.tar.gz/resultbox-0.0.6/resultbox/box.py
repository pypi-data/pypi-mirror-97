# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 08:47:07 2019

@author: Reuben

The Box class at the heart of resultbox. The idea of a Box is to be able to
pile in results during an analysis and not worry about the structure. The
results can be of different types. After the analysis has completed, tables
and plots can be generated simply from the data within the Box.

"""

import hashlib
import numpy as np
from . import variable
from .utils import listify, dict_to_str, orient
from .constants import IND, DEP, INDEP
from . import settings
from copy import deepcopy

def hashable(obj):
    ''' Make an hashable representation of an object for hashlib '''
    return bytes(str(obj), 'utf-8')

def hash_dict(dct):
    ''' Generate a hash from a dictionary '''
    h = hashlib.md5()
    def update(d):
        for k, v in d.items():
            h.update(hashable(k))
            if isinstance(v, dict):
                update(v)
            else:
                h.update(hashable(v))
    update(dct)
    return h.digest()

def validate_row(row):
    ''' Ensure row data is valid 
    
    This currently just checks that 2D arrays match the variable components.
    '''
    subkeys = [INDEP, DEP]
    for subkey in subkeys:
        for k, v in row[subkey].items():
            if v is None:
                continue
            if np.ndim(v) > 1:
                assert np.ndim(v) == 2
                if 1 not in np.shape(v):
                    assert isinstance(k, variable.Variable)
                    assert k.components is not None
                    assert len(k.components) in np.shape(v)

def scalarise(dct):
    ''' Convert any size-1 arrays to scalars '''
    d = dct.copy()
    for subkey in [DEP, INDEP]:
        for k, v in d[subkey].items():
            if isinstance(v, np.ndarray) and np.size(v) == 1:
                dct[subkey][k] = v.item()

def check_objects(row):
    subkeys = [INDEP, DEP]
    for subkey in subkeys:
        for k, v in row[subkey].items():
            if isinstance(v, np.ndarray):
                if v.dtype == 'O': # Object
                    if settings.NO_OBJECT_ARRAYS:  
                        raise ValueError("Input for variable '" + k +
                            "' is an object array." +
                            " Check each row is the same shape.")
                    elif settings.FORCE_OBJECTS_TO_FLOATS:
                        row[subkey][k] = v.astype(np.float64)


class Box(list):
    ''' A versatile container to manage and work with result data 
    
    The box class inherits from list. It's structured as a list of 
    dictionaries, each with three sub-dictionaries: an index, 
    a dictionary of independent variable values, and a dictionary of dependent
    variable values.
    
    Args:
        lst (list): Optional data to initially populate the Box instance.
    '''
    def __init__(self, lst=None):
        self._combined = {}
        if lst is not None:
            super().__init__(lst)
            for row in lst:
                self._combine(row)
        
    def add(self, indep, key=None, value=None, dep=None,
            keys=None, values=None, **kwargs):
        ''' Add a new entry 
        
        Args:
            indep (dict): A dictionary of independent values. The keys may
            be strings, but it is recommended to use Variable instances.
            key (Variable): A Variable instance (or string). Optional.
            value: The data belonging to that variable. Optional.
            dep (dict): A dictionary of Variable-value pairs for dependent
            data.
            keys (list[Variable]): A list of Variables
            values (array-like): A corresponding array of values, in which
            the number of elements in one dimension matches the number of keys.
            kwargs: Optional Variable-value pairs specified as keyword
            arguments.            
        '''
        if key is not None and value is not None:
            if isinstance(key, str):
                self.add_value(indep, key, value)
            elif isinstance(key, list):
                self.add_array(indep, key, value)
        elif keys is not None and values is not None:
            self.add_array(indep, keys, values)
        elif dep is not None:
            self.add_dict(indep, dep)
        elif isinstance(key, dict):
            self.add_dict(indep, key)
        elif len(kwargs) > 0:
            self.add_dict(indep, kwargs)
        
    def add_value(self, indep, key, value):
        ''' Add a single value or vector 
        
        Args:
            indep (dict): A dictionary of independent values. The keys may
            be strings, but it is recommended to use Variable instances.
            key (Variable): A Variable instance (or string). Optional.
            value: The data belonging to that variable. Optional.
        '''
        self.add_dict(indep, {key: value})
        
    def add_dict(self, indep, dep):
        ''' Add a dictionary of dependent data
        
        Args:
            indep (dict): A dictionary of independent values. The keys may
            be strings, but it is recommended to use Variable instances.
            dep (dict): A dictionary of Variable-value pairs for dependent
            data.
        '''
        dfull = {IND: len(self),
                 INDEP: indep.copy(),
                 DEP: dep}
        validate_row(dfull)
        check_objects(dfull)
        if settings.CONVERT_SCALAR_ARRAYS:
            scalarise(dfull)
        if settings.PRINT_UPDATES:
            print(self.show([dfull]))
        self.append(dfull)
        self._combine(dfull)
        
    def add_array(self, indep, keys, values):
        ''' Add an array of values 
        
        Args:
            indep (dict): A dictionary of independent key-value pairs
            keys (list): A list of keys
            values (array-like): The values. Rows must correspond with the keys.
        '''
        if np.ndim(values) > 1:
            values = orient(values, keys)
        dep = {k: v for k, v in zip(keys, values)}
        self.add_dict(indep, dep)
        
    def filter(self, keys, lst=None):
        ''' Return a generator for entries that all include the keys
        
        Args:
            keys (list[Variable]): The keys that all entries must include
            lst (list): An optional list to filter instead of the Box.
            
        Returns:
            list: A generator for the filtered entries
        '''
        if lst is None:
            lst = self
        if DEP in lst[0] and INDEP in lst[0]:
            filt_dep = True
        else:
            filt_dep = False
            
        def filt_func(d):
            if filt_dep:
                return all([k in d[INDEP] or k in d[DEP]
                            for k in listify(keys)])
            else:
                return all([k in d for k in listify(keys)])
            
        return filter(filt_func, lst)
    
    def filtered(self, keys, lst=None):
        ''' Return a list of entries that all include the keys
        
        Args:
            keys (list[Variable]): The keys that all entries must include
            lst (list): An optional list to filter instead of the Box.
            
        Returns:
            list: The filtered entries
        '''
        lst = self if lst is None else lst
        if len(lst) == 0:
            raise ValueError('No rows in list')
        return [row for row in self.filter(keys, lst)]
    
    def iwhere(self, dct=None, lst=None, **kwargs):
        ''' Return a generator for entries that all contain key-value pairs
        
        Args:
            dct (dict): The key-value pairs that each entry must contain
            lst (list): An optional list to filter instead of the Box.
            
        Returns:
            list: A generator for the filtered entries
        '''
        dct = {} if dct is None else dct
        m = dct.copy()
        m.update(kwargs)
        if lst is None:
            lst = self
        if DEP in lst[0] and INDEP in lst[0]:
            filt_dep = True
        else:
            filt_dep = False
            
        def filt_func(d):
            if filt_dep:
                return all([v == d[INDEP].get(k, d[DEP].get(k, None))
                            for k, v in m.items()])
            else:
                return all([v == d.get(k, None) for k, v in m.items()])
            
        return filter(filt_func, lst)
    
    def where(self, dct=None, lst=None, **kwargs):
        ''' Return a list of entries that all contain key-value pairs
        
        Args:
            dct (dict): The key-value pairs that each entry must contain
            lst (list): An optional list to filter instead of the Box.
            
        Returns:
            list: A generator for the filtered entries
        '''
        return [row for row in self.iwhere(dct, lst, **kwargs)]
    
    def minimal(self):
        ''' A minimal list of data in the Box 
        
        Returns:
            list: A list of dictionaries. Each dictionary combines
            independent and dependent entries.
        '''
        combined = self._combined
        out = []
        for k, d in combined.items():
            dct = d[INDEP].copy()
            dct.update(d[DEP])
            out.append(dct)
        return out
    
    def exclusively(self, keys, lst=None):
        ''' Return a list of dictionaries that only contain values for keys '''
        minimal = self.minimal() if lst is None else lst
        return [{k: d[k] for k in keys} for d in minimal]
    
    def _combine(self, dct):
        d = self._combined
        independent = dct[INDEP]
        h = hash_dict(independent)
        if h not in d:
            d[h] = {INDEP: independent.copy(), DEP: {}}
        d[h][DEP].update(dct[DEP])
    
    def combined(self):
        ''' List Box data, merging rows with common independent values 
        
        Returns:
            list: A list of the merged data in the Box.
        '''
        d = self._combined
        return [c for key, c in d.items()]
    
    def _merge(self, box_list):
        ''' Perform a merge operation '''
        if isinstance(box_list, self.__class__):
            box_list = [box_list]
        for box in box_list:
            for row in box:
                row[IND] = len(self)
                self.append(row)
                self._combine(row)
    
    def merge(self, box, in_place=True):
        ''' Merge this Box with one or more other Box instances 
        
        Args:
            box (Box): A Box instance of list of Box instances.
            in_place(bool): Either merge in place or return a new Box.
        '''
        if in_place:
            self._merge(box)
        else:
            base = self.copy()
            base._merge(box)
            return base
    
    def vectors(self, keys, dct=None, labels='str', combine=True,
                indep_keys=None):
        ''' List the dependent data for each key where all keys are present
        
        Args:
            keys (list[Variable]): The list of keys to return values for.
            dct (dict): A dictionary of key-value pairs that must be 
            present in all rows.
            labels (str): 'str' to return labels as strings, or 'dict' to
            return labels as dictionaries of key-value pairs. Use None or 
            False to not return labels.
            combine (bool): True (default) to combine box rows that have
            the same set of independent variables
            indep_keys (list): Optional. If given, labels are not returned. 
            Instead, corresponding vectors for each independent key are
            returned within the return tuple (after those for keys).
            
        Returns:
            tuple[list]: A list for each key, plus a list of labels if 
            labels is not False or None.
        
        Note:
            This method operates on the combined data. All keys must be present
            in a given index for the data from that index to be counted.
        '''
        keys = listify(keys)
        combined = self.combined() if combine else self
        filtered = self.filtered(keys, lst=combined)
        labels = 'dict' if indep_keys is not None else labels
        if dct is not None:
            filtered = self.where(dct, filtered)
        out = {k: [] for k in keys}
        label_list = []
        for dct in filtered:
            indep = dct[INDEP]
            if labels=='str':
                label = dict_to_str(indep, val_sep='=', key_sep=', ')
            else:
                label = indep
            label_list.append(label)
            dep = dct[DEP]
            for k in keys:
                out[k].append(dep[k])
        lst_out = [out[k] for k in keys]
        if labels is not None and labels is not False:
            if indep_keys is None:
                lst_out.append(label_list)
            else:
                for k in indep_keys:
                    lst_out.append([d[k] for d in label_list])
        return tuple(lst_out)
    
    def grouped(self, keys, labels='dict', as_dicts=False):
        ''' Return lists of values grouped by other independent variables '''
        
        # TODO: This seems method unnecessarily complex
        
        combined = self.combined()
        filtered = self.filtered(keys, lst=combined)
        out = {}
        for dct in filtered:
            d_labels = dct[INDEP].copy()
            d = {}
            keys_copy = keys.copy()
            for k in keys:
                if k in d_labels:
                    d[k] = d_labels.pop(k)
                elif k in dct[DEP]:
                    d[k] = dct[DEP][k]
            hsh = hash_dict(d_labels)
            if hsh not in out:
                f_labels = dict_to_str(d_labels) if labels=='str' else d_labels
                out[hsh] = {'labels': f_labels,
                            'values': {k: [] for k in keys_copy}}
            d_values = out[hsh]['values']
            for k in keys_copy:
                d_values[k].append(d[k])
        if as_dicts:
            return list(out.values())
        else:
            lst = []
            for group in out.values():
                row = [v for v in group['values'].values()]
                row.append(group['labels'])
                lst.append(row)
            return lst
    
    def find(self, key, lst=None):
        ''' Return a dictionary of values for the key, by index 
        
        Args:
            key (Variable): The key to find values for
            lst (list): The list to search, if not this Box.
            
        Returns:
            dict: A dictionary of values, where keys are the indexes.
        '''
        lst = self if lst is None else lst
        out = {}
        for row in lst:
            if key in row[DEP]:
                out[row[IND]] = row[DEP][key]
            elif key in row[INDEP]:
                out[row[IND]] = row[INDEP][key]
        return out
    
    def unique(self, key, lst=None):
        ''' Return unique key values 
        
        Args:
            key (Variable): The key
            lst (list): An optional list to use instead of self
            
        Returns:
            list: A list of unique values
        '''
        d = self.find(key, lst)
        vals = set(d.values())
        return sorted(list(vals))
    
    def combinations(self, key_list, lst=None):
        ''' Return unique combinations of keys in the box 
        
        Args:
            key_list (list[Variable]): A list of variables
            
        Returns:
            list: A list of dictionaries, where each dictionary is a unique
            combination of the keys
        '''
        lst = self.filtered(key_list, lst)
        tups = [tuple([d[INDEP].get(k, d[DEP].get(k)) for k in key_list])
                    for d in lst]
        s = set(tups)
        l = list(s)
        l.sort()
        return [{k: v for k, v in zip(key_list, vals)} for vals in l]
    
    def item(self, index, key):
        ''' Return the value for a key at a given index '''
        row = self[index]
        if key in row[DEP]:
            return row[DEP][key]
        elif key in row[INDEP]:
            return row[INDEP][key]
        else:
            raise KeyError
    
    def __getitem__(self, keys):
        ''' Allow easier access to data '''
        if isinstance(keys, int):
            return super().__getitem__(keys)
        elif isinstance(keys, list):
            return self.vectors(keys)
        elif isinstance(keys, str):
            return self.find(keys)
        elif isinstance(keys, tuple):
            return self.item(keys[0], keys[1])
        elif isinstance(keys, slice):
            return super().__getitem__(keys)
    
    def copy(self):
        return Box(deepcopy(self))
    
    def copy_shallow(self):
        return Box(self)
        
    def show(self, lst=None):
        ''' Format box contents in a concise way '''
        def f(v):
            if np.size(v) == 1:
                return str(v)
            elif np.size(v) > 3:
                return str(np.shape(v))
            elif np.ndim(v) > 1:
                return str(np.shape(v))
            else:
                return str(v)
        
        def buffer(l, m, n=25):
            end = len(l) - 1
            buffered = []
            for i in range(m):
                if i > end:
                    buffered.append(''.ljust(n))
                else:
                    buffered.append(l[i].ljust(n))
            return buffered
        
        lst = self if lst is None else lst
        out = [IND.ljust(7) +
               INDEP.ljust(60) +
               DEP.ljust(60)]
        for row in lst:
            ind = [str(row[IND])]
            dep = [k + ': ' + f(v) for k, v in row[DEP].items()]
            indep = [k + ': ' + f(v) for k, v in row[INDEP].items()]
            m = max(len(dep), len(indep), 1)
            ind = buffer(ind, m, 7)
            dep = buffer(dep, m, 60)
            indep = buffer(indep, m, 60)
            for a, b, c in zip(ind, indep, dep):
                out.append(a + b + c)
            out.append('')
        return '\n'.join(out)
    
    def __str__(self):
        return self.show()
    
    def __repr__(self):
        return self.show()
    
    def keys(self, dependent=True, independent=False):
        ''' Return a set of the keys in the Box 
        
        Args:
            dependent (bool): Include the dependent keys
            independent (bool): Include the independent keys
            
        Returns:
            set: The keys present in the box
        '''
        out = set()
        for row in self:
            if independent:
                out.update(row[INDEP].keys())
            if dependent:
                out.update(row[DEP].keys())
        return out
        
    