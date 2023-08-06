#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.configutils',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20210306',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'utility functions for .ini style configuration files',
  long_description =
    ('Utility functions and classes for configuration files.\n'    
 '\n'    
 '*Latest release 20210306*:\n'    
 'Fix imports from collections.abc.\n'    
 '\n'    
 '## Class '    
 '`ConfigSectionWatcher(collections.abc.Mapping,collections.abc.Collection,collections.abc.Sized,collections.abc.Iterable,collections.abc.Container)`\n'    
 '\n'    
 'A class for monitoring a particular clause in a config file.\n'    
 '\n'    
 '### Method `ConfigSectionWatcher.__init__(self, config, section, '    
 'defaults=None)`\n'    
 '\n'    
 'Initialise a ConfigSectionWatcher to monitor a particular section\n'    
 'of a config file.\n'    
 '`config`: path of config file, or ConfigWatcher\n'    
 '`section`: the section to watch\n'    
 "`defaults`: the defaults section to use, default 'DEFAULT'\n"    
 '\n'    
 '### Method `ConfigSectionWatcher.__getitem__(self, key)`\n'    
 '\n'    
 '#### Mapping methods.\n'    
 '\n'    
 '### Method `ConfigSectionWatcher.as_dict(self)`\n'    
 '\n'    
 'Return the config section as a dict.\n'    
 '\n'    
 '### Method `ConfigSectionWatcher.keys(self)`\n'    
 '\n'    
 'Return the keys of the config section.\n'    
 '\n'    
 '### Property `ConfigSectionWatcher.path`\n'    
 '\n'    
 'The pathname of the config file.\n'    
 '\n'    
 '## Class '    
 '`ConfigWatcher(collections.abc.Mapping,collections.abc.Collection,collections.abc.Sized,collections.abc.Iterable,collections.abc.Container)`\n'    
 '\n'    
 'A monitor for a windows style .ini file.\n'    
 'The current SafeConfigParser object is presented as the .config property.\n'    
 '\n'    
 '### Method `ConfigWatcher.__getitem__(self, *a, **kw)`\n'    
 '\n'    
 'Return the ConfigWatcher for the specified section.\n'    
 '\n'    
 '### Method `ConfigWatcher.as_dict(self)`\n'    
 '\n'    
 'Construct and return a dictionary containing an entry for each section\n'    
 'whose value is a dictionary of section items and values.\n'    
 '\n'    
 '### Property `ConfigWatcher.config`\n'    
 '\n'    
 'Inner wrapper for `func`.\n'    
 '\n'    
 '### Property `ConfigWatcher.path`\n'    
 '\n'    
 'The path to the config file.\n'    
 '\n'    
 '### Method `ConfigWatcher.section_keys(self, section)`\n'    
 '\n'    
 'Return the field names for the specified section.\n'    
 '\n'    
 '### Method `ConfigWatcher.section_value(self, section, key)`\n'    
 '\n'    
 'Return the value of [section]key.\n'    
 '\n'    
 '## Function `load_config(config_path, parser=None)`\n'    
 '\n'    
 'Load a configuration from the named `config_path`.\n'    
 '\n'    
 'If `parser` is missing or None, use SafeConfigParser (just\n'    
 'ConfigParser in Python 3).\n'    
 'Return the parser.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20210306*:\n'    
 'Fix imports from collections.abc.\n'    
 '\n'    
 '*Release 20190101*:\n'    
 'Internal changes.\n'    
 '\n'    
 '*Release 20160828*:\n'    
 'Update metadata with "install_requires" instead of "requires".\n'    
 '\n'    
 '*Release 20150118*:\n'    
 'Initial PyPI release.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = ['cs.py3', 'cs.fileutils', 'cs.threads'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.configutils'],
)
