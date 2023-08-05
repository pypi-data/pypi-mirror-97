#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
#import logging

from texsurgery.texsurgery import TexSurgery

class TestInsert(unittest.TestCase):
    """ Tests TexSurgery.insertAfter"""

    def __init__(self, methodName='runTest'):
        super(TestInsert, self).__init__(methodName=methodName)
        with open('tests/test_find.tex','r') as f:
            self.sample_tex = f.read()

    def test_add_choice(self):
        """finds a nested selector and inserts a hew wrongchoice after it
        """
        tex_source = self.sample_tex
        expected_res = [
            ('choices', [
                ('\wrongchoice', '$\sage{fd/a}$'),
                ('\wrongchoice', '$\sage{fd*a}$'),
                ('\wrongchoice', '$\sage{fd + a}$')
                ]),
        ]
        ts = TexSurgery(tex_source)
        ts.insertAfter(r'choices \correctchoice', '\wrongchoice{$\sage{fd/a}$}')
        res = ts.findall(r'choices \wrongchoice')
        self.assertEqual(res, expected_res)

        #part II, a different insertion point
        expected_res = [
            ('choices', [
                ('\wrongchoice', '$\sage{fd*a}$'),
                ('\wrongchoice', '$\sage{fd/a}$'),
                ('\wrongchoice', '$\sage{fd + a}$')
                ]),
        ]
        ts = TexSurgery(tex_source)
        ts.insertAfter(r'choices \wrongchoice', '\wrongchoice{$\sage{fd/a}$}')
        res = ts.findall(r'choices \wrongchoice')
        self.assertEqual(res, expected_res)

    def test_add_choice_with_comma(self):
        """Similar to test_add_choice, but the selector is more complex
        """
        tex_source = self.sample_tex
        expected_res = [
            ('choices', [
                ('\wrongchoice', '$\sage{fd*a}$'),
                ('\wrongchoice', '$\sage{fd/a}$'),
                ('\wrongchoice', '$\sage{fd + a}$')
                ]),
        ]
        ts = TexSurgery(tex_source)
        ts.insertAfter(r'choices,itemize \wrongchoice', '\wrongchoice{$\sage{fd/a}$}')
        res = ts.findall(r'choices \wrongchoice')
        self.assertEqual(res, expected_res)
