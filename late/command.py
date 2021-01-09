# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2017-2019 Jani Nikula <jani@nikula.org>

"""
Late, another terrible excuse.

An RFC5545 iCalendar search and manipulation tool.
"""

import inspect
import logging
import datetime

import icalendar as ical

from late.parse import scan
from late.query import search, debug

#
# Globals.
#

late = 'late'

logging.basicConfig(format='%(name)s: %(levelname)s: %(message)s',
                    level=logging.INFO)
log = logging.getLogger(late)


def sort_key_date(vevents, uid):
    vevent = vevents[uid][0]
    dtstart = vevent.get('dtstart')
    if not dtstart:
        return 0
    if isinstance(dtstart.dt, datetime.datetime):
        return dtstart.dt.timestamp()
    return 0

#
# Subcommands.
#

def print_uid(vevents, uid):
    print('uid:{}'.format(uid))

def print_oneline(vevents, uid):
    vevent = vevents[uid][0]

    summary = vevent.get('summary')
    if not summary:
        # only first line
        summary = vevent.get('description')
        if not summary:
            summary = uid

    dtstart = vevent.get('dtstart')
    if dtstart:
        if isinstance(dtstart.dt, datetime.datetime):
            dtstart = dtstart.dt.astimezone()
        else:
            dtstart = dtstart.dt
    else:
        dtstart = '<unknown>'

    dtend = vevent.get('dtend')
    if dtend:
        if isinstance(dtend.dt, datetime.datetime):
            dtend = dtend.dt.astimezone()
        else:
            dtend = dtend.dt
    else:
        dtend = '<unknown>'

    print('{} {} {}'.format(dtstart, dtend, summary))

def print_pretty(vevents, uid):
    for vevent in vevents[uid]:
        dtstart = vevent.get('dtstart')
        dtend = vevent.get('dtend')
        summary = vevent.get('summary')
        description = vevent.get('description')

        if summary:
            print(summary)
        else:
            print(uid)
        if dtstart:
            if isinstance(dtstart.dt, datetime.datetime):
                print(dtstart.dt.astimezone())
            else:
                print(dtstart.dt)
        if dtend:
            if isinstance(dtend.dt, datetime.datetime):
                print(dtend.dt.astimezone())
            else:
                print(dtend.dt)
        if description:
            print(description)

printers = {
    'uid': print_uid,
    'pretty': print_pretty,
    'oneline': print_oneline,
}

def late_explain(query):
    """
    Debug query language.
    """

    print(debug(query))

# Main search function, others are just with different defaults.
def late_search(source, query, output):
    """
    Search events.
    """

    vevents = scan(log, source)
    results = search(vevents, query)

    results.sort(key=lambda uid: sort_key_date(vevents, uid))

    for uid in results:
        printers[output](vevents, uid)

def late_pretty(source, query, output):
    """
    Pretty print events.

    Print a nice representation of events.
    """

    late_search(source, query, output)

def late_dump(source, query):
    """
    Dump all raw.
    """

    vevents = scan(log, source)
    results = search(vevents, query)

    cal = ical.Calendar()
    cal.add('prodid', late)
    cal.add('version', '2.0')

    for uid in results:
        for vevent in vevents[uid]:
            cal.add_component(vevent)

    print(cal.to_ical().decode('utf-8'), end='')

def list_commands():
    prefix = late + '_'
    subcommands = [(n[len(prefix):], o)
                   for n, o in globals().items()
                   if inspect.isfunction(o) and n.startswith(prefix)]

    return sorted(subcommands)
