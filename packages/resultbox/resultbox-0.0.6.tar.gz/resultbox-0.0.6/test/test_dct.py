# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 20:04:58 2019

@author: Reuben
"""

import unittest

from resultbox import Dict_Container, get_dict


def dct1():
    return {'a': 1, 'b': 2}

def dct2():
    return {'a': 3, 'b': 4, 'c': 5}
   

class Test_Dict_Container(unittest.TestCase):
    def test_init(self):
        dc = Dict_Container()

    def test_get_new(self):
        dc = Dict_Container()
        test = dc['test']
        self.assertTrue(isinstance(test, dict))
        
    def test_get_again(self):
        dc = Dict_Container()
        test = dc['test']
        test2 = dc['test2']
        test3 = dc['test']
        self.assertTrue(test is test3)
        
