Configuration files
===================

``ezvi`` can also type a file by following a configuration file. A 
configuration file is just a `YAML <https://yaml.org>`_ with certain
directives that are understood by ``ezvi``.

No need to worry if you do not know anything about YAML. This page
will tell you everything you need to know to get started with ``ezvi``
using a configuration file.

If you still want to learn more about the format, please see the official
`documentation <https://yaml.org/spec/1.2/spec.html>`_.

Writing a config file
---------------------

Creating the file
^^^^^^^^^^^^^^^^^

The configuration file is just a text file with the ``.yaml`` file extension.
You can create and edit a YAML file with the editor of your choice. You could
also simply download the template 
`file <https://github.com/TrickyTroll/ezvi/blob/main/example/config.yaml>`_
from the Github repo and then edit it however you want.

The ``create-config`` command can also be used to generate a basic configuration
file. For more information, see the :ref:`docs <generateConfig>`.

The syntax
^^^^^^^^^^

The configuration file is parsed by ``ezvi`` as a Python
`dictionary <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_.

- To create a new command, precede it with a dash and a space. This tells the 
  YAML parser that the following item will be a dictionary key.

- Every command must be followed by a colon.

- If the command takes inputs [#]_, add a space after the colon and then write
  your input.

  - If your input spans over more than one line, make sure to keep the lines
    indented the same way as your first line.

For example, if you want to write a very long line:

.. code-block:: yaml

  - write_line: This is a very, very, very long line. Since it will take more
                than 80 characters to write it and I want my file to look
                clean, I will make sure to write it on more than just one
                line.
        
- Every new command must be created on a new line.

You can put an indefinite number of new commands one after the others.

Typing the file
^^^^^^^^^^^^^^^

Once your configuration file is done and saved, you can easily tell ``ezvi``
to run it with the ``yaml`` command.

.. code-block::

  ezvi yaml [PATH/TO/CONFIG]


Why not JSON?
-------------

While pretty standard and very popular, the JSON format is not very human
friendly. It is harder to quickly find the right place to edit a parameter
in a JSON file compared to YAML [#]_.

``ezvi``'s configuration files are meant for humans. The goal is to make
these files not only easy to create and read by a computer, but also easy 
to edit by someone who wants to quickly fix their automation.

Footnotes
---------

.. [#] For example, the ``write_line`` command takes the line to write as
  an argument. For more information on what commands are available and their
  inputs, see the :doc:`actions <actions>` section.

.. [#] In fact, YAML is so easy to read that its web 
  `page <https://yaml.org>`_ can follow the language's syntax and still be
  easy to read.