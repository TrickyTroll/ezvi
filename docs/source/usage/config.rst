Configuration files
===================

``ezvi`` can also type a file by following a configuration file. A 
configuration file is just a `YAML <https://yaml.org>`_ with certain
directives that are understood by ``ezvi``.

No need to worry if you do not know anything about YAML. This page
will tell you everything you need to know to get started with ``ezvi``
using a configuration file.

If you still want to learn more about the format, please see the official
`https://yaml.org/spec/1.2/spec.html <documentation>`_.

Writing a config file
---------------------


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

.. [#] In fact, YAML is so easy to read that its web 
  `https://yaml.org <page>`_ can follow the language's syntax and still be
  easy to read.
