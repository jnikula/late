# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2017-2019 Jani Nikula <jani@nikula.org>

import os
import sys

import icalendar as ical

def parse_string(log, vevents, icalstr, filename):
    log.debug('parsing file {filename}'.format(filename=filename))

    try:
        components = ical.Calendar.from_ical(icalstr, multiple=True)
    except ValueError as e:
        log.warn('{filename}: {error}'.format(filename=filename, error=str(e)))
        return
    except Exception as e:
        log.warn('{filename}: ical {error}'.format(filename=filename,
                                                   error=str(e)))
        return

    for component in components:
        # FIXME: wrap in a vcalendar
        if component.name != 'VCALENDAR':
            log.warn('{filename}: {component} outside of vcalendar'.format(
                filename=filename, component=component.name))

        # FIXME: preserve other stuff than vevents, only filter output
        # FIXME: preserve vtimezone

        for vevent in component.walk('vevent'):
            uid = str(vevent['uid'])
            vevent.filename = filename
            if uid in vevents:
                # FIXME: this is pretty silly, find a better way
                for ve in vevents[uid]:
                    if vevent.to_ical() == ve.to_ical():
                        log.debug('duplicate vevent {uid}'.format(uid=uid))
                        break
                    elif str(vevent['sequence']) == str(ve['sequence']):
                        # same uid, same sequence, different contents
                        log.warn('duplicate sequence {uid}'.format(uid=uid))
                else:
                    vevents[uid].append(vevent)
            else:
                vevents[uid] = [vevent]

def parse_filename(log, vevents, filename):
    with open(filename, 'r') as f:
        parse_string(log, vevents, f.read(), filename)

def scan(log, paths):
    # FIXME: potentially wrap events into something that contains:
    # - parent vcalendar
    # - filename
    vevents = {}

    stdin_parsed = False
    for path in paths:
        if path == '-':
            if not stdin_parsed:
                parse_string(log, vevents, sys.stdin.read(), '<stdin>')
                stdin_parsed = True
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for f in files:
                    parse_filename(log, vevents, os.path.join(root, f))
        else:
            parse_filename(log, vevents, path)

    return vevents
