Late - An RFC5545 iCalendar search and manipulation tool
========================================================

Late aims to be a search-based RFC5545 calendar management tool for the
command-line.

Initially, there's rudimentary boolean search for calendar events, scanning
across calendar files in the file system.

Late's another terrible excuse for being late.

Documentation
-------------

There's basic help via the command-line::

  python3 -m late --help

Dependencies
------------

- icalendar for parsing calendar data
- lark for parsing queries

License
-------

Late is free software, released under the `GNU GPL version 3`_.

.. _GNU GPL version 3: https://opensource.org/licenses/GPL-3.0
