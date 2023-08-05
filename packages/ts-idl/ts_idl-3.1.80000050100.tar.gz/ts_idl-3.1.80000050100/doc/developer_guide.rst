.. py:currentmodule:: lsst.ts.idl

.. _lsst.ts.idl.developer_guide:

###############
Developer Guide
###############

Developers are expected to manually maintain the Python enumeration modules in ``lsst.ts.idl.enums``,
updating them as the enumerations in ``ts_xml`` are updated.

API
===

.. automodapi:: lsst.ts.idl
    :no-main-docstr:

.. automodapi:: lsst.ts.idl.enums.ATCamera
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.ATDome
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.ATHexapod
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.ATMCS
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.ATMonochromator
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.ATPneumatics
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.ATPtg
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.ATSpectrograph
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.ATThermoelectricCooler
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.Electrometer
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.FiberSpectrograph
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.Guider
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.LinearStage
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.MTAOS
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.MTDome
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.MTHexapod
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.MTM1M3
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.MTM2
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.MTMount
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.MTPtg
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.MTRotator
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.PMD
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.Script
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.ScriptQueue
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.TunableLaser
    :no-main-docstr:
    :no-inheritance-diagram:

.. automodapi:: lsst.ts.idl.enums.Watcher
    :no-main-docstr:
    :no-inheritance-diagram:

Build and Test
==============

This is a pure python package.
You can build IDL files (see the :ref:`user guide <lsst.ts.idl.user_guide>` for instructions), run unit tests and build documentation.

.. code-block:: bash

    setup -r .
    pytest -v  # to run tests
    package-docs clean; package-docs build  # to build the documentation

Contributing
============

``ts_idl`` is developed at https://github.com/lsst-ts/ts_idl.
You can find Jira issues for this package using `labels=ts_idl <https://jira.lsstcorp.org/issues/?jql=project%20%3D%20DM%20AND%20labels%20%20%3D%20ts_idl>`_..
