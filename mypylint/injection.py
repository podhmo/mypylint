# -*- coding:utf-8 -*-
"""
heavily inspired from below.

- Helping pylint to understand things it doesn't (Logilab.org) (http://www.logilab.org/blogentry/78354)
- pylint-django/__init__.py at master · landscapeio/pylint-django (https://github.com/landscapeio/pylint-django/blob/master/pylint_django/transforms/__init__.py)
"""

import os.path
from astroid.builder import AstroidBuilder
from astroid import nodes
from astroid import MANAGER
import sys


def register(manager, d, filename):
    package_name = filename.replace(".py", "").replace("_", ".")
    sys.stderr.write("register fake: package={}\n".format(package_name))

    filepath = os.path.join(d, filename)

    with open(filepath) as rf:
        fake_module = rf.read()
        fake = AstroidBuilder(manager).string_build(fake_module)

    def set_fake_locals(module, fake=fake):
        if module.name == package_name:
            return

        def rec_set(target, fake):
            if not hasattr(fake, "locals"):
                return
            for name in fake.locals:
                if name not in target.locals:
                    target.locals[name] = fake.locals[name]
                else:
                    rec_set(target.locals[name][0], fake.locals[name][0])
        rec_set(module, fake)
    manager.register_transform(nodes.Module, set_fake_locals)


def register_fake_module(transforms_dir, manager=MANAGER):
    for f in os.listdir(transforms_dir):
        if os.path.isdir(f):
            continue
        if f.startswith(("_", ".")):
            continue
        if f == "__init__.py":
            continue
        if f.endswith(".py"):
            register(manager, transforms_dir, f)
