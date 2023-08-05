#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for http.py """

import unittest
import logging

from texsurgery.texsurgery import TexSurgery

class TestSagemath9(unittest.TestCase):
    """ Specific tests for sagemath9 kernel """

    def test_impossible(self):
        """ Tests the simplest, unnested replacements"""
        self.assertEqual(1, 0)
