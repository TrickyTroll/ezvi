Available actions
=================

``ezvi`` offers many different tools that can be used to manipulate text files.

- Commands that can be used to automate typing are under the :ref:`tools` section.
- Commands that can be used to search text or create configuration files are under
  the :ref:`parsing` section.

.. _tools:

Vi tools
--------

These are the currently available tools for the Vi editor. They can all be
used in the YAML config file and directly in Python when the mododule is
imported.

To use the Vi tools, simply import the ``tools`` part of [#]_ this package
to your program like this:

.. code-block:: python
   
  import ezvi.tools

You can then add any function from the section below the same way they are
presented under the *Using the API* section.

To declutter your program, you can also import every Vi tool individually.

.. code-block:: python

  from ezvi.tools import *

This can be read as *from ezvi's tools module, import all*. This will allow
you to directly use the functions without specifying that they come from the
ezvi module. For example, to type three new lines, you would use

.. code-block:: python

  new_line(3)

.. caution:: Using this second method to import a module is less specific
   than the first method. This could result into 
   `namespace collisions <https://en.wikipedia.org/wiki/Naming_collision>`_
   if you are using multiple modules with methods which are named similarly.

ezvi.tools module
^^^^^^^^^^^^^^^^^

.. automodule:: ezvi.tools
   :members:
   :exclude-members: ez_encode_str, find_replace
   :undoc-members:
   :show-inheritance:

.. _parsing:

Parsing tools
-------------

Most of these tools have not been implemented yet. Please refer to the 
`latest <https://github.com/TrickyTroll/ezvi/tree/latest>`_ branch.

.. _generateConfig:

Generating a config file
^^^^^^^^^^^^^^^^^^^^^^^^

To automatically generate a config file, you can simply use the ``generate-config``
command. ``generate-config`` will create a config file to type the original
file line by line.

.. code-block::

  ezvi generate-config [PATH/TO/FILE]

- The ``-s`` option tells the program to write it's output to a file instead of
  the terminal's standard output. The path towards where the file should be saved
  must be provided.

  .. code-block ::

    ezvi generate-config -s [PATH/TO/SAVE] [PATH/TO/FILE]

.. note:: A ``diff`` function will be added soon. This will allow for the creation
   of config file based upon the differences between two files. See the
   `latest <https://github.com/TrickyTroll/ezvi/tree/latest>`_ branch for the most
   recent updates.

Footnotes
---------

.. [#] Make sure that the package is properly :doc:`installed <installation>` first.