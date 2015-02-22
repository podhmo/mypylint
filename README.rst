mypylint
========================================

mypylint is pylint plugin scaffold.
If you want to custom pylint plugin for you project, mypylint is helpful, maybe.

features

- skipping matched module(regex pattern match)
- injecting fake specification



how to use
----------------------------------------

calling `mypylint` command.

.. code-block:: bash

 $ mypyrint myplugin .

this command is generating a skeleton for your pylint plugin.

.. code-block:: bash

 $ tree myplugin

   .
  ├── __init__.py
  └── myplugin
      ├── README.rst
      ├── __init__.py
      ├── myplugin
      │   ├── __init__.py
      │   ├── fakes
      │   │   ├── __init__.py
      │   │   └── foo_bar_boo.py
      │   ├── ignore.py
      │   ├── injection.py
      │   ├── plugin.py
      │   └── transforms
      │       └── __init__.py
      └── setup.py

  4 directories, 11 files

and install generate package via `python setup.py develop`. and using with pylint.

.. code-block:: bash

  $ cd myplugin
  $ python setup.py develop
  $ ../
  $ pylint --load-plugins=myplugin <yourapp>

features
----------------------------------------

skipping matched module(regex pattern match)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

in myplugin/plugin.py. It is enable to `ignore.register_ignore_module_pattern()`

.. code-block:: python

  def register(linter, manager=MANAGER):
      transforms.register_transforms(manager)
      fakes.register_transforms(manager)

      # if you want to ignore test module, this function is useful.
      ignore.register_ignore_module_pattern(manager, ".+\.tests?\..+") # this is!

The setting, such as above, can ignore "foo.tests.bar", "boo.tests.test_foo", .. and so on.


injecting fake specification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your pylint command output is annoying messy ouput with "no-member".
(Are you using metaprogramming, right?)

.. code-block:: bash

  $ pylint -E foo/apps.py
  ************* Module demo.app
  E:  9,38: Instance of 'Foo' has no 'name' member (no-member)
  E: 22, 0: Instance of 'Bar' has no 'hey' member (no-member)

foo/app.py is this.

.. code-block:: python

  class Foo(object):
      def __init__(self):
          setattr(self, "name", "foo")

      def hello(self):
          return "{name}: hello".format(self.name)


  def hey(cls):
      cls.hey = lambda self: print("hey")
      return cls


  @hey
  class Bar:
      pass

  Bar().hey("hello")  # too many argument!!

We want to suppress annoying message such as above, and you can patching fake specification.

(the file name is IMPORTANT!!. if you want to patch at foo.app.py module, then you add fakes/foo_app.py.)

myplugin/fakes/foo_app.py.

.. code-block:: python

  class Foo:
      name = None

  class Bar:
      def hey(self):
          pass

and pylint with `load-plugins=mypylint`, it is responding with expected output.

.. code-block:: bash

  $ pylint -E --load-plugins=myplugin foo/app.py
  ************* Module demo.foo.app
  E: 22, 0: Too many positional arguments for method call (too-many-function-args)
