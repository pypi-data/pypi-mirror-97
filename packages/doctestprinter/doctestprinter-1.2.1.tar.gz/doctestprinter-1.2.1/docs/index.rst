.. isisysvic3daccess documentation master file, created by
   sphinx-quickstart on Fri Sep 25 10:54:55 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================
Documentation of doctestprinter
===============================

**doctestprinter** contains convenience functions to print outputs more adequate
for doctests.

Example features:

- removes trailing whitespaces: pandas.DataFrame generates trailing whitespaces,
  which interferes with auto text 'trailing whitespace' removal features,
  leading to failed tests.
- maximum line width: break long sequences at whitespaces to a paragraph.

.. image:: ../doctestprinter-icon.svg
   :height: 192px
   :width: 192px
   :alt: my_module
   :align: center

Indices and tables
==================

* :ref:`genindex`

Installation
============

Either install the current release from pip ...

.. code-block:: shell

   pip install doctestprinter

... or the latest development state of the gitlab repository.

.. code-block:: shell

   $ pip install git+https://gitlab.com/david.scheliga/doctestprinter.git@dev --upgrade


.. autosummary::
   :toctree: api_reference

   doctestprinter.doctest_print
   doctestprinter.doctest_iter_print
   doctestprinter.EditingItem
   doctestprinter.prepare_print
   doctestprinter.prepare_pandas
   doctestprinter.print_pandas
   doctestprinter.round_collections
   doctestprinter.remove_trailing_tabs
   doctestprinter.remove_trailing_whitespaces
   doctestprinter.remove_trailing_whitespaces_and_tabs
   doctestprinter.repr_posix_path
   doctestprinter.set_in_quotes
   doctestprinter.strip_base_path
   doctestprinter.strip_trailing_tabs
   doctestprinter.strip_trailing_whitespaces
   doctestprinter.strip_trailing_whitespaces_and_tabs