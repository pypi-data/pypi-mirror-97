IDL files for use by ts_salobj, and Python enum files generated from XML.

Contents:

* idl: IDL files. There should be one file for each SAL component you want to communication with using ``ts_salobj``.
* python: functions to get the IDL directory and QoS file, plus CSC-specific enums.
* ups: Files for using this package with eups.

To use this package:

* Make sure ``ts_idl/python`` is on the PYTHONPATH.
  If using eups this will happen automatically when you setup the package.

To generate new IDL files:

* Make sure the ``ts_sal`` package and ``ts_xml`` packages are both setup, e.g. ``setup ts_sal``.
  Alternatively you can define environment variables ``$TS_SAL_DIR`` and ``$TS_XML_DIR``
  and make sure that ``$TS_SAL_DIR/bin`` is on your ``$PATH``.
* Make sure environment variable ``$SAL_WORK_DIR`` is defined.
* Run ``make_idl_files.py sal_component_name1 [sal_component_name12 [...]]``.
  For example: ``make_idl_files.py Test Script ScriptQueue``

To generate new enum files:

* As of 2019-05-21 this is done manually; eventually it may be automated.
* Inherit from enum.IntEnum so the values can more easily be treated as integers.
* Use UPPERCASE for enum values. This is the python convention and avoids problems from using ``None`` as a value.
* Match the XML exactly (other than case), to make the mapping between XML and python more obvious and to allow automatic generation someday.
* No underscore between words, to simplify automatic generation.

This code uses ``pre-commit`` to maintain ``black`` formatting and ``flake8`` compliance.
To enable this, run the following commands once (the first removes the previous pre-commit hook)::

    git config --unset-all core.hooksPath
    pre-commit install
