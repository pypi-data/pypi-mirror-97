#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.app.mklinks',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20210306',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'Tool for finding and hardlinking identical files.',
  long_description =
    ('mklinks: tool for finding and hardlinking identical files\n'    
 '\n'    
 '*Latest release 20210306*:\n'    
 'Use cs.cmdutils.BaseCommand for main programme, add better progress '    
 'reporting.\n'    
 '\n'    
 'Mklinks walks supplied paths looking for files with the same content,\n'    
 'based on a cryptographic checksum of their content. It hardlinks\n'    
 'all such files found, keeping the newest version.\n'    
 '\n'    
 'Unlike some rather naive tools out there, mklinks only compares\n'    
 'files with other files of the same size, and is hardlink aware - a\n'    
 'partially hardlinked tree is processed efficiently and correctly.\n'    
 '\n'    
 '## Class `FileInfo`\n'    
 '\n'    
 'Information about a particular inode.\n'    
 '\n'    
 '### Method `FileInfo.assimilate(self, other, no_action=False)`\n'    
 '\n'    
 'Link our primary path to all the paths from `other`. Return success.\n'    
 '\n'    
 '### Method `FileInfo.same_dev(self, other)`\n'    
 '\n'    
 'Test whether two FileInfos are on the same filesystem.\n'    
 '\n'    
 '### Method `FileInfo.same_file(self, other)`\n'    
 '\n'    
 'Test whether two FileInfos refer to the same file.\n'    
 '\n'    
 '### Method `FileInfo.stat_key(S)`\n'    
 '\n'    
 'Compute the key `(dev,ino)` from the stat object `S`.\n'    
 '\n'    
 '## Class `Linker`\n'    
 '\n'    
 'The class which links files with identical content.\n'    
 '\n'    
 '### Method `Linker.addpath(self, path)`\n'    
 '\n'    
 'Add a new path to the data structures.\n'    
 '\n'    
 '### Method `Linker.merge(self, *a, **kw)`\n'    
 '\n'    
 'Merge files with equivalent content.\n'    
 '\n'    
 '### Method `Linker.scan(self, *a, **kw)`\n'    
 '\n'    
 'Scan the file tree.\n'    
 '\n'    
 '## Function `main(argv=None)`\n'    
 '\n'    
 'Main command line programme.\n'    
 '\n'    
 '## Class `MKLinksCmd(cs.cmdutils.BaseCommand)`\n'    
 '\n'    
 'Main programme command line class.\n'    
 '\n'    
 '### Method `MKLinksCmd.apply_defaults(self)`\n'    
 '\n'    
 'Set up the default values in `options`.\n'    
 '\n'    
 '### Method `MKLinksCmd.apply_opts(self, opts)`\n'    
 '\n'    
 'Apply command line options.\n'    
 '\n'    
 '### Method `MKLinksCmd.main(self, argv)`\n'    
 '\n'    
 'Usage: mklinks [-n] paths...\n'    
 'Hard link files with identical contents.\n'    
 '-n    No action. Report proposed actions.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20210306*:\n'    
 'Use cs.cmdutils.BaseCommand for main programme, add better progress '    
 'reporting.\n'    
 '\n'    
 '*Release 20171228*:\n'    
 'Initial PyPI release of cs.app.mklinks.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  entry_points = {'console_scripts': ['mklinks = cs.app.mklinks:main']},
  install_requires = ['cs.cmdutils', 'cs.fileutils>=20200914', 'cs.logutils', 'cs.pfx', 'cs.progress>=20200718.3', 'cs.py.func', 'cs.units', 'cs.upd>=20200914'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.app.mklinks'],
)
