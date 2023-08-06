Start by importing the Topography class from ``pymt``.

.. code:: ipython3

    from pymt.models import Topography

Create an instance of Topography and initialize it with our
configuration file. (This may take a moment to complete as data are fetched from the
internet.)

.. code:: ipython3

    m = Topography()
    m.initialize("bmi-topography.yaml")

Note that the configurtation information has been read from the
configuration file into the component as parameters.

.. code:: ipython3

    for param in m.parameters:
        print(param)


.. parsed-literal::

    ('dem_type', 'SRTMGL3')
    ('south', 36.738884)
    ('north', 38.091337)
    ('west', -120.168457)
    ('east', -118.465576)
    ('output_format', 'GTiff')
    ('cache_dir', '~/.bmi_topography')


Also note that the data have been downloaded to the cache directory:

.. code:: ipython3

    ls ~/.bmi_topography


.. parsed-literal::

    SRTMGL3_36.738884_-120.168457_38.091337_-118.465576.tif


What variables can be accessed from this component?

.. code:: ipython3

    for var in m.output_var_names:
        print(var)


.. parsed-literal::

    land_surface__elevation


What is the highest elevation in the dataset?

.. code:: ipython3

    import numpy
    
    numpy.max(m.var["land_surface__elevation"].data)




.. parsed-literal::

    4291



What are the units of this elevation value?

.. code:: ipython3

    m.var["land_surface__elevation"].units




.. parsed-literal::

    'meters'



Finish by finalizing the component.

.. code:: ipython3

    m.finalize()
