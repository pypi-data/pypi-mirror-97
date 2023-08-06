# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:12:24 2019

@author: Reuben
"""

import os
import hashlib
import pandas as pd
from collections import defaultdict
from . import utils
from . import variable
import numpy as np
from . import constants
import warnings

def encoded(obj):
    if isinstance(obj, str):
        return bytes(obj, 'utf-8')
    return bytes(obj)

def safe_hash(lst):
    h = hashlib.md5()
    for obj in lst:
        h.update(encoded(obj))
    return h.digest()
    
def listify(obj):
    if obj is None:
        return []
    if not isinstance(obj, list):
        return [obj]
    return obj

def _custom_headed_table(df, fname, sep=',', **kwargs):
    ''' CSV table with label for columns index '''
    def pad(s, n):
        out = [str(a) for a in s] if isinstance(s, list) else [str(s)]
        for i in range(n-1):
            out.append('')
        return out
    
    cols = [str(c) for c in df.columns]    
    if isinstance(df.index, pd.MultiIndex):
        n = len(df.index.levels)
        header_2 = pad(df.index.names, n + len(cols))
    else:
        n = 1
        ind_name_str = '' if df.index.name is None else df.index.name
        header_2 = pad(ind_name_str, n + len(cols))
    col_name_str = '' if df.columns.name is None else df.columns.name
    header_1 = pad(col_name_str, n) + cols
    s = sep.join(header_1) + '\n' + sep.join(header_2) + '\n'
    with open(fname, mode='a') as f:
        f.write(s)
    df.to_csv(path_or_buf=fname, sep=sep, header=None, mode='a', **kwargs)

def to_csv(df, fname, variable=None, mode='w', sep=',', **kwargs):
    if df is None:
        return
    fname = utils.safe_fname(fname)
    fname = utils.ensure_ext(fname, '.csv')
    s = '\n\n' if mode=='a' else ''
    if variable is not None:
        if isinstance(variable, (list, tuple)):
            for v in variable:
                s += v + '\n' + v.doc + '\n\n'
        else:
            s += variable + '\n' + variable.doc + '\n\n'
    with open(fname, mode=mode) as f:
        f.write(s)
    if isinstance(df.columns, pd.MultiIndex):
        # Default behaviour is OK
        df.to_csv(fname, sep=sep, mode='a', **kwargs)
    else:
        # Need some extra to print columns label
        _custom_headed_table(df, fname, sep=sep, **kwargs)
    return True

class Table():
    pass



class Tabulator():
    def guess_index(self, box, values, columns=None):
        all_keys = self.all_keys(values, columns)
        filtered = box.filtered(all_keys, box.combined())
        index = {}
        for row in filtered:
            keys = row[constants.INDEP].keys()
            for k in keys:
                if k not in index.values():
                    index[len(index)] = k
        for k, v in index.copy().items():
            if v in all_keys:
                del index[k]
        return list(index.values())
    
    def all_keys(self, *args):
        out = []
        for arg in args:
            l = listify(arg)
            out.extend([a for a in l if not a.endswith(':')])
        return out
    
    def merge_keys(self, *args):
        return [k for ks in args for k in listify(ks)]
    
    def _prepare_data(self, box, base_keys, store=None):
        keys = self.all_keys(base_keys)
        minimal = box.minimal()
        if store is not None:
            keys_to_expand = self.get_keys_to_expand(base_keys, store)
            minimal = variable.expand(minimal, store, specified=keys_to_expand)
            for k in keys_to_expand:
                keys.remove(k)
                keys.extend(store[k].subkeys)
        filtered = box.filtered(keys, minimal)
        filtered = box.exclusively(keys, filtered)
        if len(filtered) == 0:
            raise ValueError('No records left in filtered results.')
        return filtered
    
    def get_keys_to_expand(self, keys, store):
        labels = []
        for k in keys:
            if k.endswith(':'):
                name = k.rstrip(':')
                for var in store.values():
                    if var.name == name:
                        labels.append(var)
        return labels
    
    def _vec_to_str(self, filtered, protected):
        for row in filtered:
            for k, v in row.copy().items():
                if k in protected:
                    continue
                if isinstance(v, (np.ndarray, list)):
                    row[k] = utils.vec_to_str(v)
    
    def _regenerate_key_in_columns(self, var, df):
        cols = list(df.columns)
        for i, c in enumerate(cols):
            if c == var.name:
                cols[i] = var.key
        df.columns = cols
   
    def tabulate(self, box, values, columns=None, index=None, aggfunc='mean',
                 aliases=None, store=None):
        ''' General purpose tabulation
        
        Can handle mixtures of scalars and vectors
        '''
        def indices(d):
            m = 1
            for key, val in d.items():
                if isinstance(val, list):
                    m = max(m, len(val))
            return range(m)
        index = self.guess_index(box, values, columns) if index is None else index
        columns = [] if columns is None else columns
        base_keys = self.merge_keys(values, columns, index)
        filtered = self._prepare_data(box, base_keys, store)
        if aliases is not None:
            filtered = aliases.translate(filtered)
            values = aliases.translate(values)
            index = aliases.translate(index)
            columns = aliases.translate(columns)
        # Use dataframes for 'rows' to handle vectors
        if store is not None:
            keys_to_expand = self.get_keys_to_expand(base_keys, store)
            protected = keys_to_expand + listify(values)
            self._vec_to_str(filtered, protected=protected)
        if store is not None and len(keys_to_expand) > 0:
            df = pd.DataFrame(filtered)
            df["id"] = df.index
            pd.set_option('display.max_columns', 30)
            for e in keys_to_expand:
                df = pd.wide_to_long(df, stubnames=e.name, i='id', j=e.label,
                                      sep=e.sep, suffix='.*')
                self._regenerate_key_in_columns(e, df)
        else:
            rows = [pd.DataFrame(row, index=indices(row)) for row in filtered]
            df = rows[0].copy()
            for row in rows[1:]:
                df = df.append(row, sort=True)
            df = df.reset_index(drop=True)
        # pd.set_option('display.max_columns', 5)
        # print(df)
        try:
            df = pd.pivot_table(df, values=values, index=index, columns=columns,
                                aggfunc=aggfunc)
            self._order_index(df, listify(index))
            self._order_columns(df, listify(columns))
        except Exception as e:
            msg = 'Could not tabulate data. '
            dct = {'values': values, 'index': index, 'columns': columns}
            msg2 = utils.dict_to_str(dct, val_sep=' = ', key_sep='\n       ',
                                     list_sep=', ', length=250)
            raise ValueError(msg + '(' + e.args[0] + ').\n       ' + msg2)
        return df

    def _order_index(self, df, index):
        if isinstance(df.index, pd.MultiIndex):
            try:
                df.index = df.index.reorder_levels(index)
            except:
                pass
            
    def _order_columns(self, df, columns):
        if isinstance(df.columns, pd.MultiIndex):
            try:
                df.columns = df.columns.reorder_levels(columns)
            except:
                pass

    def _remove_unused_levels(self, df):
        for index in [df.index, df.columns]:
            if isinstance(index, pd.MultiIndex):
                index.remove_unused_levels()

    def _unfold_3D(self, arr, labels, label, components):
        ''' Unfold a 3D array into a 2D array 
        
        Used for vector tables in which each value is a 2D array
        '''
        def add(d, k, v):
            d2 = d.copy()
            d2.update({k: v})
            return d2
        arr2 = [np.squeeze(v) for row in arr for v in row]
        labels2 = [add(d, label, c) for d in labels for c in components]
        return arr2, labels2

    def _make_spanning_index(self, index_list, step=None, n=None):
        if len(index_list) == 0:
            return None
        test = index_list[0]
        are_all_the_same = True
        for index in index_list[1:]:
            are_all_the_same = np.array_equal(test, index)
            if not are_all_the_same:
                break
            test = index
        if are_all_the_same:
            return index_list[0]
        minimum = np.min([np.min(index) for index in index_list])
        maximum = np.max([np.max(index) for index in index_list])
        if n is None:
            step = index_list[0][1] - index_list[0][0] if step is None else step
            ret = np.arange(minimum, maximum + step, step)
        else:
            ret = np.linspace(minimum, maximum, n)
        return ret

    def vector_table(self, box, values, index, index_vals=None, orient='rows',
                     components=None, combine=True, step=None, n=None):
        ''' A table of vectors with an interpolated index
        
        Args:
            box (Box): The box of data
            values (str): The key for the values. If the values are 2D,
            components must also be specified.
            index (str): The key for the index (vector-wise)
            index_vals (list-like): The index values for the vector
            orient (str): The direction of the vectors. Defaults to 'rows'
            and can be set to 'cols'.
            components (list[str]): A list of component names. Only required
            if the values are 2D. If the 'values' is a Variable, this can
            be omitted.
            combine (bool): Combine entries with the same values of independent
            variables (defaults to True).
            step (float): An optional step size for the index.
            n (int): An optional number of values for the index.
            
        Note:
            Headings are automatically created.
        '''
        values_list, index_list, labels = box.vectors([values, index],
                                                      labels='dict',
                                                      combine=combine)
        
        labels = [{k: str(v) for k, v in label.items()} for label in labels]
        interp_list = []
        if index_vals is None:
            index_vals = self._make_spanning_index(index_list, step=step, n=n)
        else:
            index_vals = np.squeeze(index_vals)
        for vec, ind_vec in zip(values_list, index_list):
            v = np.squeeze(vec)
            ind_v = np.squeeze(ind_vec)
            interpolated = utils.interp(ind_v, v, index_vals)
            interp_list.append(interpolated)
        if np.ndim(interp_list) == 3:
            if isinstance(values, variable.Variable):
                lab = values.label 
                components = [values._append_unit(c, values.unit) 
                                for c in values.components]
            else:
                lab = values + ':'
            interp_list, labels = self._unfold_3D(interp_list, labels,
                          lab, components)
        ind_df = pd.DataFrame(labels)
        ind = pd.MultiIndex.from_frame(ind_df)
        ind_vars = list(labels[0].keys())
        if orient=='rows':
            df = pd.DataFrame(np.array(interp_list).T, index=index_vals, columns=ind)
            df = df.rename_axis(index, axis=0)
            self._order_columns(df, ind_vars)
        else:
            df = pd.DataFrame(interp_list, index=ind, columns=index_vals)
            df = df.rename_axis(index, axis=1)
            self._order_index(df, ind_vars)
        return df
    
    
tabulator = Tabulator()
vector_table = tabulator.vector_table
tabulate = tabulator.tabulate

