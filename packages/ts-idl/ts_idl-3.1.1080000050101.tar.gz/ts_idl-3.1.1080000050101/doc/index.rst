###########
lsst.ts.idl
###########

.. image:: https://img.shields.io/badge/GitHub-gray.svg
    :target: https://github.com/lsst-ts/ts_idl
.. image:: https://img.shields.io/badge/Jira-gray.svg
    :target: https://jira.lsstcorp.org/issues/?jql=labels+%3D+ts_idl
.. image:: https://img.shields.io/badge/Jenkins-gray.svg
    :target: https://tssw-ci.lsst.org/job/LSST_Telescope-and-Site/job/ts_idl/

Overview
========

The ts_idl package provides "OMG IDL" files descripting the DDS interface for our SAL/DDS components
and a package ``lsst.ts.idl.enum`` containing Python enum classes matching enumerations in our SAL XML files.

Older versions include a ``qos`` directory containing DDS quality of service configuration,
but new code should obtain that information from the ``ts_ddsconfig`` package..

.. _lsst.ts.idl.user_guide:

User Guide
==========

Most users will obtain a built copy of this package containing all the IDL files that you need.
However, developers may wish to build their own IDL files.
To do this, run the following bin script, found in ``ts_sal``::

    make_idl_files.py name1 [name2 ...]

That script also has help and support for building all IDL files.

Developer Guide
===============

.. toctree::
    developer_guide
    :maxdepth: 1

Version History
===============

.. toctree::
    version_history
    :maxdepth: 1
