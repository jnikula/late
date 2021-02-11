# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2017-2019 Jani Nikula <jani@nikula.org>

import os
import setuptools

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'late/VERSION')) as version_file:
    version = version_file.read().strip()

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'README.rst')) as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name = 'late',
    version = version,
    author = 'Jani Nikula',
    author_email = 'jani@nikula.org',
    license = 'GPLv3+',
    description = 'Late - Search Based Calendar Manager',
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    url = 'https://github.com/jnikula/late',
    packages = setuptools.find_packages(include = [
        'late',
        'late.*',
    ]),
    package_data = {
        'late': ['VERSION'],
    },
    install_requires = [
        'icalendar',
        'lark-parser',
    ],
    python_requires = '~=3.4',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'late=late.__main__:main'
        ],
    },
    keywords = 'calendar icalendar ical vcal command-line search tool',
)
