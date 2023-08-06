===============
pymt_topography
===============


.. image:: https://img.shields.io/badge/CSDMS-Basic%20Model%20Interface-green.svg
        :target: https://bmi.readthedocs.io/
        :alt: Basic Model Interface

.. image:: https://img.shields.io/pypi/v/pymt_topography
        :target: https://pypi.org/project/pymt_topography
        :alt: PyPI

.. image:: https://img.shields.io/badge/recipe-pymt_topography-green.svg
        :target: https://anaconda.org/conda-forge/pymt_topography

.. image:: https://github.com/pymt-lab/pymt_topography/actions/workflows/build-test-ci.yml/badge.svg
        :target: https://github.com/pymt-lab/pymt_topography/actions/workflows/build-test-ci.yml
        :alt: Build/Test CI

.. image:: https://readthedocs.org/projects/pymt-topography/badge/?version=latest
        :target: https://pymt-topography.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/csdms/pymt
        :alt: Code style: black


PyMT component for accessing SRTM land elevation data


* Free software: MIT License
* Documentation: https://pymt-topography.readthedocs.io.




========== ====================================
Component  PyMT
========== ====================================
Topography `from pymt.models import Topography`
========== ====================================

---------------
Installing pymt
---------------

Installing `pymt` from the `conda-forge` channel can be achieved by adding
`conda-forge` to your channels with:

.. code::

  conda config --add channels conda-forge

*Note*: Before installing `pymt`, you may want to create a separate environment
into which to install it. This can be done with,

.. code::

  conda create -n pymt python=3
  conda activate pymt

Once the `conda-forge` channel has been enabled, `pymt` can be installed with:

.. code::

  conda install pymt

It is possible to list all of the versions of `pymt` available on your platform with:

.. code::

  conda search pymt --channel conda-forge

--------------------------
Installing pymt_topography
--------------------------

Once `pymt` is installed, the dependencies of `pymt_topography` can
be installed with:

.. code::

  pip install bmi-topography

To install `pymt_topography`,

.. code::

  pip install pymt_topography
