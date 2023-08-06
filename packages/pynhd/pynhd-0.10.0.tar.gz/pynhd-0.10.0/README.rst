.. .. image:: https://raw.githubusercontent.com/cheginit/geohydrohub-examples/main/notbooks/_static/pynhd_logo.png
..     :target: https://github.com/cheginit/pynhd
..     :align: center

.. |

.. |pygeohydro| image:: https://github.com/cheginit/pygeohydro/actions/workflows/test.yml/badge.svg
    :target: https://github.com/cheginit/pygeohydro/actions?query=workflow%3Apytest
    :alt: Github Actions

.. |pygeoogc| image:: https://github.com/cheginit/pygeoogc/actions/workflows/test.yml/badge.svg
    :target: https://github.com/cheginit/pygeoogc/actions?query=workflow%3Apytest
    :alt: Github Actions

.. |pygeoutils| image:: https://github.com/cheginit/pygeoutils/actions/workflows/test.yml/badge.svg
    :target: https://github.com/cheginit/pygeoutils/actions?query=workflow%3Apytest
    :alt: Github Actions

.. |pynhd| image:: https://github.com/cheginit/pynhd/actions/workflows/test.yml/badge.svg
    :target: https://github.com/cheginit/pynhd/actions?query=workflow%3Apytest
    :alt: Github Actions

.. |py3dep| image:: https://github.com/cheginit/py3dep/actions/workflows/test.yml/badge.svg
    :target: https://github.com/cheginit/py3dep/actions?query=workflow%3Apytest
    :alt: Github Actions

.. |pydaymet| image:: https://github.com/cheginit/pydaymet/actions/workflows/test.yml/badge.svg
    :target: https://github.com/cheginit/pydaymet/actions?query=workflow%3Apytest
    :alt: Github Actions

=========== ==================================================================== ============
Package     Description                                                          Status
=========== ==================================================================== ============
PyGeoHydro_ Access NWIS, NID, HCDN 2009, NLCD, and SSEBop databases              |pygeohydro|
PyGeoOGC_   Send queries to any ArcGIS RESTful-, WMS-, and WFS-based services    |pygeoogc|
PyGeoUtils_ Convert responses from PyGeoOGC's supported web services to datasets |pygeoutils|
PyNHD_      Navigate and subset NHDPlus (MR and HR) using web services           |pynhd|
Py3DEP_     Access topographic data through National Map's 3DEP web service      |py3dep|
PyDaymet_   Access Daymet for daily climate data both single pixel and gridded   |pydaymet|
=========== ==================================================================== ============

.. _PyGeoHydro: https://github.com/cheginit/pygeohydro
.. _PyGeoOGC: https://github.com/cheginit/pygeoogc
.. _PyGeoUtils: https://github.com/cheginit/pygeoutils
.. _PyNHD: https://github.com/cheginit/pynhd
.. _Py3DEP: https://github.com/cheginit/py3dep
.. _PyDaymet: https://github.com/cheginit/pydaymet

PyNHD: Navigate and subset NHDPlus database
-------------------------------------------

.. image:: https://img.shields.io/pypi/v/pynhd.svg
    :target: https://pypi.python.org/pypi/pynhd
    :alt: PyPi

.. image:: https://img.shields.io/conda/vn/conda-forge/pynhd.svg
    :target: https://anaconda.org/conda-forge/pynhd
    :alt: Conda Version

.. image:: https://codecov.io/gh/cheginit/pynhd/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/cheginit/pynhd
    :alt: CodeCov

.. image:: https://mybinder.org/badge_logo.svg
    :target: https://mybinder.org/v2/gh/cheginit/pygeohydro/master?filepath=docs%2Fexamples
    :alt: Binder

|

.. image:: https://www.codefactor.io/repository/github/cheginit/pynhd/badge
   :target: https://www.codefactor.io/repository/github/cheginit/pynhd
   :alt: CodeFactor

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit

|

Features
--------

PyNHD is part of a software stack for retrieving and processing hydrology and climatology
datasets. This package provides access to
`WaterData <https://labs.waterdata.usgs.gov/geoserver/web/wicket/bookmarkable/org.geoserver.web.demo.MapPreviewPage?1>`__,
the National Map's `NHDPlus HR <https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer>`__,
and `NLDI <https://labs.waterdata.usgs.gov/about-nldi/>`_ web services. These web services
can be used to navigate and extract vector data from NHDPlus V2 (both medium- and
hight-resolution) database such as catchments, HUC8, HUC12, GagesII, flowlines, and water bodies.
Moreover, PyNHD gives access to
an item on `ScienceBase <https://sciencebase.usgs.gov>`_ called
`Select Attributes for NHDPlus Version 2.1 Reach Catchments and Modified Network Routed Upstream Watersheds for the Conterminous United States <https://www.sciencebase.gov/catalog/item/5669a79ee4b08895842a1d47>`_.
This item provides over 30 attributes at catchment-scale based on NHDPlus ComIDs.
These attributes are available in three categories:

