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
"""
pyGDM core routines

"""
from __future__ import print_function
from __future__ import absolute_import

import numpy as np

import gc
import warnings
import copy
import time

import numba

from pyGDM2 import propagators



#==============================================================================
# GLOBAL PARAMETERS
#==============================================================================




#==============================================================================
# EXCEPTIONS
#==============================================================================





# =============================================================================
# Deprecation Test
# =============================================================================
def _check_struct_type(struct):
    return struct
    # ## deprecation test
    # from pyGDM2 import structures
    # if type(struct) == structures.struct:
    #     warnings.warn("deprecated `structs` class is used. Automatically " +
    #                   "overloading with the new `pyGDM2.structures.struct_py` class.")
        
    #     n1, n2, n3 = struct.n1_material, struct.n2_material, struct.n3_material
    #     spacing = struct.spacing
    #     norm = struct.normalization
        
    #     new_struct = structures.struct_py(struct.step, struct.geometry, struct.material,
    #                                       n1=n1, n2=n2, n3=n3, 
    #                                       normalization=norm, spacing=spacing,
    #                                       auto_shift_structure=False, 
    #                                       check_geometry_consistency=False)
    #     return new_struct
    # else:
    #     return struct
    
    
def _check_efield_type(efield):
    pass
        

#==============================================================================
# Simulation container class
#==============================================================================
class simulation(object):
    """
    Bases: object
    
    Main GDM simulation container class - pure-python API
    
    Defines a linear GDM simulation. Contains information on: 
        - *struct* : :class:`.structures.struct`:
            - the geometry of the nano structure 
            - its dielectric function
            
        - *efield* : :class:`.fields.efield`
            - the incident field and the wavelenghts 
            - possibly further incident field configuration 
            
        - *dyads* : :class:`.propagators.DyadsBaseClass`
            - class derived from :class:`.propagators.DyadsBaseClass`
            - contains set of Green's tensors, self-terms and related functions
            - contains environment definition and polarizability calculation
    
    Parameters
    ----------
    
    struct : :class:`.structures.struct`
        structure object
        
    efield : :class:`.fields.efield`
        fundamental field
        
    dyads : :class:`.propagators.DyadsBaseClass`
        set of Green's tensors, polarizabilities, environment info
        
    dtype : (optional) `str`, default: 'f'
        precision of simulation
    
    """
    __name__ = "pygdm2 simulation"
    
    
    def __init__(self, struct, efield, dyads=None, dtype='f'):
        """Initialization"""
        
        ## --- struct includes: geometry, material(s), environment
        struct = _check_struct_type(struct)  # compatibility: check if new `struct_py`-API is used
        self.struct = struct
        
        ## --- efield includes: field_generator function, wavelengths, optional kwargs
        _check_efield_type(efield)  # compatibility: check if new `fields`-API is used
        self.efield = efield
        
        ## --- dyads includes: polarizabilities, self-terms, Green dyads, coupling-matrix setup
        if dyads is None:
            warnings.warn('No `dyads` instance specified. Falling back to `propagators.DyadsQuasistatic123`. ' +
                          'This assumes environment configuration through "struct". ' +
                          'This behavior might change in a future release.')
            dyads = propagators.DyadsQuasistatic123()
        self.dyads = dyads
        
        ## Ensure environment definition for 1-2-3 dyads. 
        ## This will be removed in a future release
        try:
            ## if not in 'dyads', set n1, n2, n3 and spacing from 'struct'
            self.dyads._legacyStructCompatibility(self.struct)
        except AttributeError:
            pass
        
        ## --- precision
        if dtype in ['f', 'F']:
            self.dtypef = np.float32
            self.dtypec = np.complex64
        elif dtype in ['d', 'D']:
            self.dtypef = np.float64
            self.dtypec = np.complex128
        self.efield.setDtype(self.dtypef, self.dtypec)
        self.struct.setDtype(self.dtypef, self.dtypec)
        
        ## --- initialize unevaluated data to `None` (postprocessing data)
        self.E = None   # placeholder: scattered E-fields inside structure
        self.H = None   # placeholder: scattered H-fields inside structure
        self.S_P = None # legcay-compatibility: placeholder for decay-rate tensors
    
        ## check consistency of structure / efield with Green's tensor framework
        self.dyads.exceptionHandling(struct=self.struct, efield=self.efield)
        
    
    def scatter(self, **kwargs):
        """wrapper to :func:`.scatter`"""
        return scatter(self, **kwargs)
    
    
    def copy(self):
        import copy
        return copy.deepcopy(self)
    
    
    def __repr__(self):
        from pyGDM2 import tools
        return tools.print_sim_info(self, prnt=False)
    
    
    def __eq__(self, other):
        ## identical geometries, identical field_kwargs keys, wavelengths, 
        ##     material, n1
        if (len(self.struct.geometry) == len(other.struct.geometry) and
               len(self.efield.wavelengths) == len(other.efield.wavelengths) and
               len(self.efield.kwargs.keys()) == len(other.efield.kwargs.keys())):
            if (np.sum(np.abs(self.struct.geometry - other.struct.geometry))==0 and 
                    np.sum(np.abs(self.efield.wavelengths - other.efield.wavelengths))==0 and 
                    self.efield.kwargs.keys() == other.efield.kwargs.keys() and 
                    self.struct.material[0].__name__ == other.struct.material[0].__name__ and 
                    self.dyads.n1_material.__name__ == other.dyads.n1_material.__name__ and 
                    self.dyads.n2_material.__name__ == other.dyads.n2_material.__name__ and 
                    self.dyads.n3_material.__name__ == other.dyads.n3_material.__name__ and 
                    self.dyads.spacing == other.dyads.spacing and 
                    self.struct.step == other.struct.step):
                return True
            else:
                return False
        else:
            return False




