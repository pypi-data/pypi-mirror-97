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
Collection of incident fields
"""

from __future__ import print_function
from __future__ import absolute_import

import itertools
import warnings
import cmath

import numpy as np
import numba




#==============================================================================
# globals
#==============================================================================
DTYPE_C = np.complex64



#==============================================================================
# Incident field container class
#==============================================================================
class efield(object):
    """incident electromagnetic field container class
    
    Defines an incident electric field including information about wavelengths,
    polarizations, focal spot or whatever optional parameter is supported by
    the used field generator.
    
    Parameters
    ----------
    field_generator : `callable`
        field generator function. Mandatory arguments are 
         - `struct` (instance of :class:`.structures.struct`)
         - `wavelength` (list of wavelengths)
    
    wavelengths : list
        list of wavelengths (wavelengths in nm)
    
    kwargs : list of dict or dict
        possible additional keyword arguments, passed to `field_generator`.
        Either dict or list of dicts.
         - If list of dicts, each entry must correspond exactly to one 
           parameters-set for `field-generator`.
         - If dict, maybe contain lists for configurations of the parameters. 
           In that case, all possible parameter-permutations will be generated.
    
    Examples
    --------
    >>> kwargs = dict(theta = [0.0,45,90])
    [{'theta': 0.0}, {'theta': 45.0}, {'theta': 90.0}]
    
    is equivalent to:
    
    >>> kwargs = [dict(theta=0.0), dict(theta=45.0), dict(theta=90.0)]
    [{'theta': 0.0}, {'theta': 45.0}, {'theta': 90.0}]
    
    """
    def __init__(self, field_generator, wavelengths, kwargs):
        """initialize field container"""
        self.field_generator = field_generator
        self.wavelengths = np.array(wavelengths)
        self.kwargs = kwargs
        
        ## --- generate parameter-sets for field-generator
        if type(kwargs) == dict:
            ## --- integer parameters to list
            for key in kwargs:
                if type(kwargs[key]) not in [list, np.ndarray]:
                    kwargs[key] = [kwargs[key]]
            
            ## --- generate all permutations of kwargs for direct use in field_generator
            varNames = sorted(kwargs)
            self.kwargs_permutations = [dict(zip(varNames, prod)) for 
                                    prod in itertools.product(*(kwargs[varName] 
                                                for varName in varNames))]
        elif type(kwargs) == list:
            self.kwargs_permutations = []
            for kw in kwargs:
                self.kwargs_permutations.append(kw)
                if type(kw) != dict:
                    raise ValueError("Wrong input for 'kwargs': Must be either dict or list of dicts.")
                
        else:
            raise ValueError("Wrong input for 'kwargs': Must be either dict or list of dicts.")
        
        ## set precision to single by default
        self.setDtype(np.float32, np.complex64)
    
    
    def setDtype(self, dtypef, dtypec):
        """set dtype of arrays"""
        self.dtypef = dtypef
        self.dtypec = dtypec


    def __repr__(self, verbose=False):
        out_str =  ' ----- incident field -----'
        out_str += '\n' + '   field generator: "{}"'.format(self.field_generator.__name__)
        out_str += '\n' + '   {} wavelengths between {} and {}nm'.format(
                         len(self.wavelengths), self.wavelengths.min(),
                         self.wavelengths.max(),)
        if verbose or len(self.wavelengths)<6:
            for i, wl in enumerate(self.wavelengths):
                out_str += '\n' + '      - {}: {}nm'.format(i,wl)
        out_str += '\n' + '   {} incident field configurations per wavelength'.format(
                                        len(self.kwargs_permutations))    
        if verbose or len(self.kwargs_permutations)<6:
            for i, kw in enumerate(self.kwargs_permutations):
                out_str += '\n' + '      - {}: {}'.format(i,str(kw).replace("{","").replace("}",""))
        return out_str








        

#==============================================================================
# Electric field generator functions
#==============================================================================
def nullfield(pos, env_dict, wavelength, returnField='E', **kwargs):
    """Zero-Field
    
    all additional kwargs are ignored
    
    Parameters
    ----------
    pos : np.array
        list of 3-tuple coordinates to evaluate field at: [[x1,y1,z1], [x2,y2,z2], ... ]
    
    env_dict : dict
        placeholder for environment description. will be ignored in `nullfield`
    
    wavelength : float
        Wavelength in nm
    
    returnField : str
        placeholder. will be ignored in `nullfield`
    
    Returns:
    ----------
      Complex zero 3-vector at each coordinate in 'pos'
    
    """
    return np.zeros((len(pos), 3), dtype=DTYPE_C)




##----------------------------------------------------------------------
##                      INCIDENT FIELDS
##----------------------------------------------------------------------


    

@numba.njit(cache=True)
def _three_layer_pw(wavelength, theta_inc, polar, z_d, spacing, n1, n2, n3, x, y, z, E0=1.0):
    """oblique incident planewave, only linear polarization
    
    Oblique incidence (from bottom to top) through n1/n2/n3 layer interfaces. 
    May be used to simulate evanescent fields in the total internal 
    reflection configuration. Linear polarization.
    Amplitude = 1 for both, E and B.
    
    Original code by Ch. Girard, python implementation by C. Majorel
    
    Parameters
    ----------
    wavelength : float
        Wavelength in nm
    
    theta_inc : float, default: 0
        incident angle in the XZ plane with respect to e_z, in degrees.
         - 0deg = along Z (from neg to pos Z)
         - 90deg = along X  (from pos to neg X)
         - 180deg = along Z  (from pos to neg Z)
         - 270deg = along X  (from neg to pos X)
    
    polar : str, default: 's'
        incident linear polarization. Either 's' or 'p'. 
        At 0 degree incident angle, 's' is polarized along x, 'p' along y.
    
    z_d : float
        bottom interface position (along z) between media 1 and 2
    
    spacing : float
        spacing between bottom interface (between media 1 and 2) and 
        top interface position (between media 2 and 3)
    
    n1, n2, n3 : complex
        (complex) refractive index of each media 
    
    x, y, z : float
        x/y/z coordinates for computation of the fields
    
    E0 : float
        amplitude of E (and B) field
    
    Returns
    -------
      E0, B0:       Complex E-B-Fields at each dipole position as 
                    6 lists of the (complex) components: 
                    Ex, Ey, Ez, Bx, By, Bz
    """
    if E0 == 0.0:
        return 0.0j, 0.0j, 0.0j, 0.0j, 0.0j, 0.0j
    
    
    z_u = z_d + spacing             # z position of upper interface
    r = np.array([x, y, z]).astype(np.complex64)         # eval. position
    theta_r = theta_inc*np.pi/180.  # inc. angle in rad 
    k0 = 2*np.pi/wavelength         # wavevector in vacuum
    
    ## -- permittivities    
    eps1 = n1**2
    eps2 = n2**2
    eps3 = n3**2
    
    if theta_r > np.pi/2. and theta_r < 3*np.pi/2.:
    ## -- Different wavevectors    
        k1 = np.array([-n3*k0*cmath.sin(theta_r), 0. , -k0*cmath.sqrt(eps1-eps3*cmath.sin(theta_r)**2)]).astype(np.complex64)        ## -- transmitted wavevector in medium 1 (bottom layer)
        k2 = np.array([-n3*k0*cmath.sin(theta_r), 0. , -k0*cmath.sqrt(eps2-eps3*cmath.sin(theta_r)**2)]).astype(np.complex64)        ## -- transmitted wavevector in medium 2 (middle layer)
        k2p = np.array([-n3*k0*cmath.sin(theta_r), 0. , k0*cmath.sqrt(eps2-eps3*cmath.sin(theta_r)**2)]).astype(np.complex64)        ## -- reflected wavevector in medium 2 (middle layer)
        k3 = np.array([-n3*k0*cmath.sin(theta_r), 0. , n3*k0*cmath.cos(theta_r)]).astype(np.complex64)                               ## -- incident wavevector in medium 3 (top layer)
        k3p = np.array([-n3*k0*cmath.sin(theta_r), 0. , -n3*k0*cmath.cos(theta_r)]).astype(np.complex64)                             ## -- reflected wavevector in medium 3 (top layer)
        
    ## -- Phase terms    
        c1p = cmath.exp(1.0j*k1[2]*z_d)
        c1m = cmath.exp(-1.0j*k1[2]*z_d)
        c2p = cmath.exp(1.0j*k2[2]*z_d)
        c2m = cmath.exp(-1.0j*k2[2]*z_d)
        c2pp = cmath.exp(1.0j*k2[2]*z_u)
        c2pm = cmath.exp(-1.0j*k2[2]*z_u)
        c3pp = cmath.exp(1.0j*k3[2]*z_u)
        c3pm = cmath.exp(-1.0j*k3[2]*z_u)
        
    ## -- z - components of the wavevector/eps for magnetic modulus    
        k1gz = k1[2]/eps1
        k2gz = k2[2]/eps2
        k3gz = k3[2]/eps3               
        
    ### --- modulus electric field in s-polarized mode    
        delta = c3pm*c1p*(c2m*c2pp*(k2[2]**2+k1[2]*k3[2]+k3[2]*k2[2]+k1[2]*k2[2])+
                c2p*c2pm*(-k2[2]**2-k1[2]*k3[2]+k1[2]*k2[2]+k3[2]*k2[2]))
        
        delta3 = c3pp*c1p*(c2m*c2pp*(-k2[2]**2-k2[2]*k1[2]+k1[2]*k3[2]+k2[2]*k3[2])+
                  c2p*c2pm*(k2[2]**2-k2[2]*k1[2]+k2[2]*k3[2]-k1[2]*k3[2]))
        
        delta2 = 2.*c2m*c1p*(k1[2]*k3[2]+k3[2]*k2[2])
        
        delta2p = 2.*c2p*c1p*(k2[2]*k3[2]-k1[2]*k3[2])
        
        delta1 = 4.*k2[2]*k3[2]
        
        cep3 = delta3/delta
        ce2 = delta2/delta
        cep2 = delta2p/delta
        ce1 = delta1/delta
        
        
    ### --- modulus magnetic field in p-polarized mode
        deltam = c3pm*c1p*(c2m*c2pp*(k2gz**2+k1gz*k3gz+k3gz*k2gz+k1gz*k2gz)+
                c2p*c2pm*(-k2gz**2-k1gz*k3gz+k1gz*k2gz+k3gz*k2gz))
        
        delta3m = c3pp*c1p*(c2m*c2pp*(-k2gz**2-k2gz*k1gz+k1gz*k3gz+k2gz*k3gz)+
                  c2p*c2pm*(k2gz**2-k2gz*k1gz+k2gz*k3gz-k1gz*k3gz))
        
        delta2m = 2.*c2m*c1p*(k1gz*k3gz+k3gz*k2gz)
        
        delta2pm = 2.*c2p*c1p*(k2gz*k3gz-k1gz*k3gz)
        
        delta1m = 4.*k2gz*k3gz
        
        cmagp3 = delta3m/deltam
        cmag2 = delta2m/deltam
        cmagp2 = delta2pm/deltam
        cmag1 = delta1m/deltam


    ### --- Determination of the differents electric and magnetic field    
        if z>z_u:
            cphase3 = cmath.exp(1.0j*np.dot(k3,r))
            cphase3p = cmath.exp(1.0j*np.dot(k3p,r))
                
            if polar=='s':
                Ex = 0.
                Ey = cphase3+cep3*cphase3p
                Ez = 0.
                
                Bx = -cphase3*k3[2]/k0-(cep3*cphase3p*k3p[2]/k0)
                By = 0.
                Bz = cphase3*k3[0]/k0+(cep3*cphase3p*k3p[0]/k0)
                
            if polar=='p':
                Ex = n3*(-cphase3*k3[2]/(eps3*k0)-cmagp3*cphase3p*k3p[2]/(eps3*k0))
                Ey = 0.
                Ez = n3*(cphase3*k3[0]/(eps3*k0)+cmagp3*cphase3p*k3p[0]/(eps3*k0))
                
                Bx = 0.
                By = -cphase3-cmagp3*cphase3p
                Bz = 0.
                
        elif z_d<z<z_u:
            cphase2 = cmath.exp(1.0j*np.dot(k2,r))
            cphase2p = cmath.exp(1.0j*np.dot(k2p,r))
                
            if polar=='s':
                Ex = 0.
                Ey = ce2*cphase2+cep2*cphase2p
                Ez = 0.
    
                Bx = -ce2*cphase2*k2[2]/k0-cep2*cphase2p*k2p[2]/k0
                By = 0.
                Bz = ce2*cphase2*k2[0]/k0+cep2*cphase2p*k2p[0]/k0
                
            if polar=='p':
                Ex = n3*(-cmag2*cphase2*k2[2]/(eps2*k0)-cmagp2*cphase2p*k2p[2]/(eps2*k0))
                Ey = 0.
                Ez = n3*(cmag2*cphase2*k2[0]/(eps2*k0)+cmagp2*cphase2p*k2p[0]/(eps2*k0))
                
                Bx = 0.
                By = -cmag2*cphase2-cmagp2*cphase2p
                Bz = 0.
                
        else:
            cphase1 = cmath.exp(1.0j*np.dot(k1,r))
            
            if polar=='s':
                Ex = 0.
                Ey = ce1*cphase1
                Ez = 0.
                
                Bx = -ce1*cphase1*k1[2]/k0
                By = 0.
                Bz = ce1*cphase1*k1[0]/k0
            
            if polar=='p':
                Ex = n3*(-cmag1*cphase1*k1[2]/(eps1*k0))
                Ey = 0.
                # Ez = 1./n3*(cmag1*cphase1*k1[0]/(eps1*k0))  # <-- this was probably wrong
                Ez = n3*(cmag1*cphase1*k1[0]/(eps1*k0))
                
                Bx = 0.
                By = -cmag1*cphase1
                Bz = 0.

    else :    
    ## -- Different wavevectors    
        k1 = np.array([-n1*k0*cmath.sin(theta_r), 0. , n1*k0*cmath.cos(theta_r)]).astype(np.complex64)                              ## -- incident wavevector in medium 1 (bottom layer)
        k1p = np.array([-n1*k0*cmath.sin(theta_r), 0. , -n1*k0*cmath.cos(theta_r)]).astype(np.complex64)                            ## -- reflected wavevector in medium 1 (bottom layer)
        k2 = np.array([-n1*k0*cmath.sin(theta_r), 0. , k0*cmath.sqrt(eps2-eps1*cmath.sin(theta_r)**2)]).astype(np.complex64)        ## -- transmitted wavevector in medium 2 (middle layer)
        k2p = np.array([-n1*k0*cmath.sin(theta_r), 0. , -k0*cmath.sqrt(eps2-eps1*cmath.sin(theta_r)**2)]).astype(np.complex64)      ## -- reflected wavevector in medium 2 (middle layer)
        k3 = np.array([-n1*k0*cmath.sin(theta_r), 0. , k0*cmath.sqrt(eps3-eps1*cmath.sin(theta_r)**2)]).astype(np.complex64)        ## -- transmitted wavevector in medium 3 (top layer)
        
    ## -- Phase terms    
        c1p = cmath.exp(1.0j*k1[2]*z_d)
        c1m = cmath.exp(-1.0j*k1[2]*z_d)
        c2p = cmath.exp(1.0j*k2[2]*z_d)
        c2m = cmath.exp(-1.0j*k2[2]*z_d)
        c2pp = cmath.exp(1.0j*k2[2]*z_u)
        c2pm = cmath.exp(-1.0j*k2[2]*z_u)
        c3pp = cmath.exp(1.0j*k3[2]*z_u)
        c3pm = cmath.exp(-1.0j*k3[2]*z_u)
        
    ## -- z - components of the wavevector/eps for magnetic modulus    
        k1gz = k1[2]/eps1
        k2gz = k2[2]/eps2
        k3gz = k3[2]/eps3
        
    ### --- modulus electric field in s-polarized mode    
        delta = c3pp*c1m*(c2m*c2pp*(-k2[2]**2-k3[2]*k1[2]+k2[2]*k3[2]+k2[2]*k1[2])+
                c2p*c2pm*(k1[2]*k2[2]+k3[2]*k1[2]+k3[2]*k2[2]+k2[2]**2))
        
        delta1 = c3pp*c1p*(c2m*c2pp*(k2[2]**2-k3[2]*k2[2]+k1[2]*k2[2]-k1[2]*k3[2])+
                  c2p*c2pm*(-k2[2]**2-k3[2]*k2[2]+k1[2]*k3[2]+k1[2]*k2[2]))
        
        delta2 = 2.*c3pp*c2pm*(k1[2]*k2[2]+k1[2]*k3[2])
        
        delta2p = 2.*c3pp*c2pp*(k1[2]*k2[2]-k1[2]*k3[2])
        
        delta3 = 4.*k1[2]*k2[2]
        
        cep1 = delta1/delta
        ce2 = delta2/delta
        cep2 = delta2p/delta
        ce3 = delta3/delta
        
        
    ### --- modulus magnetic field in p-polarized mode
        deltam = c3pp*c1m*(c2m*c2pp*(-k2gz**2-k3gz*k1gz+k2gz*k3gz+k2gz*k1gz)+
                c2p*c2pm*(k1gz*k2gz+k3gz*k1gz+k3gz*k2gz+k2gz**2))
        
        delta1m = c3pp*c1p*(c2m*c2pp*(k2gz**2-k3gz*k2gz+k1gz*k2gz-k1gz*k3gz)+
                  c2p*c2pm*(-k2gz**2-k3gz*k2gz+k1gz*k3gz+k1gz*k2gz))
        
        delta2m = 2.*c3pp*c2pm*(k1gz*k2gz+k1gz*k3gz)
        
        delta2pm = 2.*c3pp*c2pp*(k1gz*k2gz-k1gz*k3gz)
        
        delta3m = 4.*k1gz*k2gz
        
        cmagp1 = delta1m/deltam
        cmag2 = delta2m/deltam
        cmagp2 = delta2pm/deltam
        cmag3 = delta3m/deltam
    
    ### --- Determination of the differents electric and magnetic field    
        if z<z_d:
            cphase1 = cmath.exp(1.0j*np.dot(k1,r))
            cphase1p = cmath.exp(1.0j*np.dot(k1p,r))
                
            if polar=='s':
                Ex = 0.
                Ey = cphase1+cep1*cphase1p
                Ez = 0.
                
                Bx = -cphase1*k1[2]/k0-(cep1*cphase1p*k1p[2]/k0)
                By = 0.
                Bz = cphase1*k1[0]/k0+(cep1*cphase1p*k1p[0]/k0)
                
            if polar=='p':
                Ex = n1*(-cphase1*k1[2]/(eps1*k0)-cmagp1*cphase1p*k1p[2]/(eps1*k0))
                Ey = 0.
                Ez = n1*(cphase1*k1[0]/(eps1*k0)+cmagp1*cphase1p*k1p[0]/(eps1*k0))
                
                Bx = 0.
                By = -cphase1-cmagp1*cphase1p
                Bz = 0.
                
        elif z_d<z<z_u:
            cphase2 = cmath.exp(1.0j*np.dot(k2,r))
            cphase2p = cmath.exp(1.0j*np.dot(k2p,r))
                
            if polar=='s':
                Ex = 0.
                Ey = ce2*cphase2+cep2*cphase2p
                Ez = 0.
                
                Bx = -ce2*cphase2*k2[2]/k0-cep2*cphase2p*k2p[2]/k0
                By = 0.
                Bz = ce2*cphase2*k2[0]/k0+cep2*cphase2p*k2p[0]/k0
            
            if polar=='p':
                Ex = n1*(-cmag2*cphase2*k2[2]/(eps2*k0)-cmagp2*cphase2p*k2p[2]/(eps2*k0))
                Ey = 0.
                Ez = n1*(cmag2*cphase2*k2[0]/(eps2*k0)+cmagp2*cphase2p*k2p[0]/(eps2*k0))
                
                Bx = 0.
                By = -cmag2*cphase2-cmagp2*cphase2p
                Bz = 0.
                
                
        else:
            cphase3 = cmath.exp(1.0j*np.dot(k3,r))
            
            if polar=='s':
                Ex = 0.
                Ey = ce3*cphase3
                Ez = 0.
               
                Bx = -ce3*cphase3*k3[2]/k0
                By = 0.
                Bz = ce3*cphase3*k3[0]/k0
            
            if polar=='p':
                Ex = n1*(-cmag3*cphase3*k3[2]/(eps3*k0))
                Ey = 0.
                # Ez = 1./n1*(cmag3*cphase3*k3[0]/(eps3*k0))  # <-- this was probably wrong
                Ez = n1*(cmag3*cphase3*k3[0]/(eps3*k0))
                
                Bx = 0.
                By = -cmag3*cphase3
                Bz = 0.
    
    return E0*Ex, E0*Ey, E0*Ez, E0*Bx, E0*By, E0*Bz


# =============================================================================
# interface to `_three_layer_pw`
# =============================================================================
def plane_wave(pos, env_dict, wavelength, 
               inc_angle=180, inc_plane='xz',
               theta=None,
               E_s=0.0, E_p=1.0, phase_Es=0.0, phase=0.0,
               returnField='E'):
    """generalized incident planewave
    
    supports oblique angles, arbitrary polarization states, 2 interfaces.
    Default config gives incident plane wave from top (z), 
    linear polarized along x, with amplitude 1
    
    Original code by Ch. Girard, python implementation by C. Majorel
    
    Parameters
    ----------
    pos : np.array
        list of 3-tuple coordinates to evaluate field at: [[x1,y1,z1], [x2,y2,z2], ... ]
    
    env_dict : dict
        Must be compatible with `sim.dyads.getConfigDictG` typed numba dict.
        description of environment. Must contain ['eps1', 'eps2', 'eps3', 'spacing'].
        
    wavelength : float
        Wavelength in nm
    
    inc_angle : float, default: 180
        incident angle with respect to e_z, in degrees. Default is inc from top.
         - 0deg = along Z (from neg to pos Z)
         - 90deg = along X ['xz'], along Y ['yz'] (from pos to neg)
         - 180deg = along Z  (from pos to neg Z)
         - 270deg = along X ['xz'], along Y ['yz'] (from neg to pos)
    
    inc_plane : str, default: 'xz'
        plane of incidence, one of ['xz', 'yz']
        
    theta : float, default: None
        alternative specification for a linear polarization angle. 
        If given, this will override `E_s` and `E_p` as well as their respective phases.
        In degrees. 
        At normal incidence: 0deg = OX, 90deg = OY.
        If `inc_plane`=='xz': 0deg --> p-polarization; 90deg --> s-polarization
        (inverse for `inc_plane`=='yz')
        
    
    E_s, E_p : float, default: 0.0, 1.0
        Apmplitudes of s-polarized and p-polarized plane wave components.
        At 0 / 180 degrees incident angle (normal incindence), 'p' is 
        polarized along x, 's' along y. Then, at 90deg 'p' is along z.
    
    phase_Es : float, default: 0.0
        additional phase for E_s component (in rad). 
        Can be used to generate elliptic polarization.
        For instance, left circular polarization (LCP) can be obtained with:
        E_s=np.sqrt(0.5), E_p=np.sqrt(0.5), phase_Es=np.pi/2. 
        RCP: phase_Es=-np.pi/2.
        
    phase : float, default: 0.0
        additional absolute phase for entire plane wave (in rad).
    
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B' or 'H': magnetic field
    
    Returns
    -------
      E0 (B0):       Complex E-(B-)Field at each dipole position as 
                    list of (complex) 3-tuples: [(Ex1, Ey1, Ez1), ...]
    """
    if ('eps1' not in env_dict.keys() or 'eps2' not in env_dict.keys() or
        'eps3' not in env_dict.keys() or 'spacing' not in env_dict.keys()):
        raise ValueError("`env_dict` must contain ['eps1', 'eps2', 'eps3', 'spacing']")
    
    cn1 = env_dict['eps1']**0.5
    cn2 = env_dict['eps2']**0.5
    cn3 = env_dict['eps3']**0.5
    spacing = np.float32(env_dict['spacing'].real)
    z_d = 0   # position of lower interface
    
    ## -- convert angles 90 and 270 close to horizontal angles to avoid divergence
    if inc_angle in [-90, 90, -270, 270] and (cn1!=cn2 or cn2!=cn3):
        warnings.warn("Using interface with horizontal angle of incidence!" + 
                      "Please make sure if horizontal incidence makes sense in presence of an interface.")    
    if inc_angle in [-90, 90]:
        inc_angle += 0.05
    if inc_angle in [-270, 270]:
        inc_angle -= 0.05
    
    
    Ex = np.asfortranarray( np.zeros(len(pos)), dtype=DTYPE_C)
    Ey = np.asfortranarray( np.zeros(len(pos)), dtype=DTYPE_C)
    Ez = np.asfortranarray( np.zeros(len(pos)), dtype=DTYPE_C)
    
    if theta is not None:
        if inc_angle not in [0, 180]: 
            warnings.warn("non-normal incident angle, to avoid ambiguities, " +
                          "the polarization of a plane wave should not be " +
                          "defined via the `theta` keyword.")
        E_p = 1.0 * np.cos(theta * np.pi/180.)
        E_s = 1.0 * np.sin(theta * np.pi/180.)
    
    for i,R in enumerate(pos):
        if inc_plane.lower() in ['yz', 'zy']:
            y,x,z = R
        else:
            x,y,z = R
    
        ex_s,ey_s,ez_s, bx_s,by_s,bz_s = _three_layer_pw(
            wavelength, inc_angle, 's', z_d, spacing, cn1, cn2, cn3, x, y, z, E0=E_s)
    
        ex_p,ey_p,ez_p, bx_p,by_p,bz_p = _three_layer_pw(
            wavelength, inc_angle, 'p', z_d, spacing, cn1, cn2, cn3, x, y, z, E0=E_p)
        
        ## additional phases:
        ex_p = ex_p * np.exp(1j * phase)
        ey_p = ey_p * np.exp(1j * phase)
        ez_p = ez_p * np.exp(1j * phase)
        bx_p = bx_p * np.exp(1j * phase)
        by_p = by_p * np.exp(1j * phase)
        bz_p = bz_p * np.exp(1j * phase)
        ex_s = ex_s * np.exp(1j * (phase_Es + phase))
        ey_s = ey_s * np.exp(1j * (phase_Es + phase))
        ez_s = ez_s * np.exp(1j * (phase_Es + phase))
        bx_s = bx_s * np.exp(1j * (phase_Es + phase))
        by_s = by_s * np.exp(1j * (phase_Es + phase))
        bz_s = bz_s * np.exp(1j * (phase_Es + phase))
        
        ## optional scattering plane modification
        if inc_plane.lower() in ['yz', 'zy']:
            ex_s,ey_s,ez_s = ey_s,ex_s,ez_s
            bx_s,by_s,bz_s = by_s,bx_s,bz_s
            ex_p,ey_p,ez_p = ey_p,ex_p,ez_p
            bx_p,by_p,bz_p = by_p,bx_p,bz_p
        
        if returnField.lower() == 'e':
            Ex[i], Ey[i], Ez[i] = ex_s+ex_p, ey_s+ey_p, ez_s+ez_p
        else:
            Ex[i], Ey[i], Ez[i] = bx_s+bx_p, by_s+by_p, bz_s+bz_p
        
    Evec = np.transpose([Ex, Ey, Ez])
    return Evec





    


def gaussian(pos, env_dict, wavelength, 
             theta=None, polarization_state=None, 
             xSpot=0.0, ySpot=0.0, zSpot=0.0, 
             NA=-1.0, spotsize=-1.0, kSign=-1.0, 
             paraxial=False, phase=0.0, returnField='E'):
    """Normal incident (along Z) Gaussian Beam Field
    
    obligatory "einKwargs" are one of 'theta' or 'polarization_state' and 
    one of 'NA' or 'spotsize'
    
    polarization is defined by one of the two kwargs:
     - theta: linear polarization angle in degrees, theta=0 --> along X. 
              Amplitude = 1 for both, E and B 
     - polarization_state. tuple (E0x, E0y, Dphi, phi): manually 
              define x and y amplitudes, phase difference and 
              absolute phase of plane wave.
    
    
    Parameters
    ----------
    pos : np.array
        list of 3-tuple coordinates to evaluate field at: [[x1,y1,z1], [x2,y2,z2], ... ]
    
    env_dict : dict
        Must be compatible with `sim.dyads.getConfigDictG` typed numba dict.
        description of environment. Must contain ['eps1', 'eps2', 'eps3', 'spacing'].
    
    wavelength : float
          Wavelength in nm
      
    theta : float, default: None
        either 'theta' or 'polarization_state' must be given.
        linear polarization angle in degrees, 0deg = 0X direction
    
    polarization_state : 4-tuple of float, default: None
        either 'theta' or 'polarization_state' must be given.
        polarization state with field amplitudes and phases, tuple of 4 float:
        (E0x, E0y, Dphi, Aphi): E0X amplitde, E0Y amplitde, phase difference 
        between X and Y components (in rad), absolute phase of plane wave (in rad).
        The field is then calculated as E = (E0x, E0y*exp(i*Dphi*z), 0)*exp(i*Aphi*z).
            Dphi : 
                - positive: left hand rotating polarization
                - negative: right hand rotating polarization 
                - example: left circular pol. with (E0x=1, E0y=1, Dphi=np.pi/2., phi=0)
        
      xSpot,ySpot,zSpot : float, default: 0,0,0
          x/y/z coordinates of focal point
      
      NA : float
          Numerical aperture to calculate beamwaist
      
      spotsize : float (optional)
          Gaussian beamwaist (overrides "NA")
      
      kSign : float, default: -1
          Direction of Beam. -1: top to Bottom, 1 Bottom to top
      
      paraxial : bool, default: False
          Use paraxial Gaussian beam: No longitudinal fields.
          If "False", longitudinal components are obtained using Maxwell 
          equation div(E)=0 as condition
         
      phase : float, default: 0
          additional phase of the beam, in degrees
      
      returnField : str, default: 'E'
          if 'E': returns electric field; if 'B' or 'H': magnetic field
    
    Returns
    -------
      E0:       Complex E-Field at each dipole position
      
    
    Notes
    -----
     - paraxial correction : 
         see: Novotny & Hecht. "Principles of nano-optics". Cambridge University Press (2006)

    
    """
    if (theta is None and polarization_state is None) or (theta is not None and polarization_state is not None):
        raise ValueError("exactly one argument of 'theta' and 'polarization_state' must be given.")
    if theta is not None:
        polarization_state = (1.0 * np.cos(theta * np.pi/180.), 
                              1.0 * np.sin(theta * np.pi/180.), 
                              0, 0)
    
    xm, ym, zm = np.transpose(pos)
    
    if 'eps_env' in env_dict.keys():
        cn1 = cn2 = env_dict['eps_env']**0.5
    else:
        cn1 = env_dict['eps1']**0.5
        cn2 = env_dict['eps2']**0.5
        cn3 = env_dict['eps3']**0.5
        # spacing = env_dict['spacing']**0.5
        if cn1 != cn2 or cn2 != cn3:
            warnings.warn("`gaussian` only supports vacuum environment so far. " +
                          "A simulation with interface might not yield correct results.")
    
    Ex = np.asfortranarray( np.zeros(len(xm)), dtype=DTYPE_C)
    Ey = np.asfortranarray( np.zeros(len(xm)), dtype=DTYPE_C)
    Ez = np.asfortranarray( np.zeros(len(xm)), dtype=DTYPE_C)
    
    
    ## beamwaist
    if spotsize == NA == -1:
        raise ValueError("Focused Beam Error! Either spotsize or NA must be given.")
    elif spotsize == -1:
        w0 = 2*wavelength/(NA*np.pi)
    else:
        w0 = spotsize
    
    ## waist, curvature and gouy-phase
    def w(z, zR, w0):
        return w0 * np.sqrt(1 + (z/zR)**2)
    
    def R(z, zR):
        return z*( 1 + (zR/z)**2 )
    
    def gouy(z, zR):
        return np.arctan2(z,zR)
    ## constant parameters
    E0 = complex(1,0)
    k = kSign*cn2 * (2*np.pi / wavelength)    #incidence from positive Z
    zR = np.pi*w0**2 / wavelength
    
    r2 = (xm-xSpot)**2+(ym-ySpot)**2
    z = zm-zSpot
    
    
    ## amplitude and polarization
    E0x = polarization_state[0]
    E0y = polarization_state[1]
    Dphi = polarization_state[2]
    Aphi = polarization_state[3]
    
    
    ##  --------- Electric field --------- 
    E = E0 * (w0/w(z,zR,w0) * 
            np.exp(-r2 / w(z,zR,w0)**2 ) * 
            np.exp(1j * (k*z + k*r2/(2*R(z,zR)) - gouy(z, zR)) )) * np.exp(1j*phase*np.pi/180.)
    
    if returnField.lower() == 'e':
        abs_phase = np.exp(1j * Aphi)     # add an absolute phase
        Ex = E * E0x * abs_phase
        Ey = E * E0y * np.exp(1j * Dphi) * abs_phase
    else:
    ##  --------- Magnetic field --------- 
        abs_phase = -1*np.exp(1j * Aphi)     # add an absolute phase
        Ex = -1*E * E0y*np.exp(1j * Dphi) * abs_phase
        Ey = E * E0x * abs_phase        
    
    ## obtained longitudinal component using condition div(E)==0
    if paraxial:
        Ez = np.zeros(len(E))   # <-- paraxial gaussian beam: No longitudinal E-component
    else:
        Ez = (-1j * 2 / (k * w(z,zR,w0)**2)) * \
                ((xm-xSpot) * Ex + (ym-ySpot) * Ey)
    
    Evec = np.transpose([Ex, Ey, Ez]).astype(DTYPE_C)
    return Evec




def dipole_electric(pos, env_dict, wavelength, 
                    x0,y0,z0, mx,my,mz, returnField='E', 
                    R_farfield_approx=-1):
    """field emitted by an electric dipole at (x0,y0,z0) with complex amplitude (mx,my,mz)
    
    mandatory kwargs along with `wavelength` are: `x0`, `y0`, `z0`, `mx`, `my`, `mz`
    
    To take into account a dielectric interface, `dipole_electric` uses a 
    mirror-charge approximation in the (quasistatic) near-field and an 
    asymptotic approximation for the far-field. Can handle only a single interface
    (hence cases with n1 != n2 = n3).
    
    
    Parameters
    ----------
    pos : np.array
        list of 3-tuple coordinates to evaluate field at: [[x1,y1,z1], [x2,y2,z2], ... ]
    
    env_dict : dict
        Must be compatible with `sim.dyads.getConfigDictG` typed numba dict.
        description of environment. Must contain either "eps_env" or ["eps1", "eps2"].
    
    wavelength : float
        Wavelength in nm
    
    x0,y0,z0 : float
        x/y/z coordinates of electric dipole position
          
    mx,my,mz : float
        x/y/z amplitude of elec. dipole vector
          
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B' or 'H': magnetic field
          
    R_farfield_approx : float, default: -1
        optional emitter-observer distance (in nm) starting from which an asymptotic 
        farfield approximation will be used (to be used with caution!).
        `-1`: Do not use far-field approximation. 
    
    Returns
    -------
    E0/H0:   Complex field at each position ( (Ex,Ey,Ez)-tuples )
    
    Notes
    -----
    
    for free-space propagators, see e.g. 
    G. S. Agarwal, *Phys. Rev. A*, 11(230), (1975), Eqs. (4.5)/(4.6)
    
    """
    from pyGDM2.propagators import Gtot_EE_123 as GEE
    from pyGDM2.propagators import Gs_EE_asymptotic as GEE_ff
    from pyGDM2.propagators import G_HE_123 as GHE
    
    if 'eps_env' in env_dict.keys():
        eps1 = eps2 = eps3 = env_dict['eps_env']
        spacing = 5000
    else:
        eps1 = env_dict['eps1']
        eps2 = env_dict['eps2']
        eps3 = env_dict['eps3']
        spacing = np.float32(env_dict['spacing'].real)
        if eps2 != eps3:
            warnings.warn("dipole_electric only supports a single interface " + 
                          "(between `n1`/`n2`). " +
                          "The simulation might not be a good approximation.")
    
    
    R1 = np.array([x0, y0, z0])  # emitter location
    p = np.array([mx, my, mz])   # emitter dipole moment
    
    Ex = np.zeros(len(pos), dtype=DTYPE_C)
    Ey = np.zeros(len(pos), dtype=DTYPE_C)
    Ez = np.zeros(len(pos), dtype=DTYPE_C)
    
    ## calc propagator
    for i,R2 in enumerate(pos):
        if returnField.lower() == 'e':
            ## --- emitted electric field
            if np.linalg.norm(R2-R1) <= R_farfield_approx or R_farfield_approx == -1:
                ## mirror-charge NF approximation
                xx, yy, zz, xy, xz, yx, yz, zx, zy \
                        = GEE(R1, R2, wavelength, eps1, eps2, eps3, spacing)
            else:
                ## asymptotic farfield approximation:
                xx, yy, zz, xy, xz, yx, yz, zx, zy \
                        = GEE_ff(R1, R2, wavelength, eps1, eps2, eps3, spacing)
                
        else:
            ## --- emitted magnetic field
            xx, yy, zz, xy, xz, yx, yz, zx, zy \
                    = GHE(R1, R2, wavelength, eps1, eps2, eps3, spacing)
        
        ## propagate the dipole
        G = np.array([[xx,xy,xz],
                      [yx,yy,yz],
                      [zx,zy,zz]])
        E = np.matmul(G, p)
        
        Ex[i] = E[0]
        Ey[i] = E[1]
        Ez[i] = E[2]
    
    return np.transpose([Ex, Ey, Ez])


def dipole_magnetic(pos, env_dict, wavelength, 
                    x0,y0,z0, mx,my,mz, returnField='E', 
                    R_farfield_approx=-1):
    """field emitted by a magnetic dipole at (x0,y0,z0) with complex amplitude (mx,my,mz)
    
    mandatory kwargs along with `wavelength` are: `x0`, `y0`, `z0`, `mx`, `my`, `mz`
    
    To take into account a dielectric interface, `dipole_magnetic` uses a 
    mirror-charge approximation in the (quasistatic) near-field and an 
    asymptotic approximation for the far-field. Can handle only a single interface
    (hence cases with n1 != n2 = n3).
    
    
    Parameters
    ----------
    pos : np.array
        list of 3-tuple coordinates to evaluate field at: [[x1,y1,z1], [x2,y2,z2], ... ]
    
    env_dict : dict
        Must be compatible with `sim.dyads.getConfigDictG` typed numba dict.
        description of environment. Must contain either "eps_env" or ["eps1", "eps2"].
    
    wavelength : float
        Wavelength in nm
    
    x0,y0,z0 : float
        x/y/z coordinates of electric dipole position
          
    mx,my,mz : float
        x/y/z amplitude of elec. dipole vector
          
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B' or 'H': magnetic field
          
    R_farfield_approx : float, default: -1
        optional emitter-observer distance (in nm) starting from which an asymptotic 
        farfield approximation will be used (to be used with caution!).
        `-1`: Do not use far-field approximation. 
    
    Returns
    -------
    E0/H0:   Complex field at each position ( (Ex,Ey,Ez)-tuples )
    
    Notes
    -----
    
    for free-space propagators, see e.g. 
    G. S. Agarwal, *Phys. Rev. A*, 11(230), (1975), Eqs. (4.5)/(4.6)
    
    """
    from pyGDM2.propagators import Gtot_EE_123 as GEE
    from pyGDM2.propagators import Gs_EE_asymptotic as GEE_ff
    from pyGDM2.propagators import G_HE_123 as GHE
    
    if 'eps_env' in env_dict.keys():
        eps1 = eps2 = eps3 = env_dict['eps_env']
        spacing = 5000
    else:
        eps1 = env_dict['eps1']
        eps2 = env_dict['eps2']
        eps3 = env_dict['eps3']
        spacing = np.float32(env_dict['spacing'].real)
        if eps2 != eps3:
            warnings.warn("dipole_electric only supports a single interface " + 
                          "(between `n1`/`n2`). " +
                          "The simulation might not be a good approximation.")
    
    
    R1 = np.array([x0, y0, z0])  # emitter location
    p = np.array([mx, my, mz])   # emitter dipole moment
    
    Ex = np.zeros(len(pos), dtype=DTYPE_C)
    Ey = np.zeros(len(pos), dtype=DTYPE_C)
    Ez = np.zeros(len(pos), dtype=DTYPE_C)
    
    ## calc propagator
    for i,R2 in enumerate(pos):
        if returnField.lower() == 'e':
            ## --- emitted electric field
            ## GEH(R1, R2) = GHE(R2, R1)
            xx, yy, zz, xy, xz, yx, yz, zx, zy \
                    = GHE(R2, R1, wavelength, eps1, eps2, eps3, spacing)
                
        else:
            ## --- emitted magnetic field
            ## GEE(R1, R2) = GHH(R1, R2)
            if np.linalg.norm(R2-R1) <= R_farfield_approx or R_farfield_approx == -1:
                ## mirror-charge NF approximation
                xx, yy, zz, xy, xz, yx, yz, zx, zy \
                        = GEE(R1, R2, wavelength, eps1, eps2, eps3, spacing)
            else:
                ## asymptotic farfield approximation:
                xx, yy, zz, xy, xz, yx, yz, zx, zy \
                        = GEE_ff(R1, R2, wavelength, eps1, eps2, eps3, spacing)
        
        ## propagate the dipole
        G = np.array([[xx,xy,xz],
                      [yx,yy,yz],
                      [zx,zy,zz]])
        E = np.matmul(G, p)
        
        Ex[i] = E[0]
        Ey[i] = E[1]
        Ez[i] = E[2]
    
    return np.transpose([Ex, Ey, Ez])



def fast_electron(pos, env_dict, wavelength, 
                  electron_kinetic_energy, x0, y0, 
                  kSign = -1, avoid_div_lim_distance=10.0,
                  returnField='E'):
    
    """Electric field created by a fast electron moving along (OZ) 
    
    The electron beam crosses the (OXY) plane in (x0, y0)
       
    Parameters
    ----------
    pos : np.array
        list of 3-tuple coordinates to evaluate field at: [[x1,y1,z1], [x2,y2,z2], ... ]
    
    env_dict : dict
        Must be compatible with `sim.dyads.getConfigDictG` typed numba dict.
        description of environment. Must contain either "eps_env" or ["eps1", "eps2"].
    
    wavelength : float
        Wavelength in nm
    
    electron_kinetic_energy : float
        electron kinetic energy (keV)
    
    x0, y0 : float
        position of the electron beam (nm)
    
    kSign : int, default: -1
        sign of wavenumber. 
        +1: electron propagation from bottom to top (towards increasing z)
        -1: electron propagation from top to bottom (towards smaller z, default)
        either kSign or k0 must be given.
    
    avoid_div_lim_distance : float, default: 10.0
        set a min. distance (in nm) between the location where the E-field 
        is computed and the electron trajectory to avoid divergence  
    
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B': magnetic field
    
    Returns
    -------
      E0 (B0):       Complex E-(B-)Field at each dipole position as 
                     list of (complex) 3-tuples: [(Ex1, Ey1, Ez1), ...]
    """
    from scipy import special
    
    if 'eps_env' in env_dict.keys():
        n2 = n2 = n3 = env_dict['eps_env']**0.5
    else:
        n1 = env_dict['eps1']**0.5
        n2 = env_dict['eps2']**0.5
        n3 = env_dict['eps3']**0.5
        # spacing = np.float32(env_dict['spacing'].real)
        if n2 != n3:
            warnings.warn("fast_electron only supports a single interface " + 
                          "(between `n1`/`n2`). " +
                          "The simulation might not be a good approximation.")
    
    ## constant parameters
    qe = 4.80321E-10     # elementary charge (Franklin)    
    Eo_el = 511.0        # electron rest mass (keV)	   
    c = 2.99792458E10    # Speed of light (cm/s)   

    gamma = 1. + electron_kinetic_energy/Eo_el  # Gamma = Lorentz factor
    f = np.sqrt(1.-1./gamma**2.)                # speed of electrons in units of c
    kz =  n2*(2.*np.pi/wavelength)            
    

    Ex = np.zeros(len(pos), dtype=DTYPE_C)
    Ey = np.zeros(len(pos), dtype=DTYPE_C)
    Ez = np.zeros(len(pos), dtype=DTYPE_C)
    for ipos, rp in enumerate(pos):
        xpos = rp[0] - x0
        ypos = rp[1] - y0   
        zpos = rp[2]    
        ##  --------- Electric field --------- 
        R = np.sqrt(xpos**2 + ypos**2)
        if (R > avoid_div_lim_distance):
            if returnField.lower() == 'e':
                U = kz*R / (f*gamma)
                phase = np.exp(1j*kSign*kz*zpos/f)
                factor = qe * kz * 1E7 / (np.pi * c * f**2. * gamma * n2**2.)
                Er = phase * factor * special.kv(1, U)
                Ex[ipos] = - Er * xpos/R
                Ey[ipos] = - Er * ypos/R
                Ez[ipos] = kSign*factor*1j * special.kv(0, U)/gamma
        ##  --------- Magnetic field --------- 
            else:
                ## !!! TODO
                raise NotImplementedError("fast-electron magnetic field not yet implemented.")
                
        else:
            Ex[ipos] = 0.0
            Ey[ipos] = 0.0
            Ez[ipos] = 0.0
    
    return np.transpose([Ex, Ey, Ez])





##----------------------------------------------------------------------
## deprecated functions for backwards compatibilitiy
##     (may be removed in future version)
##----------------------------------------------------------------------
def planewave(pos, env_dict, wavelength,
              theta=None, polarization_state=None, 
              kSign=-1, returnField='E', deprecationwarning=True, **kwargs):
    """Normally incident (along Z) planewave in homogeneous environment
    
    *DEPRECATED* - Use :func:`.plane_wave` instead.
    
    polarization is defined by one of the two kwargs:
     - theta: linear polarization angle in degrees, theta=0 --> along X. 
              Amplitude = 1 for both, E and B 
     - polarization state. tuple (E0x, E0y, Dphi, phi): manually 
              define x and y amplitudes, phase difference and 
              absolute phase of plane wave.
    
    Parameters
    ----------
    pos : np.array
        list of 3-tuple coordinates to evaluate field at: [[x1,y1,z1], [x2,y2,z2], ... ]
    
    env_dict : dict
        Must be compatible with `sim.dyads.getConfigDictG` typed numba dict.
        description of environment. Must contain either "eps_env" or ["eps2"].
    
    wavelength : float
        Wavelength in nm
    
    theta : float, default: None
        either 'theta' or 'polarization_state' must be given.
        linear polarization angle in degrees, 0deg = 0X direction.
    
    polarization_state : 4-tuple of float, default: None
        either 'theta' or 'polarization_state' must be given.
        polarization state with field amplitudes and phases, tuple of 4 float:
        (E0x, E0y, Dphi, Aphi): E0X amplitde, E0Y amplitde, phase difference 
        between X and Y components (in rad), absolute phase of plane wave (in rad).
        The field is then calculated as E = (E0x, E0y*exp(i*Dphi*z), 0)*exp(i*Aphi*z).
            Dphi : 
                - positive: left hand rotating polarization
                - negative: right hand rotating polarization 
                - example: left circular pol. with (1, 1, np.pi/2., 0)
    
    kSign : int, default: -1
        sign of wavenumber. 
        +1: propagation from bottom to top (towards increasing z)
        -1: propagation from top to bottom (towards smaller z, default)
        either kSign or k0 must be given.
    
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B' or 'H': magnetic field
    
    deprecationwarning : bool, default: True
        whether or not to emit a deprecation warning
    
    Returns
    -------
      E0 (B0):       Complex E-(B-)Field at each dipole position as 
                     list of (complex) 3-tuples: [(Ex1, Ey1, Ez1), ...]
    """
    ## --------- deprecation warning
    if deprecationwarning:
        warnings.warn("`planewave` is deprecated and supports only normal incidence/homogeneous environments. " +
                      "It is recommended to using `plane_wave` instead (with underscore in function name).",
                      DeprecationWarning)
    
    
    
    if (theta is None and polarization_state is None) or (theta is not None and polarization_state is not None):
        raise ValueError("exactly one argument of 'theta' and 'polarization_state' must be given.")
    
    if kSign not in [-1, 1]:
        raise ValueError("planewave: kSign must be either +1 or -1!")
    
    if 'eps_env' in env_dict.keys():
        cn1 = cn2 = env_dict['eps_env']**0.5
    else:
        cn1 = env_dict['eps1']**0.5
        cn2 = env_dict['eps2']**0.5
        cn3 = env_dict['eps3']**0.5
        if cn1 != cn3 or cn2 != cn3:
            warnings.warn("`planewave` only supports a homogeneous environment. " +
                          "The simulation will not be correct. " + 
                          "Consider using `plane_wave` or `evanescent_planewave`.")
    
    if theta is not None:
        polarization_state = (1.0 * np.cos(theta * np.pi/180.), 
                              1.0 * np.sin(theta * np.pi/180.), 
                              0, 0)
    
    xm, ym, zm = np.transpose(pos)
    
    ## constant parameters
    E0x = polarization_state[0]
    E0y = polarization_state[1]
    Dphi = polarization_state[2]
    Aphi = polarization_state[3]
    
    kz = kSign*cn2 * (2*np.pi / wavelength)    #incidence from positive Z
    
    ## amplitude and polarization
    ##  --------- Electric field --------- 
    E = np.ones((len(zm), 3), dtype=DTYPE_C)
    if returnField.lower() == 'e':
        abs_phase = np.exp(1j * (kz*zm + Aphi))     # absolute phase
        E.T[0] *= E0x * abs_phase
        E.T[1] *= E0y*np.exp(1j * Dphi) * abs_phase
        E.T[2] *= 0 * abs_phase
    ##  --------- Magnetic field --------- 
    else:
        abs_phase = -1*np.exp(1j * (kz*zm + Aphi))     # absolute phase
        E.T[0] *= -1*E0y*np.exp(1j * Dphi) * abs_phase
        E.T[1] *= E0x * abs_phase
        E.T[2] *= 0 * abs_phase
    
    return E
    

    
def focused_planewave(pos, env_dict, wavelength, 
                      theta=None, polarization_state=None, 
                      xSpot=0.0, ySpot=0.0, 
                      NA=-1.0, spotsize=-1.0, kSign=-1, phase=0.0,
                      consider_substrate_reflection=False, returnField='E'):
    """Normally incident (along Z) planewave with gaussian intensity profile
    
    *DEPRECATED* - Use :func:`.gaussian` instead.
    
    focused at (x0,y0)
    
    polarization is defined by one of the two kwargs:
      - theta: linear polarization angle in degrees, theta=0 --> along X. 
              Amplitude = 1 for both, E and B 
      - polarization state. tuple (E0x, E0y, Dphi, phi): manually 
              define x and y amplitudes, phase difference and 
              absolute phase of plane wave.
    
    Parameters
    ----------
    pos : np.array
        list of 3-tuple coordinates to evaluate field at: [[x1,y1,z1], [x2,y2,z2], ... ]
    
    env_dict : dict
        Must be compatible with `sim.dyads.getConfigDictG` typed numba dict.
        description of environment. Must contain either "eps_env" or ["eps2"].
    
    wavelength : float
        Wavelength in nm
    
    theta : float, default: None
        either 'theta' or 'polarization_state' must be given.
        linear polarization angle in degrees, 0deg = 0X direction
    
    polarization_state : 4-tuple of float, default: None
        either 'theta' or 'polarization_state' must be given.
        polarization state with field amplitudes and phases, tuple of 4 float:
        (E0x, E0y, Dphi, Aphi): E0X amplitde, E0Y amplitde, phase difference 
        between X and Y components (in rad), absolute phase of plane wave (in rad).
        The field is then calculated as E = (E0x, E0y*exp(i*Dphi*z), 0)*exp(i*Aphi*z).
            Dphi : 
                - positive: left hand rotating polarization
                - negative: right hand rotating polarization 
                - example: left circular pol. with (E0x=1, E0y=1, Dphi=np.pi/2., phi=0)
    
    xSpot, ySpot : float, float, default: 0, 0
        focal spot position (in nm)
    
    kSign : int, default: -1
        sign of wavenumber. 
        +1: propagation from bottom to top (towards increasing z)
        -1: propagation from top to bottom (towards smaller z, default)
       
    phase : float, default: 0
          additional phase of the beam, in degrees
          
    consider_substrate_reflection : bool, default: False
        Whether to consider the reflection / transmission coefficient at the
        substrate for adjusting the field amplitude
        
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B': magnetic field
    
    Returns
    -------
      E0 (B0):       Complex E-(B-)Field at each dipole position as 
                      list of (complex) 3-tuples: [(Ex1, Ey1, Ez1), ...]
    """
    ## --------- deprecation warning
    warnings.warn("`focuses_planewave` is deprecated. " +
                  "It is recommended to using `gaussian` instead .",
                  DeprecationWarning)
    
    
    E = planewave(pos, env_dict, wavelength, 
                  theta=theta, polarization_state=polarization_state, kSign=kSign, 
                  consider_substrate_reflection=consider_substrate_reflection, 
                  returnField=returnField, deprecationwarning=False)
    
    
    xm, ym, zm = np.transpose(pos)
    
    ## beamwaist
    if spotsize == NA == -1:
        raise ValueError("Focused Beam Error! Either spotsize or NA must be given.")
    elif spotsize == -1:
        w0 = 2*wavelength/(NA*np.pi)
    else:
        w0 = spotsize
    
    I_gaussian =  np.exp( -1.0 * (((xm-xSpot)**2 + (ym-ySpot)**2) / (w0**2)))
    
    E = np.prod([E.T,[I_gaussian]], axis=0).T
    
    return np.asfortranarray(E, dtype=DTYPE_C)



def evanescent_planewave(pos, env_dict, wavelength, 
                         theta_inc=0, polar='p', inc_plane='xz', 
                         returnField='E'):
    """oblique incident planewave, only linear polarization
    
    *DEPRECATED* - Use :func:`.plane_wave` instead.
    
    Oblique incidence (from bottom to top) through n1/n2/n3 layer interfaces. 
    May be used to simulate evanescent fields in the total internal 
    reflection configuration. Linear polarization.
    Amplitude = 1 for both, E and B.
    
    Original fortran code by Ch. Girard, python implementation by C. Majorel
    
    Parameters
    ----------
    pos : np.array
        list of 3-tuple coordinates to evaluate field at: [[x1,y1,z1], [x2,y2,z2], ... ]
    
    env_dict : dict
        Must be compatible with `sim.dyads.getConfigDictG` typed numba dict.
        description of environment. Must contain ['eps1', 'eps2', 'eps3', 'spacing'].
        
    wavelength : float
        Wavelength in nm
    
    theta_inc : float, default: 0
        incident angle in the XZ plane with respect to e_z, in degrees.
         - 0deg = along Z (from neg to pos Z)
         - 90deg = along X  (from pos to neg X)
         - 180deg = along Z  (from pos to neg Z)
         - 270deg = along X  (from neg to pos X)
    
    polar : str, default: 'p'
        incident linear polarization. Either 's' or 'p'. 
        At 0 / 180 degrees incident angle (normal incindence), 'p' is 
        polarized along x, 's' along y. Then, at 90deg 'p' is along z.
    
    inc_plane : str, default: 'xz'
        plane of incidence, one of ['xz', 'yz']
    
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B' or 'H': magnetic field
    
    Returns
    -------
      E0 (B0):       Complex E-(B-)Field at each dipole position as 
                    list of (complex) 3-tuples: [(Ex1, Ey1, Ez1), ...]
    """
    ## --------- deprecation warning
    warnings.warn("`evanescent_planewave` is deprecated. " +
                  "It is recommended to use `plane_wave` instead .",
                  DeprecationWarning)
    
    
    
    if polar.lower() not in ['s', 'p']:
        raise ValueError("'polar' must be either 's' or 'p'.")
        
    if ('eps1' not in env_dict.keys() or 'eps2' not in env_dict.keys() or
        'eps3' not in env_dict.keys() or 'spacing' not in env_dict.keys()):
        raise ValueError("`env_dict` must contain ['eps1', 'eps2', 'eps3', 'spacing']")
    
    z_d = 0   # position of lower interface
    
    cn1 = env_dict['eps1']**0.5
    cn2 = env_dict['eps2']**0.5
    cn3 = env_dict['eps3']**0.5
    spacing = np.float32(env_dict['spacing'].real)
    
    ## -- convert angles 90 and 270 close to horizontal angles to avoid divergence
    if theta_inc in [-90, 90, -270, 270] and (cn1!=cn2 or cn2!=cn3):
        warnings.warn("Using interface with horizontal angle of incidence!" + 
                      "Please make sure if horizontal incidence makes sense in presence of an interface.")    
    if theta_inc in [-90, 90]:
        theta_inc += 0.05
    if theta_inc in [-270, 270]:
        theta_inc -= 0.05
    
    
    Ex = np.asfortranarray( np.zeros(len(pos)), dtype=DTYPE_C)
    Ey = np.asfortranarray( np.zeros(len(pos)), dtype=DTYPE_C)
    Ez = np.asfortranarray( np.zeros(len(pos)), dtype=DTYPE_C)
    
    for i,R in enumerate(pos):
        if inc_plane.lower() in ['yz', 'zy']:
            y,x,z = R
        else:
            x,y,z = R
        ex,ey,ez, bx,by,bz = _three_layer_pw(wavelength, theta_inc, polar.lower(), 
                                             z_d, spacing, cn1, cn2, cn3, x, y, z)
        if inc_plane.lower() in ['yz', 'zy']:
            ex,ey,ez = ey,ex,ez
            bx,by,bz = by,bx,bz
        
        if returnField.lower() == 'e':
            Ex[i], Ey[i], Ez[i] = ex, ey, ez
        else:
            Ex[i], Ey[i], Ez[i] = bx, by, bz
        
    Evec = np.transpose([Ex, Ey, Ez])
    return Evec


FIELDS_LIST = [plane_wave, gaussian, 
               dipole_electric, dipole_magnetic,
               focused_planewave, fast_electron]

if __name__ == "__main__":
    pass
