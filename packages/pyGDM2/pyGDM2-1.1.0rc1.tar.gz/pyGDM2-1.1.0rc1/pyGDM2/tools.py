# encoding: utf-8
#
#Copyright (C) 2017-2021, P. R. Wiecha
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
"""
Collection of various tools for (non-physical) data processing

"""
from __future__ import print_function
from __future__ import absolute_import

import six
from six.moves import cPickle as pickle

import copy
import warnings
from operator import itemgetter

import numpy as np

from pyGDM2 import core
from pyGDM2 import core_py



## --- colors for console output
import platform
if platform.system() != 'Windows':
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
else:
    class bcolors:
        HEADER = ''
        OKBLUE = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''



#==============================================================================
# Save / load simulations
#==============================================================================
def save_simulation(sim, fname, mode='h5', 
                    tables_filter_kwargs=dict(complib='blosc', complevel=5), 
                    pickle_protocol=None):
    """Save simulation object to file using  `pickle` and hdf5 via `tables`
    
    The electric fields are stored using hdf5 (via `tables`), the rest via `pickle`.
    If not `tables` module available, everything will be stored via `pickle`.
    This behavior can be forced with the `mode` parameter.
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    fname : str
        filename to save sim to
    
    mode : str, default: "hdf5"
        which method to use to store data. Either "pickle" or "hd5f" ("h5"=="hd5f")
    
    tables_filter_kwargs : dict, default: {'complib':'blosc', 'complevel':5}
        filter kwargs, passed to `tables.Filters` if using the "hdf5" mode
    
    pickle_protocol : int, default: None
        override default pickle protocol level. "2" is compatible with python2 and 3.
    
    """
    ## check extension, if none, use '.pygdmsim'
    import os
    if os.path.splitext(fname)[1] == '':
        fname += '.pygdmsim'
    
## -----    pickle + pytables (hdf5)
    def pickle_sim(sim):
        if pickle_protocol is None:
            pickle.dump( sim, open( fname, "wb" ) )
        else:
            pickle.dump( sim, open( fname, "wb" ), protocol=pickle_protocol )
    
    if mode.lower() in ['h5', 'hdf5']:
        try:
            import tables
            
                    ## write E-field to h5
            if sim.E is not None:
                FILTERS = tables.Filters(**tables_filter_kwargs)
                f = tables.open_file(fname + '.h5', 'w', filters=FILTERS)
                
                grp_E = f.create_group('/', 'E')
                
                E_dicts = []
                for i, ef in enumerate(sim.E):
                    Edict = ef[0]
                    E_dicts.append([Edict, None])   # remove E-field-data
                    E = ef[1]
                    f.create_carray(grp_E, 'E{}'.format(i), obj=E)
                f.close()
                
                ## write rest (without sim.E fields) to pickle file
                E = sim.E
                sim.E = E_dicts    
                pickle_sim(sim)
                sim.E = E
            else:
                pickle_sim(sim)
            
        except ImportError:
            warnings.warn("'hdf5' mode requires `tables` module. Seems not to be installed. " + 
                          "Falling back to pure 'pickle' mode.")
            mode = 'pickle'
    
## -----    save using pickle only 
    if mode.lower() == 'pickle':
        pickle_sim(sim)
    
    
    
    
def load_simulation(fname, pickle_encoding=None):
    """Load simulation from file using `pickle`
    
    Try loading hdf5 first, if no hdf5 file or no `tables` module available, 
    fallback to `pickle`.
    
    Parameters
    ----------
    fname : `str`
        filename to load sim from
    
    pickle_encoding : str, default: None
        for python 2/3 intercompatibility. Use "latin1" to load data 
        saved in python2 from python3
    
    Returns
    -------
    instance of :class:`.core.simulation`
    """
    ## check extension, if none, use '.pygdmsim'
    import os
    if os.path.splitext(fname)[1] == '':
        fname += '.pygdmsim'
        
        
    ## --- try first hdf5, if fails, use pure pickle
    try:
        import tables
    
        ## load meta-data from pickle ("encoding" for python 2/3 compatibility)
        if pickle_encoding is None:
            try:
                sim = pickle.load( open( fname, "rb" ) )
            except UnicodeDecodeError:
                warnings.warn('Unicode error encountered during loading. Can be cause by python2-savefiles. Trying "latin1" encoding...')
                sim = pickle.load( open( fname, "rb" ), encoding='latin1' )
        else:
            sim = pickle.load( open( fname, "rb" ), encoding=pickle_encoding )
        
        ### efields from hdf5
        f = tables.open_file(fname + '.h5', 'r')
        for ef in f.root.E:
            enr = int(ef.name[1:])
            E = ef.read()
            sim.E[enr][1] = E
        f.close()
        
    except (IOError, ImportError) as e:
        import os.path
        if os.path.isfile(fname + '.h5'):
            warnings.warn("hdf5 file seems to exists, but pytables is not installed. " +
                          "The simulation results in the file will probably not be reloaded.")
    
    
    ## --- compatibility with old API
    if not hasattr(sim, 'dyads'):
        warnings.warn("Loading old API simulation. Reconstructing internal attributes.")
        from pyGDM2 import structures
        from pyGDM2 import propagators
        
        ## reconstruct environment with the new Dyads class
        n1, n2, n3 = sim.struct.n1, sim.struct.n2, sim.struct.n3
        spacing = sim.struct.spacing
        
        struct = structures.struct(sim.struct.step, sim.struct.geometry, sim.struct.material)
        sim.struct = struct
        dyads = propagators.DyadsQuasistatic123(n1, n2, n3, spacing)
        sim.dyads = dyads
        
        ## add empty H-field
        sim.H = None
    
    return sim



    




#==============================================================================
# INFO PRINTING
#==============================================================================
def print_sim_info(sim, prnt=True, verbose=False):
    """print simulation info from simdict
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
        
    prnt : bool, default: True
        If True, print to sdtout. If False, return string
    
    verbose : bool, default: False
        if True, print more details like exhaustive incident field 
        parameter list
    
    Notes
    -----
    :func:`.print_sim_info` is implemented as its `__repr__` attribute in 
    :class:`.core.simulation`. This means
    
    >>> print sim
    
    and
    
    >>> print_sim_info(sim)
    
    will result in the identical output
    
    """
    if not hasattr(sim, 'dyads'):   # ! COMPATIBILITY WITH OLD API
        return _print_sim_info_old_API(sim, prnt, verbose)
    else:
        
        
        out_str = ''
        out_str += '\n' + ' =============== GDM Simulation Information ==============='
        out_str += '\n' + 'numerical precision: {} / {}'.format(sim.dtypef, sim.dtypec)
        
        ## -------------------- structure
        out_str += '\n\n'
        out_str += sim.struct.__repr__(verbose=verbose)
    
        ## -------------------- field
        out_str += '\n\n'
        out_str += sim.efield.__repr__(verbose=verbose)
        
        ## -------------------- environment
        out_str += '\n\n'
        out_str += sim.dyads.__repr__(verbose=verbose)
        
        ## -------------------- simulation status
        out_str += '\n' + ''
        out_str += '\n' + ' ===== *core.scatter* ======'
        if sim.E is None:
            out_str += '\n' + bcolors.FAIL + '   NO self-consistent E-fields'.format() + bcolors.ENDC
        else:
            out_str += '\n' + bcolors.OKGREEN + '   self-consistent E-fields are available'.format() + bcolors.ENDC
        try:
            if sim.H is None:
                out_str += '\n' + bcolors.FAIL + '   NO self-consistent H-fields'.format() + bcolors.ENDC
            else:
                out_str += '\n' + bcolors.OKGREEN + '   self-consistent H-fields are available'.format() + bcolors.ENDC
        except NameError:
            pass
        
        if prnt:
            print(out_str)
        else:
            return out_str


def _print_sim_info_old_API(sim, prnt=True, verbose=False):
    """print simulation info from simdict
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
        
    prnt : bool, default: True
        If True, print to sdtout. If False, return string
    
    verbose : bool, default: False
        if True, print more details like exhaustive incident field 
        parameter list
    
    Notes
    -----
    :func:`.print_sim_info` is implemented as its `__repr__` attribute in 
    :class:`.core.simulation`. This means
    
    >>> print sim
    
    and
    
    >>> print_sim_info(sim)
    
    will result in the identical output
    
    """
    warnings.warn('Deprecation warning! Simulation instance based on former API detected. ' +
                  'Compatibility will be removed in a future version.')
    S = sim
    
    ## -- meshing
    if S.struct.normalization == 1:
        meshing = 'cubic'
    else:
        meshing = 'hexagonal compact'
    
    out_str = ''
    out_str += '\n' + ' =============== GDM Simulation Information ==============='
    out_str += '\n' + 'precision: {} / {}'.format(sim.dtypef, sim.dtypec)
    out_str += '\n' + ''
    
    
    ## -------------------- structure
    out_str += '\n' + ''
    out_str += '\n' + ' ------ nano-object -------'
    if len(set(sim.struct.material)) <= 1:
        out_str += '\n' + '   Homogeneous object. '
        out_str += '\n' + '   material:             "{}"'.format(sim.struct.material[0].__name__)
    if len(set(sim.struct.material)) > 1:
        out_str += '\n' + '   Inhomogeneous object, consisting of {} materials'.format(
                                                 len(set(sim.struct.material)))
        if verbose:
            diff_mat = np.unique([s.__name__ for s in sim.struct.material])
            for i, mat in enumerate(set(diff_mat)):
                out_str += '\n' + '      - {}: "{}"'.format(i, mat)
    out_str += '\n' + '   mesh type:            {}'.format(meshing)
    out_str += '\n' + '   nominal stepsize:     {}nm'.format(sim.struct.step)
    out_str += '\n' + '   nr. of meshpoints:    {}'.format(sim.struct.n_dipoles)

    
    ## -------------------- field
    out_str += '\n' + ''
    out_str += '\n' + ' ----- incident field -----'
    out_str += '\n' + '   field generator: "{}"'.format(sim.efield.field_generator.__name__)
    out_str += '\n' + '   {} wavelengths between {} and {}nm'.format(
                     len(sim.efield.wavelengths), sim.efield.wavelengths.min(),
                     sim.efield.wavelengths.max(),)
    if verbose:
        for i, wl in enumerate(sim.efield.wavelengths):
            out_str += '\n' + '      - {}: {}nm'.format(i,wl)
    out_str += '\n' + '   {} incident field configurations per wavelength'.format(
                                    len(sim.efield.kwargs_permutations))    
    if verbose:
        for i, kw in enumerate(sim.efield.kwargs_permutations):
            out_str += '\n' + '      - {}: {}'.format(i,str(kw).replace("{","").replace("}",""))
    
    
    ## -------------------- environment
    out_str += '\n' + ''
    out_str += '\n' + ' ------ environment -------'
    out_str += '\n' + '   n3 = {}  <-- top'.format(sim.dyads.n3_material.__name__)
    out_str += '\n' + '   n2 = {}  <-- center layer (height "spacing" = {}nm)'.format(
                    sim.dyads.n2_material.__name__, sim.dyads.spacing)
    out_str += '\n' + '   n1 = {}  <-- substrate'.format(sim.dyads.n1_material.__name__)
    
    
    ## -------------------- simulation status
    out_str += '\n' + ''
    out_str += '\n' + ' ===== *core.scatter* ======'
    if sim.E is None:
        out_str += '\n' + bcolors.FAIL + '   NO self-consistent E-fields'.format() + bcolors.ENDC
    else:
        out_str += '\n' + bcolors.OKGREEN + '   self-consistent E-fields are available'.format() + bcolors.ENDC
    
    
    if prnt:
        print(out_str)
    else:
        return out_str






