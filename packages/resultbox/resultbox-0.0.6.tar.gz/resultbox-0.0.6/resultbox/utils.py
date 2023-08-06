# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 08:24:09 2019

@author: Reuben

A module of handy utility functions used elsewhere within resultbox.

"""

import numpy as np
from scipy.interpolate import interp1d


def listify(obj):
    ''' Put an object into a list if it isn't already a list '''
    if not isinstance(obj, list):
        return [obj]
    else:
        return obj

def cosort(xs, ys, min_diff=0):
    ''' Sort x and y vectors into monotonic increasing order of x
    
    Args:
        xs (vector-like): The x values
        ys (vector-like): The y values
        min_diff (float, int): The minimum step by which x must always increase
    
    Note:
        Some values may be omitted in cases where x is not monotonically
        increasing. The point is to return vectors that can be used for 
        interpolation without any problems.
    
    See: https://stackoverflow.com/questions/11851770/spline-interpolation-with-python
    '''
    # Combine lists into list of tuples
    tups = zip(xs, ys)
    
    # Sort list of tuples by x-value
    tups = sorted(tups, key=lambda tup: tup[0])
    if min_diff is not None:
        tups = deduplicate_xs(tups, min_diff=min_diff)
    # Split list of tuples into two list of x values any y values
    xs_sorted, ys_sorted = zip(*tups)
    if isinstance(xs, np.ndarray):
        return np.array(xs_sorted), np.array(ys_sorted)
    elif isinstance(xs, list):
        return list(xs_sorted), list(ys_sorted)
    else:
        return xs_sorted, ys_sorted


def deduplicate_xs(tups, min_diff=0):
    ''' Remove duplicate xs
    
    Args:
        tups (list[tuple]): A sorted list of x, y pairs from :func:`utils.cosort`
        min_diff (float, int): The minimum step by which x must always increase.
        Defaults to 0.
    
    Args:
        tups: Sorted list of tuples of values
        min_diff: Minimum difference between x values
    
    See https://www.geeksforgeeks.org/python-remove-tuples-having-duplicate-first-value-from-given-list-of-tuples/
    '''
    m = tups[0][0] - min_diff - 1
    out = []
    for t in tups:
        if t[0] > (m + min_diff):
            out.append(t)
        m = t[0]
    return out

def orient(arr, n, axis='rows'):
    ''' Orient a 2D array so that it has n rows or columns
    
    Args:
        arr (array-like): The array
        n (int, list): The number of rows for the desired output. Must equal the
        length of one array axis. Or a list of elements.
    
    Returns:
        ndarray: The oriented array. It behaves as a list.
    '''
    a = np.atleast_2d(arr)
    ax = None
    n = len(n) if isinstance(n, list) else n
    for i in range(2):
        if a.shape[i] == n:
            ax = i
    if ax is None:
        raise ValueError('Neither dimension in arr has ' + str(n) + ' elements.')
    if (axis == 'rows' and ax == 0) or (axis != 'rows' and ax == 1):
        ret = a
    else:
        ret = a.T
    if isinstance(arr, list):
        return ret.tolist()
    else:
        return ret

def unpack(arr, labels):
    ''' Unpack a 2D array correctly regardless of its orientation 
    
    Args:
        arr (array-like): The array
        labels (list, int): The labels for each vector, or an integer for
        the number of labels.
        
    Returns:
        list: A list of vectors.
    '''
    return [v for v in orient(arr, labels, axis='rows')]

def _interp_1D(xs, ys, new_xs, min_diff=1e-4, bounds_error=False, 
           fill_value=np.nan, **kwargs):
    ''' Return interpolated values for 1D array '''
    xs, ys = cosort(xs, ys, min_diff=min_diff)
    if fill_value == 'bounds':
        fill_value = (ys[0], ys[-1])
    f = interp1d(xs, ys, bounds_error=bounds_error, fill_value=fill_value,
                 **kwargs)
    return f(new_xs)    

def interp(xs, ys, new_xs, min_diff=1e-4, bounds_error=False, 
           fill_value=np.nan, **kwargs):
    ''' Interpolate an array based on a matching vector and target vector 
    
    Args:
        xs (vector-like): A 1D array or list of x values
        ys (array-like): A 1D or 2D array of y values, which matches xs in
        one dimension. 
        new_xs (vector_like): The desired output x values.
        min_diff (float): The minimum positive difference between adjacent
        x values to use during interpolation.
        bounds_error: As per scipy interp1d.
        fill_value: As per scipy interp1d.
        kwargs: Other keyword arguments to pass to scipy interp1d.
        
    Note:
        This function uses scipy's interp1d to perform the interpolation.
    '''
    n = np.ndim(ys)
    xs = xs.flatten() if isinstance(xs, np.ndarray) else xs
    if n == 1:
        return _interp_1D(xs, ys, new_xs, min_diff, bounds_error, fill_value,
                          **kwargs)
    elif n == 2:
        a = orient(ys, len(xs), 'cols')
        out = [_interp_1D(xs, row, new_xs, min_diff, bounds_error, fill_value,
                          **kwargs) for row in a]
        out = np.array(out) if isinstance(ys, np.ndarray) else out
        return out
    raise ValueError('ys must have 1 or 2 dimensions')
            
def list_to_str(lst, length=18, sep=' ', brackets=True):
    ''' Convert a list of values to a nice-to-look-at string 
    
    Args:
        lst (list): A list of values
        length (int): The maximum length of the output string. The string
        is truncated at this length if the list length is above 3.
        sep (str): The separator to use between values
        brakets (bool): True to add square brackets around the list.
    
    Returns:
        str: The string.
    '''
    l = [val_to_str(num) for num in lst]
    s = sep.join(l)
    if len(s) > length and len(lst) > 3:
        s = s[:length] + '...'
    if brackets:
        return '[' + s + ']'
    else:
        return s

def vec_to_str(num, precision=3, list_sep=' '):
    format_str = '{:0.' + str(precision) + 'g}'
    if isinstance(num, list):
        return list_to_str(num, sep=list_sep)
    elif isinstance(num, np.ndarray):
        if num.size == 1:
            return format_str.format(num.item())
        else:
            return list_to_str(num.flatten().tolist())

def val_to_str(num, precision=3, list_sep=' ', length=18):
    ''' Format a single number as a nice-to-look-at string 
    
    Args:
        num: The number
        precision (int): The precision of the output string
        
    Returns:
        str: The formatted number
    '''
    format_str = '{:0.' + str(precision) + 'g}'
    if num is None:
        return 'None'
    if isinstance(num, str):
        return num
    elif isinstance(num, int):
        return str(num)
    elif isinstance(num, float):
        return format_str.format(num)
    elif isinstance(num, list):
        return list_to_str(num, sep=list_sep, length=length)
    elif isinstance(num, dict):
        return dict_to_str(num, list_sep=list_sep, length=length)
    elif isinstance(num, np.ndarray):
        return vec_to_str(num, precision=precision, list_sep=list_sep)
    else:
        return str(num)
        
def dict_to_str(dct, val_sep=' ', key_sep=' ', list_sep=',', length=18):
    ''' Convert a dict to a nice-to-look-at string 
    
    Args:
        dct (dict): The dictionary
        val_sep (str): The separator between a key and it's value.
        key_sep (str): The separator between different key-value pairs.
        list_sep (str): The separator between list entries
    
    Returns:
        str: The formatted string
    '''
    lst = []
    for key, val in dct.items():
        s = str(key) + val_sep + val_to_str(val, list_sep=list_sep,
               length=length)
        lst.append(s)
    return key_sep.join(lst)

def str_to_dict(string, val_sep='=', key_sep=';', list_sep=','):
    ''' Convert a string of key value pairs to a dictionary 
    
    Args:
        string (str): The string
        val_sep (str): The separator between a key and its value
        key_sep (str): The separator between key-value pairs.
        list_sep (str): The separator between list entries
    
    Returns:
        dict: A new dictionary
    '''
    def make_list(s):
        s = s.strip('[]')
        lst = s.split(list_sep)
        return [interpret(item) for item in lst]
    
    def interpret(val):
        if val=='None':
            return None
        elif val.startswith('['):
            return make_list(val)
        elif val.isdigit():
            return int(val)
        elif val.isnumeric():
            return float(val)
        return val
    
    pairs = [s.split(val_sep) for s in string.split(key_sep)]
    return {p[0]: interpret(p[1]) for p in pairs}

def strip_unit(s):
    ''' Removes units within square brakets from file names 
    
    Args:
        s (str): A string
        
    Returns:
        str: The string without anything enclosed in square brackets.
    
    Note:
        Useful for removing units in a key. It will recurse pairs of brackets.
        Trailing spaces will be striped.
    '''
    start = s.find('[')
    end = s.find(']')
    if start > 0 and end > 0:
        s = s[:start].rstrip() + s[end+1:].rstrip()
    if '[' in s:
        s = strip_unit(s)
    return s

def safe_fname(fname):
    ''' Change a string if needed to make it a valid file name 
    
    Args:
        fname (str): The candidate file name
        
    Returns:
        str: The safe file name.
    
    TODO:
        This needs work.
    '''
    fname = strip_unit(fname)
    return fname

def ensure_ext(fname, ext):
    ''' Edit a string if needed to ensure it has a particular extension 
    
    Args:
        fname (str): The file name
        ext (str): The extension
        
    Returns:
        str: The file name with the desired extension (without duplication of
        the extension).
    '''
    ext = ext if ext.startswith('.') else '.' + ext
    if fname.endswith(ext):
        return fname
    else:
        return fname + ext