# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:52:34 2019

@author: Reuben

Adapters in this module transform data structures between different formats.

"""

SEP = '/'
IND = '_item_'
KEY = '_key_'

from .variable import Variable
from .utils import safe_fname

def rep_slash(k):
    return k.replace('/', '.per.')

def rev_slash(k):
    if isinstance(k, str):
        return k.replace('.per.', '/')
    return k

def flat_dict(obj, out=None, root=None, sep=SEP):
    out = {} if out is None else out
    if isinstance(obj, dict):
        _flat_dict(obj, out=out, root=root, sep=sep)
    elif isinstance(obj, list):
        _flat_list(obj, out=out, root=root, sep=sep)
    else:
        out[root] = obj
    return out

def _flat_dict(dct, out=None, root=None, sep=SEP):
    base = '' if root is None else str(root) + sep
    out = {} if out is None else out
    for k, v in dct.items():
        new_root = base + KEY + rep_slash(k)
        flat_dict(v, out=out, root=new_root, sep=sep)

def _flat_list(lst, out=None, root=None, sep=SEP):
    base = '' if root is None else str(root) + sep
    out = {} if out is None else out
    for i, v in enumerate(lst):
        new_root = base + IND + str(i)
        flat_dict(v, out=out, root=new_root, sep=sep)
    

def compose(flat, root=None, reverse_keys=None, val=None, sep=SEP):
    if root is None:
        k, v = flat.copy().popitem()
        keys = k.split(sep)
        _, is_dict = _interpret(keys[0])
        root = {} if is_dict else []
    for k, v in flat.items():
        reverse_keys = k.split(sep)
        reverse_keys.reverse()
        _assign(root, reverse_keys, v)
    return root

def _assign(current, reverse_keys, val):
    key = reverse_keys.pop()
    k, is_dict = _interpret(key)
    if len(reverse_keys) == 0:
        _safe_assign(current, k, val)
        return
    next_k, should_be_in_dict = _interpret(reverse_keys[-1])
    new_obj = {} if should_be_in_dict else []
    new_current = _safe_assign(current, k, new_obj)
    _assign(new_current, reverse_keys, val)

def _interpret(key):
    if key.startswith(KEY):
        is_dict = True
        new = key.lstrip(KEY)
    elif key.startswith(IND):
        is_dict = False
        new = int(key.lstrip(IND))
    return rev_slash(new), is_dict
    
def _safe_assign(obj, key, new_obj):
    if isinstance(obj, dict):
        if key not in obj:
            obj[key] = new_obj
    else:
        # it's a list
        if key >= len(obj):
            obj += [None]*(key - len(obj) + 1)
        if obj[key] is None:
            obj[key] = new_obj
    return obj[key]

