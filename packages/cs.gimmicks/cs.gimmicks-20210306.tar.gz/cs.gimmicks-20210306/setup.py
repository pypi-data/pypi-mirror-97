#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.gimmicks',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20210306',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    ('Gimmicks and hacks to make some of my other modules more robust and less '    
 'demanding of others.'),
  long_description =
    ('Gimmicks and hacks to make some of my other modules more robust and\n'    
 'less demanding of others.\n'    
 '\n'    
 '*Latest release 20210306*:\n'    
 'Add simple implementations of nullcontext and SimpleNamespace.\n'    
 '\n'    
 '## Function `debug(*a, **kw)`\n'    
 '\n'    
 'Wrapper for `debug()` which does a deferred import.\n'    
 '\n'    
 '## Function `error(*a, **kw)`\n'    
 '\n'    
 'Wrapper for `error()` which does a deferred import.\n'    
 '\n'    
 '## Function `exception(*a, **kw)`\n'    
 '\n'    
 'Wrapper for `exception()` which does a deferred import.\n'    
 '\n'    
 '## Function `info(*a, **kw)`\n'    
 '\n'    
 'Wrapper for `info()` which does a deferred import.\n'    
 '\n'    
 '## Function `log(*a, **kw)`\n'    
 '\n'    
 'Wrapper for `log()` which does a deferred import.\n'    
 '\n'    
 '## Function `warning(*a, **kw)`\n'    
 '\n'    
 'Wrapper for `warning()` which does a deferred import.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20210306*:\n'    
 'Add simple implementations of nullcontext and SimpleNamespace.\n'    
 '\n'    
 '*Release 20200418.1*:\n'    
 'Initial release with logging call stubs.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.gimmicks'],
)
