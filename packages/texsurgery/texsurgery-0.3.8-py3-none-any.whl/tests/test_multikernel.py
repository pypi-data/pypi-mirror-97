#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging

from texsurgery.texsurgery import TexSurgery

class MultiKernelSurgery(unittest.TestCase):
    """ Tests TexSurgery.code_surgery for the sagemath kernel"""

    def multikernel(self):
        """ Tests handling two kernels, being the first the default"""
        tex_source = r'''\usepackage[sagemath,python3]{texsurgery}
\begin{run}
1^1
\end{run}
\begin{run}[python3]
1^1
\end{run}
'''
        tex_out = r'''
1
0'''
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel
