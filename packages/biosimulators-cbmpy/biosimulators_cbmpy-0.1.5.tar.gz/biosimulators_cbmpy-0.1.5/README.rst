|Latest release| |PyPI| |CI status| |Test coverage|

BioSimulators-CBMPy
===================

BioSimulators-compliant command-line interface to the
`CBMPy <http://cbmpy.sourceforge.net/>`__ simulation program.

This command-line interface and Docker image enable users to use CBMPy
to execute `COMBINE/OMEX archives <https://combinearchive.org/>`__ that
describe one or more simulation experiments (in `SED-ML
format <https://sed-ml.org>`__) of one or more models (in `SBML
format <http://sbml.org]>`__).

A list of the algorithms and algorithm parameters supported by CBMPy is
available at
`BioSimulators <https://biosimulators.org/simulators/cbmpy>`__.

A simple web application and web service for using CBMPy to execute
COMBINE/OMEX archives is also available at
`runBioSimulations <https://run.biosimulations.org>`__.

Contents
--------

-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `Documentation <#documentation>`__
-  `License <#license>`__
-  `Development team <#development-team>`__
-  `Questions and comments <#questions-and-comments>`__

Installation
------------

Install Python package
~~~~~~~~~~~~~~~~~~~~~~

::

   pip install biosimulators-cbmpy

Install Docker image
~~~~~~~~~~~~~~~~~~~~

::

   docker pull ghcr.io/biosimulators/cbmpy

Usage
-----

Local usage
~~~~~~~~~~~

::

   usage: cbmpy [-h] [-d] [-q] -i ARCHIVE [-o OUT_DIR] [-v]

   BioSimulators-compliant command-line interface to the CBMPy simulation program <http://cbmpy.sourceforge.net/>.

   optional arguments:
     -h, --help            show this help message and exit
     -d, --debug           full application debug mode
     -q, --quiet           suppress all console output
     -i ARCHIVE, --archive ARCHIVE
                           Path to OMEX file which contains one or more SED-ML-
                           encoded simulation experiments
     -o OUT_DIR, --out-dir OUT_DIR
                           Directory to save outputs
     -v, --version         show program's version number and exit

Usage through Docker container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The entrypoint to the Docker image supports the same command-line
interface described above.

For example, the following command could be used to use the Docker image
to execute the COMBINE/OMEX archive ``./modeling-study.omex`` and save
its outputs to ``./``.

::

   docker run \
     --tty \
     --rm \
     --mount type=bind,source="$(pwd)",target=/root/in,readonly \
     --mount type=bind,source="$(pwd)",target=/root/out \
     ghcr.io/biosimulators/cbmpy:latest \
       -i /root/in/modeling-study.omex \
       -o /root/out

Documentation
-------------

Documentation is available at
https://biosimulators.github.io/Biosimulators_CBMPy/.

License
-------

This package is released under the `MIT license <LICENSE>`__.

Development team
----------------

This package was developed by the `Center for Reproducible Biomedical
Modeling <http://reproduciblebiomodels.org>`__ and the `Karr
Lab <https://www.karrlab.org>`__ at the Icahn School of Medicine at
Mount Sinai in New York.

Questions and comments
----------------------

Please contact the `BioSimulators
Team <mailto:info@biosimulators.org>`__ with any questions or comments.

.. |Latest release| image:: https://img.shields.io/github/v/tag/biosimulators/Biosimulators_CBMPy
   :target: https://github.com/biosimulations/Biosimulators_CBMPy/releases
.. |PyPI| image:: https://img.shields.io/pypi/v/biosimulators_cbmpy
   :target: https://pypi.org/project/biosimulators_cbmpy/
.. |CI status| image:: https://github.com/biosimulators/Biosimulators_CBMPy/workflows/Continuous%20integration/badge.svg
   :target: https://github.com/biosimulators/Biosimulators_CBMPy/actions?query=workflow%3A%22Continuous+integration%22
.. |Test coverage| image:: https://codecov.io/gh/biosimulators/Biosimulators_CBMPy/branch/dev/graph/badge.svg
   :target: https://codecov.io/gh/biosimulators/Biosimulators_CBMPy
