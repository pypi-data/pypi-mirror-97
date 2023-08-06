# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:46:33 2019

@author: Reuben
"""

import fastwire

import unittest


class Test_SignalBox(unittest.TestCase):
    
    def test_create_auto(self):
        b = fastwire.SignalBox()
        c = b.add()
        self.assertEqual(c.__class__, fastwire.SignalContainer)
        self.assertEqual(c.id, 1)
        self.assertEqual(b.get_container(0), c)

    def test_create_cid_int(self):
        b = fastwire.SignalBox()
        c = b.add(456)
        self.assertEqual(c.__class__, fastwire.SignalContainer)
        self.assertEqual(c.id, 456)
        self.assertEqual(b.get_container(456), c)

    def test_create_cid_str(self):
        b = fastwire.SignalBox()
        c = b.add('a_string')
        self.assertEqual(c.__class__, fastwire.SignalContainer)
        self.assertEqual(c.id, 'a_string')
        self.assertEqual(b.get_container('a_string'), c)
                
    def test_get_name_arg(self):
        sb = fastwire.SignalBox() # use default container
        signal = sb.get('test_name')
        self.assertEqual(signal.name, 'test_name')
        
    def test_get_name_kwarg(self):
        sb = fastwire.SignalBox() # use default container
        signal = sb.get(name='test_name')
        self.assertEqual(signal.name, 'test_name')

    def test_get_doc_arg(self):
        sb = fastwire.SignalBox() # use default container
        signal = sb.get('test_name', 'test_doc')
        self.assertEqual(signal.doc, 'test_doc')
        
    def test_get_doc_kwarg(self):
        sb = fastwire.SignalBox() # use default container
        signal = sb.get(name='test_name', doc='test_doc')
        self.assertEqual(signal.doc, 'test_doc')
        
    def test_get_attrs_kwarg(self):
        dct = {'a': 5}
        sb = fastwire.SignalBox() # use default container
        signal = sb.get(name='test_name', attrs=dct)
        self.assertEqual(signal.attrs, dct)
        
    def test_activate(self):
        sb = fastwire.SignalBox()
        cid1 = sb.add()
        cid2 = sb.add(3049)
        sb.set_active(cid1)
        check = sb._active
        self.assertEqual(cid1, check)
        
    def test_create_signal(self):
        sb = fastwire.SignalBox()
        sc = sb.add(id(self))
        signal = sb.signal('this_name')
        self.assertEqual(signal.name, 'this_name')
        self.assertEqual(signal.__class__, fastwire.Signal)

    def test_create_on_demand(self):
        sb = fastwire.SignalBox()
        sc = sb.add(id(self))
        signal = sb['this_name']
        self.assertEqual(signal.name, 'this_name')
        self.assertEqual(signal.__class__, fastwire.Signal)

    def test_create_on_demand_repeated(self):
        sb = fastwire.SignalBox()
        sc = sb.add(id(self))
        wire_1 = sb['this_name']
        wire_2 = sb['this_name']
        self.assertEqual(wire_1, wire_2)

    def test_get(self):
        sb = fastwire.SignalBox()
        sc = sb.add(id(self))
        wire = sb.get('this_name')
        self.assertEqual(wire.name, 'this_name')
        self.assertEqual(wire.__class__, fastwire.Signal)

    def test_get_repeated(self):
        sb = fastwire.SignalBox()
        sc = sb.add(id(self))
        wire_1 = sb.get('this_name')
        wire_2 = sb.get('this_name')
        self.assertEqual(wire_1, wire_2)

    def test_remove(self):
        sb = fastwire.SignalBox()
        sb.add(0)
        self.assertEqual(len(sb._cs), 2)
        sb.remove(0)
        self.assertEqual(len(sb._cs), 1)
        
    def test_remove_with(self):
        class A():
            pass
        a = A()
        sb = fastwire.SignalBox()
        sb.add(id(a), remove_with=a)
        self.assertEqual(len(sb._cs), 2)
        del a
        self.assertEqual(len(sb._cs), 1)
