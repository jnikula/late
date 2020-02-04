#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2017-2019 Jani Nikula <jani@nikula.org>

import os
import sys
import unittest

testdir = os.path.dirname(os.path.abspath(__file__))
rootdir = os.path.dirname(testdir)

sys.path.insert(0, rootdir)

from late.query import QueryParser, QueryDebug

class QueryParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = QueryParser()

    def parse(self, query):
        tree = self.parser.parse(query)
        return QueryDebug().transform(tree)

    def test_basic(self):
        self.assertEqual(self.parse('foo'), '(foo)')

    def test_basic_empty(self):
        self.assertEqual(self.parse(''), '')
        self.assertEqual(self.parse(' '), '')
        self.assertEqual(self.parse('  \t '), '')

    def test_basic_operators(self):
        self.assertEqual(self.parse('foo and bar'), '((foo) AND (bar))')
        self.assertEqual(self.parse('foo or bar'), '((foo) OR (bar))')
        self.assertEqual(self.parse('not foo'), '(NOT (foo))')

    def test_basic_precedence(self):
        self.assertEqual(self.parse('foo and bar or baz'),
                         '(((foo) AND (bar)) OR (baz))')
        self.assertEqual(self.parse('foo or bar and baz'),
                         '((foo) OR ((bar) AND (baz)))')

        self.assertEqual(self.parse('not foo and not bar or not baz'),
                         '(((NOT (foo)) AND (NOT (bar))) OR (NOT (baz)))')
        self.assertEqual(self.parse('not foo or not bar and not baz'),
                         '((NOT (foo)) OR ((NOT (bar)) AND (NOT (baz))))')

        self.assertEqual(self.parse('foo and bar and baz'),
                         '(((foo) AND (bar)) AND (baz))')
        self.assertEqual(self.parse('foo or bar or baz'),
                         '(((foo) OR (bar)) OR (baz))')

    def test_parens(self):
        self.assertEqual(self.parse('(foo)'), '(foo)')
        self.assertEqual(self.parse('((foo))'), '(foo)')

        self.assertEqual(self.parse('(foo and bar) or baz'),
                         '(((foo) AND (bar)) OR (baz))')
        self.assertEqual(self.parse('foo or (bar and baz)'),
                         '((foo) OR ((bar) AND (baz)))')

        self.assertEqual(self.parse('foo and (bar or baz)'),
                         '((foo) AND ((bar) OR (baz)))')
        self.assertEqual(self.parse('(foo or bar) and baz'),
                         '(((foo) OR (bar)) AND (baz))')

    def test_quotes(self):
        self.assertEqual(self.parse('"foo"'), '(foo)')
        self.assertEqual(self.parse('("foo")'), '(foo)')

        self.assertEqual(self.parse('"foo and" and bar'),
                         '((foo and) AND (bar))')

        self.assertEqual(self.parse('"foo or" or bar'),
                         '((foo or) OR (bar))')

        self.assertEqual(self.parse('"or"'), '(or)')
        self.assertEqual(self.parse('"and"'), '(and)')
        self.assertEqual(self.parse('"not"'), '(not)')

    def test_basic_operators_space(self):
        self.assertEqual(self.parse('foo bar'), '((foo) AND (bar))')
        self.assertEqual(self.parse('foo or bar'), '((foo) OR (bar))')
        self.assertEqual(self.parse('not foo'), '(NOT (foo))')

    def test_basic_precedence_space(self):
        self.assertEqual(self.parse('foo bar or baz'),
                         '(((foo) AND (bar)) OR (baz))')
        self.assertEqual(self.parse('foo or bar baz'),
                         '((foo) OR ((bar) AND (baz)))')

        self.assertEqual(self.parse('not foo not bar or not baz'),
                         '(((NOT (foo)) AND (NOT (bar))) OR (NOT (baz)))')
        self.assertEqual(self.parse('not foo or not bar not baz'),
                         '((NOT (foo)) OR ((NOT (bar)) AND (NOT (baz))))')

        self.assertEqual(self.parse('foo bar baz'),
                         '(((foo) AND (bar)) AND (baz))')
        self.assertEqual(self.parse('foo or bar or baz'),
                         '(((foo) OR (bar)) OR (baz))')

    def test_operator_matching(self):
        self.assertEqual(self.parse('more and hand'),
                         '((more) AND (hand))')

        self.assertEqual(self.parse('(foo or bar) (bar or baz)'),
                         '(((foo) OR (bar)) AND ((bar) OR (baz)))')

        self.assertEqual(self.parse('(foo bar) (bar or baz)'),
                         '(((foo) AND (bar)) AND ((bar) OR (baz)))')

        self.assertEqual(self.parse('"or" and "not"'),
                         '((or) AND (not))')

    def test_parens_space(self):
        self.assertEqual(self.parse('(foo bar) or baz'),
                         '(((foo) AND (bar)) OR (baz))')
        self.assertEqual(self.parse('foo or (bar baz)'),
                         '((foo) OR ((bar) AND (baz)))')

        self.assertEqual(self.parse('foo (bar or baz)'),
                         '((foo) AND ((bar) OR (baz)))')
        self.assertEqual(self.parse('(foo or bar) baz'),
                         '(((foo) OR (bar)) AND (baz))')

    def test_quotes_space(self):
        self.assertEqual(self.parse('"foo" "bar"'), '((foo) AND (bar))')
        self.assertEqual(self.parse('("foo") "foo bar"'),
                         '((foo) AND (foo bar))')

        self.assertEqual(self.parse('"foo and" bar'),
                         '((foo and) AND (bar))')

        self.assertEqual(self.parse('"foo or" or bar'),
                         '((foo or) OR (bar))')

    def test_prefix(self):
        self.assertEqual(self.parse('foo:bar'), '(foo:bar)')
        self.assertEqual(self.parse('foo:"foo bar"'), '(foo:foo bar)')

    def test_unicode(self):
        self.assertEqual(self.parse('"pyöreä"'), '(pyöreä)')

if __name__ == '__main__':
    unittest.main()
