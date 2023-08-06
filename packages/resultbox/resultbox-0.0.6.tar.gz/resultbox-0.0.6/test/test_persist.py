# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:44:10 2019

@author: Reuben
"""

import unittest
import tempfile
import os
import numpy as np

from resultbox import Box, load, save, Store, Variable
from resultbox import persist

def get_lst():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1, 'c': 1}, 'dependent': {'d': 11}},
           {'index': 1, 'independent': {'a': 1, 'b': 2, 'c': 2}, 'dependent': {'d': 12}},
           {'index': 2, 'independent': {'a': 1, 'b': 2, 'c': 1}, 'dependent': {'d': 13}},
           {'index': 3, 'independent': {'a': 1, 'b': 1, 'c': 2}, 'dependent': {'d': 14}},
           {'index': 4, 'independent': {'a': 2, 'b': 1, 'c': 1}, 'dependent': {'d': 15}},
           {'index': 5, 'independent': {'a': 2, 'b': 1, 'c': 2}, 'dependent': {'d': 16}},
           {'index': 6, 'independent': {'a': 2, 'b': 2, 'c': 1}, 'dependent': {'d': 17}},
           {'index': 7, 'independent': {'a': 2, 'b': 2, 'c': 2}, 'dependent': {'d': 18}}]
    return lst

def get_lst_2():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1, 'c': 1}, 'dependent': {'d': np.array([0, 10])}},
           {'index': 1, 'independent': {'a': 1, 'b': 2, 'c': 2}, 'dependent': {'d': np.array([1, 11])}},
           {'index': 2, 'independent': {'a': 1, 'b': 2, 'c': 1}, 'dependent': {'d': np.array([2, 12])}},
           {'index': 3, 'independent': {'a': 1, 'b': 1, 'c': 2}, 'dependent': {'d': np.array([3, 13])}},
           {'index': 4, 'independent': {'a': 2, 'b': 1, 'c': 1}, 'dependent': {'d': np.array([4, 14])}},
           {'index': 5, 'independent': {'a': 2, 'b': 1, 'c': 2}, 'dependent': {'d': np.array([5, 15])}},
           {'index': 6, 'independent': {'a': 2, 'b': 2, 'c': 1}, 'dependent': {'d': np.array([6, 16])}},
           {'index': 7, 'independent': {'a': 2, 'b': 2, 'c': 2}, 'dependent': {'d': np.array([7, 17])}}]
    return lst

def get_box_check(box, fname):
    with tempfile.TemporaryDirectory() as tmpdirname:
        fname = os.path.join(tmpdirname, fname)
        save(box, fname)
        box_check = load(fname)
    return box_check
            

class Test_Packing(unittest.TestCase):
    def test_serialise_vars(self):
        store = Store()
        v1 = store.add('a', 'docstring_1', 'mm')
        v2 = store.add('b', 'docstring_2', 'm/s')
        lst = [{'index': 0,
                'independent': {v1: 1, v2: 2},
                'dependent': {v1: 5, v2: 7}}]
        b = Box(lst)
        res = persist.serialise_vars(b)
        expected = ['name=a;doc=docstring_1;unit=mm;components=None;sep= - ;category=None;tags=None;identifier=None',
                    'name=b;doc=docstring_2;unit=m/s;components=None;sep= - ;category=None;tags=None;identifier=None']
        self.assertListEqual(res, expected)

    def test_deserialise_vars(self):
        lst = ['name=a;doc=docstring_1;unit=mm;components=None;sep= - ;category=None;tags=None;identifier=None',
               'name=b;doc=docstring_2;unit=m/s;components=None;sep= - ;category=None;tags=None;identifier=None']
        res = persist.deserialise_vars(lst)
        store = Store()
        v1 = store.add('a', 'docstring_1', 'mm')
        v2 = store.add('b', 'docstring_2', 'm/s')
        self.assertDictEqual(res, store)

    def test_make_pack(self):
        store = Store()
        v1 = store.add('a', 'docstring_1', 'mm')
        v2 = store.add('b', 'docstring_2', 'm/s')
        lst = [{'index': 0,
                'independent': {v1: 1, v2: 2},
                'dependent': {v1: 5, v2: 7}}]
        box = Box(lst)
        dct = persist.make_pack(box)
        expected = {'data':
                        [{'index': 0,
                          'independent': {'a [mm]': 1, 'b [m/s]': 2},
                          'dependent': {'a [mm]': 5, 'b [m/s]': 7}}],
                    'vars': 
                        ['name=a;doc=docstring_1;unit=mm;components=None;sep= - ;category=None;tags=None;identifier=None',
                         'name=b;doc=docstring_2;unit=m/s;components=None;sep= - ;category=None;tags=None;identifier=None']}
        self.assertDictEqual(dct, expected)

    def test_unpack(self):
        pack = {'data':
                    [{'index': 0,
                      'independent': {'a [mm]': 1, 'b [m/s]': 2},
                      'dependent': {'a [mm]': 5, 'b [m/s]': 7}}],
                'vars': 
                    ['name=a;doc=docstring_1;unit=mm;components=None;sep= - ;category=None;tags=None;identifier=None',
                     'name=b;doc=docstring_2;unit=m/s;components=None;sep= - ;category=None;tags=None;identifier=None']}
        store = Store()
        v1 = store.add('a', 'docstring_1', 'mm')
        v2 = store.add('b', 'docstring_2', 'm/s')
        lst = [{'index': 0,
                'independent': {v1: 1, v2: 2},
                'dependent': {v1: 5, v2: 7}}]
        box = Box(lst)
        box_unpacked = persist.unpack(pack)
        self.assertListEqual(box, box_unpacked)
        keys = list(box_unpacked[0]['dependent'].keys())
        for k in keys:
            self.assertTrue(isinstance(k, Variable))
            self.assertTrue(k in store)
            self.assertEqual(store[k].to_str(), k.to_str())
            

class Test_JSON(unittest.TestCase):
    def test_uncompresed_save_load(self):
        box = Box(get_lst())
        box_check = get_box_check(box, 'test.box')
        self.assertListEqual(box, box_check)

    def test_uncompresed_save_load_np_array(self):
        box = Box(get_lst_2())
        box_check = get_box_check(box, 'test.box')
        self.assertEqual(str(list(box)), str(list(box_check)))


class Test_CJSON(unittest.TestCase):
    def test_compressed_save_load(self):
        box = Box(get_lst())
        box_check = get_box_check(box, 'test.cbox')
        self.assertListEqual(box, box_check)

    def test_compressed_save_load_np_array(self):
        box = Box(get_lst_2())
        box_check = get_box_check(box, 'test.cbox')
        self.assertEqual(str(list(box)), str(list(box_check)))
        

class Test_NPZ(unittest.TestCase):
    def test_compressed_save_load(self):
        box = Box(get_lst())
        box_check = get_box_check(box, 'test.npz')
        self.assertListEqual(box, box_check)

    def test_compressed_save_load_np_array(self):
        box = Box(get_lst_2())
        box_check = get_box_check(box, 'test.npz')
        self.assertEqual(str(list(box)), str(list(box_check)))        