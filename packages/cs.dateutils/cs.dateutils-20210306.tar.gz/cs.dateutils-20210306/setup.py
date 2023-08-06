#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.dateutils',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20210306',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'A few conveniences to do with dates and times.',
  long_description =
    ('A few conveniences to do with dates and times.\n'    
 '\n'    
 '*Latest release 20210306*:\n'    
 'Initial release, used by cs.sqltags.\n'    
 '\n'    
 'There are some other PyPI modules providing richer date handling\n'    
 'than the stdlib `datetime` module.\n'    
 'This module mostly contains conveniences used in my other code;\n'    
 "you're welcome to it, but it does not pretend to be large or complete.\n"    
 '\n'    
 '## Function `datetime2unixtime(dt)`\n'    
 '\n'    
 'Convert a `datetime` to a UNIX timestamp.\n'    
 '\n'    
 '*Note*: unlike `datetime.timestamp`,\n'    
 'if the `datetime` is naive\n'    
 'it is presumed to be in UTC rather than the local timezone.\n'    
 '\n'    
 '## Function `isodate(when=None, dashed=True)`\n'    
 '\n'    
 'Return a date in ISO8601 YYYY-MM-DD format, or YYYYMMDD if not `dashed`.\n'    
 '\n'    
 'Modern Pythons have a `datetime.isoformat` method, use that.\n'    
 '\n'    
 '## Function `localdate2unixtime(d)`\n'    
 '\n'    
 'Convert a localtime `date` into a UNIX timestamp.\n'    
 '\n'    
 '## Class `tzinfoHHMM(datetime.tzinfo)`\n'    
 '\n'    
 'tzinfo class based on +HHMM / -HHMM strings.\n'    
 '\n'    
 '## Function `unixtime2datetime(unixtime, tz=None)`\n'    
 '\n'    
 'Convert a a UNIX timestamp to a `datetime`.\n'    
 '\n'    
 '*Note*: unlike `datetime.fromtimestamp`,\n'    
 'if `tz` is `None` the UTC timezone is used.\n'    
 '\n'    
 '## Class `UNIXTimeMixin`\n'    
 '\n'    
 'A mixin for classes with a `.unixtime` attribute,\n'    
 'a `float` storing a UNIX timestamp.\n'    
 '\n'    
 '### Method `UNIXTimeMixin.as_datetime(self, tz=None)`\n'    
 '\n'    
 'Return `self.unixtime` as a `datetime` with the timezone `tz`.\n'    
 '\n'    
 '*Note*: unlike `datetime.fromtimestamp`,\n'    
 'if `tz` is `None` the UTC timezone is used.\n'    
 '\n'    
 '### Property `UNIXTimeMixin.datetime`\n'    
 '\n'    
 'The `unixtime` as a UTC `datetime`.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20210306*:\n'    
 'Initial release, used by cs.sqltags.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = [],
  keywords = ['date', 'time', 'datetime', 'python', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.dateutils'],
)
