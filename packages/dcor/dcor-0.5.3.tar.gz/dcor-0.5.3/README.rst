dcor
====

|build-status| |docs| |coverage| |pypi| |conda|

dcor: distance correlation and related E-statistics in Python.

E-statistics are functions of distances between statistical observations
in metric spaces.

Distance covariance and distance correlation are
dependency measures between random vectors introduced in [SRB07]_ with
a simple E-statistic estimator.

This package offers functions for calculating several E-statistics
such as:

- Estimator of the energy distance [SR13]_.
- Biased and unbiased estimators of distance covariance and
  distance correlation [SRB07]_.
- Estimators of the partial distance covariance and partial
  distance covariance [SR14]_.

It also provides tests based on these E-statistics:

- Test of homogeneity based on the energy distance.
- Test of independence based on distance covariance.

Installation
============

dcor is on PyPi and can be installed using :code:`pip`:

.. code::

   pip install dcor
   
It is also available for :code:`conda` using the :code:`conda-forge` channel:

.. code::

   conda install -c conda-forge dcor
   
Previous versions of the package were in the :code:`vnmabus` channel. This
channel will not be updated with new releases, and users are recommended to
use the :code:`conda-forge` channel.

Requirements
------------

dcor is available in Python 3.5 or above and in Python 2.7, in all operating systems.

Documentation
=============
The documentation can be found in https://dcor.readthedocs.io/en/latest/?badge=latest

References
==========

.. [SR13] Gábor J. Székely and Maria L. Rizzo. Energy statistics: a class of
           statistics based on distances. Journal of Statistical Planning and
           Inference, 143(8):1249 – 1272, 2013.
           URL:
           http://www.sciencedirect.com/science/article/pii/S0378375813000633,
           doi:10.1016/j.jspi.2013.03.018.
.. [SR14]  Gábor J. Székely and Maria L. Rizzo. Partial distance correlation
           with methods for dissimilarities. The Annals of Statistics,
           42(6):2382–2412, 12 2014.
           doi:10.1214/14-AOS1255.
.. [SRB07] Gábor J. Székely, Maria L. Rizzo, and Nail K. Bakirov. Measuring and
           testing dependence by correlation of distances. The Annals of
           Statistics, 35(6):2769–2794, 12 2007.
           doi:10.1214/009053607000000505.

.. |build-status| image:: https://api.travis-ci.com/vnmabus/dcor.svg?branch=master
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.com/vnmabus/dcor

.. |docs| image:: https://readthedocs.org/projects/dcor/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://dcor.readthedocs.io/en/latest/?badge=latest
    
.. |coverage| image:: http://codecov.io/github/vnmabus/dcor/coverage.svg?branch=develop
    :alt: Coverage Status
    :scale: 100%
    :target: https://codecov.io/gh/vnmabus/dcor/branch/develop
    
.. |pypi| image:: https://badge.fury.io/py/dcor.svg
    :alt: Pypi version
    :scale: 100%
    :target: https://pypi.python.org/pypi/dcor/
    
.. |conda| image:: https://anaconda.org/conda-forge/dcor/badges/installer/conda.svg   
    :alt: Available in Conda
    :scale: 100%
    :target: https://conda.anaconda.org/conda-forge