.. isisysvic3daccess documentation master file, created by
   sphinx-quickstart on Fri Sep 25 10:54:55 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=============================================================================
Welcome to 'namefiles' documentation!
=============================================================================

**Name-files** is an approach for a standardized file naming for multiple files of
different sources with equal formatting, which all are related to the same entity.

.. image:: ../namefiles-icon.svg
   :height: 196px
   :width: 196px
   :alt: A trash panda.
   :align: center

Installation
============

Install the latest release from pip.

.. code-block:: shell

   $ pip install namefiles

.. toctree::
   :maxdepth: 3

   basic_usage
   api_reference/index

Concept
=======

The filename is defined by 6 parts, which take on different contexts, all being related
to one entity.

- identifier: The mandatory name (identification) of an entity.
- sub_id: A branch of this entity.
- source_id: The source from which the file (data) origins.
- vargroup: The possibility to state variables.
- context: Context of the files content. What is in there, not how it is stored in there.
  The context must be always accompanied with an *extension*.
- extension: The file extension, which should state the format of the file. How is it
  stored in there.

All filename parts except the identifier are optional.

Within :mod:`namefiles` file naming conventions are defined by a `JsonSchema`_ using
the `python jsonschema` module. :mod:`namefiles` proposes a standard naming convention,
which is used if no custom naming convention is defined.

.. _JsonSchema: https://json-schema.org/
.. _python jsonschema: https://pypi.org/project/jsonschema/

The ENBF of the namefiles's naming convention is

::

    filename     ::= identifier ["#" sub_id] ["#" source_id] ["#" vargroup] ["." context] ["." extension]
    identifier   ::= [0-9a-zA-Z-_]{1,36}
    sub_id       ::= [0-9A-Z]{1,4}
    source_id    ::= [0-9A-Z]{5,12} 
    vargroup     ::= ("_" var_value])+
    var_value    ::= [a-zA-Z0-9,.+-\ ]+
    context ::= (a-z)+ (a-zA-Z0-9){1, 15}
    extention    ::= common file extension (.csv, .txt, ...)

Implementation
==============

The recommended :class:`namefiles.NameGiver` implements the default :mod:`namefiles`
file naming convention, providing access to each part via properties.

.. autoattribute:: namefiles.NameGiver.identifier
   :noindex:

.. autoattribute:: namefiles.NameGiver.sub_id
   :noindex:

.. autoattribute:: namefiles.NameGiver.source_id
   :noindex:

.. autoattribute:: namefiles.NameGiver.vargroup
   :noindex:

.. autoattribute:: namefiles.NameGiver.context
   :noindex:

.. autoattribute:: namefiles.NameGiver.extension
   :noindex:


Indices and tables
==================

* :ref:`genindex`