#==============================================================================
# General purpose array / list processing tools
#==============================================================================
def unique_rows(a):
    """delete all duplicates with same x/y coordinates
    
    Parameters
    ----------
    a : list of tuples
        list of (x,y) or (x,y,z) coordinates with partially redunant (x,y) values.
    
    Returns
    -------
    list of tuples in which all multiple tuples with equal first and second value 
    (x,y coordinates) are removed.
    If 3-D data: Z-coordinate (3rd column) is replaced by 0.
    
    """
    a = np.array(a)
    if np.shape(a)[1] == 3:
        Ndim = 3
        a = np.ascontiguousarray(a.T[:2].T)
    elif np.shape(a)[1] == 2:
        Ndim = 2
        a = np.ascontiguousarray(a)
    else:
        raise ValueError("Coordinate list must consist of either 2- or 3-tuples.")
    
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    unique_a = unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

    if Ndim == 3:
        unique_a = np.append(unique_a.T, [np.zeros(unique_a.shape[0])], axis=0).T
    
    return unique_a



def unique_rows_3D(a):
    """delete all duplicates with same x/y/z coordinates
    
    Parameters
    ----------
    a : list of tuples
        list of (x,y,z) coordinates with partially redunant (x,y) values.
    
    Returns
    -------
    list of tuples in which all multiple tuples with equal (x,y,z) coordinates
    are removed.
    """
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))



def list_to_grid(arr, S=None, NX=None, NY=None, interpolation='nearest', fill_value=np.nan, **kwargs):
    """
    List of X/Y/Z tuples to 2D x/y Grid with z as intensity value
    
    Parameters
    ----------
    arr : np.array 
        array of either (X,Y) or (X,Y,Z) tuples
    
    S : np.array (optional, default: None)
        if `arr` is list of (x,y)-tuples, S is a list containing the 
        scalar Z-values corresponding to each (x,y)-coordinate.
      
    NX, NY : int, optional 
        number of points in X/Y direction for interpolation
                default: Number of unique occuring x/y elements 
                         (using np.unique)
    
    interpolation : str, default: 'nearest'
        interpolation method for grid, passed to `scipy.griddata`
        
    **kwargs are passed to `scipy.interpolate.griddata`
    
    Returns
    -------
    Z : np.array, dim=2 
        Z on X/Y plane (linear X/Y ranges)
        
    extent : tuple 
        X/Y extent of array `Z`: (Xmin,Xmax, Ymin,Ymax)
    
    """
    from scipy.interpolate import griddata
    if len(arr.T) == 2:
        arr = np.concatenate([arr, np.transpose([S])], axis=1).T
    elif len(arr.T) == 3:
        arr = arr.T
    else:
        raise ValueError("Wrong input data format.")
    
    ## --- Interpolate on 2D Grid
    Xsim0,Xsim1 = float(np.min(arr[0])), float(np.max(arr[0]))
    Ysim0,Ysim1 = float(np.min(arr[1])), float(np.max(arr[1]))
    extent = [Xsim0,Xsim1, Ysim0,Ysim1]
    
    if NX is None:
        NX=len(np.unique(arr[0]))
    if NY is None:
        NY=len(np.unique(arr[1]))
    
    grid_x, grid_y = np.mgrid[Xsim0:Xsim1:NX*1j, Ysim0:Ysim1:NY*1j]

    Z = griddata(np.transpose([arr[0],arr[1]]),      # x,y Columns
                            arr[2],                  # Z-Value Column
                            (grid_x, grid_y),        # grid to map data to
                            method=interpolation,
                            fill_value=fill_value, **kwargs)       # interpolation method
    Z = np.flipud(Z.T)
    Z = np.array(Z, dtype=arr.dtype)
    return Z, extent


def grid_to_list(arr2d, extent=None, add_z=False):
    """create list of X/Y/S tuples from 2D map data
    
    Parameters
    ----------
    arr2d : 2D np.array
        2D data array of shape (Nx, Ny)
    
    extent : 4-tuple, default: None
        X / Y limits of array as tuple (x0, x1, y0, y1). 
        If `None`, uses integer steps between 0 and Nx, Ny.
    
    add_z : bool, default: False
        if true, returns (x,y,z,S) tuples, with z=0
    
    Returns
    -------
    scalarfield : np.array
        list of (x,y,S) values, where S are the values of the original 2D map `arr2d`
    
    """
    arr2d = np.flipud(arr2d)
    if extent is None:
        extent = [0,arr2d.shape[1],0,arr2d.shape[0]]
    
    xpos = np.linspace(extent[2], extent[3], arr2d.shape[1])
    ypos = np.linspace(extent[0], extent[1], arr2d.shape[0])
    scalarfield = []
    for iy, Ly in enumerate(arr2d):
        for ix, s in enumerate(Ly):
            if add_z:
                scalarfield.append([xpos[ix], ypos[iy], 0, s])
            else:
                scalarfield.append([xpos[ix], ypos[iy], s])
    
    return np.array(scalarfield)



def map_to_grid_2D(MAP, IVALUES, NX=-1, NY=-1):
    """
    Generate XY plottable map e.g. from 2D nearfield calculation
      
    Parameters
    ----------
    MAP : list of lists or list of tuples
        2D MAP corresponding to data-array (e.g. from 'generate_NF_map').
        
        - If list of lists : 
            MAP[0] --> first coordinate; MAP[1] --> second coordinate.
            
        - If list of tuples : 
            list of (x,y) or (x,y,z) tuples. In the latter case, "z" will be ignored.
        
    IVALUES : list of floats
        Data-array: Intensity at each MAP position
    
    NX, NY : int, int, default: number of unique X/Y entries in MAP. 
        Nr of points to calculate for each dimension (do interpolation in nescessary)
    
    Returns
    -------
    NF_MAP : 2d-array
        nearfield map
    
    extent : tuple
        extent of map (x0,x1, y0,y1)
    """
    ## !!! delete this fct in future release
    warnings.warn("deprecation warning: This function will be removed in a future release." + 
                  "Use `list_to_grid` instead, which provides the same functionality. " +
                  "(tools.list_to_grid(np.transpose([MAP[0], MAP[1], IVALUES]), NX, NY))")
    
    
    if np.shape(MAP)[1] in [2,3]:
        MAP = np.transpose(MAP)
    
    if len(np.shape(IVALUES)) == 2:
        if np.shape(IVALUES)[1] == 10:
            IVALUES = IVALUES.T[-1]
    if len(IVALUES) == np.shape(MAP)[1]:
        IVALUES = IVALUES.T
    elif len(IVALUES.T) == np.shape(MAP)[1]:
        pass
    else:
        raise ValueError("Dimensions of map-definition and field-array not matching!")
    
    if NX==-1:
        NX = len(np.unique(MAP[0]))
    if NY==-1:
        NY = len(np.unique(MAP[1]))
    
    NF_MAP, extent = list_to_grid(np.transpose([MAP[0], MAP[1], IVALUES]), NX, NY)
    
    return NF_MAP, extent


    
    
#==============================================================================
# GENERAL PURPOSE GEOMETRY TOOLS 
#==============================================================================
def test_geometry(struct, step=None, delete_duplicates_first=True, 
                  plotting='fail', return_index=False, verbose=1):
    """return coordinate lists X,Y,Z either from list of tuples or `simulation` object
    
    requires `scipy`
    
    Parameters
    ----------
    struct : list of tuple *or* :class:`.core.simulation` *or* :class:`.structures.struct`
        list of coordinate tuples or instance of :class:`.core.simulation` or
        instance of :class:`.structures.struct`
    
    step : float, default: None
        Test if structure is consistent with the given step-size.
        If None, determine step from geomerty. However, step should normally 
        be given by the user. The test is likely to be false positive if 
        step is set None.
    
    delete_duplicates_first : bool, default: True
        delete duplicates, then 
    
    plotting : bool or str, default: 'fail'
        plot consistent and inconsistent parts of structure. Either True, False
        or "fail". If "fail" (default), plot only in case of insconsistent structure.
    
    return_index : bool, default: False
        if True, returns also ist of indices that compose the "correct" geometry
    
    verbose : int, default: 1
        verbose level for info printing. verbose = 2 prints additional info
    
    
    Returns
    -------
    two numpy arrays of (x,y,z) tuples:
        geo_correct, geo_wrong
    
    """
    try:
        import time
        from scipy.spatial import cKDTree as KDTree
        geo0 = get_geometry(struct, return_type='tuples')
        
        ## empty or 1-dipole structure:
        if len(geo0) <= 1:
            if return_index:
                return geo0, [], np.arange(len(geo0))
            else:    
                return geo0, []
        
        if step is None:
            warnings.warn("Geometry-test: `step` not given. Will try to infer step from geomgetry, but this geometry test might be false positive in this case.")
            step = step or get_step_from_geometry(struct)
        
        if delete_duplicates_first:
            geo_unique, idx_non_duplicate = np.unique(np.round(geo0, 5), axis=0, return_index=True)
            geo_duplicate = np.delete(geo0, idx_non_duplicate, axis=0)
            if len(geo_duplicate) > 0 and verbose >= 1:
                warnings.warn("Duplicate meshpoints found! Removed {} duplicates.".format(len(geo_duplicate)))
            geo = geo_unique
        else:
            geo = geo0
        
        if verbose >= 2: t0 = time.time()
        kdtree = KDTree(geo)
        geo_correct, geo_wrong = [], []
        index_correct = []
        for i, pos in enumerate(geo):
            next_neighbors = kdtree.query(pos, k=3)
            dist_nn = next_neighbors[0][1]
            if np.ceil(dist_nn*1E3)/1E3 < np.floor(step*1E5)/1E5:
            # if np.ceil(dist_nn*1E3)/1E3 < .1*step:
                geo_wrong.append(pos)
                if verbose >= 2:
                    print("   - Inconsistent dipole #{} at {}".format(i, pos))
            else:
                geo_correct.append(pos)
                index_correct.append(i)
            if dist_nn==np.inf:
                warnings.warn("Division by zero detected. Several dipoles may exist at same position or stepsize is set to zero?")
                geo_wrong.append(pos)
        geo_wrong = np.array(geo_wrong)
        geo_correct = np.array(geo_correct)
        
        if delete_duplicates_first:
            ## use kd-"correct" elements of non-duplicate index-list
            index_correct = idx_non_duplicate[index_correct] 
            if len(geo_wrong) > 0:
                geo_wrong = np.concatenate([geo_duplicate, geo_wrong])
        else:
            ## use only kdtree-"correct" list
            index_correct = np.array(index_correct)
        
        if verbose >= 2:
            t1 = time.time()
            print("Structure consistency analysis done in {:.2f}s.".format(t1-t0))
            if len(geo_wrong)==0:
                print("Everything ok. All {} dipoles are consistent with step={:.2f}nm.".format(len(geo), step))
        
        if str(plotting).lower() == 'true' or (str(plotting).lower()=="fail" and len(geo_wrong)!=0):
            import matplotlib.pyplot as plt
            from pyGDM2 import visu
            plt.subplot(aspect='equal')
            
            ## override `visu.structure` auto scaling
            scale = (500/max([geo.T[0].max()-geo.T[0].min(), 
                          geo.T[1].max()-geo.T[1].min()])**0.8 / np.sqrt(step))
            if len(geo_wrong)!=0:
                if len(geo_correct)!=0:
                    visu.structure(geo_correct, color='C2', show=0, absscale=1, scale=scale,
                                   label='consistent')
                visu.structure(geo_wrong, color='C3', show=0, absscale=1, scale=scale,
                               label='inconsistent')
                plt.title("! inconsistent structure !", color='C3')
                plt.legend()
            else:
                visu.structure(geo_correct, color='C2', show=0, absscale=1, scale=scale)
                plt.title("consistent structure", color='C2')
            
            plt.xlim(geo.T[0].min()-3*step, geo.T[0].max()+3*step)
            plt.ylim(geo.T[1].min()-3*step, geo.T[1].max()+3*step)
            plt.xlabel("X (nm)")
            plt.ylabel("Y (nm)")
            plt.show()
        
        if len(geo_wrong)!=0:
            warnings.warn("Inconsistent structure!!! {} of {} dipoles don't match with step={:.2f}nm.".format(
                                len(geo_wrong), len(geo0), step))
        
        if return_index:
            return geo_correct, geo_wrong, index_correct            
        else:
            return geo_correct, geo_wrong
    
    except ImportError:
        warnings.warn("`scipy` seems to be not installed. Skipping geometry consistency check.")
        return geo, np.array([])


def get_geometry(struct, return_type='lists'):
    """return coordinate lists X,Y,Z either from list of tuples or `simulation` object
    
    Parameters
    ----------
    struct : list of tuple *or* :class:`.core.simulation` *or* :class:`.structures.struct`
        list of coordinate tuples or instance of :class:`.core.simulation` or
        instance of :class:`.structures.struct`
    
    projection : str, default: "XY"
        2D plane for projection. One of ['XY', 'XZ', 'YZ']
        
    return_type : str, default: 'lists'
        either 'lists' or 'tuples'
         - 'tuples' : return list of (X,Y,Z)-tuples
         - 'lists' : return 3 lists with X, Y and Z values
    
    Returns
    -------
    if return_type == 'lists' :
        np.array containing 3 np.arrays with the X, Y and Z coordinates
    if return_type == 'tuples' :
        list of 3-tuples : (x,y,z) coordinates of geometry
    """
    from pyGDM2 import structures
    
    if type(struct) in [list, np.ndarray]:
        pass
    elif type(struct) in [core.simulation, core_py.simulation] :
        struct = struct.struct.geometry
    elif type(struct) == structures.struct:
        struct = struct.geometry
    else:
        raise Exception("Got no valid structure data.")
        
    if return_type.lower() == 'lists':
        return_value = np.transpose(struct)
    elif return_type.lower() == 'tuples':
        return_value = struct
    else:
        raise ValueError("`return_type` must be either 'lists' or 'tuples'.")
    
    return return_value


def get_step_from_geometry(struct, max_meshpoints=1000):
    """Calculate step from coordinate list defining a nano-object
    
    Will return closest distance occuring between two meshpoints. 
    Uses `scipy.spatial.distance`.
    
    
    Parameters
    ----------
    struct : list of tuples or :class:`.core.simulation`
    
    max_meshpoints : int, default: 1000
        maximum number of meshpoints to consider for step-calculation if using 
        `scipy.spatial.distance`. (for computational speed at large structures)
        
    Returns
    -------
    step : float
        stepsize between mesh-points
    
    """
    from pyGDM2 import structures
    
    ## coordinate list
    if type(struct) in [list, np.ndarray]:
        from scipy.spatial import distance
        geometry = get_geometry(struct, return_type='tuples')
        
        if len(geometry) == 1:
            warnings.warn("structure consists of a single dipole. Is this on purpose?")
            step = 1
        elif len(geometry) == 0:
            warnings.warn("empty structure. Setting step to 1.")
            step = 1
        else:
            if len(geometry) > max_meshpoints:
                geometry = geometry[:max_meshpoints]
            step = distance.pdist(geometry).min()
    
    ## simulation object   
    elif type(struct) in [core.simulation, core_py.simulation]:

        step = struct.struct.step
    ## structure object   
    elif type(struct) == structures.struct:
        step = struct.step
    
    else:
        raise Exception("Got no valid structure data.")
    
    return step


def get_mesh_from_geometry(geo, N_try=20, verbose=0):
    """Try to identify the mesh type from the dipole positions
    
    If meshpoint determination fails, falling back to `cube`
    
    
    Parameters
    ----------
    geo : list of tuples or :class:`.core.simulation`
        list of meshpoints to determine grid-type
    
    N_try : int, default: 20
        maximum number of random evaluation point tries in order to find a
        "bulk" meshpoint.
        
    verbose: int, default: 0
        if 1, print runtime info
        
    Returns
    -------
    mesh : str
        mesh type ('cube' or 'hex')
    
    """
    lookup_meshtype = {
        10.24:"cube",  # 3D
        10.66:"cube",  # 2-layer 3D
        11.66:"cube",  # 2D

        9.0:"hex",     # 3D
        11.0:"hex",   # 2-layer 3D
        11.20:"hex",   # 2D - config1
        11.28:"hex",   # 2D - config2
        }
    
    if len(geo) <= 1:
        if len(geo) == 0:
            warnings.warn("Empty structure. Setting mesh to 'cubic'.")
        if len(geo) == 1:
            warnings.warn("Single dipole. Setting mesh to 'cubic'.")
        return 'cube'
    
    step = get_step_from_geometry(geo)
    
    all_distsum = []
    for  i_try in range(N_try):
        idx_center = np.random.randint(len(geo))
        all_distsum.append(np.sort(np.linalg.norm(geo - geo[idx_center], axis=1))[:10].sum() / step)
        
    distsum = np.min(all_distsum)
    try:
        meshtype = lookup_meshtype[np.round(distsum, 2)]
        if verbose:
            print("step= {:.1f}, distsum={:.2f} --> mesh: '{}'".format(step, distsum, meshtype))
    except KeyError:
        warnings.warn("Mesh not detected, falling back to 'cubic'.")
        meshtype = 'cube'
    
    return meshtype