#==============================================================================
# scattered fields
#==============================================================================
def scatter(sim, method='lu', calc_H=False, verbose=True, callback=None, **kwargs):
    """Perform a linear scattering GDM simulation
    
    Calculate the electric field distribution inside a nano-structure.
    Optionally calculate also the internal magnetic field.
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    method : string, default: "lu"
        inversion method. One of ["lu", "numpyinv", "scipyinv", "cupy", "cuda"]
         - "lu" LU-decomposition (`scipy.linalg.lu_factor`)
         - "scipyinv" scipy default inversion (`scipy.linalg.inv`)
         - "numpyinv" numpy inversion (`np.linalg.inv`, if numpy compiled accordingly: LAPACK's `dgesv`)
         - "cupy" uses CUDA GPU via `cupy`
         - "cuda" (equivalent to "cupy")
    
    calc_H : bool, default: False
        if True, calculate also the internal magnetic field H. This has an 
        impact on performance and memory requirement, so it is deactivated by 
        default.
    
    verbose : bool, default False
        Print timing info to stdout
        
    callback : func, default: None
        optional callback function, which is called after each wavelength.
        Passes a dict to `callback` containing current wavelength, 
        simulation and timing info. 
        Available dict_keys: ['i_wl', 'wavelength', 'sim', 't_inverse', 't_repropa'].
        Callback needs to return `True` for simulation to continue. 
        If callback returns `False` the simulation will be canceled, and `scatter`
        returns the simulation results until the moment when it was interrupted.
    
      
    Returns
    -------
        - 1, if finished succesfully
        - -1, if canceled
    
    
    Notes
    -----
    - The complex electric fields inside the structure are also copied into the 
      :class:`.simulation` instance as attribute `simulation.E`
    
    - For details on the concept of the generalized propagator, see e.g.:
      Martin, O. J. F. & Girard, C. & Dereux, A. **Generalized Field Propagator 
      for Electromagnetic Scattering and Light Confinement.**
      Phys. Rev. Lett. 74, 526–529 (1995).
    
    - The `scipy` solvers (like 'lu', 'ilu' and 'cg') run parallelized if BLAS
      is compiled with multithreading support. See:
      http://scipy-cookbook.readthedocs.io/items/ParallelProgramming.html#use-parallel-primitives
      (last called 05/2020)
      
    - To limit the number of threads for the multi-threaded parallelized parts, 
      you might do something like explained in: 
      https://stackoverflow.com/questions/29559338/set-max-number-of-threads-at-runtime-on-numpy-openblas
      (website called 05/2020).
      Or use the `threadpoolctl` package (example for 4 threads:):
        >>> from threadpoolctl import threadpool_limits
        >>> threadpool_limits(limits=4, user_api='blas')
        
    """
# =============================================================================
#     Exception handling
# =============================================================================
    if method.lower() == "cuda":
        method = "cupy"
    if method.lower() == "cupy":
        import cupy
        if int(cupy.__version__[0])<7:
            raise ValueError("`cupy` version 7 or higher required. Found cupy version {}. Please upgrade cupy.".format(cupy.__version__))
        
    if method.lower() not in ["numpyinv", "scipyinv", "lu", "cupy"]:
        raise ValueError('Error: Unknown solving method. Must be one of' +
                         ' ["lu", "numpyinv", "scipyinv", "cuda", "cupy"].')
    
    if method.lower() == 'lu' and calc_H:
        warnings.warn("calculating 'H' is not efficient with LU decomposition. " +
                      "Consider using `scipyinv` instead.")
    
    if len(kwargs)!=0:
        warnings.warn("Following function-less kwargs were ignored: {}".format([a for a in kwargs]))
        
    
