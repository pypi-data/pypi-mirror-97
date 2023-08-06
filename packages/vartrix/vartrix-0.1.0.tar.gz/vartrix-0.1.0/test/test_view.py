# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 21:11:42 2019

@author: Reuben
"""

import unittest

from vartrix.container import Container
from vartrix.view import View
from vartrix import settings

def get_c():
    c = Container()
    c.set('a.b', 5)
    c.set('b.c', 7)
    return c

class Test_View(unittest.TestCase):
    def test_init(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        self.assertTrue(isinstance(v, dict))
        
    def test_init_none(self):
        c = get_c()
        v = View(c, dotkeys=None)
        expected = {'a': {'b': 5}, 'b': {'c': 7}}
        self.assertDictEqual(v, expected)

    def test_init_empty(self):
        c = get_c()
        v = View(c, dotkeys=[''])
        expected = {'a': {'b': 5}, 'b': {'c': 7}}
        self.assertDictEqual(v, expected)

    def test_init_dot(self):
        c = get_c()
        v = View(c, dotkeys=['.'])
        expected = {'a': {'b': 5}, 'b': {'c': 7}}
        self.assertDictEqual(v, expected)
    
    def test_get(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        res = v['b']
        expected = 5
        self.assertEqual(res, expected)

    def test_get_attr(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        res = v.b
        expected = 5
        self.assertEqual(res, expected)
        
    def test_refresh(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        v.clear()
        v.refresh()
        v.refresh()
        res = v['b']
        expected = 5
        self.assertEqual(res, expected)
               
    def test_refresh_attr(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        del v.b
        v.refresh()
        res = v.b
        expected = 5
        self.assertEqual(res, expected)   
                
    def test_set(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        v['b'] = 99
        res = v['b']
        expected = 99
        self.assertEqual(res, expected)
        res2 = c['a.b']
        self.assertEqual(res2, expected)

    def test_nested_set(self):
        c = get_c()
        c['a.g.h'] = 55
        dotkeys = ['a']
        v = View(c, dotkeys)
        v['g.h'] = 99
        res = v['g']
        expected = {'h': 99}
        self.assertDictEqual(res, expected)
        
        
    def test_set_remote(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        c['a.b'] = 99
        res = v['b']
        expected = 99
        self.assertEqual(res, expected)
        res2 = c['a.b']
        self.assertEqual(res2, expected)
        
    def test_new_key(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        c['a.new'] = 99
        res = v['new']
        expected = 99
        self.assertEqual(res, expected)

    def test_live_remote(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        v.live = False
        c['a.b'] = 99
        res = v['b']
        expected = 5
        self.assertEqual(res, expected)
        res2 = c['a.b']
        expected2 = 99
        self.assertEqual(res2, expected2)
        v.live = True
        res3 = v['b']
        expected3 = 99
        self.assertEqual(res3, expected3)
        
    def test_live_local(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        v.live = False
        v['b'] = 99
        res = c['a.b']
        expected = 5
        self.assertEqual(res, expected)
        res2 = v['b']
        expected2 = 99
        self.assertEqual(res2, expected2)
        v.live = True
        res3 = v['b']
        expected3 = 5
        self.assertEqual(res3, expected3)

    def test_live_settings(self):
        c = get_c()
        dotkeys = ['a']
        settings.LIVE_VIEWS = False
        v = View(c, dotkeys)
        # v.live = False
        settings.LIVE_VIEWS = True
        c['a.b'] = 99
        res = v['b']
        expected = 5
        self.assertEqual(res, expected)
        res2 = c['a.b']
        expected2 = 99
        self.assertEqual(res2, expected2)
        v.live = True
        res3 = v['b']
        expected3 = 99
        self.assertEqual(res3, expected3)
        
    def test_context(self):
        c = get_c()
        dotkeys = ['a']
        v = View(c, dotkeys)
        with v.context({'b': 77}):
            self.assertEqual(v['b'], 77)
        self.assertEqual(v['b'], 5)
        