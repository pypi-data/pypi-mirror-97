This package aims at providing a unified and easy to use interface to access Gravitational Wave (GW) data and output some *well organised* datasets, ready to be used for Machine Learning projects or Data Analysis purposes (source properties, noise studies, etc.).

.. image:: https://gitlab.com/gwprojects/gwdama/badges/master/pipeline.svg
    :alt: Pipeline status

.. image:: https://img.shields.io/website-up-down-green-red/http/shields.io.svg
    :target: https://gwnoisehunt.gitlab.io/gwdama
    :alt: Documentation Status
 
.. image:: https://badge.fury.io/py/gwdama.svg
    :target: https://badge.fury.io/py/gwdama
 

===========================
 Data Preparation Workflow
===========================

The typical use case of this package is the data acquisition and preparation, which can be seen, in a *pipeline*, as the preliminary stage for Data Analysis. Although it is primarily meant for GW analyses, it is built to be sufficiently generic to handle any data type. The basic workflow that can be implemented with this package is the following:

1. **Data acquisition**: Data from GW detectors can be fetched from different locations, such as from *local* `frame files <https://lappweb.in2p3.fr/virgo/FrameL/>`_ (gwf) and `datasets <https://gwnoisehunt.gitlab.io/gwdama/dataset.html>`_ previously produced by `GWdama <https://gwnoisehunt.gitlab.io/gwdama/>`_, or from *remote*, especially from the `Gravitational Wave Open Science Center <https://www.gw-openscience.org/>`_ (GWOSC).

2. **Organisation into groups**: *Raw* and *pre-processed* data, from various *acquisition channels* (strain, auxiliary sensors, etc.) and various *epochs*, can be organised in a hierarchical way in various `groups and subgroups <http://docs.h5py.org/en/stable/high/groups.html>`_, each containing their own metadata;

3. **Data preparation**: This package includes several functions commonly used to `pre-process the data <https://gwnoisehunt.gitlab.io/gwdama/preprocessing.html>`_, such as filtering and spectral analysis methods. These operations can be performed in the "data preparation" phase of a pipeline, before storing the sophisticated dataset and/or forwarding it to the subsequent Data Analysis stage. This processed data is conveniently organised into new groups, and the "raw" ones can be removed to save memory;

4. **Reading and Writing**: Once the dataset specific for a task has been created, this can be saved to disk into `hdf5 format <https://www.hdfgroup.org/solutions/hdf5/>`_, preserving all the hierarchical group and sub-group structure and the metadata. This can be readily read back by `GWdama <https://gwnoisehunt.gitlab.io/gwdama/>`_ for further data manipulation and preparation.


==================================
 GW data manager package overview
==================================

`GWdama <https://gwnoisehunt.gitlab.io/gwdama/>`_ currently comprises the main class `GwDataManager <https://gwnoisehunt.gitlab.io/gwdama/gwdatamanager.html>`_, which behaves as a multi-purpose and multi-format container for data. This is based on the `h5py.File class <http://docs.h5py.org/en/stable/high/file.html>`_ with the addition of the methods and the attributes to import and manipulate GW data. Differently from the common application of ``h5py.File`` objects, a ``GwDataManager`` instance is, by default, set to occupy only a temporary file or some space in the RAM, which is authomatically deleted by python once the program is closed. Refer to the `full documentation <'https://gwnoisehunt.gitlab.io/gwdama'>`_ for further details. 

Inside ``GwDataManager`` objects, data is stored into `Dataset <https://gwnoisehunt.gitlab.io/gwdama/dataset.html>`_ objects, organised into a hierarchical structure of `h5py.Groups <http://docs.h5py.org/en/stable/high/group.html>`_ and sub-groups. These Datasets are created within an instance of ``GwDataManager`` with the usual methods of ``h5py``: ``create_dataset(name, shape, dtype)``. They contain data, typically of numeric type, and some attributes (or metadata). For example, for GW data, and in general all time series, it is important the information of when they have been recorded, and at which sampling frequency. A name and a unit are also useful. These can be conveniently added and customised. Also, a ``GwDatamanager`` object contains attributes for itself. 

--------------
 Installation
--------------

`GWdama <https://gwnoisehunt.gitlab.io/gwdama/>`_ can be installed via `pip <https://docs.python.org/3/installing/index.html>`_:

.. code-block:: console

    $ pip install gwdama

and requires Python 3.6.0 or higher. The previous command automatically fulfils all the required dependencies (like on ``numpy``, ``matplotlib``), so you are ready to start generating datasets and making plots.

Further details can be found in the `documentation <https://gwnoisehunt.gitlab.io/gwdama/>`_.


-------------
 Quick start
-------------