# =============================================================================
#     iterate wavelengths
# =============================================================================
    field_generator = sim.efield.field_generator
    wavelengths = sim.efield.wavelengths
    
    scattered_fields_E = []
    scattered_fields_H = []
    for i_wl, wavelength in enumerate(wavelengths):
        
# =============================================================================
#     get generalized propagator
# =============================================================================
        t0 = time.time()
        K = get_general_propagator(sim=sim, method=method, 
                                      wavelength=wavelength, calc_H=calc_H,
                                      verbose=verbose)
        t1 = time.time()
        
#==============================================================================
#    each wl: Incident field evaluation
#==============================================================================
        ## --- At fixed wavelength: Use generalized propagator on all incident field parameters
        def generalized_propagator_operation(field_kwargs, K, sim, wavelength):
            env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
            ## --- optional: E0
            E0 = field_generator(sim.struct.geometry, env_dict, wavelength, **field_kwargs)
            E0_supervec = _fieldListToSuperVector(E0)
            
            ## --- optional: H0
            if calc_H:
                field_kwargs_H = copy.deepcopy(field_kwargs)
                field_kwargs_H["returnField"] = "H"
                H0 = field_generator(sim.struct.geometry, env_dict, wavelength, **field_kwargs_H)
                H0_supervec = _fieldListToSuperVector(H0)
                E0_supervec = np.concatenate([E0_supervec, H0_supervec])
                E = np.dot(K, E0_supervec)
                H = _superVectorToFieldList(E[3*len(sim.struct.geometry):])
            
            ## --- generalized propagator times incident field:
            elif method.lower() == 'lu' and not calc_H:
                import scipy.linalg as la
                E = la.lu_solve(K, E0_supervec)
            elif method.lower() == 'cupy':
                ## --- cupy GPU matrix vector multiplication
                import cupy as cp
                E0_supervec_gpu = cp.array(np.ascontiguousarray(E0_supervec))  # move vec to device memory
                E_gpu = cp.dot(K, E0_supervec_gpu)
                E = E_gpu.get()
            else:
                E = np.dot(K, E0_supervec)
            
            E = _superVectorToFieldList(E[:3*len(sim.struct.geometry)])
            kwargs_final = copy.deepcopy(field_kwargs)
            kwargs_final["wavelength"] = wavelength
            
            ## --- optional: H
            if calc_H:
                return dict(kw=kwargs_final, E=E, H=H)
            else:
                return dict(kw=kwargs_final, E=E, H=None)
        
        ## --- loop over incident field configurations
        for field_kwargs in sim.efield.kwargs_permutations:
            scat_results = generalized_propagator_operation(field_kwargs, K, sim, wavelength)
            scattered_fields_E.append([scat_results['kw'], scat_results['E']]) 
            scattered_fields_H.append([scat_results['kw'], scat_results['H']])
            sim.E = scattered_fields_E
            if calc_H:
                sim.H = scattered_fields_H
                
        if verbose: print("repropa.: {:.1f}ms ({} field configs), tot: {:.1f}ms".format(
                                        1000.*(time.time()-t1), 
                                        len(sim.efield.kwargs_permutations), 
                                        1000.*(time.time()-t0)))
# =============================================================================
#       if applicable: call callback
# =============================================================================
        if callback is not None:
            cb_continue = callback(dict(
                i_wl=i_wl, wavelength=wavelength, sim=sim,
                t_inverse=1000.*(t1-t0), t_repropa=1000.*(time.time()-t1))
                                  )
            if not cb_continue:
                return -1
            
    gc.collect()
    
    return 1



        
