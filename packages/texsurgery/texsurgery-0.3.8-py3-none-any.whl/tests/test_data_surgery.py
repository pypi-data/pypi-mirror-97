#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for http.py """

import unittest
import logging

from texsurgery.texsurgery import TexSurgery

class TestDataSurgery(unittest.TestCase):
    """ Tests TexSurgery.data_surgery """

    def test_simple_replace(self):
        """ Tests the simplest, unnested replacements"""
        tex_source = r'A \adjective test'
        rplc = dict(adjective='simple')
        tex_out = 'A simple test'
        ts = TexSurgery(tex_source).data_surgery(rplc)
        self.assertEqual(ts.src, tex_out)

    def test_multiple_replace(self):
        """A command is replaced twice"""
        tex_source = r'A \adjective test, and the same \adjective test again'
        rplc = dict(adjective='simple')
        tex_out = 'A simple test, and the same simple test again'
        ts = TexSurgery(tex_source).data_surgery(rplc)
        self.assertEqual(ts.src, tex_out)

    def test_different_replace(self):
        """Two commands are replaced"""
        tex_source = r'A \adjective test, and a \differentadjective test'
        rplc = dict(adjective='simple', differentadjective='not so simple')
        tex_out = 'A simple test, and a not so simple test'
        ts = TexSurgery(tex_source).data_surgery(rplc)
        self.assertEqual(ts.src, tex_out)

    def test_replace_in_command(self):
        """ Tests a replacement inside a comment"""
        tex_source = r'A \textbf{\adjective} test'
        rplc = dict(adjective='nested')
        tex_out = r'A \textbf{nested} test'
        ts = TexSurgery(tex_source).data_surgery(rplc)
        self.assertEqual(ts.src, tex_out)

    def test_replace_in_environment(self):
        """ Tests a replacement inside an environment"""
        tex_source = 'List begins:\n'
        '\\begin{itemize}\n\\item A \\textbf{\\adjective} test\\end{itemize}'
        'List has ended'
        rplc = dict(adjective='nested-in-environment')
        tex_out = 'List begins:\n'
        '\\begin{itemize}\n\\item A nested-in-environment test\\end{itemize}'
        'List has ended'
        ts = TexSurgery(tex_source).data_surgery(rplc)
        self.assertEqual(ts.src, tex_out)