def get_geometry_2d_projection(struct, projection='XY'):
    """return the geometry projection onto a 2D-plane
    
    Parameters
    ----------
    struct : list of tuples or :class:`.core.simulation`
    
    projection : str, default: "XY"
        2D plane for projection. One of ['XY', 'XZ', 'YZ']
    
    Returns
    -------
    list of 3-tuples : (x,y,z) coordinates of 2D-projection (third coordinate set to zero)
        
    """
    geometry = get_geometry(struct, return_type='lists')
    
    if projection.lower() == "xy":
        geo_reduced = geometry[ [0,1] ]
    elif projection.lower() == "xz":
        geo_reduced = geometry[ [0,2] ]
    elif projection.lower() == "yz":
        geo_reduced = geometry[ [1,2] ]
    else:
        raise ValueError("Invalid projection parameter!")
    
    twoD = unique_rows(geo_reduced.T).T
    
    if projection.lower() == "xy":
        geo_proj_2d = np.concatenate([[twoD[0]], [twoD[1]], [np.zeros(len(twoD[0]))]], axis=0).T
    elif projection.lower() == "xz":
        geo_proj_2d = np.concatenate([[twoD[0]], [np.zeros(len(twoD[0]))], [twoD[1]]], axis=0).T
    elif projection.lower() == "yz":
        geo_proj_2d = np.concatenate([[np.zeros(len(twoD[0]))], [twoD[0]], [twoD[1]]], axis=0).T
        
    return geo_proj_2d


def get_geometric_cross_section(struct, projection='XY', step=None):
    """return the geometrical cross-section (='footprint') of struct in nm
    
    Parameters
    ----------
    struct : list of tuples or :class:`.core.simulation`
    
    projection : str, default: "XY"
        2D plane for projection. One of ['XY', 'XZ', 'YZ']
    
    step : float, default: None
        optional pass step-size. If `None`, calculate it from geometry (may be slower)
    
    Returns
    -------
    float : geometric cross section of structure projection in nm^2
    """
    twoD_projection = get_geometry_2d_projection(struct, projection='XY')
    if step is None:
        step = get_step_from_geometry(struct)
    
    geom_cs = step**2 * len(twoD_projection)
    
    if type(struct) in [core.simulation, core_py.simulation]:
        norm = struct.struct.normalization
        geom_cs /= norm
    else:
        warnings.warn("Geometric cross-section from meshpoint-list! List does not include info about mesh-type. Assuming cubic mesh!")
    return float(geom_cs)


def get_surface_meshpoints(struct, NN_bulk=6, max_bound=1.2, 
                           NN_surface=-1, max_bound_sf=5.0,
                           return_sfvec_all_points=False):
    """get surface elements and normal surface vectors of structure
    
    Calculate normal vectors using next-neighbor counting.
    
    To use outmost surface layer only, parameters are:
     - 2D: NN_bulk=4, max_bound=1.1
     - 3D: NN_bulk=6, max_bound=1.1
    
    
    Parameters
    ----------
      - struct : structure
        list of tuples or instance of :class:`.core.simulation`
    
      - NN_bulk : int (default: 6)
        Number of Next neighbors of a bulk lattice point
    
      - max_bound : float (default: 1.1)
        Max. distance in step-units to search for next neighbors
      
      - NN_surface : float (default: -1 = value of NN_bulk)
        different number of neighbours to consider for normal surfacevectors
      
      - max_bound_sf : float (default: 5.0)
        different calculation range for normal surfacevectors. 
        By default, use search radius of up to 5 steps. If a large number of 
        neighbours should be considered for vector calculation, it might be 
        necessary to increased this limit, which might however slow down the 
        KD-tree queries.
        
      - return_sfvec_all_points : bool, default: False
        if True, return vector list for all meshpoints, with zero length if bulk
    
    Returns
    -------
      - SF : list of surface meshpoint coordinates
      
      - SF_vec : list of normal surface vectors
      
    """
    from scipy.spatial import cKDTree as KDTree
    
    if NN_surface == -1: 
        NN_surface = NN_bulk
    
    X,Y,Z = get_geometry(struct)
    geometry = np.transpose([X,Y,Z])

    step = get_step_from_geometry(struct)
    
    ## Find number and positions of next neigbours using KD-Tree queries
    kdtree = KDTree(geometry)
    
    SF, SF_vec = [], []
    for i, pos in enumerate(geometry):
        ## query for nearest neighbors
        resultNNbulk = kdtree.query(pos, k=NN_bulk+1, distance_upper_bound=max_bound*step)
        if NN_surface != NN_bulk:
            resultNNsurface = kdtree.query(pos, k=NN_surface+1, 
                                    distance_upper_bound=max_bound_sf*step)
        else:
            resultNNsurface = resultNNbulk
        
        ## exclude center and "empty" positions, get number of neighbors
        IDX = ((resultNNbulk[0] != 0) & (resultNNbulk[0] != np.inf))
        NN = len(resultNNbulk[0][IDX])
        IDXsf = ((resultNNsurface[0] != 0) & (resultNNsurface[0] != np.inf))
        
        ## surface-positions
        if NN < NN_bulk:
            x,y,z = geometry[i]
            ## calculate normal surface vector using nearest neighbors
            Nvec = [(pos[:3] - geometry[j][:3]) for j in resultNNsurface[1][IDXsf]]
            Nvec = np.sum(Nvec, axis=0)
            if np.linalg.norm(Nvec)==0:
                warnings.warn("Indefinite surface element (meshpoint is part of two surfaces)! Using one of two possible sides for normal vector direction!")
                if pos[:3][0] != 0:
                    Nvec = np.array([0,1,0])
                elif pos[:3][1] != 0:
                    Nvec = np.array([1,0,0])
                elif pos[:3][2] != 0:
                    Nvec = np.array([0,1,0])
            else:
                Nvec = Nvec / np.linalg.norm(Nvec)
            SF.append(geometry[i])
            SF_vec.append(Nvec)
        else:
            if return_sfvec_all_points:
                SF_vec.append(np.array([0,0,0]))
    
    return np.array(SF), np.array(SF_vec)




#==============================================================================
# Incident field configuration tools (i.e. searching `field_index`)
#==============================================================================
def get_field_indices(sim):
    """List all field-configurations including wavelength sorted by field-index 
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    Returns
    -------
    list of dict : 
        list of kwargs-dict containing field-config parameters. list in the 
        order of the "field_index" convention.
    """
    wavelengths = sim.efield.wavelengths
    kwargs_permutations = sim.efield.kwargs_permutations
    
    keys = []
    for wavelength in wavelengths:
        for field_kwargs in kwargs_permutations:
            field_kwargs_copy = copy.deepcopy(field_kwargs)
            field_kwargs_copy["wavelength"] = wavelength
            keys.append(field_kwargs_copy)
    
    return keys



def get_closest_field_index(sim, search_kwargs):
    """Find closest calculated scattered field matching to search parameters
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    search_kwargs : dict
        searched kwargs for incident field
    
    
    Returns
    -------
    index : int
        index of field which matches closest search incident field parameters
    """
    if sim.E is None: 
        warnings.warn("Scattered field inside the structure not yet evaluated. Run the `core.scatter` simulation before further evaluations.")
    
    ## -- create dict of differences compared to search-parameters
    keys = get_field_indices(sim)
    
    keys_diff = []
    for idx, d in enumerate(keys):
       keys_diff.append(dict(idx=idx))
       for sk in search_kwargs:
           if type(search_kwargs[sk]) == str:
               ## compare strings
               a = int("".join([str(int(s, base=36)) for s in d[sk]]))
               b = int("".join([str(int(s, base=36)) for s in search_kwargs[sk]]))
               keys_diff[-1][sk] = abs(a - b)
           else:
               ## compare numerical values
               keys_diff[-1][sk] = abs(d[sk]-search_kwargs[sk])
    
    ## -- sort list of difference-dicts using only the search-keys
    sorted_keys_diff = sorted(keys_diff, key=itemgetter(*[k for k in search_kwargs]))
    
    field_index = sorted_keys_diff[0]['idx']    # closest match
    return field_index




#==============================================================================
# Tools for spectrum calculation
#==============================================================================
def get_possible_field_params_spectra(sim):
    """Return all possible field-parameter permutations for spectra
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    Returns
    -------
    params : list of dict
        list of all possible parameter-permutation at each wavelength
    """
    return sorted(sim.efield.kwargs_permutations, key=sorted)


def calculate_spectrum(sim, field_kwargs, func, verbose=False, callback=None, **kwargs):
    """calculate spectra using function `func`
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    field_kwargs : `dict` or `int`
        dict of field-configuration to use from simulation. If an `int` is given,
        it is used as field-index (use e.g. :func:`get_closest_field_index`)
    
    func : function
        evaluation function, which will be called as:
        `func(sim, field_index, **kwargs)`
    
    callback : func, default: None
        optional callback function, which is called after each wavelength.
        Passes a dict to `callback` containing current wavelength, so far
        calculated spectrum and timing info.
    
    **kwargs : 
        all other keyword args are passed to `func`
    
    Returns
    -------
    np.array : wavelengths
    
    np.array : results of `func` for each wavelength
    
    """
    import time
    
    if sim.E is None: 
        raise ValueError("Error: Scattered field inside the structure not yet evaluated. Run `core.scatter` simulation first.")
    
    if type(field_kwargs) == int:
        kw_index = field_kwargs
        field_kwargs = get_possible_field_params_spectra(sim)[field_kwargs]
        if verbose:
            warnings.warn("'field_kwargs' are index instead of dict." + 
                      "Using `get_possible_field_params_spectra`." + 
                      "Using configuration #{}: '{}'".format(kw_index, field_kwargs))
        
    
    if len(field_kwargs) != len(sim.E[0][0])-1 or 'wavelength' in field_kwargs:
        raise ValueError("'field_kwargs' must define every field-parameter except 'wavelength'!")
    
    ## --- spectrum for selected config and evaluation function
    spectrum = []
    wl = []
    for i, E in enumerate(sim.E):
        t0 = time.time()
        params = E[0]
        skip = False
        for kw in field_kwargs:
            try:
                if params[kw] != field_kwargs[kw]:
                    skip = True
            except ValueError:
                if np.all(params[kw] != field_kwargs[kw]):
                    skip = True
        if not skip:
            dat = func(sim, i, **kwargs)
            wl.append(params['wavelength'])
            spectrum.append(dat)
            if callback is not None:
                cb_continue = callback(dict(
                    spectrum=spectrum, wavelengths=wl,
                    t_wl=1000.*(time.time()-t0))
                                  )
                if not cb_continue:
                    break           # quit if callback returns False
    
    ## --- try to convert to numpy arrays
    try:
        wl = np.array(wl)
        spectrum = np.array(spectrum)
        if len(spectrum) > 1 and spectrum.shape[-1] == 1:
            spectrum = spectrum.T[0].T
    except:
        pass
    
    return wl, spectrum
    

    




