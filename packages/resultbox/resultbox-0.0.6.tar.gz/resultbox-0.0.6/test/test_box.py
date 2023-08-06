# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 20:13:44 2019

@author: Reuben
"""

import unittest

from resultbox import Box, Variable


def get_dct():
    dct = {'a': 1, 'b': 2}
    return dct
   
def get_lst3():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1}, 'dependent': {'d': [12, 30]}},
           {'index': 1, 'independent': {'a': 1, 'b': 2}, 'dependent': {'d': [13, 31]}},
           {'index': 4, 'independent': {'a': 1, 'b': 1}, 'dependent': {'e': [1, 2]}},
           {'index': 7, 'independent': {'a': 1, 'b': 2}, 'dependent': {'e': [1, 2]}}]
    return lst

def get_lst4():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1}, 'dependent': {'c': 4}},
           {'index': 1, 'independent': {'a': 1, 'b': 2}, 'dependent': {'c': 5}},
           {'index': 2, 'independent': {'a': 2, 'b': 1}, 'dependent': {'c': 6}},
           {'index': 3, 'independent': {'a': 2, 'b': 2}, 'dependent': {'c': 7}}]
    return lst

def get_lst5():
    lst = [{'index': 0, 'independent': {'a': 1}, 'dependent': {'b': [1, 2], 'e': [12, 30]}},
           {'index': 1, 'independent': {'a': 1}, 'dependent': {'b': [1, 2],'e': [13, 31]}},
           {'index': 4, 'independent': {'a': 1}, 'dependent': {'d': [7, 8], 'e': [1, 2]}},
           {'index': 7, 'independent': {'a': 1}, 'dependent': {'d': [7, 8], 'e': [1, 2]}}]
    return lst

def get_lst6():
    lst = [{'index': 0, 'independent': {'a': 1}, 'dependent': {'b': 1}},
           {'index': 1, 'independent': {'a': 1}, 'dependent': {'b': 2}},
           {'index': 1, 'independent': {'a': 1}, 'dependent': {'b': 3}},
           {'index': 2, 'independent': {'a': 2}, 'dependent': {'b': 1}},
           {'index': 3, 'independent': {'a': 2}, 'dependent': {'b': 2}}]
    return lst


class Test_Box(unittest.TestCase):
    def test_init(self):
        b = Box()

    def test_add(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        self.assertEqual(len(b), 1)
        expected = {'index': 0, 'independent': {'a': 1, 'b': 2},
                    'dependent': {'test': 7}}
        self.assertEqual(b[0], expected)

    def test_add_arr(self):
        b = Box()
        dct = get_dct()
        var = Variable('a', components=['x', 'y', 'z'])
        val = [[0, 1], [2, 3], [4, 5]]
        b.add(dct, var, val)
        self.assertEqual(len(b), 1)
        expected = {'index': 0, 'independent': {'a': 1, 'b': 2},
                    'dependent': {'a': val}}
        self.assertEqual(b[0], expected)

    def test_add_array_list(self):
        b = Box()    
        dct = get_dct()
        arr = [0, 1, 2]
        labels = ['a', 'b', 'c']
        b.add_array(dct, labels, arr)
        self.assertEqual(len(b), 1)
        expected = {'index': 0, 'independent': {'a': 1, 'b': 2},
                    'dependent': {'a': 0, 'b': 1, 'c': 2}}
        self.assertEqual(b[0], expected)
        
    def test_add_array(self):
        b = Box()    
        dct = get_dct()
        arr = [[0, 1], [2, 3], [4, 5]]
        labels = ['a', 'b', 'c']
        b.add_array(dct, labels, arr)
        self.assertEqual(len(b), 1)
        expected = {'index': 0, 'independent': {'a': 1, 'b': 2},
                    'dependent': {'a': [0, 1], 'b': [2, 3], 'c': [4, 5]}}
        self.assertEqual(b[0], expected)
        
    def test_filtered(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        b.add(dct, 'test2', 8)
        dct['b'] = 3
        b.add(dct, 'test2', 9)
        dct['b'] = 6
        b.add(dct, 'test', 11)
        expected = [{'index': 1, 'independent': {'a': 1, 'b': 2},
                     'dependent': {'test2': 8}},
                    {'index': 2, 'independent': {'a': 1, 'b': 3},
                     'dependent': {'test2': 9}}]
        ret = b.filtered('test2')
        self.assertEqual(ret, expected)
        ret = b.filtered(['test2'])
        self.assertEqual(ret, expected)
        
    def test_where(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        b.add(dct, 'test2', 8)
        dct['b'] = 3
        b.add(dct, 'test', 9)
        b.add(dct, 'test2', 11)
        expected = [{'index': 2, 'independent': {'a': 1, 'b': 3},\
                     'dependent': {'test':  9}},
                    {'index': 3, 'independent': {'a': 1, 'b': 3},
                     'dependent': {'test2':  11}}]
        ret = b.where({'b': 3})
        self.assertEqual(ret, expected)
        ret = b.where(b=3)
        self.assertEqual(ret, expected)
        
    def test_minimal(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        b.add(dct, 'test2', 8)
        minimal = b.minimal()
        expected = [{'a': 1, 'b': 2, 'test': 7, 'test2': 8}]
        self.assertEqual(minimal, expected)
        
    def test_combined(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        b.add(dct, 'test2', 8)
        combined = b.combined()
        expected = [{'independent': {'a': 1, 'b': 2},
                     'dependent': {'test': 7, 'test2': 8}}]
        self.assertEqual(combined, expected)
        
    def test_merge_in_place(self):
        b1 = Box()
        b2 = Box()
        dct = get_dct()
        b1.add(dct, 'test', 7)
        b2.add(dct, 'test2', 8)
        b1.merge(b2)
        expected = [{'index': 0,
                     'independent': {'a': 1, 'b': 2}, 
                     'dependent': {'test': 7}},
                    {'index': 1,
                     'independent': {'a': 1, 'b': 2}, 
                     'dependent': {'test2': 8}}]
        self.assertListEqual(b1, expected)

    def test_merge_not_in_place(self):
        b1 = Box()
        b2 = Box()
        dct = get_dct()
        b1.add(dct, 'test', 7)
        b2.add(dct, 'test2', 8)
        b3 = b1.merge(b2, in_place=False)
        expected = [{'index': 0,
                     'independent': {'a': 1, 'b': 2}, 
                     'dependent': {'test': 7}},
                    {'index': 1,
                     'independent': {'a': 1, 'b': 2}, 
                     'dependent': {'test2': 8}}]
        self.assertListEqual(b3, expected)

        
    def test_getitem(self):
        b = Box(get_lst3())
        keys = ['d', 'e']
        vec0, vec1, labels = b[keys]
        expected_vec0 = [[12, 30], [13, 31]]
        expected_vec1 = [[1, 2], [1, 2]]
        expected_labels = ['a=1, b=1', 'a=1, b=2']
        self.assertListEqual(expected_vec0, vec0)
        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_labels, labels)
        
    def test_vectors(self):
        b = Box(get_lst3())
        keys = ['d', 'e']
        vec0, vec1, labels = b.vectors(keys)
        expected_vec0 = [[12, 30], [13, 31]]
        expected_vec1 = [[1, 2], [1, 2]]
        expected_labels = ['a=1, b=1', 'a=1, b=2']
        self.assertListEqual(expected_vec0, vec0)
        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_labels, labels)

    def test_vectors_scalar(self):
        b = Box(get_lst4())
        keys = ['c']
        c, labels = b.vectors(keys, labels='dict')
        expected_c = [4, 5, 6, 7]
        expected_labels = [{'a': 1, 'b': 1}, {'a': 1, 'b': 2},
                           {'a': 2, 'b': 1}, {'a': 2, 'b': 2}]
        self.assertListEqual(expected_c, c)
        self.assertListEqual(expected_labels, labels)

    def test_vectors_indep_keys(self):
        b = Box(get_lst4())
        keys = ['c']
        c, a, b = b.vectors(keys, indep_keys=['a', 'b'])
        expected_c = [4, 5, 6, 7]
        expected_a = [1, 1, 2, 2]
        expected_b = [1, 2, 1, 2]
        self.assertListEqual(expected_c, c)
        self.assertListEqual(expected_a, a)
        self.assertListEqual(expected_b, b)

    def test_vectors_uncombined(self):
        b = Box(get_lst5())
        keys = ['b', 'e']
        vec0, vec1, labels = b.vectors(keys, combine=False)
        expected_vec0 = [[1, 2], [1, 2]]
        expected_vec1 = [[12, 30], [13, 31]]
        expected_labels = ['a=1', 'a=1']
        self.assertListEqual(expected_vec0, vec0)
        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_labels, labels)
        
    def test_vectors_nonstr(self):
        b = Box(get_lst3())
        keys = ['d', 'e']
        vec0, vec1, labels = b.vectors(keys, labels='dict')
        expected_vec0 = [[12, 30], [13, 31]]
        expected_vec1 = [[1, 2], [1, 2]]
        expected_labels = [{'a': 1, 'b': 1}, {'a': 1, 'b': 2}]
        self.assertListEqual(expected_vec0, vec0)
        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_labels, labels)
        
    def test_grouped_as_dicts(self):
        b = Box(get_lst4())
        keys = ['a', 'c']
        res = b.grouped(keys, as_dicts=True)
        expected = [{'labels': {'b': 1}, 'values': {'a': [1, 2], 'c': [4, 6]}}, {'labels': {'b': 2}, 'values': {'a': [1, 2], 'c': [5, 7]}}]
        self.assertListEqual(res, expected)

    def test_grouped_as_lists(self):
        b = Box(get_lst4())
        keys = ['a', 'c']
        res = b.grouped(keys, as_dicts=False)
        expected = [[[1, 2], [4, 6], {'b': 1}], [[1, 2], [5, 7], {'b': 2}]]
        self.assertListEqual(res, expected)

    def test_unique(self):
        b = Box(get_lst6())
        self.assertListEqual(b.unique('a'), [1, 2])
        self.assertListEqual(b.unique('b'), [1, 2, 3])

    def test_combinations(self):
        b = Box(get_lst6())
        combinations = b.combinations(['a', 'b'])
        expected = [{'a': 1, 'b': 1},
                    {'a': 1, 'b': 2},
                    {'a': 1, 'b': 3},
                    {'a': 2, 'b': 1},
                    {'a': 2, 'b': 2}]
        self.assertListEqual(combinations, expected)
        