|Latest release| |PyPI| |CI status| |Test coverage|

BioSimulators test suite
========================

The BioSimulators test suite is a tool for validating that biosimulation
software tools implement the `BioSimulators standards for biosimulation
tools <https://biosimulators.org/standards>`__.

The test suite is composed of two parts:

-  A collection of example modeling projects. Each project is
   represented by a single `COMBINE/OMEX
   archive <https://combinearchive.org/>`__ that contains one or more
   simulation experiments described using the `Simulation Experiment
   Description Markup Language (SED-ML) <https://sed-ml.org>`__ and one
   or more models described using a format such as the `BioNetGen
   Language (BNGL) <https://bionetgen.org>`__ or the `Systems Biology
   Markup Language (SBML) <http://sbml.org>`__.

-  Software for checking that biosimulation tools execute these projects
   according to the BioSimulators standards.

   -  Simulation tools support the `BioSimulators standard command-line
      arguments <https://biosimulators.org/standards/simulator-interfaces>`__.
   -  Simulation tools support the `BioSimulators conventions for Docker
      images <https://biosimulators.org/standards/simulator-images>`__.
   -  Simulation tools follow the `BioSimulators conventions for
      executing simulations described by SED-ML files in COMBINE/OMEX
      archives <https://biosimulators.org/standards/simulation-experiments>`__.
   -  Simulation tools support the `BioSimulators conventions for the
      outputs of SED-ML files in COMBINE/OMEX
      archives <https://biosimulators.org/standards/simulation-reports>`__.

Contents
--------

-  `Installation instructions, tutorial, and API
   documentation <#installation-instructions,-tutorial,-and-API-documentation>`__
-  `License <#license>`__
-  `Development team <#development-team>`__
-  `Contributing to the test suite <#contributing-to-the-test-suite>`__
-  `Acknowledgements <#acknowledgements>`__
-  `Questions and comments <#questions-and-comments>`__

Installation instructions, tutorial, and API documentation
----------------------------------------------------------

Installation instructions, tutorial, and API documentation are available
`here <https://biosimulators.github.io/Biosimulators_test_suite/>`__.

License
-------

The software in this package is released under the `MIT
License <LICENSE>`__. The modeling projects in this package are released
under the `Creative Commons 1.0 Universal (CC0)
license <LICENSE-DATA>`__.

Development team
----------------

This package was developed by the `Karr Lab <https://www.karrlab.org>`__
at the Icahn School of Medicine at Mount Sinai in New York, the
https://health.uconn.edu/cell-analysis-modeling/ at the University of
Connecticut, and the `Center for Reproducible Biomedical
Modeling <http://reproduciblebiomodels.org>`__.

Contributing to the test suite
------------------------------

We enthusiastically welcome contributions to the test suite! Please see
the `guide to contributing <CONTRIBUTING.md>`__ and the `developer's
code of conduct <CODE_OF_CONDUCT.md>`__.

Acknowledgements
----------------

This work was supported by National Institutes of Health award
P41EB023912.

Questions and comments
----------------------

Please contact the `BioSimulators
Team <mailto:info@biosimulators.org>`__ with any questions or comments.

.. |Latest release| image:: https://img.shields.io/github/v/release/biosimulators/Biosimulators_test_suite
   :target: https://github.com/biosimulators/Biosimulators_test_suite/releases
.. |PyPI| image:: https://img.shields.io/pypi/v/Biosimulators-test-suite
   :target: https://pypi.org/project/Biosimulators-test-suite/
.. |CI status| image:: https://github.com/biosimulators/Biosimulators_test_suite/workflows/Continuous%20integration/badge.svg
   :target: https://github.com/biosimulators/Biosimulators_test_suite/actions?query=workflow%3A%22Continuous+integration%22
.. |Test coverage| image:: https://codecov.io/gh/biosimulators/Biosimulators_test_suite/branch/dev/graph/badge.svg
   :target: https://codecov.io/gh/biosimulators/Biosimulators_test_suite
