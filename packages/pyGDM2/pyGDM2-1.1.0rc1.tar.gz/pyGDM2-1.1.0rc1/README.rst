***********************************
Requirements / Installation
***********************************

pyGDM is an open source python toolkit for electro-dynamical simulations, implementing the `Green dyadic method (GDM) <https://doi.org/10.1088/0034-4885/68/8/R05>`_, a volume discretization technique. 
pyGDM is based on simulation codes and theoretical models developed over the past 20 years by `Christian Girard <http://www.cemes.fr/Theory-of-Complex-Nano-optical?lang=en>`_ at CEMES (see e.g. `Ch. Girard 2005 Rep. Prog. Phys. 68 1883 <https://doi.org/10.1088/0034-4885/68/8/R05>`_), with contributions from A. Arbouet, R. Marty and P.R. Wiecha.
In contrast to most other coupled-dipole codes, pyGDM uses a generalized 
propagator, which allows to cost-efficiently treat large monochromatic problems 
such us polarization-resolved calculations or raster-scan simulations.

pyGDM2 is available on `pypi <https://pypi.python.org/pypi/pygdm2/>`_ and `gitlab <https://gitlab.com/wiechapeter/pyGDM2>`_. 

Detailed documentation with many examples is can be found at the `pyGDM2 documentation website <https://wiechapeter.gitlab.io/pyGDM2-doc/>`_. See also the `documentation paper on arXiv (1802.04071) <https://arxiv.org/abs/1802.04071>`_ or a more `theoretical review about the GDM method <https://doi.org/10.1088/0034-4885/68/8/R05>`_.




Requirements
================================

Python
------------------
    - **python** (3.5+, `python <https://www.python.org/>`_)
    - **numba** (to drastically accelerate computations we use `numba <http://numba.pydata.org/>`_)
    - **numpy** (`numpy <http://www.numpy.org/>`_)
    - **scipy** >= v0.17.0, lower versions supported with restrictions (`scipy <https://www.scipy.org/>`_)

Optional Python packages
-------------------------------------
    - **pytables** (v3.x recommended. For hdf5 saving/loading of simulations. `pytables <https://www.pytables.org/>`_)
    - **matplotlib** (*Strongly recommended*. For all 2D visualization tools. `matplotlib <https://matplotlib.org/>`_)
    - **mayavi** (for all 3D visualization. `mayavi <http://docs.enthought.com/mayavi/mayavi/mlab.html>`_)
    - **mpi4py** (for MPI parallelized calculation of spectra. `mpi4py <http://mpi4py.readthedocs.io/en/stable/>`_)
    - **PIL** (image processing. `PIL <https://pypi.python.org/pypi/PIL>`_)
    - **PaGMO / PyGMO** (version 2.4+. *Required* for the **EO** submodule. `pagmo <https://esa.github.io/pagmo2/>`_)
    - **cupy** (version 7+, for GPU-based matrix inversion) `cupy <https://docs-cupy.chainer.org/en/stable/index.html>`_)

(all available via `pip <https://pypi.python.org/pypi/pip>`_)



Installation under linux
=============================================

Via pip
-------------------------------

Install from pypi repository via

.. code-block:: bash
    
    $ pip install pygdm2



Via source code
-------------------------------

From source, install pyGDM via the setup-script. *DO NOT use the setup.py directly for installation*, this may install pyGDM as "egg" which leads to problems with *numba* caching.
Please use pip instead. Run the following command in the source directory:

.. code-block:: bash
    
    $ pip3 install . --user

For a system wide installation, run as superuser without the *--user* argument. 
To install to a user-defined location, use the *target* option:

.. code-block:: bash
    
    $ pip3 install . --target=/some/specific/location


To only compile without installation, you can use the setup.py script

.. code-block:: bash
    
    $ python3 setup.py build sdist


        


Installation under windows
=============================================

For windows, we also recommend `Anaconda <https://www.anaconda.com/download/#windows>`_ in which pyGDM can be installed easily via pip. From pyGDM2 V1.1 on, installation from source should work straightforward in any other python distribution as well (described above).

Via pip
-------------------------------

We provide a 64bit windows binary on the pypi repository (tested on Win7 and Win10). Install via

.. code-block:: bash
    
    $ pip install pygdm2



Installation under Mac OS X
=============================================

Tested with the pypi version, installation via pip, with the Anaconda distribution. From pyGDM2 V1.1 on, installation from source should work straightforward in any other python distribution as well (described above).

   .. code-block:: bash
    
        $ pip install pygdm2




Authors
=========================

Python implementation
------------------------
   - P\. R. Wiecha
   - contributions by C\. Majorel


Original fortran code by
-------------------------
   - **Ch\. Girard**
   - A\. Arbouet
   - R\. Marty
   - P\. R. Wiecha



   