#==============================================================================
# Tools for rasterscan calculation
#==============================================================================
def get_possible_field_params_rasterscan(sim, key_x_pos='xSpot', key_y_pos='ySpot'):
    """Return all possible field-parameter permutations for raster-scan simulations
    
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    key_x_pos : `str`, default: 'xSpot'
        parameter-name defining the rasterscan beam/illumination x-position
    
    key_y_pos : `str`, default: 'ySpot'
        parameter-name defining the rasterscan beam/illumination y-position
    
    Returns
    -------
    params : `list` of `dict`
        `list` of `dict` for all possible parameter-permutation, defining rasterscan map
    """
    kw_all_perm = sim.efield.kwargs_permutations
    kw_without_spotpos = copy.deepcopy(kw_all_perm)
    
    if key_x_pos not in kw_all_perm[0] or key_y_pos not in kw_all_perm[0]:
        raise ValueError("x-position and y-position defining parameters (currently: '{}' and '{}') must exist in simulation!".format(key_x_pos, key_y_pos))
    
    ## --- remove spot-positions from dicts, then delete duplicate dicts
    for p in kw_without_spotpos:
        p.pop(key_x_pos, None)
        p.pop(key_y_pos, None)
    permutations_without_wavelength = [dict(t) for t in 
                           set([tuple(d.items()) for d in kw_without_spotpos])]
    
    ## ---  add wavelengths
    permutations = []
    for wl in sim.efield.wavelengths:
        for p in permutations_without_wavelength:
            permutations.append(copy.deepcopy(p))
            permutations[-1]['wavelength'] = wl
    
    return sorted(permutations, key=lambda d: sorted(d.items()))



def get_rasterscan_fields(sim, search_kwargs, key_x_pos='xSpot', key_y_pos='ySpot'):
    """Return list of all field-parameter sets for a raster-scan
    
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    search_kwargs : dict
        searched kwargs for incident field
    
    key_x_pos : str, default: 'xSpot'
        parameter-name defining the rasterscan beam/illumination x-position
    
    key_y_pos : str, default: 'ySpot'
        parameter-name defining the rasterscan beam/illumination y-position
    
    
    Returns
    -------
    NF_rasterscan : list of lists
        Each element corresponds to the simulated E-field inside the 
        particle at a scan position: [field_param_dict, NF]
        - field_param_dict is the dict with the field-generator parameters
        - NF is the nearfield, as list of complex 3-tuples (Ex_i, Ey_i, Ez_i)
    """
    kw_all_perm = sim.efield.kwargs_permutations
    if type(search_kwargs) == int:
        kw_index = search_kwargs
        search_kwargs = get_possible_field_params_rasterscan(sim, key_x_pos, key_y_pos)[search_kwargs]
        warnings.warn("'search_kwargs' are index instead of dict. Using `get_possible_field_params_rasterscan`. Using configuration #{}: '{}'".format(kw_index, search_kwargs))
    
    if len(search_kwargs) != len(kw_all_perm[0])-1 or 'wavelength' not in search_kwargs:
        raise ValueError("'search_kwargs' must define every field-parameter except the 2 position parameters.")
    if sim.E is None: 
        raise ValueError("Error: Scattered field inside the structure not yet evaluated. Run `core.scatter` simulation first.")
    
    
    NF_rasterscan = []
    for i in sim.E:
        skip = False
        for kw in search_kwargs:
            if i[0][kw] != search_kwargs[kw]:
                skip = True
        if not skip:
            NF_rasterscan.append(i)
    
    return NF_rasterscan


def get_rasterscan_field_indices(sim, search_kwargs, key_x_pos='xSpot', key_y_pos='ySpot'):
    """Return list of all field-parameter-indices corresponding to a raster-scan
    
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    search_kwargs : dict
        searched kwargs for incident field
    
    key_x_pos : str, default: 'xSpot'
        parameter-name defining the rasterscan beam/illumination x-position
    
    key_y_pos : str, default: 'ySpot'
        parameter-name defining the rasterscan beam/illumination y-position
    
    
    Returns
    -------
    NF_rasterscan_indices : list of int
        index of field which matches closest search incident field parameters
    """
    kw_all_perm = sim.efield.kwargs_permutations
    if type(search_kwargs) == int:
        kw_index = search_kwargs
        search_kwargs = get_possible_field_params_rasterscan(sim, key_x_pos, key_y_pos)[search_kwargs]
        warnings.warn("'search_kwargs' are index instead of dict. Using `get_possible_field_params_rasterscan`. Using configuration #{}: '{}'".format(kw_index, search_kwargs))
        
    if len(search_kwargs) != len(kw_all_perm[0])-1 or 'wavelength' not in search_kwargs:
        raise ValueError("'search_kwargs' must define every field-parameter except the 2 position parameters.")
    if sim.E is None: 
        raise ValueError("Error: Scattered field inside the structure not yet evaluated. Run `core.scatter` simulation first.")
    
    
    NF_rasterscan_indices = []
    for i, Efield in enumerate(sim.E):
        skip = False
        for kw in search_kwargs:
            if Efield[0][kw] != search_kwargs[kw]:
                skip = True
        if not skip:
            NF_rasterscan_indices.append(i)
    
    return NF_rasterscan_indices



def calculate_rasterscan(sim, field_kwargs, func, 
                        key_x_pos='xSpot', key_y_pos='ySpot', 
                        verbose=False, callback=None, **kwargs):
    """calculate rasterscan using function `func`
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
        
    field_kwargs : `dict` or `int`
        dict of field-configuration to use from simulation. If an `int` is given,
        it is used as index on results of :func:`get_possible_field_params_rasterscan`
    
    func : function
        evaluation function, which will be called as:
        `func(sim, field_index, **kwargs)`
    
    key_x_pos : str, default: 'xSpot'
        parameter-name defining the rasterscan beam/illumination x-position
    
    key_y_pos : str, default: 'ySpot'
        parameter-name defining the rasterscan beam/illumination y-position
    
    verbose : bool, default: False
        print some runtime info
    
    callback : func, default: None
        optional callback function, which is called after each wavelength.
        Passes a dict to `callback` containing current wavelength, so far
        calculated data and timing info.
        
    **kwargs : 
        all other keyword args are passed to `func`
    
    Returns
    -------
    list of tuples (x,y) : 
        positions of raster-scan evaluation
        
    list of float or tuple (S) : 
        S is the scalar (or tuple) returned by `func`
    
    """
    import time
    
    if sim.E is None: 
        raise ValueError("Error: Scattered field inside the structure not yet evaluated. Run `core.scatter` simulation first.")
    
    if type(field_kwargs) == int:
        kw_index = field_kwargs
        field_kwargs = get_possible_field_params_rasterscan(sim, key_x_pos, 
                                                       key_y_pos)[field_kwargs]
        if verbose:
            warnings.warn("'field_kwargs' are index instead of dict." + 
                      "Using `get_possible_field_params_rasterscan`." + 
                      "Using configuration #{}: '{}'".format(kw_index, field_kwargs))
        
    kw_all_perm = sim.efield.kwargs_permutations
    if len(field_kwargs) != len(kw_all_perm[0])-1 or 'wavelength' not in field_kwargs:
        raise ValueError("'search_kwargs' must define every field-parameter except the 2 position parameters.")
    
    N_rasterscan_post = int(len(kw_all_perm) / 
                            (len(get_possible_field_params_rasterscan(
                                                sim, key_x_pos, key_y_pos)) / 
                                len(sim.efield.wavelengths)))
    
    ## --- calc. rasterscan for selected config and evaluation function
    S = []
    coords = []
    for i, E in enumerate(sim.E):
        t0 = time.time()
        params = E[0]
        skip = False
        for kw in field_kwargs:
            try:
                if params[kw] != field_kwargs[kw]:
                    skip = True
            except ValueError:
                if np.all(params[kw] != field_kwargs[kw]):
                    skip = True
        if not skip:
            dat = func(sim, i, **kwargs)
            coords.append( [params[key_x_pos], params[key_y_pos]] )
            S.append(dat)
            
            ## optional callback (call every 10th position)
            if callback is not None and len(S)%10==1:
                cb_continue = callback(dict(
                            coords=coords, dat=S, t_wl=1000.*(time.time()-t0),
                            i_scan=len(S), N_scan=N_rasterscan_post)
                                          )
                if not cb_continue:
                    break           # quit if callback returns False
    
    ## --- try to convert to numpy arrays
    try:
        coords = np.array(coords)
        S = np.array(S)
        if len(S) > 1 and S.shape[-1] == 1:
            S = S.T[0].T
    except:
        pass
    
    return coords, S




