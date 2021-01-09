# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2019 Jani Nikula <jani@nikula.org>

def _match(vevent, value):
    for attr in ['summary', 'description']:
        if value in str(vevent.get(attr, '')):
            return True

    return False

def _prefix_match(vevent, prefix, value):
    # 'foo:' matches if vevent has no foo field
    # FIXME: should this apply to *all* prefix queries?
    if not value:
        return not vevent.has_key(prefix)

    return value in str(vevent.get(prefix, ''))

def _exact_prefix_match(vevent, prefix, value):
    return vevent.has_key(prefix) and value == str(vevent.get(prefix))

prefix_queries = {
    'uid': _exact_prefix_match,
    'status': _exact_prefix_match,
}

def vevent_match(vevent, prefix, value):
    if prefix:
        prefix = prefix.lower()
        queryfn = prefix_queries.get(prefix, _prefix_match)
        return queryfn(vevent, prefix, value)
    else:
        return _match(vevent, value)
