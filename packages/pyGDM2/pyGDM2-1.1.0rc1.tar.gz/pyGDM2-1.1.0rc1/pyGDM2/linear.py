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
linear optical effects

"""
from __future__ import print_function
from __future__ import absolute_import

import warnings
# import math

import numpy as np
import copy
import numba

import time


#==============================================================================
# GLOBAL PARAMETERS
#==============================================================================




#==============================================================================
# EXCEPTIONS
#==============================================================================






# =============================================================================
# general field propagation routines
# =============================================================================
@numba.njit(parallel=True, cache=True)
def _calc_repropagation(P, Escat, G_dyad_list):
    if len(P) != G_dyad_list.shape[2]//3:
        raise Exception("polarization and Greens tensor arrays don't match in size!")
    _P = P.flatten()
    for i_p_r in numba.prange(G_dyad_list.shape[0]):
        Escat[i_p_r] = np.dot(G_dyad_list[i_p_r], _P)
    
    



#==============================================================================
# Linear Field processing functions
#==============================================================================
#import numba
#@numba.njit(parallel=True)
def _calc_extinct(wavelength, n_env, alpha_tensor, E0, E, 
                  with_radiation_correction=False):
    """actual calculation of extinction and absorption cross sections
    
    numba compatible. tested.
    """
    P = np.matmul(alpha_tensor, E[...,None])[...,0]
    
    cext = ((8 * np.pi**2 / wavelength) / n_env * 
            np.sum(np.multiply(np.conjugate(E0), P))).imag
    cabs = ((8 * np.pi**2 / wavelength) / n_env * 
            (np.sum(np.multiply(P, np.conjugate(E)))).imag).real
    
    if with_radiation_correction:
        ak0 = 2*np.pi / wavelength
        cabs -= ((8 * np.pi**2 / wavelength) / n_env * 
                 (2/3)*ak0**3 * np.sum(np.multiply(P, np.conjugate(P))))
    csca = cext - cabs
    
    return cext, csca, cabs
    

def extinct(sim, field_index, with_radiation_correction=False):
    """Extinction, scattering and absorption cross-sections
    
    Calculates extinction, scattering and absorption crosssections
    for each wavelength of the GDM simulation
    
    Pure python implementation.
    
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    with_radiation_correction : bool, default: False
        Adds an optional radiative correction to the absorption section (hence 
        it interferes also in the scattering section).See 
        *B. Draine, in: Astrophys. J. 333, 848–872 (1988)*, equation (3.06).
        Using the correction can lead to better agreement for very large 
        discretization stepsizes, but has only a weak influence on simulations
        with fine meshes.
    
    Returns
    -------
    ext-section : float
        extinction cross-section
    
    scat-section : float
        scattering cross-section
    
    abs-section : float
        apsorption cross-section
        
    
    Notes
    -----
    For the calculation of the cross-sections from the complex nearfield, 
    see e.g.: 
    Draine, B. T. & Flatau, P. J. **Discrete-dipole approximation for scattering 
    calculations.**
    Journal of the Optical Society of America, A 11, 1491 (1994).
    
    """
    if sim.E is None: 
        raise ValueError("Error: Scattering field inside the structure not yet evaluated. " +
                         "Run `sim.scatter` simulation first.")
    
    ## --- incident field configuration
    field_params    = sim.E[field_index][0]
    wavelength      = field_params['wavelength']
    sim.struct.setWavelength(wavelength)
    n_env = sim.dyads.getEnvironmentIndices(wavelength, sim.struct.geometry[:1])[0]  # assume structure is fully in one environment
    
    ## --- get polarizability at wavelength
    alpha_tensor = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
    
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(sim.struct.geometry, 
                                    env_dict, **field_params)
    E = sim.E[field_index][1]
    
    return _calc_extinct(wavelength, n_env, alpha_tensor, E0, E, 
                         with_radiation_correction)





def multipole_decomp(sim, field_index, r0=None, quadrupoles=False):
    """multipole decomposition of nanostructure optical response
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    Multipole decomposition of electromagnetic field inside nanostructure for 
    electric and magnetic dipole and quadrupole moments.


    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r0 : array, default: None
        [x,y,z] position of multipole decomposition development. 
        If `None`, use structure's center of gravity
        
    quadrupoles : bool, default: False
        if True, return also quadrupole moments. Otherwise return only 
        electric and magnetic dipole moments.
        This is a direct implementation of  Evlyukhin et al (see Notes) and is not tested.
    
    
    Returns
    -------
    
    p : 3-vector
        electric dipole moment
    
    m : 3-vector
        magnetic dipole moment
        
    q : 3x3 tensor
        electric quadrupole moment
        
    mq : 3x3 tensor
        magnetic quadrupole moment
    
    
    Notes
    -----
    For details about the method, see: 
    Evlyukhin, A. B. et al. *Multipole analysis of light scattering by 
    arbitrary-shaped nanoparticles on a plane surface.*, 
    JOSA B 30, 2589 (2013)
    """
    warnings.warn("Multipole decomposition is a new functionality still under testing. " + 
                  "Please use with caution.")
    
    field_params = sim.E[field_index][0]
    wavelength = field_params['wavelength']
    k0 = 2*np.pi / wavelength
    
    geo = sim.struct.geometry
    E = sim.E[field_index][1]
    ex, ey, ez = E.T
    
    ## --- polarizability of each meshpoint
    sim.struct.setWavelength(wavelength)
    alpha_tensor = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
    
    
    ## --- use center of gravity for multimode expansion
    if r0 is None:
        r0 = np.average(geo, axis=0)
    Dr = geo - r0
    
    
    ## --- total electric dipole moment:
    ##     P = sum_i p(r_i) = chi V_cell sum_i E(r_i)
    P = np.matmul(alpha_tensor, E[...,None])[...,0]
    p = np.sum(P, axis=0)  # = volume integral
    
    ## --- total magnetic dipole moment: (X=curl)
    ##     M = -iw0/2c  sum_i (r_i - r0) X p(r_i) 
    ##       = -ik0/2 sum_i chi Vcell (r_i - r0) X E(r_i)
    M = -(1j*k0/2.) * np.cross(Dr, P)
    m = np.sum(M, axis=0)
        
    if quadrupoles:
        ## --- total electric quadrupole moment: (X=curl)
        ##     Q = 3 * sum_i (Dr p(r_i) + p(r_i) Dr)
        ##       = 3 * sum_i chi Vcell (Dr E(r_i) + E(r_i) Dr)
        Q = 3 * (np.einsum('li,lj->lji', Dr, P) + np.einsum('li,lj->lji', P, Dr))
        q = np.sum(Q, axis=0)
        
        ## --- total magnetic dipole moment: (X=curl)
        ##     M = -2iw0/3c  sum_i (r_i - r0) X p(r_i) 
        ##       = -2ik0/3 sum_i chi Vcell (r_i - r0) X E(r_i)
        MQ = -(2j*k0/3.) * np.einsum('li,lj->lji', np.cross(Dr, P), Dr)
        mq = np.sum(MQ, axis=0)
        
        return p, m, q, mq

    else:
        return p, m
        
    
def mutlipole_decomp(sim, field_index, r0=None):
    """wrapper for correctly spelled function"""
    warnings.warn('Please adapt your code to use the correctly spelled "multipole_decomp" function.')
    return multipole_decomp(sim, field_index, r0, quadrupoles=True)

    
    
def multipole_decomp_extinct(sim, field_index, r0=None, eps_dd=0.1, quadrupoles=False):
    """extinction from multipole decomposition
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    Returns extinction cross sections for electric and magnetic dipole and 
    quadrupole moments of the multipole decomposition.
    
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r0 : array, default: None
        [x,y,z] position of mulipole decomposition development. 
        If `None`, use structure's center of gravity
    
    
    eps_dd : float, default: 0.1
        numerical integration stepsize (in nm). Used for e/m quadrupole.
    
    quadrupoles : bool, default: False
        if True, return also quadrupole moments. Otherwise return only 
        electric and magnetic dipole moments.
        This is a direct implementation of  Evlyukhin et al (see Notes) and is not tested.
    
    Returns
    -------
    
    sigma_ext_p : float
        electric dipole extinction cross section (in nm^2)
    
    sigma_ext_m : float
        magnetic dipole extinction cross section (in nm^2)
        
    sigma_ext_q : float
        electric quadrupole extinction cross section (in nm^2)
        
    sigma_ext_mq : float
        magnetic quadrupole extinction cross section (in nm^2)
    
    
    Notes
    -----
    For details about the method, see: 
    Evlyukhin, A. B. et al. *Multipole analysis of light scattering by 
    arbitrary-shaped nanoparticles on a plane surface.*, 
    JOSA B 30, 2589 (2013)
    
    """
    ## --- by default, use center of gravity for multimode expansion
    field_params = sim.E[field_index][0]
    wavelength = field_params['wavelength']
    sim.struct.setWavelength(wavelength)
    k0 = 2*np.pi / wavelength
    
    geo = sim.struct.geometry
    n2 = sim.dyads.getEnvironmentIndices(wavelength, geo[:1])[0]  # assume structure is fully in one environment
    E = sim.E[field_index][1]
    ex, ey, ez = E.T
    
    if r0 is None:
        r0 = np.average(geo, axis=0)
    
    if quadrupoles:
        p, m, q, mq = multipole_decomp(sim, field_index, r0=r0, quadrupoles=quadrupoles)
    else:
        p, m = multipole_decomp(sim, field_index, r0=r0, quadrupoles=quadrupoles)
    
# =============================================================================
#     dipole extinction cross sections
# =============================================================================
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(r0[None,:], env_dict, **field_params)
    H0 = sim.efield.field_generator(r0[None,:], env_dict, returnField='H', **field_params)
    
    E2in = np.sum(np.abs(E0)**2)     # incident intensity
    sigma_ext_p = (4 * np.pi * k0 / n2 * 1/E2in * np.sum(np.conjugate(E0)*p)).imag
    sigma_ext_m = (4 * np.pi * k0 / n2 * 1/E2in * np.sum(np.conjugate(H0)*m)).imag
    
# =============================================================================
#     quadrupole extinction cross sections
# =============================================================================
    if quadrupoles:
        DX_pos = np.array([r0-np.array([eps_dd,0,0]), r0+np.array([eps_dd,0,0])])
        DY_pos = np.array([r0-np.array([0,eps_dd,0]), r0+np.array([0,eps_dd,0])])
        DZ_pos = np.array([r0-np.array([0,0,eps_dd]), r0+np.array([0,0,eps_dd])])
        EDXcj = np.conjugate(sim.efield.field_generator(DX_pos, env_dict, **field_params))
        EDYcj = np.conjugate(sim.efield.field_generator(DY_pos, env_dict, **field_params))
        EDZcj = np.conjugate(sim.efield.field_generator(DZ_pos, env_dict, **field_params))
        gradE0cj = np.array([[EDXcj[1,0]-EDXcj[0,0], EDYcj[1,0]-EDYcj[0,0], EDZcj[1,0]-EDZcj[0,0]],
                             [EDXcj[1,1]-EDXcj[1,1], EDYcj[1,1]-EDYcj[0,1], EDZcj[1,1]-EDZcj[0,1]],
                             [EDXcj[1,2]-EDXcj[1,2], EDYcj[1,2]-EDYcj[0,2], EDZcj[1,2]-EDZcj[0,2]]])
        sigma_ext_q = (np.pi * k0 / n2 * 1/(3. * E2in) * 
                               np.sum(np.tensordot(gradE0cj + gradE0cj.T, q) )).imag
        
        HDXcj = np.conjugate(sim.efield.field_generator(DX_pos, env_dict, returnField='H', **field_params))
        HDYcj = np.conjugate(sim.efield.field_generator(DY_pos, env_dict, returnField='H', **field_params))
        HDZcj = np.conjugate(sim.efield.field_generator(DZ_pos, env_dict, returnField='H', **field_params))
        gradH0cj = np.array([[HDXcj[1,0]-HDXcj[0,0], HDYcj[1,0]-HDYcj[0,0], HDZcj[1,0]-HDZcj[0,0]],
                             [HDXcj[1,1]-HDXcj[1,1], HDYcj[1,1]-HDYcj[0,1], HDZcj[1,1]-HDZcj[0,1]],
                             [HDXcj[1,2]-HDXcj[1,2], HDYcj[1,2]-HDYcj[0,2], HDZcj[1,2]-HDZcj[0,2]]])
        sigma_ext_mq = (2 * np.pi * k0 / n2 * 1/E2in * 
                               np.sum(np.tensordot(gradH0cj.T, mq) )).imag
        
        return sigma_ext_p, sigma_ext_m, sigma_ext_q, sigma_ext_mq

    else:
        return sigma_ext_p, sigma_ext_m

def mutlipole_decomp_extinct(sim, field_index, r0=None, eps_dd=0.1):
    """wrapper for correctly spelled function"""
    warnings.warn('Please adapt your code to use the correctly spelled "multipole_decomp_extinct" function.')
    return multipole_decomp_extinct(sim, field_index, r0, eps_dd, quadrupoles=True)



# =============================================================================
# internal field intensity helper
# =============================================================================
def internal_field_intensity(sim, field_index, which_value='average',
                             which_field='E'):
    """return internal field intensity
    
    returns either average or peak (min or max) internal field intensity for 
    either electric of magnetic field.
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
        
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    which_value : str, default: 'average'
        - if 'average', 'avg' or 'mean': average field intensity
        - if 'max' or 'maximum': maximum field intensity
        - if 'min' or 'minimum': minimum field intensity
    
    which_field : str, default: 'E'
        one of 'E', 'H' or 'both' (either electric or magnetic field or both)
    
    
    """
    ## --- E field
    if which_field.lower() in ['e', 'both']:
        if sim.E is not None:
            E = sim.E[field_index][1]
            I_E_mean = np.sum(np.abs(E)**2, axis=1).mean()
        else:
            raise Exception("E field not evaluated. Please run 'sim.scatter()'.")
    
    ## --- H field
    if which_field.lower() in ['h', 'b', 'both']:
        if sim.H is not None:
            H = sim.H[field_index][1]
            I_H_mean = np.sum(np.abs(H)**2, axis=1).mean()
        else:
            raise Exception("H field not evaluated. Please run 'sim.scatter(calc_H=True)'.")
    
    if which_field.lower() in ['h', 'b']:
        return I_H_mean
    elif which_field.lower() in ['e']:
        return I_E_mean
    else:
        return I_E_mean, I_H_mean
    


# =============================================================================
# farfield
# =============================================================================
def farfield(sim, field_index, 
                r_probe=None,
                r=100000., 
                tetamin=0, tetamax=np.pi/2., Nteta=10, 
                phimin=0, phimax=2*np.pi, Nphi=36, 
                polarizerangle='none', return_value='map'):
    """spatially resolved and polarization-filtered far-field scattering 
    
    For a given incident field, calculate the electro-magnetic field 
    (E-component) in the far-field around the nanostructure 
    (on a sphere of radius `r`).
    
    Propagator for scattering into a substrate contributed by C. Majorel
    
    Pure python implementation.
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
        
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r_probe : tuple (x,y,z) or list of 3-lists/-tuples. optional. Default: don't use
        defaults to *None*, which means it is not used and a solid angle defined by
        a spherical coordinate range is used instead. If `r_probe` is given, this
        overrides `r`, `tetamin`, `tetamax`, `Nteta`, `Nphi`.
        (list of) coordinate(s) to evaluate farfield on. 
        Format: tuple (x,y,z) or list of 3 lists: [Xmap, Ymap, Zmap] 
        
    r : float, default: 10000.
        radius of integration sphere (distance to coordinate origin in nm)
        
    tetamin, tetamax : float, float; defaults: 0, np.pi/2
        minimum and maximum polar angle in radians 
        (in linear steps from `tetamin` to `tetamax`)
        
    phimin, phimax : float, float; defaults: 0, 2*np.pi
        minimum and maximum azimuth angle in radians, excluding last position
        (in linear steps from `phimin` to `phimax`)
        
    Nteta, Nphi : int, int; defaults: 10, 36
        number of polar and azimuthal angles on sphere to calculate,
        
    polarizerangle : float or 'none', default: 'none'
        optional polarization filter angle **in degrees**(!). If 'none' (default), 
        the total field-intensity is calculated (= no polarization filter)
    
    return_value : str, default: 'map'
        Values to be returned. Either 'map' (default) or 'integrated'.
          - "map" : (default) return spatially resolved farfield intensity at each spherical coordinate (5 lists)
          - "efield" : return spatially resolved E-fields at each spherical coordinate (5 lists)
          - "int_Es" : return the integrated scattered field (as float)
          - "int_E0" : return the integrated fundamental field (as float)
          - "int_Etot" : return the integrated total field (as float)
    
    
    Returns
    -------
    using `r_probe` for position definition:
        3 lists of 6-tuples (x,y,z, Ex,Ey,Ez), complex : 
            - scattered Efield or E-intensity
            - total Efield (inlcuding fundamental field) or total E intensity
            - fundamental Efield (incident field) or E0 intensity
        
    if solid angle is defined via spherical coordinate range:
        - return_value == "map" : 5 arrays of shape (Nteta, Nphi) : 
            - [tetalist : teta angles - if solid angle range input]
            - [philist : phi angles - if solid angle range input]
            - I_sc : intensity of scattered field, 
            - I_tot : intensity of total field (I_tot=|E_sc+E_0|^2), 
            - I0 : intensity of incident field
        
        - return_value == "efield" : float
            - [tetalist : teta angles - if solid angle range input]
            - [philist : phi angles - if solid angle range input]
            - E_sc : complex scattered field at each pos.
            - E_tot : complex total field at each pos. (E_sc+E0)
            - E0 : complex incident field at each pos.
            
        - return_value == "int_XX" : float
            integrated total intensity over specified solid angle
        
    Notes
    -----
    For details of the asymptotic (non-retarded) far-field propagators for a 
    dipole above a substrate, see e.g.:
    Colas des Francs, G. & Girard, C. & Dereux, A. **Theory of near-field 
    optical imaging with a single molecule as light source.** 
    The Journal of Chemical Physics 117, 4659–4666 (2002)
        
    """
    from pyGDM2 import fields_py as fields # !!! adapt this later to final namespace
    
# =============================================================================
#     exception handling
# =============================================================================
    if sim.E is None: 
        raise ValueError("Error: Scattering field inside the structure not yet evaluated. Run `core.scatter` simulation first.")
    
    if str(polarizerangle).lower() == 'none':
        polarizer = 0
    else:
        polarizer = polarizerangle * np.pi/180.
    
    if np.pi < tetamax < 0:
        raise ValueError("`tetamax` out of range, must be in [0, pi]")
    
    if r_probe is not None and return_value in ['int_es', 'int_E0', 'int_Etot']:
        raise ValueError("probing farfield on user-defined positions does not support integration " +
                         "of the intensity since no surface differential can be defined. Use spherical " +
                         "coordinate definition to do the integration.")
    
    
# =============================================================================
#     preparation
# =============================================================================
    ## --- spherical probe coordinates
    if r_probe is None:
        tetalist = np.ones((int(Nteta), int(Nphi)))*np.linspace(tetamin, tetamax, Nteta)[:,None]
        philist = np.ones((int(Nteta), int(Nphi)))*np.linspace(phimin, phimax, Nphi, endpoint=False)[None,:]
        xff = (r * np.sin(tetalist) * np.cos(philist)).flatten()
        yff = (r * np.sin(tetalist) * np.sin(philist)).flatten()
        zff = (r * np.cos(tetalist)).flatten()
        _r_probe = np.transpose([xff, yff, zff])
    else:
        _r_probe = r_probe
        
    ## --- spherical integration steps
    dteta = (tetamax-tetamin)/float(Nteta-1)
    dphi = 2.*np.pi/float(Nphi)
    
    ## --- incident field config
    field_params    = sim.E[field_index][0]
    wavelength      = field_params['wavelength']
    
    ## --- environment
    sim.struct.setWavelength(wavelength)
    conf_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    if sim.dyads.n2_material.__name__ != sim.dyads.n3_material.__name__:
        raise ValueError("`farfield` does not support a cladding layer at the moment. " +
                         "It implements only an asymptotic Green's tensor for an " +
                         "environment with a single interface (substrate).")
    
#==============================================================================
#     electric polarization of structure, fundamental field
#==============================================================================        
    ## --- fundamental field - use dummy structure with 
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(_r_probe, env_dict, **field_params)
    # ## apply correct phase for Z<0 for dipole emitter fundamental fields
    # if sim.efield.field_generator in [fields.dipole_electric, fields.dipole_magnetic]:
    #     E0[_r_probe.T[2]<0] *= -1
    
    ## --- electric polarization of each discretization cell via tensorial polarizability
    Eint = sim.E[field_index][1]
    alpha_tensor = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
    P = np.matmul(alpha_tensor, Eint[...,None])[...,0]
    
    
    ## --- Greens function for each dipole
    G_FF_EE = np.zeros((len(sim.struct.geometry), len(_r_probe), 3, 3), 
                       dtype = sim.efield.dtypec)
    sim.dyads.eval_G(sim.struct.geometry, _r_probe, 
                          sim.dyads.G_EE_ff, wavelength, 
                          conf_dict, G_FF_EE)
    
    ## propagate fields 
    G_FF_EE = np.moveaxis(G_FF_EE, 0,2).reshape((len(_r_probe), 3, -1))  # re-arrange for direct matrix-vector multiplication
    Escat = np.zeros(shape=(len(_r_probe), 3), dtype=sim.efield.dtypec)
    _calc_repropagation(P, Escat, G_FF_EE)
    
    Iscat = np.sum((np.abs(Escat)**2), axis=1)
    
    
    
#==============================================================================
#    calc. fields through optional polarization filter
#==============================================================================
    if str(polarizerangle).lower() != 'none':
        ## --- scattered E-field parallel and perpendicular to scattering plane
        Es_par  = ( Escat.T[0] * np.cos(tetalist.flatten()) * np.cos(philist.flatten()) + 
                    Escat.T[1] * np.sin(philist.flatten()) * np.cos(tetalist.flatten()) - 
                    Escat.T[2] * np.sin(tetalist.flatten()) )
        Es_perp = ( Escat.T[0] * np.sin(philist.flatten()) - Escat.T[1] * np.cos(philist.flatten()) )
        ## --- scattered E-field parallel to polarizer
        Es_pol  = ( Es_par * np.cos(polarizer - philist.flatten()) - 
                    Es_perp * np.sin(polarizer - philist.flatten()) )
        
        ## --- fundamental E-field parallel and perpendicular to scattering plane
        E0_par  = ( E0.T[0] * np.cos(tetalist.flatten()) * np.cos(philist.flatten()) + 
                    E0.T[1] * np.sin(philist.flatten()) * np.cos(tetalist.flatten()) - 
                    E0.T[2] * np.sin(tetalist.flatten()) )
        E0_perp = ( E0.T[0] * np.sin(philist.flatten()) - E0.T[1] * np.cos(philist.flatten()) )
        ## --- fundamental E-field parallel to polarizer
        E0_pol  = ( E0_par * np.cos(polarizer - philist.flatten()) - 
                    E0_perp * np.sin(polarizer - philist.flatten()) )

#==============================================================================
#     Intensities with and without fundamental field / polarizer
#==============================================================================
    ## --- total field (no polarizer)
    if r_probe is None:
        out_shape = tetalist.shape
    else:
        out_shape = len(_r_probe)
        
    I_sc  = Iscat.reshape(out_shape)
    I0    = np.sum((np.abs(E0)**2), axis=1).reshape(out_shape)
    I_tot = np.sum((np.abs(E0 + Escat)**2), axis=1).reshape(out_shape)
    
    ## --- optionally: with polarizer
    if str(polarizerangle).lower() != 'none':
        I_sc  = (np.abs(Es_pol)**2).reshape(out_shape)
        I0    = (np.abs(E0_pol)**2).reshape(out_shape)
        I_tot = (np.abs(Es_pol + E0_pol)**2).reshape(out_shape)
    
    
    if return_value.lower() == 'map':
        if r_probe is None:
            return tetalist, philist, I_sc, I_tot, I0
        else:
            return I_sc, I_tot, I0
    elif return_value.lower() in ['efield', 'fields', 'field']:
        if r_probe is None:
            return tetalist, philist, Escat, Escat + E0, E0
        else:
            return I_sc, I_tot, I0
    else:
        d_solid_surf = r**2 * np.sin(tetalist) * dteta * dphi
        if return_value.lower() == 'int_es':
            return np.sum(I_sc * d_solid_surf)
        elif return_value.lower() == 'int_e0':
            return np.sum(I0 * d_solid_surf)
        elif return_value.lower() == 'int_etot':
            return np.sum(I_tot * d_solid_surf)
        else:
            raise ValueError("Parameter 'return_value' must be one of ['map', 'int_es', 'int_e0', 'int_etot'].")












def nearfield(sim, field_index, r_probe, which_fields=["Es","Et","Bs","Bt"],
                 val_inside_struct="field", N_neighbors_internal_field=4,
                 method='numba'):
    """Nearfield distribution in proximity of nanostructre
    
    For a given incident field, calculate the electro-magnetic field in the 
    proximity of the nanostructure (positions defined by `MAP`).
    
    - Pure python implementation.
    
    - CUDA support to run on GPU, which can be significantly faster on large problems.
    
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r_probe : tuple (x,y,z) or list of 3-lists/-tuples
        (list of) coordinate(s) to evaluate nearfield on. 
        Format: tuple (x,y,z) or list of 3 lists: [Xmap, Ymap, Zmap] 
        (the latter can be generated e.g. using :func:`.tools.generate_NF_map`)
        
    which_fields : list of str, default: ["Es","Et","Bs","Bt"]
        which fields to calculate and return. available options: 
            ["Es","Et","E0", "Bs","Bt","B0"]

    val_inside_struct : str, default: "field"
        one of ["field", "0", "zero", "NaN", "none", None].
        value to return for positions inside structure. default "field" returns 
        the field at the location of the closest meshpoint. Can be very coarse.
        Disable by setting "None", but note that inside the structure the 
        Green's function will diverge in the latter case.
    
    N_neighbors_internal_field : int, default: 4
        Average internal field over field at *N* closes meshpoints. Neighbor 
        fields are weighted by the distance of the evaluation point to 
        the respective neighbor mesh cell.
    
    method : str, default: "numba"
        either "numba" or "cuda", working on CPU or CUDA-compatible GPU. Both 
        via `numba`.
        
    
    Returns
    -------
    depending on kwarg `which_fields`, up to 4 lists of 6-tuples, complex : 
        - scattered Efield ("Es")
        - total Efield ("Et", inlcuding fundamental field)
        - scattered Bfield ("Bs")
        - total Bfield ("Bt", inlcuding fundamental field)
    
    the tuples are of shape (X,Y,Z, Ax,Ay,Az) with Ai the corresponding 
    complex field component
        
    
    Notes
    -----
    For details of the calculation of the scattered field outside the 
    nano-object using the self-consistent field inside the particle, see e.g.: 
    Girard, C. **Near fields in nanostructures.** 
    Reports on Progress in Physics 68, 1883–1933 (2005).
        
    """
    from pyGDM2 import fields_py as fields # !!! adapt this later to final namespace
    
# =============================================================================
#     Exception handling
# =============================================================================
    if sim.E is None: 
        raise ValueError("Error: Scattering field inside the structure not yet " +
                         "evaluated. Run `core.scatter` simulation first.")
    
    if str(val_inside_struct).lower() == 'none':
        try:
            import scipy
            if int(scipy.__version__.split('.')[0]) == 0 and int(scipy.__version__.split('.')[1]) < 17:
                raise Exception("scipy with version < 0.17.0 installed! " +
                                "Positions inside nanostructure cannot be " +
                                "identified. Please upgrade or set `val_inside_struct`=None.")
        except ImportError:
            raise Exception("It seems scipy is not installed. Scipy is required " +
                            "by `nearfield` for detecting internal field positions. " +
                            "Please install scipy >=v0.17, or set `val_inside_struct`=None.")
        
    which_fields = [wf.lower() for wf in which_fields]
    
# =============================================================================
#     preparation
# =============================================================================
    if len(np.shape(r_probe)) == 1:
        if len(r_probe) == 3:
            r_probe = [[r_probe[0]], [r_probe[1]], [r_probe[2]]]
        else: 
            raise ValueError("If 'r_probe' is tuple, must consist of *exactly* 3 elements!")
    elif len(np.shape(r_probe)) == 2:
        if np.shape(r_probe)[0] != 3 and np.shape(r_probe)[1] != 3:
            raise ValueError("'r_probe' must consist of *exactly* 3 elements!")
        if np.shape(r_probe)[0] != 3:
            r_probe = np.transpose(r_probe)
    else:
        raise ValueError("wrong format for 'r_probe'. must consist of *exactly* 3 " +
                         "elements, either floats, or lists.")
    r_probe = np.transpose(r_probe)
    
    field_kwargs    = sim.E[field_index][0]
    wavelength      = field_kwargs['wavelength']
    
    sim.struct.setWavelength(wavelength)
    conf_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    
    
# =============================================================================
#     evaluate Green's function and propagate fields
# =============================================================================
    ## --- fundamental field - use dummy structure with 
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(r_probe, env_dict, **field_kwargs)
    
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    B0 = sim.efield.field_generator(r_probe, env_dict, returnField='H', **field_kwargs)
    
    ## --- electric polarization of each discretization cell via tensorial polarizability
    if "es" in which_fields or "et" in which_fields or \
                "bs" in which_fields or "bt" in which_fields or \
                "hs" in which_fields or "ht" in which_fields:
        Eint = sim.E[field_index][1]
        alpha_tensor = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
        P = np.matmul(alpha_tensor, Eint[...,None])[...,0]
    
    
    ## +++++++++++++ electric field +++++++++++++
    if "es" in which_fields or "et" in which_fields:
        if method.lower()=='numba':
            ## Greens function for each dipole
            G_NF = np.zeros((len(sim.struct.geometry), len(r_probe), 3, 3), 
                            dtype = sim.efield.dtypec)
            sim.dyads.eval_G(sim.struct.geometry, r_probe, 
                                     sim.dyads.G_EE, wavelength, 
                                     conf_dict, G_NF)
            ## propagate fields 
            G_NF = np.moveaxis(G_NF, 0,2).reshape((len(r_probe), 3, -1))  # re-arrange for direct matrix-vector multiplication
            Escat = np.zeros(shape=(len(r_probe), 3), dtype=sim.efield.dtypec)
            _calc_repropagation(P, Escat, G_NF)
            
    ## +++++++++++++ magnetic field +++++++++++++
    if "bs" in which_fields or "bt" in which_fields or "hs" in which_fields or "ht" in which_fields:
        if method.lower()=='numba':
            ## Greens function for each dipole
            G_NF = np.zeros((len(sim.struct.geometry), len(r_probe), 3, 3), 
                            dtype = sim.efield.dtypec)
            sim.dyads.eval_G(sim.struct.geometry, r_probe, 
                                     sim.dyads.G_HE, wavelength, 
                                     conf_dict, G_NF)
            
            ## propagate fields 
            G_NF = np.moveaxis(G_NF, 0,2).reshape((len(r_probe), 3, -1))  # re-arrange for direct matrix-vector multiplication
            Bscat = np.zeros(shape=(len(r_probe), 3), dtype=sim.efield.dtypec)
            _calc_repropagation(P, Bscat, G_NF)
# =============================================================================
#     treat positions inside structure
# =============================================================================
    val_inside_struct = str(val_inside_struct)
    if val_inside_struct.lower() != "none":
#    if str(val_inside_struct).lower() != "field":
        from scipy.linalg import norm
        for i, R in enumerate(r_probe):
            dist_list = norm(sim.struct.geometry - R, axis=1)
            idcs_min_dist = np.argsort(dist_list)
            ## --- if inside, replace fields
            if abs(dist_list[idcs_min_dist[0]]) <= 1.005*sim.struct.step:
                if val_inside_struct.lower() == "nan":
                    fill_valueE = np.nan
                    fill_valueB = np.nan
                elif val_inside_struct.lower() == "field":  # calc internal scattered field
                    fill_valueE = np.average(Eint[idcs_min_dist[:N_neighbors_internal_field]], 
                                 weights = 1/(sim.struct.step/100. + dist_list[idcs_min_dist[:N_neighbors_internal_field]]**1), 
                                 axis=0) - E0[i]  # subtract E0 --> scattered field only
                    if sim.H is not None:
                        Hint = sim.H[field_index][1]
                        fill_valueB = np.average(Hint[idcs_min_dist[:N_neighbors_internal_field]], 
                                 weights = 1/(sim.struct.step/100. + dist_list[idcs_min_dist[:N_neighbors_internal_field]]**1), 
                                 axis=0) - B0[i]  # subtract B0 --> scattered field only
                    else:
                        warnings.warn("No H-values inside structure calculated. Setting internal magnetic field zero. " + 
                                      "Please run 'scatter' with the according parameter.")
                        fill_valueB = 0   # here we need the B-field inside. Not yet implemented
                else:
                    fill_valueE = 0
                    fill_valueB = 0
                if "es" in which_fields or "et" in which_fields:
                    Escat[i] = fill_valueE
                if "bs" in which_fields or "bt" in which_fields or "hs" in which_fields or "ht" in which_fields:
                    Bscat[i] = fill_valueB
    
    if "et" in which_fields:
        Etot = Escat + E0
    if "bt" in which_fields or "ht" in which_fields:
        Btot = Bscat + B0
    
        
# =============================================================================
#     bundle output
# =============================================================================
    return_field_list = []
    if "es" in which_fields:
        Escat = np.concatenate([r_probe, Escat], axis=1)
        return_field_list.append(Escat)
    if "et" in which_fields:
        Etot = np.concatenate([r_probe, Etot], axis=1)
        return_field_list.append(Etot)
    if "e0" in which_fields:
        E0 = np.concatenate([r_probe, E0], axis=1)
        return_field_list.append(E0)
        
    if "bs" in which_fields or "hs" in which_fields:
        Bscat = np.concatenate([r_probe, Bscat], axis=1)
        return_field_list.append(Bscat)
    if "bt" in which_fields or "ht" in which_fields:
        Btot = np.concatenate([r_probe, Btot], axis=1)
        return_field_list.append(Btot)
    if "b0" in which_fields or "h0" in which_fields:
        B0 = np.concatenate([r_probe, B0], axis=1)
        return_field_list.append(B0)
    
    # if len(return_field_list) == 1:
    #     return_field_list = return_field_list[0]
    return return_field_list


# =============================================================================
# field gradients
# =============================================================================
def field_gradient(sim, field_index, 
                   r_probe=None, delta=None, 
                   which_fields=["Et"]):
    """nearfield gradient distribution inside or in proximity of nanostructure
    
    Calculate field-gradients (positions defined by `r_probe`). 
    Using center difference for the numerical derivatives.
    
    Implemented by C. Majorel.
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r_probe : tuple (x,y,z) or list of 3-lists/-tuples, default: positions inside geometry
        (list of) coordinate(s) to evaluate nearfield on. 
        Format: tuple (x,y,z) or list of 3 lists: [Xmap, Ymap, Zmap] 
        (the latter can be generated e.g. using :func:`.tools.generate_NF_map`)
        If `None`: calculate inside nanostructure
    
    delta : float, default=None
        differential step for numerical center-derivative (in nanometers).
        If `None`, use stepsize, which is recommended inside a nanostructure.
        Finer steps are recommended for fields outside the nanostructure
        (1nm may be a good choice).
        
    which_fields : list of str, default: ["Et"]
        for which fields to calculate the gradient. available options: 
            ["Es","Et","E0", "Hs","Ht,"H0]  ("B" can be used as equivalent to "H")
    
    Returns
    -------
    depending on kwarg `which_gradfields`, up to 6 lists of 3 lists of 6-tuples, complex : 
        - gradient scattered Efield ("Es")
        - gradient total Efield ("Et", includes incident field)
        - gradient incident Efield ("E0")
        - gradient scattered Hfield ("Hs")
        - gradient total Hfield ("Ht", includes incident field)
        - gradient incident Hfield ("H0")
    
    each of the lists contains 3 lists [dAx, dAy, dAz] with dAj the differential terms
    dE[0] = dE/dx = [dE0x/dx, dE0y/dx, dE0z/dx]
    dE[1] = dE/dy = [dE0x/dy, dE0y/dy, dE0z/dy]
    dE[2] = dE/dz = [dE0x/dz, dE0y/dz, dE0z/dz]
        
    """
# =============================================================================
#     Exception handling
# =============================================================================
    if r_probe is None:
        r_probe = sim.struct.geometry
    if delta is None:
        delta= sim.struct.step
    
    
    if len(np.shape(r_probe)) == 1:
        if len(r_probe) == 3:
            r_probe = [[r_probe[0]], [r_probe[1]], [r_probe[2]]]
        else: 
            raise ValueError("If 'r_probe' is tuple, must consist of *exactly* 3 elements!")
    elif len(np.shape(r_probe)) == 2:
        if np.shape(r_probe)[0] != 3 and np.shape(r_probe)[1] != 3:
            raise ValueError("'r_probe' must consist of *exactly* 3 elements!")
        if np.shape(r_probe)[0] != 3:
            r_probe = np.transpose(r_probe)
    else:
        raise ValueError("wrong format for 'r_probe'. must consist of *exactly* 3 " +
                         "elements, either floats, or lists.")
    r_probe = np.transpose(r_probe)
    
    if sim.E is None: 
        raise ValueError("Error: Scattering field inside the structure not yet " +
                         "evaluated. Run `core.scatter` simulation first.")
    
    
# =============================================================================
#     preparation
# =============================================================================
    which_fields = [wf.lower() for wf in which_fields]
    
    field_kwargs = sim.E[field_index][0]
    wavelength = field_kwargs['wavelength']
    sim.struct.setWavelength(wavelength)    
    
    
# =============================================================================
#     calc field gradients
# =============================================================================
    ## --- d/dx    
    r_probe_px = copy.deepcopy(r_probe)     # Xmap+delta
    r_probe_mx = copy.deepcopy(r_probe)     # Xmap-delta
    r_probe_px.T[0] += delta
    r_probe_mx.T[0] -= delta
    F_px = nearfield(sim, field_index, r_probe_px, which_fields)
    F_Mx = nearfield(sim, field_index, r_probe_mx, which_fields)

    dFdx = []
    for Epx, Emx in zip(F_px, F_Mx):
        dFdx.append(np.array([np.ravel((Epx.T[3:].T - Emx.T[3:].T) / (2.*delta))]))

    ## --- d/dy
    r_probe_py = copy.deepcopy(r_probe)     # Ymap+delta
    r_probe_my = copy.deepcopy(r_probe)     # Ymap-delta
    r_probe_py.T[1] += delta
    r_probe_my.T[1] -= delta
    F_py = nearfield(sim, field_index, r_probe_py, which_fields)
    F_My = nearfield(sim, field_index, r_probe_my, which_fields)
    
    dFdy = []
    for Epy, Emy in zip(F_py, F_My):
        dFdy.append(np.array([np.ravel((Epy.T[3:].T - Emy.T[3:].T) / (2.*delta))]))
    
    ## --- d/dz    
    r_probe_pz = copy.deepcopy(r_probe)     # Zmap+delta
    r_probe_mz = copy.deepcopy(r_probe)     # Zmap-delta
    r_probe_pz.T[2] += delta
    r_probe_mz.T[2] -= delta
    F_pz = nearfield(sim, field_index, r_probe_pz, which_fields)
    F_Mz = nearfield(sim, field_index, r_probe_mz, which_fields)
    
    ## --- assemble
    dFdz = []
    for Epz, Emz in zip(F_pz, F_Mz):
        dFdz.append(np.array([np.ravel((Epz.T[3:].T - Emz.T[3:].T) / (2.*delta))]))
        
        
    return_field_list = []
    for Fdx, Fdy, Fdz in zip(dFdx, dFdy, dFdz):
        ddx = np.concatenate([r_probe, np.reshape(Fdx, (len(r_probe), 3))], axis=1)
        ddy = np.concatenate([r_probe, np.reshape(Fdy, (len(r_probe), 3))], axis=1)
        ddz = np.concatenate([r_probe, np.reshape(Fdz, (len(r_probe), 3))], axis=1)
        return_field_list.append([ddx.copy(), ddy.copy(), ddz.copy()])
    
    if len(return_field_list) == 1:
        return_field_list = return_field_list[0]
    return return_field_list





def optical_force(sim, field_index, 
                  return_value='total'):
    """optical force acting on the nanostructure
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    return_value : str, default: 'total'
        Values to be returned. Either 'total' (default) or 'structure'.
        
        - "total" : return the total deposited heat in nW (float)
        
        - "structure" : return spatially resolved force, in other words 
        the force acting on each meshpoint. --> list of tuples [x,y,z,q])
    
    
    Returns
    -------
    F : tuple (Fx,Fy,Fz) *or* list of force vectors [x,y,z,Fx,Fy,Fz]
    
        - `return_value`=="total" : (return float)
          total force on structure 

        - `return_value`=="structure" : (return list of tuples [x,y,z,q])
          force at each mesh-cell positions [x,y,z].
    
    
    Notes
    -----
    For details on optical force calculations see e.g.:
    
    [1] Chaumet & Nieto-Vesperinas. 
    *Coupled dipole method determination of the electromagnetic force 
    on a particle over a flat dielectric substrate*. 
    Phys. Rev. B 61, 14119–14127 (2000)
        
    """
    warnings.warn("Optical force calculation is a beta-functionality and still under testing. " +
                  "Please use with caution.")
    
    ## -- electric polarization of structure 
    Eint = sim.E[field_index][1]
    alpha_tensor = sim.dyads.getPolarizabilityTensor(sim.E[field_index][0]['wavelength'], 
                                                     sim.struct)
    P = np.matmul(alpha_tensor, Eint[...,None])[...,0]
    
    
    ## -- field gradients inside half structure 
    gradE_inside = field_gradient(sim, field_index)
    
    ## -- separate the derivatives
    dEdx = gradE_inside[0][...,3:]       #  [X, Y, Z, dEX/dx, dEY/dx, dEZ/dx] --> [dEX/dx, dEY/dx, dEZ/dx]
    dEdy = gradE_inside[1][...,3:]       # --> [dEX/dy, dEY/dy, dEZ/dy]
    dEdz = gradE_inside[2][...,3:]       # --> [dEX/dz, dEY/dz, dEZ/dz]
    
    ## -- calculate the force
    Fx = 0.5 * np.real( P[...,0] * np.conj(dEdx[...,0]) + 
                        P[...,1] * np.conj(dEdx[...,1]) + 
                        P[...,2] * np.conj(dEdx[...,2]) )
    Fy = 0.5 * np.real( P[...,0] * np.conj(dEdy[...,0]) + 
                        P[...,1] * np.conj(dEdy[...,1]) + 
                        P[...,2] * np.conj(dEdy[...,2]) )
    Fz = 0.5 * np.real( P[...,0] * np.conj(dEdz[...,0]) + 
                        P[...,1] * np.conj(dEdz[...,1]) + 
                        P[...,2] * np.conj(dEdz[...,2]) )
    
    ## -- return results
    if return_value.lower() == "structure":
        np.transpose([sim.struct.geometry.T[0], 
                      sim.struct.geometry.T[1], 
                      sim.struct.geometry.T[2], 
                      np.sum(Fx), np.sum(Fy), np.sum(Fz)])
    else:
        F_tot = np.array([np.sum(Fx), np.sum(Fy), np.sum(Fz)])
        return F_tot







def optical_chirality(sim, field_index, r_probe, which_field="t", **kwargs):
    """calculate the optical chirality of the electromagnetic field
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    Returns the normalized electromagnetic chirality *C / C_LCP*, as defined in [2].
    Normalized to a left circular polarized (LCP) plane wave of amplitude |È0|=1.
    
     - LCP: C = +2 P0 c/omega
     - RCP: C = -2 P0 c/omega
    
    P0 is the time-averaged electric energy density, c the speed of light and omega
    the angular frequency of the time-harmonic electric field. 
    
    |C/C_LCP|>1 means that the local field is "superchiral", 
    hence a chiral molecule is excited with higher selectivity than it would be
    with circular polarized light.
    
    kwargs are passed to :func:`.nearfield`.
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r_probe : tuple (x,y,z) or list of 3-lists/-tuples
        (list of) coordinate(s) to evaluate nearfield on. 
        Format: tuple (x,y,z) or list of 3 lists: [Xmap, Ymap, Zmap] 
        (the latter can be generated e.g. using :func:`.tools.generate_NF_map`)
    
    which_field : str, default: 't'
        either of:
            - "s", "Es" for *scattered field*
            - "t", "Et" for *total field* (with illumination, i.e. Et=Es+E0; Bt=Bs+B0)
    
    Returns
    -------
    list of tuples (X,Y,Z, X). Each tuple consists of the position and the 
    (normalized) optical chirality *C / C_LCP*.
    
    
    Notes
    -----
    For details on the optical chirality, see:
    
    [1] Tang, Y. & Cohen, A. E.: **Optical Chirality and Its Interaction 
    with Matter**. Phys. Rev. Lett. 104, 163901 (2010)
    
    [2] Meinzer, N., Hendry, E. & Barnes, W. L.: **Probing the chiral nature 
    of electromagnetic fields surrounding plasmonic nanostructures**. 
    Phys. Rev. B 88, 041407 (2013)
    
    A discussion about the proper normalization of C can be found in:
    
    [3] Schäferling M., Yin X., Engheta N., Giessen H. **Correction to Helical 
    Plasmonic Nanostructures as Prototypical Chiral Near-Field Sources**. 
    ACS Photonics 3(10), 2000-2002 (2016)
    
    """
    warnings.warn("Chirality is a beta-functionality still under testing. " +
                  "Please use with caution.")
    
    Es, Et, Bs, Bt = nearfield(sim, field_index, r_probe, **kwargs)
    
    if which_field.lower() in ["s", "es", "scat", "scattered"]:
        Et = Es
        Bt = Bs
    
    ## Ref. [2]: C ~ Im(E* B)
    C = np.concatenate([
                    Et.T[:3].real, # positions
                    [np.sum(np.multiply(np.conjugate(Et.T[3:]), 
                                                     Bt.T[3:]), axis=0).imag]
                        ]).astype(np.float)
    
    if len(np.shape(r_probe)) == 1 or len(r_probe) == 1:
        return C[3][0]
    else:
        return C
    


# =============================================================================
# heat and temperature
# =============================================================================
def heat(sim, field_index, power_scaling_e0=1.0, return_value='total', return_units='nw'):
    """calculate the total induced heat in the nanostructure
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    power_scaling_e0 : float, default: 1
        incident laser power scaling. power_scaling_e0 = 1 corresponds 
        to 1 mW per micron^2. See [1].
    
    return_value : str, default: 'total'
        Values to be returned. Either 'total' (default) or 'structure'.
        
        - "total" : return the total deposited heat in nW (float)
        
        - "structure" : return spatially resolved deposited heat at each 
          meshpoint in nW (list of tuples [x,y,z,q])
    
    return_units : str, default: "nw"
        units of returned heat values, either "nw" or "uw" (nano or micro Watts)
    
    
    Returns
    -------
    Q : float *or* list of tuples [x,y,z,q]
    
        - `return_value`=="total" : (return float)
          total deposited heat in nanowatt (optionally in microwatt). 

        - `return_value`=="structure" : (return list of tuples [x,y,z,q])
          The returned quantity *q* is the total deposited heat 
          at mesh-cell position [x,y,z] in nanowatt. To get the heating 
          power-density, please divide by the mesh-cell volume.
    
    
    Notes
    -----
    For details on heat/temperature calculations and raster-scan simulations, see:
    
    [1] Baffou, G., Quidant, R. & Girard, C.: **Heat generation in plasmonic 
    nanostructures: Influence of morphology**
    Applied Physics Letters 94, 153109 (2009)
    
    [2] Teulle, A. et al.: **Scanning optical microscopy modeling in nanoplasmonics** 
    Journal of the Optical Society of America B 29, 2431 (2012).


    """
    warnings.warn("`linear_py.heat` does not support tensorial permittivity yet.")
    
    
    if sim.E is None: 
        raise ValueError("Error: Scattering field inside the structure not yet evaluated. Run `core.scatter` simulation first.")
    
    power_scaling_e0 *= 0.01    # for mW/cm^2
    
    field_params = sim.E[field_index][0]
    wavelength   = field_params['wavelength']
    
    ## --- Factor allowing to have the released power in nanowatt 
    released_power_scaling = 100.
    
    ## --- polarizabilities and electric fields
    sim.struct.setWavelength(wavelength)
    n_env        = sim.dyads.getEnvironmentIndices(wavelength, sim.struct.geometry[:1])[0]  # assume structure is fully in one environment
    alpha_tensor = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
    E = sim.E[field_index][1]
    P = np.matmul(alpha_tensor, E[...,None])[...,0]

    
    ## heat at each meshpoint in nW/nm^3
    q = (((8 * np.pi**2 / wavelength) / n_env) * np.sum(np.multiply(P, np.conjugate(E)), axis=1).imag
                         * power_scaling_e0 * released_power_scaling).real
    
    ## --- optional conversion to micro watts
    if return_units.lower() == 'uw':
        q /= 1.0E3
    
    if return_value == 'total':
        return np.sum(q)
    elif return_value in ['structure', 'struct']:
        x,y,z = sim.struct.geometry.T
        return np.concatenate([[x],[y],[z],[q]]).T
    else:
        raise ValueError("`return_value` must be one of ['total', 'structure', 'struct'].")



def temperature(sim, field_index, r_probe, 
                kappa_env=0.6, kappa_subst=None, incident_power=1.0):
    """calculate the temperature rise at locations outside the nano-particle
    
    Calculate the temperature increase close to a optically excited 
    nanostructure using the approach described in [2] and [3] (Ref. [3] 
    introduces a further correction term for particles lying on a substrate)
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r_probe : tuple (x,y,z) or list of 3-lists/-tuples
        (list of) coordinate(s) to evaluate nearfield on. 
        Format: tuple (x,y,z) or list of 3 lists: [Xmap, Ymap, Zmap] 
        (the latter can be generated e.g. using :func:`.tools.generate_NF_map`)
    
    kappa_env : float, default: 0.6
        heat conductivity of environment. default: kappa_env = 0.6 (water). 
        (air: kappa=0.024, for more material values see e.g. [4]). In W/mK.
    
    kappa_subst : float, default: None
        heat conductivity of substrate. default: None --> same as substrate. 
        Using the mirror-image technique described in [3]. (glass: kappa=0.8)
    
    incident_power : float, default: 1.0
        incident laser power density in mW per micron^2. See also [1].
    
    
    Returns
    -------
    if evaluating at a single position, D_T : float
        temperature increase in Kelvin at r_probe
    
    if evaluating at a list of positions, list of tuples [x, y, z, D_T] 
        where D_T is the temperature increase in Kelvin at (x,y,z), which
        are the positions defined by `r_probe`
    
    Notes
    -----
    For details on heat/temperature calculations and raster-scan simulations, see:
    
    [1] Baffou, G., Quidant, R. & Girard, C.: **Heat generation in plasmonic 
    nanostructures: Influence of morphology**
    Applied Physics Letters 94, 153109 (2009)
    
    [2] Baffou, G., Quidant, R. & Girard, C.: **Thermoplasmonics modeling: 
    A Green’s function approach** 
    Phys. Rev. B 82, 165424 (2010)

    [3] Teulle, A. et al.: **Scanning optical microscopy modeling in nanoplasmonics**
    Journal of the Optical Society of America B 29, 2431 (2012).
    
    
    For the thermal conductivity of common materials, see:
    
    [4] Hugh D Young, Francis Weston Sears: **University Physics**, *chapter 15*,
    8th. edition: Addison-Wesley, 1992
    (see also e.g.: http://hyperphysics.phy-astr.gsu.edu/hbase/Tables/thrcn.html)

    """
    kappa_subst  = kappa_subst or kappa_env
    field_params = sim.E[field_index][0]
    wavelength   = field_params['wavelength']
    sim.struct.setWavelength(wavelength)
    n_env        = sim.dyads.getEnvironmentIndices(wavelength, sim.struct.geometry[:1])[0]  # assume structure is fully in one environment
    
    if sim.E is None: 
        raise ValueError("Error: Scattering field inside the structure not yet evaluated. Run `core.scatter` simulation first.")
    
    if kappa_subst == kappa_env and sim.dyads.n1_material.__name__ != sim.dyads.n2_material.__name__:
        warnings.warn("Substrate and environment have different indices but same heat conductivity.")
    if kappa_subst != kappa_env and sim.dyads.n1_material.__name__ == sim.dyads.n2_material.__name__:
        warnings.warn("Substrate and environment have same ref.index but different heat conductivity.")
    
    incident_power *= 0.01          # for mW/cm^2
    released_power_scaling = 100.   # output in nW
    
    ## --- main heat generation function
    def calc_heat_single_position(sim, r_probe):
        ## --- polarizability and field in structure
        alpha_tensor = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
        E = sim.E[field_index][1]
        P = np.matmul(alpha_tensor, E[...,None])[...,0]
        
        ## --- meshpoint distance to probe, polarizabilities and electric fields
        r_mesh = sim.struct.geometry
        dist_probe = np.sqrt( np.sum( np.power((np.array(r_probe) - r_mesh), 2), axis=1) )
        
        ## --- mirror structure below substrate for heat reflection at substrate
        if kappa_subst != kappa_env:
            r_mesh_mirror = copy.deepcopy(sim.struct.geometry)
            r_mesh_mirror.T[2] *= -1
            dist_probe_mirror = np.sqrt( np.sum( np.power((np.array(r_probe) - r_mesh_mirror), 2), axis=1) ) 
        
        ## --- temperature rise at r_probe
        q = (((2 * np.pi / wavelength) / n_env) * np.sum(np.multiply(P, np.conjugate(E)), axis=1).imag
                         * incident_power * released_power_scaling).real
        D_T = np.sum( q / dist_probe )
        if kappa_subst != kappa_env:
            D_T += np.sum( q / dist_probe_mirror ) * (kappa_subst - kappa_env) / (kappa_subst + kappa_env)
        D_T /= kappa_env
        
        return D_T
    
    
    ## --- single position:
    if len(np.shape(r_probe)) == 1 or len(r_probe) == 1:
        D_T = calc_heat_single_position(sim, r_probe)
    ## --- multiple positions:
    else:
        D_T = []
        if np.shape(r_probe)[1] != 3:
            r_probe = np.transpose(r_probe)
        for i in r_probe:
            D_T.append([i[0], i[1], i[2], 
                        calc_heat_single_position(sim, i)])
        D_T = np.array(D_T)
    
    return D_T







































# =============================================================================
# experimental CUDA propagator functions
# =============================================================================
##
## ---  Call like :
##
#     elif method.lower()=='cuda':
#         G_NF = _calc_multidipole_NF_EE_GPU(sim.struct.geometry, r_probe, 
#                                            wavelength, eps1, eps2, eps3, spacing)
#         Escat = _calc_repropagation_GPU(P, G_NF)

#     elif method.lower()=='cuda':
#         G_NF = _calc_multidipole_NF_HE_GPU(sim.struct.geometry, r_probe, 
#                                            wavelength, eps_env)
#         Bscat = _calc_repropagation_GPU(P, G_NF)

# def _calc_multidipole_NF_EE_GPU(dp_pos, r_probe, wavelength, eps1, eps2, eps3, spacing,
#                                 threadsperblock=(16,16)):
#     from numba import cuda
    
#     ## --- cuda version of propagator
#     G_cuda = cuda.jit(device=True)(G_EE)
    
#     ## --- cuda kernel
#     @cuda.jit()
#     def multidp_kernel_cuda(dp_pos, r_probe, wavelength, eps1, eps2, eps3, spacing, M):
#         """
#         Code for kernel.
#         """
#         i, j = cuda.grid(2)    # indices of current cuda thread
#         if i < M.shape[0] and j < M.shape[1]:
#             _pos = dp_pos[i]
#             _r = r_probe[j]
#             xx, yy, zz, xy, xz, yx, yz, zx, zy = G_cuda(_pos, _r,
#                                                wavelength, eps1, eps2, eps3, spacing)
#             ## return list of Greens tensors
#             M[i,j,0,0], M[i,j,1,1], M[i,j,2,2] = xx, yy, zz
#             M[i,j,1,0], M[i,j,2,0], M[i,j,0,1] = yx, zx, xy
#             M[i,j,2,1], M[i,j,0,2], M[i,j,1,2] = zy, xz, yz
            
#     ## --- cuda threads config
#     M = np.zeros((len(dp_pos), len(r_probe),3,3), dtype=np.complex64)
#     blockspergrid_x = math.ceil(M.shape[0] / threadsperblock[0])
#     blockspergrid_y = math.ceil(M.shape[1] / threadsperblock[1])
#     blockspergrid = (blockspergrid_x, blockspergrid_y)
    
#     ## -- run cuda kernel
#     cuda.select_device(0)
#     multidp_kernel_cuda[blockspergrid, threadsperblock](dp_pos, r_probe, wavelength, 
#                                            eps1, eps2, eps3, spacing, M)
#     cuda.close()
    
#     return M


# def _calc_multidipole_NF_HE_GPU(dp_pos, r_probe, wavelength, eps_env, threadsperblock=(16,16)):
#     from numba import cuda

#     ## --- cuda version of propagator
#     G_cuda = cuda.jit(device=True)(G0_HE)
    
#     ## --- cuda kernel
#     @cuda.jit()
#     def multidp_kernel_cuda(dp_pos, r_probe, wavelength, eps_env, M):
#         """
#         Code for kernel.
#         """
#         i, j = cuda.grid(2)    # indices of current cuda thread
#         if i < M.shape[0] and j < M.shape[1]:
#             _pos = dp_pos[i]
#             _r = r_probe[j]
#             xx, yy, zz, xy, xz, yx, yz, zx, zy = G_cuda(_pos, _r, wavelength, eps_env)
#             ## return list of Greens tensors
#             M[i,j,0,0], M[i,j,1,1], M[i,j,2,2] = xx, yy, zz
#             M[i,j,1,0], M[i,j,2,0], M[i,j,0,1] = yx, zx, xy
#             M[i,j,2,1], M[i,j,0,2], M[i,j,1,2] = zy, xz, yz
            
#     ## --- cuda threads config
#     M = np.zeros((len(dp_pos), len(r_probe),3,3), dtype=np.complex64)
#     blockspergrid_x = math.ceil(M.shape[0] / threadsperblock[0])
#     blockspergrid_y = math.ceil(M.shape[1] / threadsperblock[1])
#     blockspergrid = (blockspergrid_x, blockspergrid_y)
    
#     ## -- run cuda kernel
#     cuda.select_device(0)
#     multidp_kernel_cuda[blockspergrid, threadsperblock](dp_pos, r_probe, wavelength, eps_env, M)
#     cuda.close()
    
#     return M


# def _calc_repropagation_GPU(P, G_dyad_list, threadsperblock=(16,16)):
#     from numba import cuda

#     ## --- cuda kernel
#     @cuda.jit()
#     def repropa_kernel_cuda(P, Escat_all, G_dyad_list):
#         """
#         Code for kernel.
#         """
#         i, j = cuda.grid(2)    # indices of current cuda thread
#         if i < G_dyad_list.shape[0] and j < G_dyad_list.shape[1]:
#             _G = G_dyad_list[i, j]
#             _P = P[i]
# #            _Es = np.dot(_G, P[i])
#             Escat_all[i, j, 0] = _G[0,0]*_P[0] + _G[0,1]*_P[1] + _G[0,2]*_P[2]
#             Escat_all[i, j, 1] = _G[1,0]*_P[0] + _G[1,1]*_P[1] + _G[1,2]*_P[2]
#             Escat_all[i, j, 2] = _G[2,0]*_P[0] + _G[2,1]*_P[1] + _G[2,2]*_P[2]
    
#     ## --- cuda threads config
#     Escat_all = np.zeros(shape=(len(P), G_dyad_list.shape[1], 3), dtype=np.complex64)
#     blockspergrid_x = math.ceil(Escat_all.shape[0] / threadsperblock[0])
#     blockspergrid_y = math.ceil(Escat_all.shape[1] / threadsperblock[1])
#     blockspergrid = (blockspergrid_x, blockspergrid_y)
    
#     ## -- run cuda kernel
#     cuda.select_device(0)
#     repropa_kernel_cuda[blockspergrid, threadsperblock](P, Escat_all, G_dyad_list)
#     cuda.close()
#     Escat = np.sum(Escat_all, axis=0)  # sum all meshpoints' contributions
    
#     return Escat
