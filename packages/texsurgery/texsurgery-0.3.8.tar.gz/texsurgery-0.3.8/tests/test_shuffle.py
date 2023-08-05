#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
#import logging

from texsurgery.texsurgery import TexSurgery

class TestShuffle(unittest.TestCase):
    """ Tests TexSurgery.insertAfter"""

    def __init__(self, methodName='runTest'):
        super(TestShuffle, self).__init__(methodName=methodName)
        with open('tests/test_shuffle.tex','r') as f:
            self.sample_tex = f.read()

    def test_shuffle_all_choices(self):
        """shuffles wrongchoice and correctchoice inside all choices environments
        """
        tex_source = self.sample_tex

        ts = TexSurgery(tex_source)
        ts.shuffle('choices', 'correctchoice,wrongchoice', seed=1)

        # #uncomment to "reset" the test
        # with open('tests/test_shuffle_out_1.tex','r') as f:
        #     tex_out = f.write(ts.src)
        #     print(tex_out)
        with open('tests/test_shuffle_out_1.tex','r') as f:
            tex_out = f.read()
        self.maxDiff = None
        self.assertEqual(ts.src, tex_out)

    def test_shuffle_one_choices(self):
        """shuffles wrongchoice and correctchoice inside only one choices environment
        """
        tex_source = self.sample_tex

        ts = TexSurgery(tex_source)
        ts.shuffle(
            'questionmultx{questionid}[questionid=basic-multiplication] choices',
            'correctchoice,wrongchoice',
            seed=1)

        # #uncomment to "reset" the test
        # with open('tests/test_shuffle_out_2.tex','r') as f:
        #     tex_out = f.write(ts.src)
        #     print(tex_out)
        with open('tests/test_shuffle_out_2.tex','r') as f:
            tex_out = f.read()
        self.maxDiff = None
        self.assertEqual(ts.src, tex_out)
