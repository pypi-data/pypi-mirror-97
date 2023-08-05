#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
#import logging

from texsurgery.texsurgery import TexSurgery

class TestFind(unittest.TestCase):
    """ Tests TexSurgery.find and  TexSurgery.findall"""

    def __init__(self, methodName='runTest'):
        super(TestFind, self).__init__(methodName=methodName)
        with open('tests/test_find.tex','r') as f:
            self.sample_tex = f.read()

    def test_find_one_environment(self):
        """use find for a non nested environment
        """
        tex_source = self.sample_tex
        expected_res = ('run', "print('The random seed is ', seed)\n")
        res = TexSurgery(tex_source).find('run')
        self.assertEqual(res, expected_res)

    def test_find_unexisting(self):
        """use find for an environment that is not in the document
        """
        tex_source = self.sample_tex
        expected_res = None
        res = TexSurgery(tex_source).find('runmeplease')
        self.assertEqual(res, expected_res)

    def test_find_nested(self):
        """use find for a non nested environment
        """
        tex_source = self.sample_tex
        expected_res = ('choices', '\correctchoice', '$\sage{fd}$')
        res = TexSurgery(tex_source).find('run,choices \correctchoice')
        self.assertEqual(res, expected_res)

    def test_findall_one_environment(self):
        """finds all apperances of one non nested environment
        that appears only once.
        """
        tex_source = self.sample_tex
        expected_res = [('run', "print('The random seed is ', seed)\n")]
        res = TexSurgery(tex_source).findall('run')
        self.assertEqual(res, expected_res)

    def test_find_all(self):
        """finds all apperances of a non nested environment
        that appears a few times.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('runsilent', """seed = 1\nset_random_seed(seed)\n"""),
            ('runsilent', """a = randint(1,10)\n"""),
            ('runsilent', """a = randint(2,10)\n"""),
            ('runsilent', """a = randint(2,10)\nf = sin(a*x)\nfd = f.derivative(x)\n"""),
        ]
        res = TexSurgery(tex_source).findall('runsilent')
        self.assertEqual(res, expected_res)

    def test_find_nested(self):
        """finds all apperances of a command nested inside
        an environment that appears once.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('choices', [('\correctchoice', '$\sage{fd}$')]),
        ]
        res = TexSurgery(tex_source).findall(r'choices \correctchoice')
        self.assertEqual(res, expected_res)

    def test_find_nested_2(self):
        """finds all apperances of a command nested inside
        an environment which is nested inside
        another environment that appears once.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('question', [
               ('choices', [('\correctchoice', '$\sage{fd}$')])
               ]),
        ]
        res = TexSurgery(tex_source).findall(r'question choices \correctchoice')
        self.assertEqual(res, expected_res)

        expected_res = [
          ('question',
            [('choices', [
                ('\wrongchoice', '$\sage{fd*a}$'),
                ('\wrongchoice', '$\sage{fd + a}$')])])
        ]
        res = TexSurgery(tex_source).findall(r'question choices \wrongchoice')
        self.assertEqual(res, expected_res)

    def test_find_comma_nested(self):
        """finds all apperances of a command nested inside an environment
        nested inside another environment which can be of two different types.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('question', [
               ('choices', [('\correctchoice', '$\sage{fd}$')])
               ]),
        ]
        res = TexSurgery(tex_source).findall(r'question,questionmultx choices \correctchoice')
        self.assertEqual(res, expected_res)

    def test_find_nested_comma_nested_mult(self):
        """finds all apperances of a command nested inside an environment
        which is nested inside another environment which can be of two different types.
        It matches the tex twice.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('questionmultx', [('runsilent', 'a = randint(1,10)\n')]),
            ('questionmultx', [('runsilent', 'a = randint(2,10)\n')]),
            ('question',
             [('runsilent', 'a = randint(2,10)\nf = sin(a*x)\nfd = f.derivative(x)\n')])
        ]
        res = TexSurgery(tex_source).findall('question,questionmultx runsilent')
        self.assertEqual(res, expected_res)

    def test_find_comma_alternatives(self):
        """tests a selector consisting of two selectors separated by a comma.
        """
        tex_source = self.sample_tex
        expected_res = (
            'question', [('choices', [('\correctchoice', '$\sage{fd}$')])]
        )
        res = TexSurgery(tex_source).find(r'question choices \correctchoice, questionmultx \AMCnumericChoices')
        self.assertEqual(res, expected_res)

    def test_findall_comma_alternatives(self):
        """tests a selector consisting of two selectors separated by a comma.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('question', [('choices', [('\correctchoice', '$\sage{fd}$')])]),
            ('questionmultx', [('\\AMCnumericChoices', '\\eval{8+a}')]),
            ('questionmultx', [('\\AMCnumericChoices', '\\eval{8*a}')])
        ]
        res = TexSurgery(tex_source).findall(r'question choices \correctchoice, questionmultx \AMCnumericChoices')
        self.assertEqual(res, expected_res)

    def test_find_command_with_two_arguments(self):
        """tests a selector consisting of a command with two mandatory arguments in braces {}.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('questionmultx',
             [('\\AMCnumericChoices',
                {'arg0':'\\eval{8+a}',
                 'arg1':'digits=2,sign=false,scoreexact=3'})]),
            ('questionmultx',
             [('\\AMCnumericChoices',
                {'arg0':'\\eval{8*a}',
                 'arg1':'digits=2,sign=false,scoreexact=3'})])
        ]
        res = TexSurgery(tex_source).findall(r'questionmultx \AMCnumericChoices[_nargs=2]')
        self.assertEqual(res, expected_res)

    def test_find_command_with_a_named_argument(self):
        """tests a selector consisting of a command with a named argument in braces {}.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('questionmultx',
             [('\\AMCnumericChoices',
                {'solution':'\\eval{8+a}',
                 'options':'digits=2,sign=false,scoreexact=3'})]),
            ('questionmultx',
             [('\\AMCnumericChoices',
                {'solution':'\\eval{8*a}',
                 'options':'digits=2,sign=false,scoreexact=3'})])
        ]
        res = TexSurgery(tex_source).findall(
            r'questionmultx \AMCnumericChoices{solution}{options}'
        )
        self.assertEqual(res, expected_res)

    def test_find_command_with_a_named_argument_and_nargs(self):
        """tests a selector consisting of a command with a named argument in braces {}.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('questionmultx',
             [('\\AMCnumericChoices',
                {'solution':'\\eval{8+a}',
                 'arg0':'digits=2,sign=false,scoreexact=3'})]),
            ('questionmultx',
             [('\\AMCnumericChoices',
                {'solution':'\\eval{8*a}',
                 'arg0':'digits=2,sign=false,scoreexact=3'})])
        ]
        res = TexSurgery(tex_source).findall(
            r'questionmultx \AMCnumericChoices{solution}[_nargs=1]'
        )
        self.assertEqual(res, expected_res)

    def test_find_mixed(self):
        """tests a mixed selector combining commas at two different levels
        """
        tex_source = self.sample_tex
        expected_res = (
            'questionmultx', [('\\AMCnumericChoices', '\\eval{8+a}')]
        )
        res = TexSurgery(tex_source).find(r'questionmultx,question \correctchoice,\AMCnumericChoices')
        self.assertEqual(res, expected_res)

    def test_findall_mixed(self):
        """tests a mixed selector combining commas at two different levels
        """
        tex_source = self.sample_tex
        expected_res = [
            ('questionmultx', [('\\AMCnumericChoices', '\\eval{8+a}')]),
            ('questionmultx', [('\\AMCnumericChoices', '\\eval{8*a}')]),
            ('question', [('\\correctchoice', '$\\sage{fd}$')])
        ]
        res = TexSurgery(tex_source).findall(r'questionmultx,question \correctchoice,\AMCnumericChoices')
        self.assertEqual(res, expected_res)

    def test_find_environment_with_argument(self):
        """finds all apperances of one environment with a named argument.
        """
        tex_source = self.sample_tex
        expected_res = [('question',
            {'questionid':'derivativesin'},
r'''\scoring{e=-0.5,b=1,m=-.25,p=-0.5}
\begin{runsilent}
a = randint(2,10)
f = sin(a*x)
fd = f.derivative(x)
\end{runsilent}
  What is the first derivative of $\sage{f}$?
  \begin{choices}
    \correctchoice{$\sage{fd}$}
    \wrongchoice{$\sage{fd*a}$}
    \wrongchoice{$\sage{fd + a}$}
  \end{choices}
'''
        )]
        res = TexSurgery(tex_source).findall('question{questionid}')
        self.assertEqual(res, expected_res)

    def test_find_exact_argument(self):
        """finds an environment with an exact text for a specific argument
        """
        tex_source = self.sample_tex
        expected_res = (
            'questionmultx',
            {'questionid':'basic-multiplication'},
            r'''\begin{runsilent}
a = randint(2,10)
\end{runsilent}
What is $8*\eval{a}$?
\AMCnumericChoices{\eval{8*a}}{digits=2,sign=false,scoreexact=3}
'''
        )
        res = TexSurgery(tex_source).find(r'questionmultx{questionid}[questionid=basic-multiplication]')
        self.assertEqual(res, expected_res)

    def test_find_command_with_square_and_curly_brackets(self):
        """finds a command with both mandatory and optional arguments
        """
        tex_source = self.sample_tex
        expected_res = (
            '\\documentclass',
            {'dtype':'article'}
        )
        res = TexSurgery(tex_source).find(r'\documentclass{dtype}')
        self.assertEqual(res, expected_res)
