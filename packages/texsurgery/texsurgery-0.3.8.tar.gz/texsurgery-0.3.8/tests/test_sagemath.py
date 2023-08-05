#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging

from texsurgery.texsurgery import TexSurgery

class TestSagemathSurgery(unittest.TestCase):
    """ Tests TexSurgery.code_surgery for the sagemath kernel"""

    def test_simple_addition(self):
        """ Tests a simple addition"""
        tex_source = r'\usepackage[sagemath]{texsurgery}2+2=\eval{2+2}'
        tex_out = r'2+2=4'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

    def test_sif(self):
        """ Tests \sif{}{}{}"""
        tex_source = r'\usepackage[sagemath]{texsurgery}3 is a \sif{is_prime(3)}{prime}{composite} number'
        tex_out = r'3 is a prime number'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

        tex_source = r'\usepackage[sagemath]{texsurgery}4 is a \sif{is_prime(4)}{prime}{composite} number'
        tex_out = r'4 is a composite number'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

    def test_symbolic(self):
        """ Tests substitution of sqrt(2)"""
        tex_source = r'\usepackage[sagemath]{texsurgery}\sqrt{2}=\sage{sqrt(2)}=\eval{sqrt(2)}=\eval{n(sqrt(2),20)}'
        tex_out = r'\sqrt{2}=\sqrt{2}=sqrt(2)=1.4142'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

    def test_sprel(self):
        """ Tests substitution of sqrt(2)"""
        tex_source = r'''\usepackage[sagemath]{texsurgery}
\begin{srepl}
1+1
sin(pi)
for i in [1,2,3]:
    print(i^2)
    if i>1:
        print(i)
\end{srepl}
'''
        tex_out = r'''
\begin{verbatim}
sage: 1+1
2
sage: sin(pi)
0
sage: for i in [1,2,3]:
....:     print(i^2)
....:     if i>1:
....:         print(i)
1
4
2
9
3

\end{verbatim}
'''
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel
