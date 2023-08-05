#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
#import logging

from texsurgery.texsurgery import TexSurgery

class TestImports(unittest.TestCase):
    """ Tests TexSurgery.add_import and remove_import"""

    def test_add_import(self):
        """Add a sample usepackage with an option"""
        tex_source = r'''\documentclass[a4paper]{article}
\usepackage[sagemath]{texsurgery}
\begin{document}
2+2=\eval{2+2}
\end{document}'''
        tex_out = r'''\documentclass[a4paper]{article}
\usepackage[option]{mypackage}
\usepackage[sagemath]{texsurgery}
\begin{document}
2+2=\eval{2+2}
\end{document}'''
        ts = TexSurgery(tex_source).add_import('mypackage', options='option')
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel
