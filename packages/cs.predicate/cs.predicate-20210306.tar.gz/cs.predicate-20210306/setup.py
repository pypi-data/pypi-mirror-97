#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.predicate',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20210306',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'fnctions for expressing predicates',
  long_description =
    ('Trite support for code predicates, presently just the context manager '    
 '`post_condition`.\n'    
 '\n'    
 '*Latest release 20210306*:\n'    
 'Package install_requires fix.\n'    
 '\n'    
 'Interested people should also see the `icontract` module.\n'    
 '\n'    
 '## Function `post_condition(*predicates)`\n'    
 '\n'    
 'Context manager to test post conditions.\n'    
 '\n'    
 'Predicates may either be a tuple of `(description,callable)`\n'    
 'or a plain callable.\n'    
 'For the latter the description is taken from `callable.__doc__`\n'    
 'or `str(callable)`.\n'    
 'Raises `AssertionError` if any predicates are false.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20210306*:\n'    
 'Package install_requires fix.\n'    
 '\n'    
 '*Release 20190221*:\n'    
 'One bugfix, other tiny changes.\n'    
 '\n'    
 '*Release 20160828*:\n'    
 'Use "install_requires" instead of "requires" in DISTINFO.\n'    
 '\n'    
 '*Release 20160827*:\n'    
 'Initial release with post_condition context manager.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = ['cs.logutils', 'cs.pfx'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.predicate'],
)