#==============================================================================
# nearfield / internal field tools
#==============================================================================
def get_field_as_list(NF, struct):
    """convert field `NF` and geometry `struct` to a list of coordinate/field tuples
    
    Note, that usually it is easier to use :func:`.get_field_as_list_by_fieldindex` instead.
    
    Parameters
    ----------
    NF : list of 3-tuples, complex
        field as returned e.g. from :func:`.core.scatter`
    
    struct : list of tuples, float
        geometry of nano-object, as returned by structure generated in 
        module `structures`
    
    Returns
    -------
    fieldlist : list of 6-tuples
        geometry and field in one list: [(x,y,z, Ex,Ey,Ez), (...), ...]
    """
    if len(NF) == 2:
        NF = NF[1]
    
    if len(NF.T) == 6:
        X,Y,Z, UX,UY,UZ = np.transpose(NF)
    elif len(NF.T) == 3 and struct is not None:
        UX,UY,UZ = np.transpose(NF)
        X,Y,Z = get_geometry(struct)
    else:
        raise ValueError("Error: Wrong number of columns in vector field. Expected (Ex,Ey,Ez)-tuples + `simulation` object or (x,y,z, Ex,Ey,Ez)-tuples.")
    
    return np.transpose([X,Y,Z, UX, UY, UZ])


def get_field_as_list_by_fieldindex(sim, field_index, which_field='E', 
                                    full_volume=False, fill_value='nan'):
    """return internal fields in structure as list of (x,y,z,Ex,Ey,Ez) tuples
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    field_index : int
        field-index corresponding to the incident field configuration
    
    which_field : str, default: "E"
        "E" or "H", for electric or magnetic field
    
    full_volume : bool, default: False
        if True, returns the field in the entire cuboidal volume which contains
        the structure, but the field is set to zero outside the structure.
    
    fill_value : str, default: 'nan'
        if full_volume, value to fill outside of structure. Either "zero" or "nan"
    
    
    Returns
    -------
    fieldlist : list of 6-tuples
        geometry and field in one list: [(x,y,z, Ex,Ey,Ez), (...), ...]
    """
    if full_volume:
        step = get_step_from_geometry(sim)
        
        voxels, voxels_eps, voxels_field = get_field_as_3D_array(
                                        sim, 0, fill_field_outside=fill_value)
        
        ## offset 
        offsetX = sim.struct.geometry.T[0].min()
        offsetY = sim.struct.geometry.T[1].min()
        offsetZ = sim.struct.geometry.T[2].min()
        
        ## size of full structure frame
        extent = [0,voxels_field.shape[0],
                  0,voxels_field.shape[1],
                  0,voxels_field.shape[2]]
        
        xpos = np.linspace(extent[0], extent[1], voxels_field.shape[0])  # units of step
        ypos = np.linspace(extent[2], extent[3], voxels_field.shape[1])
        zpos = np.linspace(extent[4], extent[5], voxels_field.shape[2])
        
        vectorfield = []
        for ix, Lx in enumerate(voxels_field):
            for iy, Ly in enumerate(Lx):
                for iz, s in enumerate(Ly):
                    _x = offsetX + xpos[ix]*step
                    _y = offsetY + ypos[iy]*step
                    _z = offsetZ + zpos[iz]*step
                    vectorfield.append([_x, _y, _z, s[0], s[1], s[2]])
        
        # return np.array(vectorfield)
        NF_full_volume = np.array(vectorfield)
        return NF_full_volume
        
    else:
        if which_field.lower() in ['h', 'b']:
            try:
                NF = sim.H[field_index]
            except (NameError, TypeError):
                raise Exception("Internal magnetic fields not available. Re-run `scatter` with 'calc_H=`True`'.")
        else:
            if sim.E is None:
                raise Exception("Internal fields not available. Run `scatter` first.")
            NF = sim.E[field_index]
    
        return get_field_as_list(NF, sim)


def get_field_as_3D_array(sim, field_index, which_field='e', 
                          minX=0, minY=0, minZ=0, 
                          fill_surrounding=False, fill_field_outside="zero",
                          wl=None, verbose=False):
    """convert coordinate-lists (geometry and fields) to 3D representations
    
    Note: Geometry x and y coordinates must be on a cubic grid of even multiples of "step"
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    field_index : int
        field-index corresponding to the incident field configuration
    
    which_field : str, default: "E"
        "E" or "H", for electric or magnetic field
    
    minX, minY, minZ: int, default: 0
        minimum extension of 3d array in x/y/z direction
    
    fill_field_outside: str, default: 'zero'
        either "zero" or "none" / "nan"
        
    wl : float, default: None
        as alternative to 'field_index', wavelength to evaluate material dispersion of 
        structure. field_index must be set `None` if wl is used.
    
    verbose : bool, default: False
        print runtime info
    
    Returns
    -------
    voxels, voxels_eps, voxels_field:
      - voxels: 3D binary np-array. 1=structure, 2=no structure
      - voxels_eps: 3D complex np-array with permittivity at each geometry-position. =0 at all other positions.
      - voxels_field: 3D complex np-array. Ex, Ey, Ez at each position
    
    """
    if verbose:
        print("conversion to volumetric arrays...", end='')
    if field_index is not None:
        wavelength = sim.E[field_index][0]['wavelength']
    else:
        wavelength = wl
    geopos       = sim.struct.geometry.copy()
    step         = sim.struct.step
    
    ## offset to 0,0 as starting point
    geopos.T[0] -= geopos.T[0].min()
    geopos.T[1] -= geopos.T[1].min()
    geopos.T[2] -= geopos.T[2].min()
    
    ## determine size of volume containing the structure
    max_X = max([int(minX), int(np.round(geopos.T[0].max() / step)) + 1])
    max_Y = max([int(minY), int(np.round(geopos.T[1].max() / step)) + 1])
    max_Z = max([int(minZ), int(np.round(geopos.T[2].max() / step)) + 1])
    
            
    ## --- 3D structure geometry
    voxels = np.zeros(shape=(max_X, max_Y, max_Z), dtype=np.uint8)  # only geometry (0=none, 1=material)
    
    ## --- epsilon at each position
    voxels_eps = np.ones(shape=(max_X, max_Y, max_Z), dtype=np.complex64)  # permittivity at each pos
    if fill_surrounding:
        ## !!! TODO: evaluate environment epsilon at every position separately
        n_env = sim.dyads.getEnvironmentIndices(wavelength, np.array([[0,0,10]]))
        voxels_eps *= n_env[0]**2
    else:
        voxels_eps *= 0.0
    
    for i_pos, pos in enumerate(geopos):
        eps = sim.struct.material[i_pos].epsilon(wavelength)
        pos = np.round(pos / sim.struct.step)
        pos = pos.astype(int)
        voxels[pos[0],pos[1],pos[2]] = 1
        voxels_eps[pos[0],pos[1],pos[2]] = eps
    
    
    ## --- 3D internal complex electric field
    voxels_field = np.zeros(shape=(max_X, max_Y, max_Z, 3), dtype=np.complex64)
    if fill_field_outside.lower() not in ['0', 'zero', 'zeros']:
        voxels_field *= np.nan
    
    ## calculate field everywhere
    if field_index is not None:
        if fill_surrounding:
            ## field everywhere
            from pyGDM2 import linear_py
            x = np.arange(0, step*(max_X), step)
            y = np.arange(0, step*(max_Y), step)
            z = np.arange(0, step*(max_Z), step)
            xx, yy, zz = np.meshgrid(x, y, z)
            r_probe = np.reshape(np.transpose([xx, yy, zz]), (-1, 3))
            whichf = 'Et' if which_field.lower()=='e' else 'Bt'
            field = linear_py.nearfield(sim, field_index, r_probe, 
                                        which_fields=[whichf], N_neighbors_internal_field=7)
            field = field[:,3:]  # remove coordinates
        else:
            ## internal field only
            r_probe = geopos
            if which_field.lower() == 'e':
                field = sim.E[field_index][1]
            else:
                field = sim.H[field_index][1]
        
    for i_pos, pos in enumerate((r_probe/step).astype(int)):
        if field_index is not None:
            voxels_field[pos[0],pos[1],pos[2], 0] = field[i_pos][0]
            voxels_field[pos[0],pos[1],pos[2], 1] = field[i_pos][1]
            voxels_field[pos[0],pos[1],pos[2], 2] = field[i_pos][2]
        
    return voxels, voxels_eps, voxels_field


def get_intensity_from_fieldlist(NF_list):
    """calculate intensity values from complex fields in field-vector-list
    
    Parameters
    ----------
    NF : list of 6-tuples, complex
        field as returned e.g. from :func:`.linear.nearfield`
    
    struct : list of tuples, float
        geometry of nano-object, as returned by structure generated in 
        module `structures`
    
    Returns
    -------
    fieldlist : list of 4-tuples
        list of tuples containing coordinates and field-intensity: [(x,y,z, I), (...), ...]
    """
    if len(NF_list) == 2:
        NF_list = NF_list[1]
    
    if len(NF_list) == 6:
        NF_list = np.transpose(NF_list)
    
    if len(NF_list.T) == 6:
        X,Y,Z, UX,UY,UZ = np.transpose(NF_list)
    else:
        raise ValueError("Error: Wrong number of columns in vector field. Expected (x,y,z, Ex,Ey,Ez)-tuples or (Ex,Ey,Ez)-tuples + `simulation` object.")
    
    I = np.abs(UX)**2 + np.abs(UY)**2 + np.abs(UZ)**2
    
    return np.transpose([X,Y,Z, I]).real





