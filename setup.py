# -*- coding:utf-8 -*-

import os
import sys


from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ''


install_requires = [
    'filegen',
]


docs_extras = [
]

tests_require = [
]

testing_extras = tests_require + [
]

setup(name='mypylint',
      version='0.1',
      description='individual pylint plugin scaffold',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: Implementation :: CPython",
      ],
      keywords='',
      author="podhmo",
      author_email="",
      url="https://github.com/podhmo/mypylint",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          'testing': testing_extras,
          'docs': docs_extras,
      },
      tests_require=tests_require,
      test_suite="mypylint.tests",
      entry_points="""
[console_scripts]
mypylint = mypylint:main
""")

