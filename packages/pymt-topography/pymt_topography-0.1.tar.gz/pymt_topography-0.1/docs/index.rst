Topography data component
=========================

The Topography data component, *pymt_topography*,
is a `Python Modeling Toolkit`_ (*pymt*) library for fetching and caching
NASA `Shuttle Radar Topography Mission`_ (SRTM) land elevation data 
using the `OpenTopography`_ `REST API`_.

Access to the following global raster datasets is provided:

* SRTM GL3 (90m)
* SRTM GL1 (30m)
* SRTM GL1 (Ellipsoidal)

The *pymt_topography* component provides `BMI`_-mediated access to SRTM data as a service,
allowing it to be coupled in *pymt* with other data or model components that expose a BMI.


Installation
------------

*pymt*, and components that run within it,
are distributed through `Anaconda`_ and the `conda`_ package manager.
Instructions for `installing`_ Anaconda can be found on their website.
In particular,
*pymt* components are available through the community-led `conda-forge`_ organization.

Install the `pymt` and `pymt_topography` packages in a new environment with:

.. code::

  $ conda create -n pymt -c conda-forge python=3 pymt pymt_topography
  $ conda activate pymt

*conda* automatically resolves and installs any required dependencies.


Use
---

The *pymt_topography* data component is designed to access SRTM land elevation data,
with the user providing the dataset type,
a latitude-longiture bounding box, and
the output file format for the desired data.
This information can be provided through a configuration file
or specified through parameters.

With a configuration file
.........................

The *pymt_topography* configuration file is a `YAML`_ file
containing keys that map to parameter names.
An example is :download:`bmi-topography.yaml`:

.. include:: bmi-topography.yaml
   :literal:

:download:`Download <bmi-topography.yaml>` this file
for use in the following example.

.. include:: pymt_topography_config_file_ex.rst


With parameters
...............

Configuration information can also be passed directly to *pymt_topography* as parameters.

.. include:: pymt_topography_parameters_ex.rst


API documentation
-----------------

Looking for information on a particular function, class, or method?
This part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   modules


Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. Links:

.. _Python Modeling Toolkit: https://pymt.readthedocs.io
.. _Shuttle Radar Topography Mission: https://www2.jpl.nasa.gov/srtm/
.. _OpenTopography: https://opentopography.org/
.. _REST API: https://portal.opentopography.org/apidocs/
.. _BMI: https://bmi.readthedocs.io
.. _Anaconda: https://www.anaconda.com/products/individual
.. _conda: https://docs.conda.io/en/latest/
.. _installing: https://docs.anaconda.com/anaconda/install/
.. _conda-forge: https://conda-forge.org/
.. _YAML: https://en.wikipedia.org/wiki/YAML
