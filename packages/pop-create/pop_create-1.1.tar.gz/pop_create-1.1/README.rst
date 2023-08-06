==========
pop-create
==========

pop-create was originally an internal function of the pop project named
pop-seed.

pop-create will initialize a new pop project.


Geting Started
==============

.. code-block:: bash

    pip3 install pop-create

Now that you have pop-create installed you can run:


.. code-block:: bash

    pop-create seed --help
    pop-create seed -n poppy


This initial release should have identical functionality as `pop-seed` as
currently provided by the `pop` project.

Dynamic Name Spaces
===================

You can specify dynamic namespaces that your app will extend with "-d".
In this example we extend the dynamic name spaces of "states", "exec", "acct", and "tool";
All common extensions of the `idem` project.

.. code-block:: bash

    pop-create seed -n poppy -d exec states acct tool

Vertically App Merged Project
=============================

If your entrypoint will exist in another project, then you are making a vertically app merged project.
For example, if you are extending `idem` to write exec modules or states modules, your project won't have an entrypoint.
The code of your project will be dynamically
extended on top of the namespace of those other tools.

Create a vertically app merged project by adding the `--vertical` flag to `pop-create seed`

.. code-block:: bash

    pop-create seed --vertical -n poppy

Tests
=====

Now create the boilerplate code for your project's tests.
This will set your project up with some useful fixtures for testing pop projects and some basic unit/integration tests.

.. code-block:: bash

    pop-create tests -n poppy


Docs
====

Now create the boilerplate code for your project's docs.
This will set your project up with a rudimentary docs directory that can be easily added to and built.

.. code-block:: bash

    pop-create docs -n poppy