#==============================================================================
# generate 2D map coordinate lists
#==============================================================================
def generate_NF_map(X0,X1,NX,  Y0,Y1,NY,  Z0=0, projection='XY', dtype='f'):
    """Generate coordinate list with equidistant positions on a rectangular map
    
    e.g. for nearfield calcuation on this map
      
    Parameters
    ----------
        - X0,X1 : float, float
            X-Limits for Map
        
        - NX : int
            Nr of discretization pts in first projection direction
        
        - Y0,Y1 : float, float
            Y-Limits for Map
        
        - NY : int
            Nr of discretization pts in second projection direction
            
        - Z0 : float
            Z-Height of map
            
        - projection : str (optional)
            projection of map. must be one of ['XY','XZ','YZ'], default: 'XY'
            
        - dtype : str (otional)
            dtype of coordinates.
            passed to `np.asfortranarray`. e.g. "f" (single) or "d" (double).
            default: "f"
        
    Returns
    -------
        list of lists :
            list of 3 lists of X, Y, Z coordinates, to use e.g. in :func:`.linear.nearfield`
      
    """
    if projection.lower() =='xy':
        MAP = generate_NF_map_XY(X0,X1,NX,  Y0,Y1,NY,  Z0, dtype)
    elif projection.lower() =='xz':
        MAP = generate_NF_map_XZ(X0,X1,NX,  Y0,Y1,NY,  Z0, dtype)
    elif projection.lower() == 'yz':
        MAP = generate_NF_map_YZ(X0,X1,NX,  Y0,Y1,NY,  Z0, dtype)
    else:
        raise ValueError("Invalid projection specified. Must be one of: ['XY','XZ','YZ'].")
    
    return MAP


def generate_NF_map_XY(X0,X1,NX,  Y0,Y1,NY,  Z0=0, dtype='f'):
    """Generate coordinate list with equidistant positions on a rectangular map in XY plane
    
    see :func:`generate_NF_map` for doc.
    """
    XMAP=[]; YMAP=[]; ZMAP=[]
    for xi in np.linspace(X0,X1,NX):
        for yi in np.linspace(Y0,Y1,NY):
            XMAP.append(xi)
            YMAP.append(yi)
            ZMAP.append(Z0)
    XMAP = np.asfortranarray(XMAP, dtype=dtype)
    YMAP = np.asfortranarray(YMAP, dtype=dtype)
    ZMAP = np.asfortranarray(ZMAP, dtype=dtype)
    
    MAP = np.array([XMAP, YMAP, ZMAP])
    return MAP.T


def generate_NF_map_XZ(X0,X1,NX,  Z0,Z1,NZ,  Y0=0, dtype='f'):
    """Generate coordinate list with equidistant positions on a rectangular map in XZ plane
     
    see :func:`generate_NF_map` for doc.
    """
    XMAP=[]; YMAP=[]; ZMAP=[]
    for xi in np.linspace(X0,X1,NX):
        for zi in np.linspace(Z0,Z1,NZ):
            XMAP.append(xi)
            YMAP.append(Y0)
            ZMAP.append(zi)
    XMAP = np.asfortranarray(XMAP, dtype=dtype)
    YMAP = np.asfortranarray(YMAP, dtype=dtype)
    ZMAP = np.asfortranarray(ZMAP, dtype=dtype)
    
    MAP = np.array([XMAP, YMAP, ZMAP])
    return MAP.T


def generate_NF_map_YZ(Y0,Y1,NY,  Z0,Z1,NZ,  X0=0, dtype='f'):
    """Generate coordinate list with equidistant positions on a rectangular map in YZ plane
     
    see :func:`generate_NF_map` for doc.
    """
    XMAP=[]; YMAP=[]; ZMAP=[]
    for yi in np.linspace(Y0,Y1,NY):
        for zi in np.linspace(Z0,Z1,NZ):
            XMAP.append(X0)
            YMAP.append(yi)
            ZMAP.append(zi)
    XMAP = np.asfortranarray(XMAP, dtype=dtype)
    YMAP = np.asfortranarray(YMAP, dtype=dtype)
    ZMAP = np.asfortranarray(ZMAP, dtype=dtype)
    
    MAP = np.array([XMAP, YMAP, ZMAP])
    return MAP.T


def map_to_grid_XY(MAP, ivalues, NX=-1, NY=-1, map_indices=(0,1)):
    """
    Generate XY plottable map e.g. from (XY) nearfield calculation
      
    Parameters
    ----------
    MAP : list of 3 lists
        list of 3 lists X,Y,Z (coordinate positions). 
        e.g. generated using :func:`generate_NF_map`
    
    ivalues : array-like
        Data-array: e.g. intensity at each MAP coordinate
        
    NX, NY : int, int (optional)
        by default: number of unique X/Y entries in MAP. 
        Nr of X/Y points to calculate (do interpolation in nescessary)
    
    map_indices : tuple (optional)
        indices of coordinates in MAP to use (X=0, Y=1, Z=2). default: (0,1)
    
    Returns
    -------
    NF_MAP : 2d-array
        nearfield map
    
    extent : tuple
        extent of map (x0,x1, y0,y1). Can be used in `matplotlib`'s `imshow`.
    """
    if len(np.shape(ivalues)) == 2:
        if np.shape(ivalues)[1] == 10:
            ivalues = ivalues.T[-1]
    if len(ivalues) != np.shape(MAP)[1]:
        raise ValueError("Dimensions of map-definition and field-array not matching!")
    
    if NX==-1:
        NX = len(np.unique(MAP[map_indices[0]]))
    if NY==-1:
        NY = len(np.unique(MAP[map_indices[1]]))
    NF_MAP, extent = list_to_grid(np.transpose([MAP[map_indices[0]], 
                                                MAP[map_indices[1]], 
                                                ivalues]), NX, NY)
    return NF_MAP, extent





def adapt_map_to_structure_mesh(mapping, structure, projection=None,
                                min_dist=1.1,
                                occupy_all_geo_positions=False, verbose=False):
    """changes the positions of mapping coordinates close to structure meshpoints
    
    All coordinates closer than a minimum (e.g. the stepsize) to a meshpoint 
    of the nanostructure are replaced by the position of the closest meshpoint.
    Optionally all meshpoint positions can be added to the mapping.
    
    Parameters
    ----------
    mapping : list of 3-tuples
        list containing the mapping coordinates. 
    
    structure : list of coordinate 3-tuples or :class:`.core.simulation`
        instance of object containing the mapping information. Accepts list 
        of coordinate tuples or instance of :class:`.core.simulation`
    
    projection : str, default: None
        consider some geometric projection. possible values: ['XY', 'XZ', 'YZ', None]
        if None: use closest meshpoint no matter which direction in space. If 
        one of the strings, only consider meshpoints in the same plane as the mapping
        coordinates.
        
    min_dist : float, default: 1.5
        minimum distance to meshpoints in units of stepsize
    
    occupy_all_geo_positions : bool, default: False
        if true and a planar mapping or a specific projection is chosen, 
        all positions in the geometry-mesh plane closest to the scan-height will 
        be added to the new mapping as well.
    
    verbose : bool, default: False
        print timing info
        
    Returns
    -------
    coords : list of 3-tuples
        mapping with positions close to / inside the structure replaced by the 
        nearest mesh-point coordinates
    """
    try:
        import scipy
        from scipy.linalg import norm
        if int(scipy.__version__.split('.')[0]) == 0 and int(scipy.__version__.split('.')[1]) < 17:
            raise Exception("scipy with version < 0.17.0 installed! " +
                            "Positions inside nanostructure cannot be " +
                            "identified. Please upgrade or set `val_inside_struct`=None.")
    except ImportError:
        raise Exception("It seems scipy is not installed. Scipy is required " +
                        "by `nearfield` for detecting internal field positions. " +
                        "Please install scipy >=v0.17, or set `val_inside_struct`=None.")
    import time

    ## --- check the mapping data
    if len(np.shape(mapping)) == 1:
        if len(mapping) == 3:
            mapping = np.array([[mapping[0], mapping[1], mapping[2]]])
        else: 
            raise ValueError("If 'mapping' is tuple, must consist of *exactly* 3 elements!")
    elif len(np.shape(mapping)) == 2:
        if np.shape(mapping)[1] != 3:
            raise ValueError("'mapping' must consist of 3-tuples!")
    else:
        raise ValueError("wrong format for 'mapping'. must consist of *exactly* 3 elements, either floats, or lists.")
    r_probe = mapping.copy()
    
    if str(projection).lower() == 'none':
        projection = 99
        if  len(np.unique(r_probe.T[0]))==1:
            projection = 'yz'
        elif  len(np.unique(r_probe.T[1]))==1:
            projection = 'xz'
        elif  len(np.unique(r_probe.T[2]))==1:
            projection = 'xy'
    
    if projection.lower() == 'xz':
        projection = 1
    elif projection.lower() == 'xy':
        projection = 2
    elif projection.lower() == 'yz':
        projection = 0
    elif projection != 99:
        raise ValueError("'projection' must be one of [None, 'XZ', 'XY', 'YZ'].")
    
    ## --- get stepsize and structure coordinates
    step = get_step_from_geometry(structure)
    geo = get_geometry(structure).copy().T
    
    ## --- compare the two lists of coordinates
    t0 = time.time()
    ## --- no specific projection plane awareness:
    new_r_probe = []
    if projection==99:
        for i, R in enumerate(r_probe):
            new_r_probe.append(R)
            dist_list = norm(geo - R, axis=1)
            idcs_min_dist = np.argsort(dist_list)
            ## --- if inside, replace fields
            if abs(dist_list[idcs_min_dist[0]]) <= min_dist*step:
                new_r_probe[-1] = geo[idcs_min_dist[0]]
    
    ## --- scan and relocate plane-by-plane
    else:
        scan_levels = np.unique(r_probe.T[projection])
        for lvl in scan_levels:
            lvl_indices = r_probe.T[projection]==lvl
            for i, R in enumerate(r_probe[lvl_indices]):
                new_r_probe.append(R)
                ## check if meshpoint is too close
                dist_list = norm(geo - R, axis=1)
                idcs_min_dist = np.argsort(dist_list)
                if abs(dist_list[idcs_min_dist[0]]) <= min_dist*step:
                    new_r_probe[-1] = geo[idcs_min_dist[0]].copy()
                    new_r_probe[-1][projection] = lvl
        if occupy_all_geo_positions:
            ## for every 'height' level in mapping, add full geometry plane closest to that level
            unique_geo_planes = np.unique(geo.T[projection])
            for lvl in scan_levels:
                closest_geo_plane_lvl = unique_geo_planes[np.argmin(np.abs(unique_geo_planes-lvl))]
                _geo_lvl = geo.copy()[geo.T[projection]==closest_geo_plane_lvl]
                _geo_lvl.T[projection] = lvl
                new_r_probe = np.concatenate([new_r_probe, _geo_lvl])
    
    ## --- delete duplicates
    new_r_probe = unique_rows_3D(new_r_probe).T
    if verbose: print("time: {}ms".format((time.time() - t0)*1000.))
    
    return new_r_probe









