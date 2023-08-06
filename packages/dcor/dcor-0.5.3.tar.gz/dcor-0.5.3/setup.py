# encoding: utf-8

"""
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

References
----------
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

"""
import os
import sys

from setuptools import setup, find_packages

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

DOCLINES = (__doc__ or '').split("\n")

with open(os.path.join(os.path.dirname(__file__),
                       'VERSION'), 'r') as version_file:
    version = version_file.read().strip()

setup(name='dcor',
      version=version,
      description=DOCLINES[1],
      long_description="\n".join(DOCLINES[3:]),
      url='https://github.com/vnmabus/dcor',
      author='Carlos Ramos Carreño',
      author_email='vnmabus@gmail.com',
      include_package_data=True,
      platforms=['any'],
      license='MIT',
      packages=find_packages(),
      python_requires='>=3.6, <4',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords=['distance correlation', 'distance covariance',
                'energy distance', 'e-statistic',
                'dependency measure', 'homogeneity'],
      install_requires=['numpy',
                        'numba>=0.51',
                        'scipy'],
      setup_requires=pytest_runner,
      tests_require=['pytest-cov',
                     'pytest-subtests',
                     'numpy>=1.17'  # Requires matmul on objects
                     ],
      test_suite='dcor.tests',
      zip_safe=False)
