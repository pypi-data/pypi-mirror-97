# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 20:04:58 2019

@author: Reuben
"""

import os
import unittest

from resultbox import Store, Variable, Aliases
from resultbox import variable

class Test_Expand(unittest.TestCase):
    def test_expand_basic(self):
        s = Store()
        key_a = s.new('a', components=['x', 'y'])
        dct = {key_a: [0, 1]}
        out = variable.expand(dct, s)
        expected = {'a - x': 0, 'a - y': 1}
        self.assertDictEqual(out, expected)

    def test_expand_nested(self):
        s = Store()
        key_a = s.new('a', components=['x', 'y'])
        dct = {'dependent': {'another_level': {key_a: [0, 1]}}}
        out = variable.expand(dct, s)
        expected = {'dependent': {'another_level': {'a - x': 0, 'a - y': 1}}}
        self.assertDictEqual(out, expected)

    def test_expand_list_of_dicts(self):
        s = Store()
        key_a = s.new('a', components=['x', 'y'])
        dct = [{'index': 0, 'dependent': {key_a: [0, 1]}}]
        out = variable.expand(dct, s)
        expected = [{'index': 0, 'dependent': {'a - x': 0, 'a - y': 1}}]
        self.assertListEqual(out, expected)


class Test_Store(unittest.TestCase):
    def test_new(self):
        s = Store()
        name = 'a'
        doc = 'b'
        unit = 'c'
        v = s.new(name, doc, unit)
        v_check = Variable(name, doc, unit)
        self.assertEqual(str(v_check), str(v))
        self.assertTrue(v in s)
        self.assertEqual(str(s[v]), str(v))

    def test_add(self):
        s = Store()
        v = s.add('test')
        self.assertEqual(len(s), 1)

    def test_nearest(self):
        s = Store()
        s.new('dummy')
        s.new('the one we want')
        s.new('irrelevant')
        v = s.nearest('one we wnt')
        self.assertEqual(v.name, 'the one we want')
        
    def test_suffixed(self):
        s = Store()
        v1 = s.add('test')
        v2 = s.suffixed(v1, ' suffix')
        self.assertEqual(len(s), 2)
        test2 = s['test suffix']
        self.assertTrue(v2 is test2)
            
    def test_identifier_getitem(self):
        s = Store()
        v = s.add('test', identifier='TEST')
        self.assertEqual(s['TEST'], v)
        
    def test_identifier_getattr(self):
        s = Store()
        v = s.add('test', identifier='TEST')
        self.assertEqual(s.TEST, v)

    def test_add_csv(self):
        s = Store()
        folder = os.path.dirname(os.path.abspath(__file__))
        fname = os.path.join(folder, 'test_variable.csv')
        v = s.add_csv(fname, encoding='utf-8')
        d1 =  {'name': 'variable a',
               'doc': None,
               'unit': 'mm',
               'components': None,
               'sep': ' - ',
               'category': 'test',
               'tags': None,
               'identifier': 'VAR_A'}
        self.assertDictEqual(d1, s['VAR_A'].to_dict())
        d2 =  {'name': 'variable b',
               'doc': None,
               'unit': 's',
               'components': None,
               'sep': ' - ',
               'category': 'test',
               'tags': ['new', 'tag'],
               'identifier': 'VAR_B'}
        self.assertDictEqual(d2, s['VAR_B'].to_dict())
        d3 =  {'name': 'variable c',
               'doc': 'some doc',
               'unit': 'm',
               'components': ['x', 'y', 'z'],
               'sep': ' - ',
               'category': 'test',
               'tags': None,
               'identifier': 'VAR_C'}
        self.assertDictEqual(d3, s['VAR_C'].to_dict())
        

class Test_Variable(unittest.TestCase):
    def test_init(self):
        name = 'a'
        doc = 'b'
        unit = 'c'
        v = Variable(name, doc, unit)
        self.assertEqual(v.name, name)
        self.assertEqual(v.doc, doc)
        self.assertEqual(v.unit, unit)
        
    def test_str(self):
        name = 'a'
        doc = 'b'
        unit = 'mm'
        v = Variable(name, doc, unit)
        self.assertEqual(str(v), 'a [mm]')
        
    def test_components_getitem(self):
        name = 'a'
        doc = 'b'
        unit = 'mm'
        xyz = ['x', 'y', 'z']
        sep = ' - '
        v = Variable(name, doc, unit, components=xyz, sep=sep)
        self.assertEqual(v['x'], 'a - x [mm]')
        
    def test_components_key(self):
        name = 'a'
        doc = 'b'
        unit = 'mm'
        xyz = ['x', 'y', 'z']
        sep = ' - '
        v = Variable(name, doc, unit, components=xyz, sep=sep)
        self.assertEqual(v.key, 'a [mm]')
        
    def test_components_keys(self):
        name = 'a'
        doc = 'b'
        unit = 'mm'
        xyz = ['x', 'y', 'z']
        sep = ' - '
        v = Variable(name, doc, unit, components=xyz, sep=sep)
        keys = ['a - x [mm]', 'a - y [mm]', 'a - z [mm]']
        self.assertListEqual(v.subkeys, keys)
        
    def test_to_dict(self):
        dct = {'name': 'a',
               'doc': 'b',
               'unit': 'mm',
               'components': ['x', 'y', 'z'],
               'sep': ' - ',
               'category': 'category_1',
               'tags': ['tag_1', 'tag_2'],
               'identifier': 'test_var'}
        v = Variable(**dct)
        d = v.to_dict()
        self.assertDictEqual(d, dct)
        
    def test_from_dict(self):
        dct = {'name': 'a',
               'doc': 'b',
               'unit': 'mm',
               'components': ['x', 'y', 'z'],
               'sep': ' - ',
               'category': 'category_1',
               'tags': ['tag_1', 'tag_2'],
               'identifier': 'test_var'}
        v = Variable.from_dict(dct)
        d = v.to_dict()
        self.assertDictEqual(d, dct)
        
    def test_to_str(self):
        dct = {'name': 'a',
               'doc': 'b',
               'unit': 'mm',
               'components': ['x', 'y', 'z'],
               'sep': ' - ',
               'category': 'category_1',
               'tags': ['tag_1', 'tag_2'],
               'identifier': 'test_var'}
        v = Variable(**dct)
        s = v.to_str()
        expected = 'name=a;doc=b;unit=mm;components=[x,y,z];sep= - ;category=category_1;tags=[tag_1,tag_2];identifier=test_var'
        self.assertEqual(s, expected)
        
    def test_from_str(self):
        s = 'name=a;doc=b;unit=mm;components=[x,y,z];sep= - ;category=category_1;tags=[tag_1,tag_2];identifier=test_var'
        dct = {'name': 'a',
               'doc': 'b',
               'unit': 'mm',
               'components': ['x', 'y', 'z'],
               'sep': ' - ',
               'category': 'category_1',
               'tags': ['tag_1', 'tag_2'],
               'identifier': 'test_var'}
        v = Variable.from_str(s)
        v_check = Variable(**dct)
        self.assertEqual(v.to_str(), v_check.to_str())
        
class Test_Aliases(unittest.TestCase):
    def test_init(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        self.assertDictEqual(a, dct)

    def test_translate_str(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        s = 'a'
        ret = a.translate(s)
        expected = 'something'
        self.assertEqual(ret, expected)
        
    def test_translate_dict(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        d = {'a': 3}
        ret = a.translate(d)
        expected = {'something': 3}
        self.assertDictEqual(ret, expected)

    def test_translate_dict_vals(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        d = {'one': 'a'}
        ret = a.translate_dict_vals(d)
        expected = {'one': 'something'}
        self.assertDictEqual(ret, expected)

    def test_translate_list(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        lst = ['a']
        ret = a.translate(lst)
        expected = ['something']
        self.assertListEqual(ret, expected)
        
    def test_translate_dlist(self):
        dct = {'a': 'something', 'b': 'other'}
        a = Aliases(dct)
        lst = [{'a': 3, 'b': 5}, {'a': 7, 'b': 8}]
        ret = a.translate(lst)
        expected = [{'something': 3, 'other': 5}, {'something': 7, 'other': 8}]
        self.assertListEqual(ret, expected)
        
    def test_translate_dlist_variables(self):
        dct = {'a': Variable('one', 'blah', 'mm'),
               'b': Variable('two', 'blah2', 's')}
        a = Aliases(dct)
        lst = [{'a': 3, 'b': 5}, {'a': 7, 'b': 8}]
        ret = a.translate(lst)
        expected = [{'one [mm]': 3, 'two [s]': 5},
                     {'one [mm]': 7, 'two [s]': 8}]
        self.assertListEqual(ret, expected)
        
    def test_translate_boxlike(self):
        dct = {'a': 'something', 'b': 'other'}
        a = Aliases(dct)
        lst = [{'index': 0,
                'independent': {'c': 55},
                'dependent': {'a': 3, 'b': 5}},
               {'index': 1,
                'independent': {'c': 66},
                'dependent': {'a': 7, 'b': 8}}]
        ret = a.translate(lst)
        expected = [{'index': 0,
                'independent': {'c': 55},
                'dependent': {'something': 3, 'other': 5}},
               {'index': 1,
                'independent': {'c': 66},
                'dependent': {'something': 7, 'other': 8}}]
        self.assertListEqual(ret, expected)