def scatter_mpi(sim, calc_H=False, verbose=False, scatter_verbose=False, **kwargs):
    """MPI wrapper to :func:`.scatter` for embarrassingly parallel calculation of spectra
    
    *requires:* **mpi4py**
    
    run with "mpirun -n X python scriptname.py", where `X` is the number of 
    parallel processes (ideally an integer divisor of the number of wavelengths)
    
    
    Parameters
    ----------
    sim : :class:`.simulation` 
        simulation description
    
    calc_H : bool, default: False
        if True, calculate also the internal magnetic field H.
    
    verbose, scatter_verbose: bool, default: False
        turns on some mpi-routine info printing, respectively controls verbose setting for :func:`.scatter`
    
    **kwargs : 
        all kwargs are passed to :func:`.scatter`


    Notes 
    -----
    - On single machines it is usually easier to install `scipy` 
      compiled with parallel BLAS (parallel LU / CG routines). Usually the
      parallel BLAS is will be already installed automatically. Try to not use 
      both parallelisation techniques simultaneously unless properly
      configured for instance via a batch script (e.g. `SLURM`). 
      *Overloading the CPUs will usually result in decreased calculation speed.*
    
    - see :func:`.scatter` for main documentation
    
    """
    from pyGDM2 import fields_py as fields  # !!! adapt namespace in final version
    from mpi4py import MPI
    
    comm = MPI.COMM_WORLD
    nprocs, rank = comm.Get_size(), comm.Get_rank()
    
    
    ## --- create list of jobs and split in equal parts depending on `nprocs`
    def split(jobs, nprocs):
        return [jobs[i::nprocs] for i in range(nprocs)]
    
    if comm.rank == 0:
        if nprocs == 1:
            warnings.warn("Executing only one MPI process! Should be run using" +
                          " e.g. 'mpirun -n X python scriptname.py', where X" +
                          " is the number of parallel processes.")
        if verbose: 
            print("")
            print("number of MPI processes:        ", nprocs)
            print("number of wavelengths:          ", len(sim.efield.wavelengths))
            print("number of wavelengths / process:", int(np.ceil(len(sim.efield.wavelengths) / float(nprocs))))
            print("")
        
        if verbose: print("Generating and splitting jobs... ", end='')
        jobs_all = []
        for i, wl in enumerate(sim.efield.wavelengths):
            ## --- generate simulation objects for each individual wavelength
            _sim = copy.deepcopy(sim)
            _efield = fields.efield(_sim.efield.field_generator, [wl], _sim.efield.kwargs)
            _efield.setDtype(_sim.dtypef, _sim.dtypec)
#            _sim.efield.wavelengths = [wl]
            _sim.efield = copy.deepcopy(_efield)
            jobs_all.append(_sim)
        jobs = split(jobs_all, nprocs)
        if len(np.unique([len(i) for i in jobs])) > 1:
            warnings.warn("Efficiency warning: Number of wavelengths ({}) ".format(
                                                len(sim.efield.wavelengths)) + 
                          "not divisable by Nr of processes ({})!".format(nprocs))
        if verbose: print("Done.")
    else:
        jobs = None
    
    
    ## --- Scatter jobs across processes and perform GDM simulations for each wavelength
    jobs = comm.scatter(jobs, root=0)
    
    resultsE = []
    resultsH = []
    for job in jobs:
        if verbose: print(" process #{}: Calculating wavelength".format(rank) + \
                               " {}nm".format(job.efield.wavelengths[0]))
        scatter(job, calc_H=calc_H, verbose=scatter_verbose, **kwargs)
        scattered_Efield = job.E
        for _scatf in scattered_Efield:
            resultsE.append(_scatf)
        if calc_H:
            scattered_Hfield = job.H
            for _scatf in scattered_Hfield:
                resultsH.append(_scatf)
    
    
    ## --- Gather results on rank 0
    resultsE = MPI.COMM_WORLD.gather(resultsE, root=0)
    resultsH = MPI.COMM_WORLD.gather(resultsH, root=0)
    
    if comm.rank == 0:
        if verbose: print("All simulations done. Recombining... ", end='')
        ## --- recombine data and sort by wavelength
        resultsE = [i for temp in resultsE for i in temp]
        resultsE = sorted(resultsE, key=lambda k: k[0]['wavelength'])
        sim.E = resultsE
        if calc_H:
            resultsH = [i for temp in resultsH for i in temp]
            resultsH = sorted(resultsH, key=lambda k: k[0]['wavelength'])
            sim.H = resultsH
        if verbose: print("Done.")
    
    return 1
    


# =============================================================================
# Decay rate calculation
# =============================================================================
def _get_K_as_matrix(K, method):
    if method.lower() =='lu':
        warnings.warn("'LU' is not most efficient for explicit matrix inversion. " +
                      "Consider using `scipyinv` instead.")
    ## --- get explicit matrix
    if method.lower() == 'lu':
        import scipy.linalg as la
        K = la.lu_solve(K, np.identity(K.shape[0], dtype=K[0].dtype))
    if method.lower() in ['cuda', "cupy"]:
        if type(K) != np.ndarray:
            K = K.get()
    return K


@numba.njit(parallel=True, cache=True)
def _do_double_integral(K, Q, S, chi, Sp):
    for i_probe in numba.prange(Q.shape[0]):
        for i in range(Q.shape[1]):
            for j in range(Q.shape[1]):
                ## matrix multiplication numpy (slow with 'parallel=True')
                # Sp[i_probe] += np.dot(Q[i_probe, i], np.dot(np.dot(chi[i], K[i,j]), S[j, i_probe]))
                
                ## explicit double matrix multiplication (fast with 'parallel=True')
                S_tmp1 = np.zeros((3,3), dtype=np.complex64)
                S_tmp2 = np.zeros((3,3), dtype=np.complex64)
                ## inner matrix multiplication
                for l in range(3): 
                    for m in range(3): 
                        for k in range(3): 
                            S_tmp1[l,m] += chi[i,l,k] * K[i,j,k,m]
                ## middle matrix multiplication
                for l in range(3): 
                    for m in range(3): 
                        for k in range(3): 
                            S_tmp2[l,m] += S_tmp1[l,k] * S[j,i_probe,k,m] 
                ## outer matrix multiplication
                for l in range(3): 
                    for m in range(3): 
                        for k in range(3): 
                            Sp[i_probe,l,m] += Q[i_probe,i,k,m] * S_tmp2[k,m]


