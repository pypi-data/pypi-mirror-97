# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:46:33 2019

@author: Reuben
"""

import fastwire

import unittest


class Test_WireBox(unittest.TestCase):
    
    def test_create_auto(self):
        b = fastwire.WireBox()
        c = b.add()
        self.assertEqual(c.__class__, fastwire.WireContainer)
        self.assertEqual(c.id, 1)
        self.assertEqual(b.get_container(0), c)

    def test_create_cid_int(self):
        b = fastwire.WireBox()
        c = b.add(456)
        self.assertEqual(c.__class__, fastwire.WireContainer)
        self.assertEqual(c.id, 456)
        self.assertEqual(b.get_container(456), c)

    def test_create_cid_str(self):
        b = fastwire.WireBox()
        c = b.add('a_string')
        self.assertEqual(c.__class__, fastwire.WireContainer)
        self.assertEqual(c.id, 'a_string')
        self.assertEqual(b.get_container('a_string'), c)
        
    def test_get_name_arg(self):
        wb = fastwire.WireBox() # use default container
        wire = wb.get('test_name')
        self.assertEqual(wire.name, 'test_name')
        
    def test_get_name_kwarg(self):
        wb = fastwire.WireBox() # use default container
        wire = wb.get(name='test_name')
        self.assertEqual(wire.name, 'test_name')

    def test_get_doc_arg(self):
        wb = fastwire.WireBox() # use default container
        wire = wb.get('test_name', 'test_doc')
        self.assertEqual(wire.doc, 'test_doc')
        
    def test_get_doc_kwarg(self):
        wb = fastwire.WireBox() # use default container
        wire = wb.get(name='test_name', doc='test_doc')
        self.assertEqual(wire.doc, 'test_doc')
        
    def test_get_attrs_kwarg(self):
        dct = {'a': 5}
        wb = fastwire.WireBox() # use default container
        wire = wb.get(name='test_name', attrs=dct)
        self.assertEqual(wire.attrs, dct)
        
    def test_activate(self):
        wb = fastwire.WireBox()
        cid1 = wb.add()
        cid2 = wb.add(3049)
        wb.set_active(cid1)
        check = wb._active
        self.assertEqual(cid1, check)
        
    def test_create_wire(self):
        wb = fastwire.WireBox()
        wc = wb.add(id(self))
        wire = wb.wire('this_name')
        self.assertEqual(wire.name, 'this_name')
        self.assertEqual(wire.__class__, fastwire.Wire)

    def test_create_on_demand(self):
        wb = fastwire.WireBox()
        wc = wb.add(id(self))
        wire = wb['this_name']
        self.assertEqual(wire.name, 'this_name')
        self.assertEqual(wire.__class__, fastwire.Wire)

    def test_create_on_demand_repeated(self):
        wb = fastwire.WireBox()
        wc = wb.add(id(self))
        wire_1 = wb['this_name']
        wire_2 = wb['this_name']
        self.assertEqual(wire_1, wire_2)

    def test_get(self):
        wb = fastwire.WireBox()
        wc = wb.add(id(self))
        wire = wb.get('this_name')
        self.assertEqual(wire.name, 'this_name')
        self.assertEqual(wire.__class__, fastwire.Wire)

    def test_get_repeated(self):
        wb = fastwire.WireBox()
        wc = wb.add(id(self))
        wire_1 = wb.get('this_name')
        wire_2 = wb.get('this_name')
        self.assertEqual(wire_1, wire_2)

    def test_remove(self):
        wb = fastwire.WireBox()
        wb.add(0)
        self.assertEqual(len(wb._cs), 2)
        wb.remove(0)
        self.assertEqual(len(wb._cs), 1)
        
    def test_remove_with(self):
        class A():
            pass
        a = A()
        wb = fastwire.WireBox()
        wb.add(id(a), remove_with=a)
        self.assertEqual(len(wb._cs), 2)
        del a
        self.assertEqual(len(wb._cs), 1)
