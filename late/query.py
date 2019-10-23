# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2017-2019 Jani Nikula <jani@nikula.org>

import lark

query_grammar = '''
?start: or_expr
| empty_query

?or_expr: [or_expr _OR] and_expr

?and_expr: [and_expr _AND] term

?term: query
| _NOT term -> not_expr
| "(" or_expr ")"

_AND: [_WHITESPACE "and"i] _WHITESPACE

_OR: _WHITESPACE "or"i _WHITESPACE

_NOT: "not"i _WHITESPACE

_WHITESPACE: /[ \t]+/i

?empty_query: -> op_empty
| _WHITESPACE -> op_empty

?query: string -> op_query
| prefix ":" string -> op_prefix_query

?prefix: /[a-zA-Z0-9-]+/

?string: quoted_string | plain_string

quoted_string: ESCAPED_STRING

?plain_string: /(?!(or|and|not))[a-z0-9.@_-]+/i

%import common.ESCAPED_STRING
'''

class QueryParser(lark.Lark):
    def __init__(self):
        super().__init__(query_grammar)

class Query(lark.InlineTransformer):
    def __init__(self, vevents={}):
        self.vevents = vevents
        super().__init__()

    def quoted_string(self, s):
        return s[1:-1].replace('\\"', '"')

    def and_expr(self, x, y):
        return x & y

    def or_expr(self, x, y):
        return x | y

    def not_expr(self, x):
        return set(self.vevents.keys()) - x

    def op_empty(self):
        return set(self.vevents.keys())

    def op_query(self, x):
        results = set()
        if x == '':
            return set(self.vevents.keys())
        for uid, vevent_list in self.vevents.items():
            for vevent in vevent_list:
                for attr in ['summary', 'description']:
                    if x in str(vevent.get(attr, '')):
                        results.add(uid)
                        break

        return results

    def op_prefix_query(self, prefix, x):
        results = set()

        for uid, vevent_list in self.vevents.items():
            for vevent in vevent_list:
                if x != '' and x in str(vevent.get(prefix, '')):
                    results.add(uid)
                elif x == '' and not vevent.has_key(prefix):
                    results.add(uid)

        return results

class QueryDebug(Query):
    def or_expr(self, x, y):
        return '({x} OR {y})'.format(x=x, y=y)

    def and_expr(self, x, y):
        return '({x} AND {y})'.format(x=x, y=y)

    def not_expr(self, x):
        return '(NOT {x})'.format(x=x)

    def op_empty(self):
        return ''

    def op_query(self, x):
        return '({x})'.format(x=x)

    def op_prefix_query(self, prefix, x):
        return '({prefix}:{x})'.format(prefix=prefix, x=x)

# return a list of uid based on query
def search(vevents, query):
    query = ' '.join(query)
    parser = QueryParser()
    tree = parser.parse(query)

    # if log.isEnabledFor(logging.DEBUG):
    #     log.debug('parse tree:\n' + tree.pretty())
    #     log.debug(QueryDebug().transform(tree))

    results = Query(vevents).transform(tree)

    return list(results)

# Meh, dedupe this with the above
def debug(query):
    query = ' '.join(query)
    parser = QueryParser()
    tree = parser.parse(query)

    return QueryDebug().transform(tree)
