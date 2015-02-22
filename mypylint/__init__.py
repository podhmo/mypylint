# -*- coding:utf-8 -*-
from filegen import Filegen


def source_code(fg):
    with fg.file("__init__.py") as wf:
        wf.write("""\
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from . import plugin

register = plugin.register""")
    with fg.file("plugin.py") as wf:
        wf.write("""\
# -*- coding:utf-8 -*-
from . import transforms
from . import fakes
from astroid import MANAGER


def register(linter, manager=MANAGER):
    transforms.register_transforms(manager)
    fakes.register_transforms(manager)""")

    with fg.dir("transforms"):
        with fg.file("__init__.py") as wf:
            wf.write("""\
def register_transforms(manager):
    pass""")
    with fg.file("injection.py") as wf:
        import inspect
        from mypylint import injection
        with open(inspect.getsourcefile(injection)) as rf:
            wf.write(rf.read())

    with fg.dir("fakes"):
        with fg.file("foo_bar_boo.py") as wf:
            wf.write("""\
# used by register_fake_module()
class Dummy:
    id = None
""")
        with fg.file("__init__.py") as wf:
            wf.write("""\
import os.path
from ..injection import register_fake_module

# if you patching information with fake file.
# package name = "foo.bar.boo"
# then creating "./foo_bar_boo.py"


def register_transforms(manager):
    transforms_dir = os.path.dirname(__file__)
    register_fake_module(transforms_dir, manager)
""")


def setup_code(fg, name):
    with fg.file("README.rst") as wf:
        wf.write("""\
{name}
========================================
""".format(name=name))

    with fg.file("setup.py") as wf:
        wf.write("""\
# -*- coding:utf-8 -*-
import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
except IOError:
    README = ''


install_requires = [
    'pylint',
    'pylint-plugin-utils',
]

setup(name='{name}',
      version='0.1',
      description="pylint individual plugin",
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: Implementation :: CPython",
      ],
      keywords='',
      author="",
      author_email="",
      url="",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires)
""".format(name=name))


def mypylint(name):
    normalized = name.replace("-", "_")
    fg = Filegen(normalized)
    with fg.dir(normalized):
        with fg.dir(normalized):
            source_code(fg)
        setup_code(fg, name)
    return fg


def main():
    import sys
    _, name, path = sys.argv
    fg = mypylint(name)
    fg.to_python_module(path)