1. Local (`local`): For individual reach catchments,
2. Total (`upstream_acc`): For network-accumulated values using total cumulative drainage area,
3. Divergence (`div_routing`): For network-accumulated values using divergence-routed.

A list of these attributes for each characteristic type can be accessed using ``nhdplus_attrs``
function.

Additionally, PyNHD offers some extra utilities for processing the flowlines:

- ``prepare_nhdplus``: For cleaning up the dataframe by, for example, removing tiny networks,
  adding a ``to_comid`` column, and finding a terminal flowlines if it doesn't exist.
- ``topoogical_sort``: For sorting the river network topologically which is useful for routing
  and flow accumulation.
- ``vector_accumulation``: For computing flow accumulation in a river network. This function
  is generic and any routing method can be plugged in.

These utilities are developed based on an ``R`` package called
`nhdplusTools <https://github.com/USGS-R/nhdplusTools>`__.

You can find some example notebooks `here <https://github.com/cheginit/geohydrohub-examples>`__.

Please note that since this project is in early development stages, while the provided
functionalities should be stable, changes in APIs are possible in new releases. But we
appreciate it if you give this project a try and provide feedback. Contributions are most welcome.

Moreover, requests for additional functionalities can be submitted via
`issue tracker <https://github.com/cheginit/pynhd/issues>`__.

Installation
------------

You can install PyNHD using ``pip`` after installing ``libgdal`` on your system
(for example, in Ubuntu run ``sudo apt install libgdal-dev``):

.. code-block:: console

    $ pip install pynhd

Alternatively, PyNHD can be installed from the ``conda-forge`` repository
using `Conda <https://docs.conda.io/en/latest/>`__:

.. code-block:: console

    $ conda install -c conda-forge pynhd

Quick start
-----------

Let's explore the capabilities of ``NLDI``. We need to instantiate the class first:

.. code:: python

    from pynhd import NLDI, WaterData, NHDPlusHR
    import pynhd as nhd

First, let’s get the watershed geometry of the contributing basin of a
USGS station using ``NLDI``:

.. code:: python

    nldi = NLDI()
    station_id = "01031500"

    basin = nldi.get_basins(station_id)

The ``navigate_byid`` class method can be used to navigate NHDPlus in
both upstream and downstream of any point in the database. Let’s get ComIDs and flowlines
of the tributaries and the main river channel in the upstream of the station.

.. code:: python

    flw_main = nldi.navigate_byid(
        fsource="nwissite",
        fid=f"USGS-{station_id}",
        navigation="upstreamMain",
        source="flowlines",
        distance=1000,
    )

    flw_trib = nldi.navigate_byid(
        fsource="nwissite",
        fid=f"USGS-{station_id}",
        navigation="upstreamTributaries",
        source="flowlines",
        distance=1000,
    )

We can get other USGS stations upstream (or downstream) of the station
and even set a distance limit (in km):

.. code:: python

    st_all = nldi.navigate_byid(
        fsource="nwissite",
        fid=f"USGS-{station_id}",
        navigation="upstreamTributaries",
        source="nwissite",
        distance=1000,
    )

    st_d20 = nldi.navigate_byid(
        fsource="nwissite",
        fid=f"USGS-{station_id}",
        navigation="upstreamTributaries",
        source="nwissite",
        distance=20,
    )

Now, let’s get the `HUC12 pour
points <https://www.sciencebase.gov/catalog/item/5762b664e4b07657d19a71ea>`__:

.. code:: python

    pp = nldi.navigate_byid(
        fsource="nwissite",
        fid=f"USGS-{station_id}",
        navigation="upstreamTributaries",
        source="huc12pp",
        distance=1000,
    )

.. image:: https://raw.githubusercontent.com/cheginit/geohydrohub-examples/main/notebooks/_static/nhdplus_navigation.png
    :target: https://github.com/cheginit/geohydrohub-examples/blob/main/notebooks/nhdplus.ipynb
    :width: 400
    :align: center