# =============================================================================
# OTHER
# =============================================================================
def evaluate_incident_field(field_generator, wavelength, kwargs, r_probe, 
                            n1=1.0,n2=1.0,n3=None, spacing=5000.0):
    """Evaluate an incident field generator
    
    Calculate the field defined by a field_generator function for a given set
    of coordinates.
      
    Parameters
    ----------
    field_generator : `callable`
        field generator function. Mandatory arguments are 
         - `struct` (instance of :class:`.structures.struct`)
         - `wavelength` (list of wavelengths)
    
    wavelength : float
        wavelength in nm
    
    kwargs : dict
        optional kwargs for the `field_generator` functions (see also 
        :class:`.fields.efield`).
         
    r_probe : tuple (x,y,z) or list of 3-lists/-tuples
        (list of) coordinate(s) to evaluate nearfield on. 
        Format: tuple (x,y,z) or list of 3 lists: [Xmap, Ymap, Zmap] 
        (the latter can be generated e.g. using :func:`.tools.generate_NF_map`)
    
    n1,n2,n3 : complex, default: 1.0, 1.0, None
        indices of 3 layered media. if n3==None: n3=n2.
        
    spacing : float, default: 5000
        distance between substrate and cladding (=thickness of layer "n2")
    
    Returns
    -------
    field_list : list of tuples
        field at coordinates as list of tuples (x,y,z, Ex,Ey,Ez)
    
    """
    from pyGDM2 import materials
    from pyGDM2 import structures
    
    ## ---------- Setup dummy-structure for fundamental field-calculation
    r_probe = np.array(r_probe)
    if len(r_probe.shape)==1:
        r_probe = np.array([r_probe])
    if r_probe.shape[0] == 3 and r_probe.shape[1] != 3:
        r_probe = r_probe.T
    if r_probe.shape[-1] != 3:
        raise ValueError("'r_probe': Wrong shape or wrong number of coordinates.")
    
    ## dummy parameters
    material = materials.dummy(1.0)
    geometry = r_probe
    step = get_step_from_geometry(geometry)
    
    struct = structures.struct(
                    step, geometry, material, 
                    n1,n2, 1.0, n3=n3, spacing=spacing, 
                    auto_shift_structure=False, check_geometry_consistency=False
                    )
    struct.setDtype(np.float32, np.complex64)
    struct.geometry = r_probe
    struct.setWavelength(wavelength)
    
    E = field_generator(struct, wavelength, **kwargs)
    NF = np.concatenate([struct.geometry, E], axis=1)
    
    return NF
    

def split_simulation(sim, geo_split, verbose=0):
    """split structure in simulation and return two sim with the sub-geometries
    
    Can be used to artificially *disable* optical interactions between several 
    structures
    
    Parameters
    ----------
    sim : :class:`.simulation`
        instance of :class:`.simulation`, efield may be pre-calculated, in which
        case they will be also split and returned in the splitted simulations
    
    geo_split : list of 3-tuples or  :class:`.simulation`
        list of coordinates to be split off the simulation geometry or simulation 
        in which case its geometry will be extracted and used.
    
    verbose : bool, default: False
        print some info
    
    Returns
    -------
    list of 2 :class:`.simulation` instances
        new simulation with splitted geometries and other same parameters
        as well as pre-calculated fields
        first sim is split part, second sim is remaining part of original geometry
    
    """
    from pyGDM2.core import simulation
    if type(geo_split) == simulation:
        geo_sp = get_geometry(geo_split, return_type='tuples')
    else: 
        geo_sp = geo_split
            
        if np.shape(geo_split)[1] != 3 and len(np.shape(geo_split)) != 2:
            raise Exception('geo_split list of coordinates has wrong format.')
    
    step = sim.struct.step
    geo = sim.struct.geometry
    idx_split = []
    idx_remain = []
    for i, pos in enumerate(geo):
        ## test if 'pos' exists in geometry
        if np.linalg.norm(geo_sp - pos, axis=1).min() < step/4 :
            idx_split.append(i)
        else:
            idx_remain.append(i)
    
    if len(idx_split) == 0:
        warnings.warn("No meshpoints in agreement with split-list detected. Splitted sim has empty geometry!")
    
    ## split part
    sim_split = copy.deepcopy(sim)
    sim_split.struct.geometry = geo[idx_split]
    sim_split.struct.n_dipoles = len(sim_split.struct.geometry)
    sim_split.struct.material = np.array(sim_split.struct.material)[idx_split]
    
    ## remaining part
    sim_remain = copy.deepcopy(sim)
    sim_remain.struct.geometry = geo[idx_remain]
    sim_remain.struct.n_dipoles = len(sim_remain.struct.geometry)
    sim_remain.struct.material = np.array(sim_remain.struct.material)[idx_remain]
    
    ## if available, split pre-calculated internal fields
    if sim.E is not None:
        for i in range(len(sim.E)):
            sim_split.E[i][1] = sim_split.E[i][1][idx_split]
        for i in range(len(sim.E)):
            sim_remain.E[i][1] = sim_remain.E[i][1][idx_remain]
    
    if verbose:
        print("number of original sim meshpoints: {}".format(len(geo)))
        print("number of search meshpoints:       {}".format(len(geo_sp)))
        print("number of sim1 meshpoints:         {}".format(len(sim_split.struct.geometry)))
        print("number of sim2 meshpoints:         {}".format(len(sim_remain.struct.geometry)))
    
    return [sim_split, sim_remain]
    
    


def combine_simulations(sim_list):
    """Combine several simulations
    
    Can be used to artificially *disable* optical interactions between several 
    structures
    
    Parameters
    ----------
    sim_list : list of sim
        list of :class:`.simulation` instances, efield and environment configuration
        must be identical for the different simulations
    
    
    Returns
    -------
    sim : :class:`.simulation`
        new simulation with combined geometry
    
    """
    import copy
    combined_sim = copy.deepcopy(sim_list[0])
    
    combined_geo = []
    combined_materials = []
    for sim in sim_list:
        if len(sim.efield.kwargs_permutations) != len(combined_sim.efield.kwargs_permutations):
            raise ValueError("Unequal simulation configuration. Same number of incident field configs required!")
        if not np.all(sim.efield.wavelengths == combined_sim.efield.wavelengths):
            raise ValueError("Unequal simulation configuration. Same wavelengths required!")
        if sim.efield.field_generator.__name__ != combined_sim.efield.field_generator.__name__:
            raise ValueError("Unequal simulation configuration. Same field generator!")
        if (sim.dyads.n1_material.__name__ != combined_sim.dyads.n1_material.__name__) or \
                (sim.dyads.n2_material.__name__ != combined_sim.dyads.n2_material.__name__) or \
                (sim.dyads.n3_material.__name__ != combined_sim.dyads.n3_material.__name__):
            raise ValueError("Unequal environment configuration. Same materials for layer n1, n2 and n3 required!")
        if sim.dyads.spacing != combined_sim.dyads.spacing:
            raise ValueError("Unequal spacing parameter. Same spacing size required!")
        if sim.struct.step != combined_sim.struct.step:
            raise ValueError("Unequal stepsize. Same step required!")
        if sim.struct.normalization != combined_sim.struct.normalization:
            raise ValueError("Unequal mesh. Same mesh required!")
        # if sim.dyads.with_radiation_correction != combined_sim.dyads.with_radiation_correction:
        #     raise ValueError("Unequal radiative corretion config. Must be the same for all simulations!")
        
        combined_geo.append(copy.deepcopy(sim.struct.geometry))
        combined_materials.append(copy.deepcopy(sim.struct.material))
    
    ## -- combined `struct` instance
    from pyGDM2 import structures
    combined_sim.struct = structures.struct_py(
                    combined_sim.struct.step, 
                    np.concatenate(combined_geo), np.concatenate(combined_materials), 
                    normalization=combined_sim.struct.normalization,
                    check_geometry_consistency=False)
    
    ## -- combined pre-calculated E-fields (if available)
    if combined_sim.E is not None:
        for i_E in range(len(combined_sim.E)):
            combined_E = []
            for sim in sim_list:
                combined_E.append(sim.E[i_E][1])
            combined_sim.E[i_E][1] = np.concatenate(combined_E, axis=0)
    
    ## -- combined pre-calculated H-fields (if available)
    if combined_sim.H is not None:
        for i_H in range(len(combined_sim.H)):
            combined_H = []
            for sim in sim_list:
                combined_H.append(sim.H[i_H][1])
            combined_sim.H[i_H][1] = np.concatenate(combined_H, axis=0)
    
    ## test minimum distances to next neighbor on combined geometry. 
    ## must not be < step
    from scipy.spatial import cKDTree as KDTree
    kdtree = KDTree(combined_sim.struct.geometry)
    mindist = kdtree.query(combined_sim.struct.geometry, k=2, 
                 distance_upper_bound=combined_sim.struct.step*2)[0].T[1]
    if mindist.min() < (0.99 * combined_sim.struct.step / combined_sim.struct.normalization):
        raise ValueError("Too small distance between neighbor meshpoints detected. " +
                         "Minimum allowed distance between cells is one stepsize.")
        
    return combined_sim



if __name__ == "__main__":
    pass