A dataset of, say, random numbers can be readily created with the aid of `numpy.random <https://numpy.org/doc/stable/reference/random/index.html>`_ routines::

    >>> from gwdama.io import GwDataManager
    >>> import numpy as np
    
    >>> dama = GwDataManager("my_dama")
    >>> dama.create_dataset('random', data=np.random.normal(0, 1, (10,)))
    
The *string representation* of the ``GwDataManager`` class provides a quick look at its structure and its attributes::

    >>> print(dama)
    my_dama:
      └── random

      Attributes:
         dama_name : my_dama
        time_stamp : 20-07-28_19h36m47s
    
Other attributes can be added to both the ``GwDataManager`` object and the `Datasets <https://gwnoisehunt.gitlab.io/gwdama/dataset.html>`_ therein::

    >>> dama.attrs['owner'] = 'Francesco'  # The new attribute "owner" is added with value "Francesco"
    >>> dama.show_attrs
    my_dama:
      └── random

      Attributes:
         dama_name : my_dama
             owner : Francesco
        time_stamp : 20-07-28_19h36m47s  
        
`Datasets <https://gwnoisehunt.gitlab.io/gwdama/dataset.html>`_ can be accessed from their *keys*, as reported in the structure shown above, with a syntax similar to that for Python dictionaries::

    >>> dset = dama['random']       # 'random' is the dataset key
    >>> dset.attrs['t0'] = 0        # It is conveninet to use gps times
    >>> dset.attrs['fsample'] = 10  # measured in Hz
    
    >>> dset.show_attrs
    fsample : 10
         t0 : 0

To get the data contained in this dataset, call its attribute ``data``::

    >>> dset.data
    array([-0.73796689, -1.34206706, -0.97898291, -0.19846702,
           -0.85056961,  0.20206334,  0.84720009,  0.19527366,
           -0.9246727 , -0.04808732])

------------------------------
 Writing and reading datasets
------------------------------

So far, data is stored on temporary or volatile memory. To secure it to disk, we can call the write method of our ``GwdataManager`` object::

    >>> out_f = 'out_dataset.h5'
    >>> write_gwdama(out_f)
    
Then remember to **close your previous file** before leaving the session:
::

    >>> dama.close()
    >>> del dama       # Redundant but usefull

.. note:: This operation is automatically performed every time the session is closed. However, it is good practice to do this manually every time there is no more need of a certain variable.

To *read back* the data::

    >>> new_dama = GwDataManager(out_f)  # Same namse as the line above
    Reading dama
    >>> print(new_dama)
    my_dama:
      └── random

      Attributes:
         dama_name : my_dama
             owner : Francesco
        time_stamp : 20-07-30_12h19m32s

----------------
 Read open data 
----------------

Open data can be accessed from both online and local virtual disks provided by `CVMFS <https://cernvm.cern.ch/fs/>`_. 

From online GWOSC
-----------------
GW strain data can be read by means of the ``.read_gwdata()`` method. This basically takes as input an interval of time, which can be provided as a ``float`` in gps units or in UTC, in a human readible format (see next example), besides the label of the detector (``H1``, ``L1`` or ``V1``):
::

    >>> event_gps = 1186746618                                      # GW170814
    >>> dama = GwDataManager()                                      # Default name 'mydama' assigned
    >>> dama.read_gwdata(event_gps - 50, event_gps +10, ifo='L1',   # Required params
                         m_data_source="gwosc-remote",              # data source
                         dts_key='online')                          # group key (optional, but useful)


From local CVMFS
----------------
 
CernVM-FS must be installed and configured on your computer. Refer to its `description on the GWOSC website <https://www.gw-openscience.org/cvmfs/>`_ 
or to `this Quick start guide <https://cernvm.cern.ch/portal/filesystem/quickstart>`_.

Assuming your data are stored at the following path (you can always modify it by passing it as a parameter to ``read_gwdata()``)::

   cvmfs_path = '/data2/cvmfs/gwosc.osgstorage.org/gwdata/' 

data can be read with:

::

    >>> start='2017-06-08 01:00:00'  # starting UTC time as a string
    >>> end='2017-06-08 02:00:00'    # ending time as a string
    >>> ifo='H1'                     # interfereometer tag

    >>> rate='4k'                    # sample rate: 4k or 16k
    >>> frmt='hdf5'                  # format of the data: gwf or hdf5
    
    >>> dama.read_gwdata(start, end, m_data_source="gwosc-cvmfs", ifo=ifo, m_data_format=frmt)
    
    
===========
 Changelog
===========

**0.4.5**

* Added interface with GWpy;
* Multi-Taper Method.

**0.4.1**

* Methods: ``hist``, ``duration``;
* Attributes: ``groups``;
* Preprocessing functions: ``PSD``, ``whiten``, ``taper``.

**0.4.0**

* Implemented support for data on Virgo Farm.

**0.3.0**

* Only open data can be imported either from online or via CVMFS;
* New methods to access data and attributes of datasets.