def decay_rate(sim, field_index=None, wavelength=None, 
               r_probe=None, r_emitter=None, component='E', 
               return_value='decay_rates', method='scipyinv', verbose=True):
    """local decay rate modification of a electric or magnetic dipole transition
    
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    field_index : int, default: None
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`.
        Either `field_index` or `wavelength` must be given.
    
    wavelength: float, default: None
        Optional wavelength (alternative to `field_index`) at which to 
        calculate susceptibility matrix (in nm). 
        Either `field_index` or `wavelength` must be given.
    
    r_probe : tuple (x,y,z) or list of 3-lists/-tuples
        (list of) coordinate(s) to evaluate the decay rate on. 
        Format: tuple (x,y,z) or list of 3 lists: [Xmap, Ymap, Zmap] 
        (the latter can be generated e.g. using :func:`.tools.generate_NF_map`)
    
    r_emitter : tuple (x,y,z), default: None
        optional fixed coordinate of the emitter, use to evaluate the cross-DOS. 
        If given, the Cross-DOS due to an emitter at `r_emitter` is evaluated 
        at all positions `r_probe`, hence the emitter will be fixed.
        See: *Cazé et al. PRL 110, 063903 (2013)*
    
    component : str, default: 'E'
        "E" or "H": which LDOS component to calculate (electric or magnetic).
    
    return_value : str, default: 'decay_rates'
        Values to be returned. one of:
            - 'decay_rates': relative decayrates for X,Y and Z oriented dipole
            - 'decay_rate_x': relative, partial decayrate for X-oriented dipole
            - 'decay_rate_y': relative, partial decayrate for Y-oriented dipole
            - 'decay_rate_z': relative, partial decayrate for Z-oriented dipole
            - 'decay_rate_total': relative, orientation-averaged decayrate (--> propto Im(Tr(Sp)) )
            - 'field_susceptibility': complex field-susceptibility tensor `Sp` at each r_probe position
    
    method : string, default: "scipyinv"
        inversion method. One of ["lu", "numpyinv", "scipyinv", "cupy", "cuda"]
         - "scipyinv" scipy default inversion (`scipy.linalg.inv`)
         - "numpyinv" numpy inversion (`np.linalg.inv`, if numpy compiled accordingly: LAPACK's `dgesv`)
         - "cupy" uses CUDA GPU via `cupy`
         - "cuda" (equivalent to "cupy")
         - "lu" LU-decomposition (`scipy.linalg.lu_factor`) - inefficient for `decay_rate`!
        
    verbose : bool default=True
        print runtime info
        
    
    Returns:
    ----------
    see parameter `return_value`
    
    
    Notes
    -----
    For details about the underlying formalism, see:
    Wiecha, P. R., Girard, C., Cuche, A., Paillard, V. & Arbouet, A. 
    **Decay Rate of Magnetic Dipoles near Non-magnetic Nanostructures.** 
    Phys. Rev. B 97(8), 085411 (2018)
    
    For details on the concept of the Cross-DOS, see:
    A. Cazé, R. Pierrat & R. Carminati
    **Spatial Coherence in Complex Photonic and Plasmonic Systems**
    Phys. Rev. Lett. 110, 063903 (2013)
    """
# =============================================================================
#     Exception handling
# =============================================================================
    if field_index is None and wavelength is None:
        raise Exception("Either `field_index` or `wavelength` must be given!")
        
    if field_index is not None and wavelength is not None:
        raise Exception("`field_index` AND `wavelength` are given! Ignoring `wavelength`.")
        
    if r_probe is None:
        raise Exception("`r_probe` must be given!.")
        
    if method.lower() not in ["numpyinv", "scipyinv", "lu", "cupy"]:
        raise ValueError('Error: Unknown solving method. Must be one of' +
                         ' ["lu", "numpyinv", "scipyinv", "cuda", "cupy"].')
    
    if r_emitter is not None:
        warnings.warn("Cross-DOS calculation is a new experimental functionality. Use with caution!")
        r_emitter = np.array(r_emitter)
        if np.linalg.norm(sim.struct.geometry - r_emitter).min() <= sim.struct.step:
            raise Exception("`r_emitter` for CDOS must be outside nanostructure. " +
                            "CDOS-emitters inside the structure might get implemented in a future version.")
    
