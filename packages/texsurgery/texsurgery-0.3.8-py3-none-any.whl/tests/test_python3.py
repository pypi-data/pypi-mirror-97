#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging

from texsurgery.texsurgery import TexSurgery

class TestPython3Surgery(unittest.TestCase):
    """ Tests TexSurgery.code_surgery for the python3 kernel"""

    def test_simple_addition(self):
        """ Tests a simple addition"""
        tex_source = r'\usepackage[python3]{texsurgery}2+2=\eval{2+2} '
        tex_out = r'2+2=4 '
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

    def test_division(self):
        """ Tests a simple addition"""
        tex_source = r'\usepackage[python3]{texsurgery}1/2=\eval{1/2}'
        tex_out = r'1/2=0.5'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

    def test_nested_brackets(self):
        """ Tests an expression eval{ with {nested} brackets }"""
        tex_source = r"\usepackage[python3]{texsurgery}The first prime number is \eval{sorted({7,3,5,2})[0]}"
        tex_out = r'The first prime number is 2'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

    def test_return_str(self):
        """evalstr{'python string'} should not return the quotes"""
        tex_source = r"\usepackage[python3]{texsurgery}My favourite colour is \evalstr{'blue'} "
        tex_out = r'My favourite colour is blue '
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

    def test_sif(self):
        """ Tests \sif{}{}{}"""
        tex_source = r'\usepackage[python3]{texsurgery}'\
        r'\begin{runsilent}a=3\end{runsilent}'\
        r'\eval{a} is an \sif{a%2}{odd}{even} number'
        tex_out = r'3 is an odd number'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

        tex_source = r'\usepackage[python3]{texsurgery}'\
        r'\begin{runsilent}a=4\end{runsilent}'\
        r'\eval{a} is an \sif{a%2}{odd}{even} number'
        tex_out = r'4 is an even number'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

    def test_sinput(self):
        """\\sinput{file.py} should read that file and run it immediately"""
        tex_source = r"\usepackage[python3]{texsurgery}"\
        r'\begin{runsilent}a=4\end{runsilent}'\
        r'\sinput{tests/add_1_to_a.py}'\
        r'a=\eval{a}'
        tex_out = r'a=5'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

    # def test_comment(self):
    #     """ignore comments => no longer in use"""
    #     tex_source = r"\usepackage[python3]{texsurgery}"\
    #     r'\begin{runsilent}a=4# some comment'\
    #     '\na+=1\\end{runsilent}'\
    #     r'a=\eval{a}%\eval{would be an error}'
    #     tex_out = r'a=5%\eval{would be an error}'
    #     ts = TexSurgery(tex_source).code_surgery()
    #     self.assertEqual(ts.src, tex_out)
    #     del ts #shutdow kernel
