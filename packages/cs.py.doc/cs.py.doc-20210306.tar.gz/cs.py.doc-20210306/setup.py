#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py.doc',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20210306',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'Create documentation from python modules and other objects.',
  long_description =
    ('Create documentation from python modules and other objects.\n'    
 '\n'    
 '*Latest release 20210306*:\n'    
 'Drop noise leaked into output.\n'    
 '\n'    
 '## Function `is_dunder(name)`\n'    
 '\n'    
 'Test whether a name is a dunder name (`__`*foo*`__`).\n'    
 '\n'    
 '## Function `module_doc(module, *, sort_key=<function <lambda> at '    
 '0x10922e280>, filter_key=<function <lambda> at 0x10922e310>, '    
 'method_names=None)`\n'    
 '\n'    
 'Fetch the docstrings from a module and assemble a MarkDown document.\n'    
 '\n'    
 'Parameters:\n'    
 '* `module`: the module or module name to inspect\n'    
 '* `sort_key`: optional key for sorting names in the documentation;\n'    
 '  default: `name`\n'    
 '* filter_key`: optional test for a key used to select or reject keys\n'    
 '  to appear in the documentation\n'    
 '\n'    
 '## Function `obj_docstring(obj)`\n'    
 '\n'    
 'Return a docstring for `obj` which has been passed through '    
 '`stripped_dedent`.\n'    
 '\n'    
 'This function uses `obj.__doc__` if it is not `None`,\n'    
 'otherwise `getcomments(obj)` if that is not `None`,\n'    
 "otherwise `''`.\n"    
 'The chosen string is passed through `stripped_dedent` before return.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20210306*:\n'    
 'Drop noise leaked into output.\n'    
 '\n'    
 '*Release 20210123*:\n'    
 '* module_doc: include properties/descriptors.\n'    
 '* DISTINFO: this is not Python 2 compatible, drop tag.\n'    
 '\n'    
 '*Release 20200718*:\n'    
 '* New is_dunder(name) function to test whether name is a dunder name.\n'    
 '* module_doc: new method_names parameter to report only specific attributes '    
 'from a class - default is all public names and most dunder methods - things '    
 'without docs are not reported.\n'    
 '* Assorted small changes.\n'    
 '\n'    
 '*Release 20200521*:\n'    
 'Initial PyPI release.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = ['cs.lex', 'cs.logutils', 'cs.pfx', 'cs.py.modules'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.py.doc'],
)