Next, we retrieve the medium- and high-resolution flowlines within the bounding box of our
watershed and compare them. Moreover, Since serveral web services offer access to NHDPlus database,
``NHDPlusHR`` has an argument for selecting a service and also an argument for automatically
switching between services.

.. code:: python

    mr = WaterData("nhdflowline_network")
    nhdp_mr = mr.bybox(basin.geometry[0].bounds)

    hr = NHDPlusHR("networknhdflowline", service="hydro", auto_switch=True)
    nhdp_hr = hr.bygeom(basin.geometry[0].bounds)

.. image:: https://raw.githubusercontent.com/cheginit/geohydrohub-examples/main/notebooks/_static/hr_mr.png
    :target: https://github.com/cheginit/geohydrohub-examples/blob/main/notebooks/nhdplus.ipynb
    :width: 400
    :align: center

Moreover, ``WaterData`` can find features within a given radius (in meters) of a point:

.. code:: python

    eck4 = "+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
    coords = (-5727797.427596455, 5584066.49330473)
    rad = 5e3
    flw_rad = mr.bydistance(coords, rad, loc_crs=eck4)
    flw_rad = flw_rad.to_crs(eck4)

Instead of getting all features withing a radius of the coordinate, we can snap to the closest
flowline using NLDI:

.. code:: python

    comid_closest = nldi.comid_byloc((x, y), eck4)
    flw_closest = nhdp_mr.byid("comid", comid_closest.comid.values[0])


.. image:: https://raw.githubusercontent.com/cheginit/geohydrohub-examples/main/notebooks/_static/nhdplus_radius.png
    :target: https://github.com/cheginit/geohydrohub-examples/blob/main/notebooks/nhdplus.ipynb
    :width: 400
    :align: center

Since NHDPlus HR is still at the pre-release stage let's use the MR flowlines to
demonstrate the vector-based accumulation.
Based on a topological sorted river network
``pynhd.vector_accumulation`` computes flow accumulation in the network.
It returns a dataframe which is sorted from upstream to downstream that
shows the accumulated flow in each node.

PyNHD has a utility called ``prepare_nhdplus`` that identifies such
relationship among other things such as fixing some common issues with
NHDPlus flowlines. But first we need to get all the NHDPlus attributes
for each ComID since ``NLDI`` only provides the flowlines’ geometries
and ComIDs which is useful for navigating the vector river network data.
For getting the NHDPlus database we use ``WaterData``. Let’s use the
``nhdflowline_network`` layer to get required info.

.. code:: python

    wd = WaterData("nhdflowline_network")

    comids = flw_trib.nhdplus_comid.to_list()
    nhdp_trib = wd.byid("comid", comids)
    flw = nhd.prepare_nhdplus(nhdp_trib, 0, 0, purge_non_dendritic=False)

To demonstrate the use of routing, let's use ``nhdplus_attrs`` function to get list of available
NHDPlus attributes

.. code:: python

    char = "CAT_RECHG"
    area = "areasqkm"

    local = nldi.getcharacteristic_byid(comids, "local", char_ids=char)
    flw = flw.merge(local[char], left_on="comid", right_index=True)

    def runoff_acc(qin, q, a):
        return qin + q * a

    flw_r = flw[["comid", "tocomid", char, area]]
    runoff = nhd.vector_accumulation(flw_r, runoff_acc, char, [char, area])

    def area_acc(ain, a):
        return ain + a

    flw_a = flw[["comid", "tocomid", area]]
    areasqkm = nhd.vector_accumulation(flw_a, area_acc, area, [area])

    runoff /= areasqkm

Since these are catchment-scale characteristic, let’s get the catchments
then add the accumulated characteristic as a new column and plot the
results.

.. code:: python

    wd = WaterData("catchmentsp")
    catchments = wd.byid("featureid", comids)

    c_local = catchments.merge(local, left_on="featureid", right_index=True)
    c_acc = catchments.merge(runoff, left_on="featureid", right_index=True)

.. image:: https://raw.githubusercontent.com/cheginit/geohydrohub-examples/main/notebooks/_static/flow_accumulation.png
    :target: https://github.com/cheginit/geohydrohub-examples/blob/main/notebooks/nhdplus.ipynb
    :width: 600
    :align: center

More examples can be found `here <https://pygeohydro.readthedocs.io/en/latest/examples.html>`__.

Contributing
------------

Contributions are very welcomed. Please read
`CONTRIBUTING.rst <https://github.com/cheginit/pynhd/blob/master/CONTRIBUTING.rst>`__
file for instructions.