# =============================================================================
# preparation
# =============================================================================
    if r_probe.shape[0]==3 and r_probe.shape[1]!=3:
        r_probe = np.transpose(r_probe)
    
    if field_index is not None:
        from pyGDM2 import tools
        wavelength = tools.get_field_indices(sim)[field_index]['wavelength']
    
    ## ------- dyads / GDM config
    if component.lower() == 'e':
        ## electric LDOS
        Q = sim.dyads.G_EE
        S = sim.dyads.G_EE
        calc_H = 0
        ## exclude self-term (assume homogeneous mesh and environment)
        selfterm = sim.dyads.getSelfTermEE(wavelength, sim.struct)[0]
    else:
        ## magnetic LDOS
        Q = sim.dyads.G_HE
        S = sim.dyads.G_HE
        calc_H = 0
        ## exclude self-term (assume homogeneous mesh and environment)
        selfterm = sim.dyads.getSelfTermHE(wavelength, sim.struct)[0]
    
    ## exclusion distance to avoid divergence of Greens function
    dist_div_G = sim.struct.step
    
    geo = sim.struct.geometry
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
        
    
# =============================================================================
#     the actual calculation
# =============================================================================
    t0 = time.time()
    Sp = np.zeros((len(r_probe), 3, 3), dtype=sim.efield.dtypec)
    
    ## generalized propagator, chi
    if verbose: 
        print("{}-LDOS at wl={:.1f}nm - ".format(component.upper(), wavelength), end='')
    t1 = time.time()
    alpha_tensor = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
    K = get_general_propagator(sim, wavelength, method=method, calc_H=calc_H)
    K = _get_K_as_matrix(K, method)
    K2 = K.reshape(len(K)//3, 3, -1, 3).swapaxes(1,2).reshape(-1, 3, 3).reshape(len(K)//3,len(K)//3, 3, 3)
    KE2 = K2[:len(geo), :len(geo)]
    # KH2 = K2[len(geo):, :len(geo)]      # K-HE (--> H-field inside)
    if verbose: 
        print("K: {:.1f}s, ".format((time.time() - t1)), end='')
    
# ------------------------------------
# E-LDOS: calc positions in source zone via K
# ------------------------------------
    ## determine positions inside source zone
    if component.lower() != 'e':
        idx_r_outside = np.arange(len(r_probe))
    else:
        from scipy.linalg import norm
        t2 = time.time()
        alpha_inv = np.linalg.inv(alpha_tensor)  # --> list of inverse polarizabilities
        idx_r_outside = []
        for ir, Rp in enumerate(r_probe):
            dist_list = norm(geo - Rp, axis=1)
            idcs_min_dist = np.argsort(dist_list)
            i_in = idcs_min_dist[0]    ## closest meshpoint
            ## --- if inside, use susceptibility at closest meshpoint
            if abs(dist_list[i_in]) <= 1.005*sim.struct.step:
                Sp[ir] = ( KE2[i_in, i_in] - np.eye(3) ) * alpha_inv[i_in]
            else:
                idx_r_outside.append(ir)
        if verbose and len(idx_r_outside)!=len(r_probe): 
            print("source-zone ({}/{} pos): {:.1f}s, ".format(len(r_probe)-len(idx_r_outside), 
                                      len(r_probe), (time.time() - t2)), end='')
    
# ------------------------------------
#     evaluate Green's tensors
# ------------------------------------
    if len(idx_r_outside)>0:
        idx_r_outside = np.array(idx_r_outside)
        _Sp_out = np.zeros((len(idx_r_outside), 3, 3), dtype=sim.efield.dtypec)
        r_probe_out = r_probe.copy()[idx_r_outside]
        
        
        ## light: dipole --> structure
        ## CDOS: fix emitter position, scan only probe position
        if r_emitter is not None:
            r_probe_out = np.ones(r_probe_out.shape) * r_emitter
        t3 = time.time()
        Q_list = np.zeros((len(r_probe_out), len(geo), 3, 3), dtype=sim.efield.dtypec)
        sim.dyads.eval_G(r_probe_out, geo, Q, wavelength, env_dict, Q_list, 
                         selfterm=selfterm, dist_div_G=dist_div_G)
        if verbose: 
            print("Q: {:.1f}s, ".format((time.time() - t3)), end='')
        
        
        ## light: structure --> dipole
        r_probe_out = r_probe.copy()[idx_r_outside]
        t4 = time.time()
        S_list = np.zeros((len(geo), len(r_probe_out), 3, 3), dtype=sim.efield.dtypec)
        sim.dyads.eval_G(geo, r_probe_out, S, wavelength, env_dict, S_list, 
                         selfterm=selfterm, dist_div_G=dist_div_G)
        if verbose: 
            print("S: {:.1f}s, ".format((time.time() - t4)), end='')
        
        
        ## perform double volume integral for each probe position --> numba accelerated
        t5 = time.time()
        _do_double_integral(KE2, Q_list, S_list, alpha_tensor, _Sp_out)
        Sp[idx_r_outside] = _Sp_out
        if verbose: 
            print("integrate: {:.1f}s, ".format((time.time() - t5)), end='')
    if verbose: 
        print("Done in {:.1f}s".format((time.time() - t0)))
    
    
# ------------------------------------
#     return results
# ------------------------------------
    if return_value.lower() == 'field_susceptibility':
        return Sp
    else:
        # =====================================================================
        # evaluate field-susceptibilities
        # =====================================================================
        k0 = 2*np.pi/wavelength
        gamma_0 = 1
        if return_value.lower() == 'decay_rates':
            dp_list = np.array([[1,0,0], [0,1,0], [0,0,1]])
        if return_value.lower() == 'decay_rate_x':
            dp_list = np.array([[1,0,0]])
        if return_value.lower() == 'decay_rate_y':
            dp_list = np.array([[0,1,0]])
        if return_value.lower() == 'decay_rate_z':
            dp_list = np.array([[0,0,1]])
        
        if return_value.lower() not in ['decay_rate_tot', 'decay_rate_total']:
            gamma_scalar_maps = []
            for i_mu, mu in enumerate(dp_list):
                l_mu = np.linalg.norm(mu)
                mu_e = mu / l_mu
                
                gamma = np.zeros(len(r_probe), dtype=sim.dtypef)
                for i, Sp_i in enumerate(Sp):
                    gamma[i] = (gamma_0 + (3./2.) * (1./k0**3) * gamma_0 * 
                                    l_mu * np.dot(np.dot(mu_e, Sp_i.imag), mu_e))
            
                gamma_scalar_maps.append(np.concatenate([r_probe, gamma[:,None]], axis=1))
            return gamma_scalar_maps
        else:
            Sp_tot = (gamma_0 + (3./2.) * (1./k0**3) * gamma_0 * np.trace(Sp.imag, axis1=1, axis2=2))
            return np.concatenate([r_probe, Sp_tot[:,None]], axis=1)





#==============================================================================
# Matrix operations
#==============================================================================
def get_general_propagator(sim=None, wavelength=None, method='lu', 
                           calc_H=False, verbose=False):
    """invert dipole-coupling matrix
    
    Parameters
    ----------
    sim : :class:`.simulation`
        simulation description
    
    wavelength: float
        Wavelength at which to calculate susceptibility matrix (in nm)
    
    method : string, default: "lu"
        inversion method. One of ["lu", "numpyinv", "scipyinv", "cupy", "cuda"]
         - "lu" LU-decomposition (`scipy.linalg.lu_factor`)
         - "scipyinv" scipy default inversion (`scipy.linalg.inv`)
         - "numpyinv" numpy inversion (`np.linalg.inv`, if numpy compiled accordingly: LAPACK's `dgesv`)
         - "cupy" uses CUDA GPU via `cupy`
         - "cuda" (equivalent to "cupy")
    
    calc_H : bool, default: False
        if True, calculate also the internal magnetic field H. This has an 
        impact on performance and memory requirement, so it is deactivated by 
        default.
    
    verbose : bool, default False
        Print timing info to stdout
        
    
    Returns
    -------
      - K: Generalized Propagator
    
    
    Notes
    -----
    For details on the concept of the generalized propagator, see e.g.:
    Martin, O. J. F. & Girard, C. & Dereux, A. **Generalized Field Propagator 
    for Electromagnetic Scattering and Light Confinement.**
    Phys. Rev. Lett. 74, 526–529 (1995).
    
    For the Electric-magnetic mixed field calculation, see e.g.:
    Schröter, U. **Modelling of magnetic effects in near-field optics.** 
    Eur. Phys. J. B 33, 297–310 (2003).
    """
# =============================================================================
#     Exception handling
# =============================================================================
    if method.lower() == 'lu' and calc_H:
        warnings.warn("calculating 'H' is not efficient with LU decomposition. " +
                      "Consider using `scipyinv` instead.")
    
    if method.lower() == "cuda":
        method = "cupy"
    if method.lower() == "cupy":
        import cupy
        if int(cupy.__version__[0])<7:
            raise ValueError("`cupy` version 7 or higher required. Found cupy " +
                             "version {}. Please upgrade cupy.".format(cupy.__version__))
    
# =============================================================================
#     setup EE coupling matrix
# =============================================================================
    t0 = time.time()
    ## --- construct matrix
    M_EE = get_SBS_EE(sim, wavelength=wavelength, invertible=True)                
    
    if verbose: 
        print('timing for wl={:.2f}nm - setup: EE {:.1f}ms, '.format(
                            wavelength, 1000.*(time.time()-t0)), end='')
    t0b = time.time()
    
# =============================================================================
#    inversion of EE part (via chosen method)
# =============================================================================
    ## --- scipy inversion methods
    if method.lower() in ["numpyinv", "scipyinv", "lu"]:
        if method.lower() in ["numpyinv"]:     # pyGDM2 default
            K_EE = np.linalg.inv(M_EE)
        elif method.lower() in ["scipyinv"]:
            import scipy.linalg as la
            K_EE = la.inv(M_EE, overwrite_a=True)
        elif method.lower() in ["lu"]:
            import scipy.linalg as la
            K_EE = la.lu_factor(M_EE, overwrite_a=True)
        del M_EE; gc.collect()
    
    ## --- CUDA based inversion on GPU via `cupy`
    elif method.lower() == "cupy":
        import cupy as cp
        import cupy.linalg
        ## move array to cuda device, cuda inversion
        Agpu = cp.array(np.ascontiguousarray(M_EE))
        Ainv_gpu = cupy.linalg.inv(Agpu)
        K_EE = Ainv_gpu
    
    else:
        raise ValueError('Invalid inversion method. Must be one of ["lu", ' +
                         '"numpyinv", "scipyinv", "cupy", "cuda"].')
    
# =============================================================================
#     get HE part of propagator and calc full K via block-inversion
# =============================================================================
    t1 = time.time()
    if calc_H:
        M_HE = get_SBS_HE(sim, wavelength)
        
        if method.lower() == 'lu':
            import scipy.linalg as la
            K_EE = la.lu_solve(K_EE, np.identity(3*len(sim.struct.geometry), 
                                                 dtype=K_EE[0].dtype))
        
        if method.lower() == 'cupy':
            import cupy as cp
            K_HE = -1*cp.dot(cp.array(np.ascontiguousarray(M_HE)), K_EE)
            K_HE = K_HE.get()
            K_EE = K_EE.get()
        else:
            K_HE = -1.*np.dot(M_HE, K_EE)
        
        M_zero     = np.zeros(2*[3*len(sim.struct.geometry)], dtype=sim.dtypec)
        M_I        = np.identity(3*len(sim.struct.geometry), dtype=sim.dtypec)
        
        ## -- block inversion K = [[M_EE^-1, 0], [-1*M_HE*M_EE^-1, Identity]]
        K = np.block([[K_EE, M_zero],
                      [K_HE, M_I]])
        if verbose: 
            print('HE {:.1f}ms, '.format(1000.*(time.time()-t1)), end='')
    else:
        K = K_EE
    
    ## -- done
    if verbose: 
        print('inv.: {:.1f}ms, '.format(1000.*(t1-t0b)), end='')
    
    return K




# =============================================================================
# CPU - side-by-side matrix setup
# =============================================================================
def get_SBS_EE(sim, wavelength, invertible=True):
    ##  --- simulation config
    geo = sim.struct.geometry
    
    ## --- material permittivity related config
    self_term_tensors = sim.dyads.getSelfTermEE(wavelength, sim.struct)
    alpha_tensors = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)

    ## --- run numba routine for EE coupling
    M_EE = np.zeros((len(geo)*3,len(geo)*3), dtype=sim.dtypec)
    conf_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    sim.dyads.tsbs_EE(geo, wavelength, self_term_tensors, alpha_tensors, 
                      conf_dict, M_EE)
    
    N = np.shape(M_EE)[0]
    if not invertible:
        M_EE = np.asfortranarray(np.identity(N) - M_EE, dtype=sim.dtypec)
    
    return M_EE


def get_SBS_HE(sim, wavelength):
    ##  --- simulation config
    geo = sim.struct.geometry
    
    ## --- material permittivity related config
    self_term_tensors = sim.dyads.getSelfTermHE(wavelength, sim.struct)
    alpha_tensors = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
    
    ## --- run numba routine for EH coupling
    M_HE = np.zeros((len(geo)*3,len(geo)*3), dtype=sim.dtypec)
    conf_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    sim.dyads.tsbs_HE(geo, wavelength, self_term_tensors, alpha_tensors, 
                      conf_dict, M_HE)
    
    return M_HE










#==============================================================================
# Internal Helper Functions
#==============================================================================
def _superVectorToFieldList(E):
    """convert complex 3N supervector E to list of N field tuples (Ex,Ey,Ez)"""
    return np.reshape(E, (int(len(E)/3), 3))


def _fieldListToSuperVector(E):
    """convert list of N field tuples (Ex,Ey,Ez) to complex 3N supervector E"""
    return np.reshape(E, (np.product(E.shape)))









#%%
if __name__ == "__main__":
    pass
    

