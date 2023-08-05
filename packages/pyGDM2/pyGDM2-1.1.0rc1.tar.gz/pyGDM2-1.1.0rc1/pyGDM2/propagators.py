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
python implementations of the Green's Dyads, accelerated using `numba`
"""
from __future__ import print_function
from __future__ import absolute_import

import copy
import warnings

import numpy as np
import math
import cmath

import numba
# from numba import cuda

# =============================================================================
# Base `dyads` class
# =============================================================================
### --- dyad class 3D non-retarded
class DyadsBaseClass(object):
    """
    Bases: object
    
    Green's tensors container class - pure-python API
    
    Defines the frame of a linear GDM simulation via the Green's tensors,
    self-terms and material-polarizability relations.
    
    Parameters
    ----------
        
    dtype : (optional) `str`, default: 'f'
        precision ('f': float/single/32bit or 'd': double/64bit)
    
    """
    __name__ = "Base Green's tensors class"
    
    def __init__(self, dtype='f'):
        if dtype=='f':
            self.dtypef = np.float32
            self.dtypec = np.complex64
        else:
            self.dtypef = np.float64
            self.dtypec = np.complex128
    
        ## Dyads
        self.G_EE = self.notImplemented
        self.G_HE = self.notImplemented
        self.G_EE_ff = self.notImplemented
        
        ## repropagator routine
        self.repropagate = self.notImplemented
        
        ## coupling matrix constructor routines
        self.tsbs_EE = self.notImplemented
        self.tsbs_HE = self.notImplemented
        
    
    def __repr__(self):
        """description about simulation environment defined by set of dyads
        """
        out_str =  ' ------ NULL Tensors -------'
        return out_str
    
    
    def _legacyStructCompatibility(self, struct):
        if (self.n1_material is None or self.n2_material is None or 
            self.n3_material is None or self.spacing is None):
            ## !!! use `struct` object will be deprecated in the future!
            warnings.warn("Deprecation warning: " +
                          "Environment should be specified in the `dyads` object. " +
                          "Falling back to definition from `struct` class. " +
                          "This will raise an Exception in future versions of pyGDM.")
            if hasattr(struct, 'n1_material'):
                self.spacing = struct.spacing
                self.n1_material = struct.n1_material
                self.n2_material = struct.n2_material
                self.n3_material = struct.n3_material
            else:
                raise Exception("Structure does not contain environment definition. " +
                                "Please specify the environment in the Green's tensor class.")
    
    
    def notImplemented(self, *args, **kwargs):
        raise NotImplementedError("This feature is not implemented in this Green's tensor set.")
    
    
    def exceptionHandling(self, struct, efield):
        """Exception handling / consistency check for the set of tensors"""
        warnings.warn("Dummy exception handling. Should be implemented in child class.")
        return True
    
    
    def getConfigDictG(self, wavelength, struct, efield):
        """return numba typed-dict which is used by Green's tensor functions"""
        raise NotImplementedError("Definition missing! This function needs to be overridden in child class!")
    
    
    def getEnvironmentIndices(self, wavelength, geo):
        """return list of encironment permittivity at each meshpoint location"""
        raise NotImplementedError("Definition missing! This function needs to be overridden in child class!")
        
        
    def getSelfTermEE(self, wavelength, struct):
        """return list of 'EE' self-term tensors (3x3) at each meshpoint"""
        raise NotImplementedError("Definition missing! This function needs to be overridden in child class!")

        
    def getSelfTermHE(self, wavelength, struct):
        """return list of 'HE' self-term tensors (3x3) at each meshpoint"""
        raise NotImplementedError("Definition missing! This function needs to be overridden in child class!")
        
        
    def getPolarizabilityTensor(self, wavelength, struct):
        """return list of polarizability tensors (3x3) at each meshpoint"""
        raise NotImplementedError("Definition missing! This function needs to be overridden in child class!")


### --- non retarded 3D
# =============================================================================
# numba compatible propagators (CPU + CUDA), 3D
# =============================================================================
## --- free space propagator
@numba.njit(cache=True)
def _G0(R1, R2, wavelength, eps):
    """
    R1: dipole position
    R2: evaluation position
    """
    Dx = R2[0] - R1[0]
    Dy = R2[1] - R1[1]
    Dz = R2[2] - R1[2]
    lR = math.sqrt(Dx**2 + Dy**2 + Dz**2)
    
    k = 2*np.pi / wavelength
    cn = cmath.sqrt(eps)
    ck0 = 1j * k * cn
    k2 = k*k*eps
    
    r25 = math.pow((Dx*Dx+Dy*Dy+Dz*Dz), 2.5)
    r2 = math.pow((Dx*Dx+Dy*Dy+Dz*Dz), 2.0)
    r15 = math.pow((Dx*Dx+Dy*Dy+Dz*Dz), 1.5)
    
#!C-------------------------------------------------------------------
    T1XX = -1*(Dy*Dy+Dz*Dz) / r15
    T2XX = (2*Dx*Dx-Dy*Dy-Dz*Dz) / r2
    T3XX = (2*Dx*Dx-Dy*Dy-Dz*Dz) / r25
#!C-------------------------------------------------------------------
    T1XY = Dx*Dy / r15
    T2XY = 3*Dx*Dy / r2
    T3XY = 3*Dx*Dy / r25
#!C-------------------------------------------------------------------
    T1XZ = Dx*Dz / r15
    T2XZ = 3*Dx*Dz / r2
    T3XZ = 3*Dx*Dz / r25
#!C-------------------------------------------------------------------
    T1YY = -(Dx*Dx+Dz*Dz) / r15
    T2YY = (2*Dy*Dy-Dx*Dx-Dz*Dz) / r2
    T3YY = (2*Dy*Dy-Dx*Dx-Dz*Dz) / r25
#!C-------------------------------------------------------------------
    T1YZ = Dy*Dz / r15
    T2YZ = 3*Dy*Dz / r2
    T3YZ = 3*Dy*Dz / r25
#!C------------------------------------------------------------------
    T1ZZ = -(Dx*Dx+Dy*Dy) / r15
    T2ZZ = (2*Dz*Dz-Dx*Dx-Dy*Dy) / r2
    T3ZZ = (2*Dz*Dz-Dx*Dx-Dy*Dy) / r25
    
    CFEXP = cmath.exp(1j*k*cn*lR)
    
    
    ## setting up the tensor
    xx = CFEXP*(T3XX - ck0*T2XX - k2*T1XX) / eps
    yy = CFEXP*(T3YY - ck0*T2YY - k2*T1YY) / eps
    zz = CFEXP*(T3ZZ - ck0*T2ZZ - k2*T1ZZ) / eps
    
    xy = CFEXP*(T3XY - ck0*T2XY - k2*T1XY) / eps
    xz = CFEXP*(T3XZ - ck0*T2XZ - k2*T1XZ) / eps
    
    yz = CFEXP*(T3YZ - ck0*T2YZ - k2*T1YZ) / eps
        
    yx = xy
    zx = xz
    zy = yz
    
    return xx, yy, zz, xy, xz, yx, yz, zx, zy


@numba.njit(cache=True)
def _G0_HE(R1, R2, wavelength, eps):
    """
    R1: dipole position
    R2: evaluation position
    """
    # eps: environment index
    Dx = R2[0] - R1[0]
    Dy = R2[1] - R1[1]
    Dz = R2[2] - R1[2]
    lR2 = (Dx**2 + Dy**2 + Dz**2)
    
    k0 = 2*np.pi / wavelength
    k02n = cmath.sqrt(eps) * k0**2
#-----------------------------------------------------------------
    T2XY = Dz/lR2
    T3XY = Dz/lR2**1.5
#-----------------------------------------------------------------
    T2XZ = -Dy/lR2
    T3XZ = -Dy/lR2**1.5
#-----------------------------------------------------------------
    T2YZ = Dx/lR2
    T3YZ = Dx/lR2**1.5
#-----------------------------------------------------------------
    CFEXP = -1*cmath.exp(1j*k0*cmath.sqrt(eps)*math.sqrt(lR2))
    
    xx = 0
    yy = 0
    zz = 0
    
    xy = CFEXP * (1j*k0*T3XY + k02n*T2XY)
    xz = CFEXP * (1j*k0*T3XZ + k02n*T2XZ)
    yz = CFEXP * (1j*k0*T3YZ + k02n*T2YZ)

    yx = -xy
    zx = -xz
    zy = -yz
    
    return xx, yy, zz, xy, xz, yx, yz, zx, zy


## --- "1-2-3" slab propagator, via method of mirror charges for 2 surfaces
@numba.njit(cache=True)
def _G_mirrorcharge_123(R1, R2, wavelength, eps1, eps2, eps3, spacing):
    """
    R1: dipole position
    R2: evaluation position
    """
    Dx = R2[0] - R1[0]
    Dy = R2[1] - R1[1]
    Dz = R2[2] + R1[2]
    
    if R1[2] <= 0:
        cdelta12 = (eps2-eps1)/(eps1+eps2)
        cdelta23 = (eps3-eps2)/(eps3+eps2)
    elif spacing >= R1[2] > 0:
        cdelta12 = (eps1-eps2)/(eps1+eps2)
        cdelta23 = (eps3-eps2)/(eps3+eps2)
    elif R1[2] > spacing:
        cdelta12 = (eps1-eps2)/(eps1+eps2)
        cdelta23 = (eps2-eps3)/(eps3+eps2)
    
    
#!************* Interface: (1,2) *******************************
    r25 = math.pow((Dx*Dx+Dy*Dy+Dz*Dz), 2.5)
     
    SXX12 = cdelta12*(Dz*Dz+Dy*Dy-2*Dx*Dx) / r25
    SYY12 = cdelta12*(Dz*Dz+Dx*Dx-2*Dy*Dy) / r25
    SZZ12 = cdelta12*(2*Dz*Dz-Dx*Dx-Dy*Dy) / r25
    SXY12 = cdelta12*(-3*Dx*Dy) / r25
    SXZ12 = cdelta12*(3*Dx*Dz) / r25
    SYZ12 = cdelta12*(3*Dy*Dz) / r25

#!************* Interface: (2,3) *******************************
    GZ = Dz - 2*spacing
    rgz25 = math.pow((Dx*Dx+Dy*Dy+GZ*GZ), 2.5)
    
    SXX23 = cdelta23*(GZ*GZ+Dy*Dy-2*Dx*Dx) / rgz25
    SYY23 = cdelta23*(GZ*GZ+Dx*Dx-2*Dy*Dy) / rgz25
    SZZ23 = cdelta23*(2*GZ*GZ-Dx*Dx-Dy*Dy) / rgz25
    SXY23 = cdelta23*(-3*Dx*Dy) / rgz25
    SXZ23 = cdelta23*(3*Dx*GZ) / rgz25
    SYZ23 = cdelta23*(3*Dy*GZ) / rgz25
#!**************************************************************
    
    xx = (SXX12+SXX23)
    yy = (SYY12+SYY23)
    zz = (SZZ12+SZZ23)
    
    xy = (SXY12+SXY23)
    xz = (SXZ12+SXZ23)
    
    yx = xy
    yz = (SYZ12+SYZ23)
    
    zx = -xz
    zy = -yz
    
    return xx, yy, zz, xy, xz, yx, yz, zx, zy



## --- the full propagator: vacuum + surface term -- nearfield approximation!
##     assuming emitter in center layer, to calcualte resulting field anywhere
@numba.njit(cache=True)
def G0_EE_123(R1, R2, wavelength, eps1, eps2, eps3, spacing):
    """evaluate field of dipole emitter in 1-2-3 layer environment (NF approx.)
    
    R1: dipole position
    R2: evaluation position
    """
    if eps1==eps2 and eps2==eps3:
        eps = eps2
        scr_f = 1.0
    else:
        ## ----- emitter dipole situated in substrate layer ('eps1')
        if R1[2] < 0:
            ## field evaluated in bottom layer ("substrate")
            if R2[2] < 0:
                eps = eps1
                scr_f = 1.0
            ## field evaluated in center layer (same as emitter dipole)
            elif 0 <= R2[2] <= spacing:
                eps = eps2
                scr_f = eps * 2.0/(eps1+eps2)   # factor 'eps' to take 1/eps in G0 into account
            ## field evaluated in top cladding layer
            elif spacing < R2[2]:
                eps = eps3
                scr_f = eps * 2.0/(eps1+eps3)   # factor 'eps' to take 1/eps in G0 into account
        
        ## ----- emitter dipole situated in center layer ('eps2')
        if 0 <= R1[2] <= spacing:
            ## field evaluated in bottom layer ("substrate")
            if R2[2] < 0:
                eps = eps1
                scr_f = eps * 2.0/(eps1+eps2)   # factor 'eps' to take 1/eps in G0 into account
            ## field evaluated in center layer (same as emitter dipole)
            elif 0 <= R2[2] <= spacing:
                eps = eps2
                scr_f = 1.0
            ## field evaluated in top cladding layer
            elif spacing < R2[2]:
                eps = eps3
                scr_f = eps * 2.0/(eps2+eps3)   # factor 'eps' to take 1/eps in G0 into account
        
        ## ----- emitter dipole situated in top cladding layer ('eps3')
        if R1[2] > spacing:
            ## field evaluated in bottom layer ("substrate")
            if R2[2] < 0:
                eps = eps1
                scr_f = eps * 2.0/(eps1+eps3)   # factor 'eps' to take 1/eps in G0 into account
            ## field evaluated in center layer (same as emitter dipole)
            elif 0 <= R2[2] <= spacing:
                eps = eps2
                scr_f = eps * 2.0/(eps2+eps3)   # factor 'eps' to take 1/eps in G0 into account
            ## field evaluated in top cladding layer
            elif spacing < R2[2]:
                eps = eps3
                scr_f = 1.0
    
    ## ----- free space dyad
    xx, yy, zz, xy, xz, yx, yz, zx, zy = _G0(R1, R2, wavelength, eps)

    return scr_f*xx, scr_f*yy, scr_f*zz, \
           scr_f*xy, scr_f*xz, scr_f*yx, \
           scr_f*yz, scr_f*zx, scr_f*zy


@numba.njit(cache=True)
def Gs_EE_123(R1, R2, wavelength, eps1, eps2, eps3, spacing):
    """evaluate field of mirror-charge in 1-2-3 layer environment (NF approx.)
    
    R1: dipole position
    R2: evaluation position
    """
    xx, yy, zz, xy, xz, yx, yz, zx, zy = [np.complex64(0)]*9
    
    ## ----- actual interface present
    if eps1!=eps2 or eps2!=eps3:
        ## ----- emitter dipole situated in same layer as observer
        if ( (0 <= R1[2] <= spacing and 0 <= R2[2] <= spacing) or
             (R1[2] < 0 and R2[2] < 0) or 
             (R1[2] > spacing and R2[2] > spacing) ):
            ## mirror charges NF Green's tensor
            xx, yy, zz, xy, xz, yx, yz, zx, zy = _G_mirrorcharge_123(R1, R2, wavelength, 
                                                        eps1, eps2, eps3, spacing)

    return xx, yy, zz, xy, xz, yx, yz, zx, zy


@numba.njit(cache=True)
def Gtot_EE_123(R1, R2, wavelength, eps1, eps2, eps3, spacing):
# def G_EE_123(R1, R2, wavelength, conf_dict):
    """evaluate field of dipole emitter in 1-2-3 layer environment (NF approx.)
    
    R1: dipole position
    R2: evaluation position
    """
    ## ----- free space term
    xx, yy, zz, xy, xz, yx, yz, zx, zy = G0_EE_123(R1, R2, wavelength, 
                                                   eps1, eps2, eps3, spacing)
    
    ## ----- surface term
    xxs,yys,zzs,xys,xzs,yxs,yzs,zxs,zys = Gs_EE_123(R1, R2, wavelength, 
                                                    eps1, eps2, eps3, spacing)

    return xx + xxs, yy + yys, zz + zzs, \
           xy + xys, xz + xzs, yx + yxs, \
           yz + yzs, zx + zxs, zy + zys



@numba.njit(cache=True)
def G_HE_123(R1, R2, wavelength, eps1, eps2, eps3, spacing=0):
    """evaluate field of dipole emitter in 1-2-3 layer environment
    
    R1: dipole position
    R2: evaluation position
    """
    ## field evaluated in bottom layer ("substrate")
    if R2[2] < 0:
        eps = eps1
    ## field evaluated in center layer (same as emitter dipole)
    elif 0 <= R2[2] <= spacing:
        eps = eps2
    ## field evaluated in top cladding layer
    elif spacing <= R2[2]:
        eps = eps3
    
    ## ----- free space contribution
    xx, yy, zz, xy, xz, yx, yz, zx, zy = _G0_HE(R1, R2, wavelength, eps)
    
    return xx, yy, zz, xy, xz, yx, yz, zx, zy





### --- ff asymptotic 3D
# =============================================================================
# asymptotic propagators for far-field, 3D
# =============================================================================
@numba.njit(cache=True)
def _G0_EE_asymptotic(R1, R2, wavelength, eps2): 
    """Asymptotic vacuum Green's Dyad
    
    Parameters
    ----------
    R1 : np.array of 3 float
        dipole position [x,y,z]
    R2 : np.array of 3 float
        evaluation position
    wavelength : float
        emitter wavelength in nm
    eps1 : float, complex
        substrate permittivity
    """
    ## transform to spherical coordinates
    lR = np.linalg.norm(R2)
    theta = np.arccos(R2[2] / lR)
    phi = np.arctan2(R2[1], R2[0])
    
    if lR < wavelength:
        raise Exception("Distance too close. Trying to evaluate asymtpotic far-field dyad in the near-field region (R < wavelength).")
    
    ## wavenumber
    kvac = 2 * np.pi / wavelength                   # in vacuum
    k2 = 2 * np.pi * cmath.sqrt(eps2) / wavelength     # in surrounding medium of emitting dipole
    
    ## tensor prefactor
    A = ((kvac**2)*np.exp(1.0j*k2*lR)/lR * 
                      np.exp(-1.0j*k2*np.sin(theta) * 
                     (R1[0]*np.cos(phi) + R1[1]*np.sin(phi))) * 
                      np.exp(-1.0j*k2*np.cos(theta)*R1[2]))
    
    ## matrix elements
    S0_XX = A * (1.-np.sin(theta)**2*np.cos(phi)**2)
    S0_XY = A * (-np.sin(theta)**2*np.cos(phi)*np.sin(phi))
    S0_XZ = A * (-np.sin(theta)*np.cos(theta)*np.cos(phi))
    S0_YX = A * (-np.sin(theta)**2*np.cos(phi)*np.sin(phi))
    S0_YY = A * (1.-np.sin(theta)**2*np.sin(phi)**2)
    S0_YZ = A * (-np.sin(theta)*np.cos(theta)*np.sin(phi))
    S0_ZX = A * (-np.sin(theta)*np.cos(theta)*np.cos(phi))
    S0_ZY = A * (-np.sin(theta)*np.cos(theta)*np.sin(phi))
    S0_ZZ = A * (np.sin(theta)**2)
    
    return S0_XX, S0_YY, S0_ZZ, \
           S0_XY, S0_XZ, S0_YX, \
           S0_YZ, S0_ZX, S0_ZY


@numba.njit(cache=True, fastmath=True)
def Gs_EE_asymptotic(R1, R2, wavelength, eps1, eps2, eps3=0, spacing=0):
    """Asymptotic Green's Dyad for dipole above dielectric interface (inside eps2)
    
    Electric field propagator for electric dipole transition.
    
    In contrast to the nearfield propagators, this includes the vacuum contribution!
    
    Parameters
    ----------
    R1 : np.array of 3 float
        dipole position [x,y,z]
    R2 : np.array of 3 float
        evaluation position
    wavelength : float
        emitter wavelength in nm
    eps1 : float, complex
        substrate permittivity
    eps2 : float, complex
        emitter environment permittivity (above substrate)
    eps3, spacing : dummy parameters, ignored
    
    """
    ## transform to spherical coordinates
    lR = np.linalg.norm(R2)
    theta = np.arccos(R2[2] / lR)
    phi = np.arctan2(R2[1], R2[0])

    
    if lR < wavelength:
        raise Exception("Distance too close. Trying to evaluate asymtpotic far-field dyad in the near-field region (R < wavelength).")
    
    ## refractive index of media
    n1 = cmath.sqrt(eps1)
    n2 = cmath.sqrt(eps2)
    ## wavenumber
    kvac = 2 * np.pi / wavelength        # in vacuum
    k1 = 2 * np.pi * n1 / wavelength     # in substrate
    k2 = 2 * np.pi * n2 / wavelength     # in surrounding medium of emitting dipole
    
    ## workaround for positions too close to substrate
    if np.abs(np.cos(theta)) < 1E-10:
        theta -= np.sign(np.cos(theta))*0.001*np.pi
    
# =============================================================================
# Surface propagator above the surface
# =============================================================================
    if np.cos(theta) >= 0:
        ## tensor prefactors
        A0 = (kvac**2 * np.exp(1.0j*k2*lR) / lR * 
                              np.exp(-1.0j*k2*np.sin(theta) * 
                             (R1[0]*np.cos(phi) + R1[1]*np.sin(phi))))
        A_vac = A0 * np.exp(-1.0j*k2*np.cos(theta)*R1[2])
        A_up = -1 * A0 * np.exp(1.0j*k2*np.cos(theta)*R1[2])
        
        
        ## ------------------------------ vacuum contribution
        ## matrix elements
        S0_11 = A_vac * (1.-np.sin(theta)**2 * np.cos(phi)**2)
        S0_12 = A_vac * (-np.sin(theta)**2 * np.cos(phi) * np.sin(phi))
        S0_13 = A_vac * (-np.sin(theta) * np.cos(theta) * np.cos(phi))
        S0_21 = A_vac * (-np.sin(theta)**2 * np.cos(phi) * np.sin(phi))
        S0_22 = A_vac * (1.-np.sin(theta)**2 * np.sin(phi)**2)
        S0_23 = A_vac * (-np.sin(theta) * np.cos(theta) * np.sin(phi))
        S0_31 = A_vac * (-np.sin(theta) * np.cos(theta) * np.cos(phi))
        S0_32 = A_vac * (-np.sin(theta) * np.cos(theta) * np.sin(phi))
        S0_33 = A_vac * (np.sin(theta)**2)
        
        
        ## ------------------------------ surface contribution
        ## -- Fresnel coefficients
        r_p = ((eps1*n2*np.cos(theta) - eps2*cmath.sqrt(eps1 - eps2*np.sin(theta)**2)) /
               (eps1*n2*np.cos(theta) + eps2*cmath.sqrt(eps1 - eps2*np.sin(theta)**2)))
        
        r_s = ((n2*np.cos(theta) - cmath.sqrt(eps1 - eps2*np.sin(theta)**2)) /
               (n2*np.cos(theta) + cmath.sqrt(eps1 - eps2*np.sin(theta)**2)))
        
        ## -- matrix elements
        Sp11 = A_up * (r_p * np.cos(theta)**2 * np.cos(phi)**2 - r_s*np.sin(phi)**2)
        Sp12 = A_up * ((r_p * np.cos(theta)**2 + r_s) * np.sin(phi) * np.cos(phi))
        Sp13 = A_up * (r_p * np.cos(theta) * np.sin(theta) * np.cos(phi))
        Sp21 = Sp12
        Sp22 = A_up * (r_p * np.cos(theta)**2*np.sin(phi)**2 - r_s*np.cos(phi)**2)
        Sp23 = A_up * (r_p * np.cos(theta) * np.sin(theta) * np.sin(phi))
        Sp31 = -Sp13
        Sp32 = -Sp23
        Sp33 = A_up * (-r_p * np.sin(theta)**2)
        
        Sp11 += S0_11
        Sp12 += S0_12
        Sp13 += S0_13
        Sp21 += S0_21
        Sp22 += S0_22
        Sp23 += S0_23
        Sp31 += S0_31
        Sp32 += S0_32
        Sp33 += S0_33
    
        
# =============================================================================
# Surface propagator under the surface 
# =============================================================================
    else:
        ## -- coeff.
        D_eps_eff = cmath.sqrt(eps2 - eps1*np.sin(theta)**2)
        
        delta_s = ((-n1*np.cos(theta) - D_eps_eff)/
                   (-n1*np.cos(theta) + D_eps_eff))
        tau_s = 1. - delta_s
        phi_s = n1*tau_s / D_eps_eff 
        
        delta_p = ((-eps2*n1*np.cos(theta) - eps1*D_eps_eff)/
                   (-eps2*n1*np.cos(theta) + eps1*D_eps_eff))
        tau_p = delta_p + 1.
        phi_p = n1*tau_p * D_eps_eff
    
        A_low = ((kvac**2)*np.exp(1.0j*k1*lR) / lR*np.exp(-1.0j*k1*np.sin(theta)*
              (R1[0]*np.cos(phi) + R1[1]*np.sin(phi)))*np.exp(1.0j*kvac*D_eps_eff*R1[2]))
        
        ## -- matrix elements
        Sp11 = A_low * ((phi_p/eps2*np.cos(phi)**2 + phi_s*np.sin(phi)**2)*np.cos(theta))
        Sp12 = A_low * ((phi_p/eps2-phi_s)*np.cos(theta)*np.sin(phi)*np.cos(phi))
        Sp13 = A_low * (tau_p*eps1/eps2*np.cos(phi)*np.cos(theta)*np.sin(theta))
        Sp21 = A_low * ((phi_p/eps2-phi_s)*np.cos(theta)*np.sin(phi)*np.cos(phi))
        Sp22 = A_low * ((phi_p/eps2*np.sin(phi)**2 + phi_s*np.cos(phi)**2)*np.cos(theta))
        Sp23 = A_low * (tau_p*eps1/eps2*np.sin(phi)*np.cos(theta)*np.sin(theta))
        Sp31 = A_low * (-phi_p/eps2*np.sin(theta)*np.cos(phi))
        Sp32 = A_low * (-phi_p/eps2*np.sin(theta)*np.sin(phi))
        Sp33 = A_low * (-tau_p*eps1/eps2*np.sin(theta)**2)
    
    return Sp11, Sp22, Sp33, \
           Sp12, Sp13, Sp21, \
           Sp23, Sp31, Sp32





# =============================================================================
# ensemble-propagator routines
# =============================================================================
## --- multi-dipole / multi-probe propagator evaluation
@numba.njit(parallel=True)
def greens_tensor_evaluation(dp_pos, r_probe, G_func, wavelength, conf_dict, M, 
                             selfterm=np.zeros((3,3)).astype(np.complex64), 
                             dist_div_G=0.5):
    eps1 = conf_dict['eps1']
    eps2 = conf_dict['eps2']
    eps3 = conf_dict['eps3']
    spacing = np.float32(conf_dict['spacing'].real)
    
    for i in numba.prange(len(dp_pos)):   # explicit parallel loop
        _pos = dp_pos[i]
        for j in range(len(r_probe)):
            _r = r_probe[j]
            if np.sqrt((_r[0]-_pos[0])**2 + (_r[1]-_pos[1])**2 + (_r[2]-_pos[2])**2)<dist_div_G:
                xx, xy, xz = selfterm[0]
                yx, yy, yz = selfterm[1]
                zx, zy, zz = selfterm[2]
                # xx, yy, zz, xy, xz, yx, yz, zx, zy = selfterm
            else:
                xx, yy, zz, xy, xz, yx, yz, zx, zy = G_func(_pos, _r, wavelength, 
                                                            eps1, eps2, eps3, spacing)
            ## return list of Greens tensors
            M[i,j,0,0], M[i,j,1,1], M[i,j,2,2] = xx, yy, zz
            M[i,j,1,0], M[i,j,2,0], M[i,j,0,1] = yx, zx, xy
            M[i,j,2,1], M[i,j,0,2], M[i,j,1,2] = zy, xz, yz



### --- coupling matrix setup
@numba.njit(parallel=True, cache=True)
def t_sbs(geo, wavelength, cnorm, eps1, eps2, eps3, spacing, alpha, M):
    """for compatibility with old `core.scatter` implementation.
    
    was used in temporary pure-python API
    
    will be deprecated!
    """
    
    for i in numba.prange(len(geo)):    # explicit parallel loop
        R2 = geo[i]
        for j in range(len(geo)):
            R1 = geo[j]
            aj = alpha[j]
            
            ## --- vacuum dyad
            if i==j:
                ## self term
                xx, yy, zz = cnorm, cnorm, cnorm
                xy, xz = 0, 0
                yx, yz = 0, 0
                zx, zy = 0, 0
            else:
                xx, yy, zz, xy, xz, yx, yz, zx, zy = _G0(R1, R2, wavelength, eps2)
            
            
            ## --- 1-2-3 surface dyad (non retarded NF approximation)
            if eps1!=eps2 or eps2!=eps3:
                xxs,yys,zzs,xys,xzs,yxs,yzs,zxs,zys = _G_mirrorcharge_123(
                                 R1, R2, wavelength, eps1, eps2, eps3, spacing)
                
                ## combined dyad
                xx, yy, zz, xy, xz, yx, yz, zx, zy = xx+xxs, yy+yys, zz+zzs, \
                                                     xy+xys, xz+xzs, yx+yxs, \
                                                     yz+yzs, zx+zxs, zy+zys
            
            ## return invertible matrix:  delta_ij*1 - G[i,j] * alpha[j]
            M[3*i+0, 3*j+0] = -1*(xx*aj[0,0] + xy*aj[1,0] + xz*aj[2,0])
            M[3*i+1, 3*j+1] = -1*(yx*aj[0,1] + yy*aj[1,1] + yz*aj[2,1])
            M[3*i+2, 3*j+2] = -1*(zx*aj[0,2] + zy*aj[1,2] + zz*aj[2,2])
            M[3*i+0, 3*j+1] = -1*(xx*aj[0,1] + xy*aj[1,1] + xz*aj[2,1])
            M[3*i+0, 3*j+2] = -1*(xx*aj[0,2] + xy*aj[1,2] + xz*aj[2,2])
            M[3*i+1, 3*j+0] = -1*(yx*aj[0,0] + yy*aj[1,0] + yz*aj[2,0])
            M[3*i+1, 3*j+2] = -1*(yx*aj[0,2] + yy*aj[1,2] + yz*aj[2,2])
            M[3*i+2, 3*j+0] = -1*(zx*aj[0,0] + zy*aj[1,0] + zz*aj[2,0])
            M[3*i+2, 3*j+1] = -1*(zx*aj[0,1] + zy*aj[1,1] + zz*aj[2,1])
            
            if i==j:
                M[3*i+0, 3*j+0] += 1
                M[3*i+1, 3*j+1] += 1
                M[3*i+2, 3*j+2] += 1
                
                
@numba.njit(parallel=True, cache=True)
def t_sbs_EE_123_quasistatic(geo, wavelength, selfterms, alpha, conf_dict, M):
    eps1 = conf_dict['eps1']
    eps2 = conf_dict['eps2']
    eps3 = conf_dict['eps3']
    spacing = np.float32(conf_dict['spacing'].real)
    
    for i in numba.prange(len(geo)):    # explicit parallel loop
        R2 = geo[i]       # "observer"
        for j in range(len(geo)):
            R1 = geo[j]   # emitter
            aj = alpha[j]
            st = selfterms[j]
            ## --- vacuum dyad
            if i==j:
                ## self term
                xx, yy, zz = st[0,0], st[1,1], st[2,2]
                xy, xz, yx = st[0,1], st[0,2], st[1,0]
                yz, zx, zy = st[1,2], st[2,0], st[2,1]
            else:
                xx, yy, zz, xy, xz, yx, yz, zx, zy = G0_EE_123(R1, R2, wavelength, 
                                                                eps1, eps2, eps3, spacing)
            
            ## --- 1-2-3 surface dyad (non retarded NF approximation)
            if eps1!=eps2 or eps2!=eps3:
                xxs,yys,zzs,xys,xzs,yxs,yzs,zxs,zys = Gs_EE_123(
                                  R1, R2, wavelength, eps1, eps2, eps3, spacing)
                ## combined dyad
                xx, yy, zz, xy, xz, yx, yz, zx, zy = xx+xxs, yy+yys, zz+zzs, \
                                                      xy+xys, xz+xzs, yx+yxs, \
                                                      yz+yzs, zx+zxs, zy+zys
            
            ## return invertible matrix:  delta_ij*1 - G[i,j] * alpha[j]
            M[3*i+0, 3*j+0] = -1*(xx*aj[0,0] + xy*aj[1,0] + xz*aj[2,0])
            M[3*i+1, 3*j+1] = -1*(yx*aj[0,1] + yy*aj[1,1] + yz*aj[2,1])
            M[3*i+2, 3*j+2] = -1*(zx*aj[0,2] + zy*aj[1,2] + zz*aj[2,2])
            M[3*i+0, 3*j+1] = -1*(xx*aj[0,1] + xy*aj[1,1] + xz*aj[2,1])
            M[3*i+0, 3*j+2] = -1*(xx*aj[0,2] + xy*aj[1,2] + xz*aj[2,2])
            M[3*i+1, 3*j+0] = -1*(yx*aj[0,0] + yy*aj[1,0] + yz*aj[2,0])
            M[3*i+1, 3*j+2] = -1*(yx*aj[0,2] + yy*aj[1,2] + yz*aj[2,2])
            M[3*i+2, 3*j+0] = -1*(zx*aj[0,0] + zy*aj[1,0] + zz*aj[2,0])
            M[3*i+2, 3*j+1] = -1*(zx*aj[0,1] + zy*aj[1,1] + zz*aj[2,1])
            if i==j:
                M[3*i+0, 3*j+0] += 1
                M[3*i+1, 3*j+1] += 1
                M[3*i+2, 3*j+2] += 1


@numba.njit(parallel=True, cache=True)
# def t_sbs_HE_123_quasistatic(geo, wavelength, eps1, eps2, eps3, spacing, selfterms, alpha, M):
def t_sbs_HE_123_quasistatic(geo, wavelength, selfterms, alpha, conf_dict, M):
    eps2 = conf_dict['eps2']
    
    for i in numba.prange(len(geo)):    # explicit parallel loop
        R2 = geo[i]        # "observer"
        for j in range(len(geo)):
            R1 = geo[j]    # emitter
            aj = alpha[j]
            st = selfterms[j]
            ## --- vacuum dyad
            if i==j:
                ## self term
                xx, yy, zz = st[0,0], st[1,1], st[2,2]
                xy, xz, yx = st[0,1], st[0,2], st[1,0]
                yz, zx, zy = st[1,2], st[2,0], st[2,1]
            else:
                ## we need G^HE: H-field due to e-dipole
                xx, yy, zz, xy, xz, yx, yz, zx, zy = _G0_HE(R1, R2, wavelength, eps2)
            
            ## return: G[i,j] * alpha[j]
            ## --- magnetic-electric part
            M[3*i+0, 3*j+0] = -1*(xx*aj[0,0] + xy*aj[1,0] + xz*aj[2,0])
            M[3*i+1, 3*j+1] = -1*(yx*aj[0,1] + yy*aj[1,1] + yz*aj[2,1])
            M[3*i+2, 3*j+2] = -1*(zx*aj[0,2] + zy*aj[1,2] + zz*aj[2,2])
            M[3*i+0, 3*j+1] = -1*(xx*aj[0,1] + xy*aj[1,1] + xz*aj[2,1])
            M[3*i+0, 3*j+2] = -1*(xx*aj[0,2] + xy*aj[1,2] + xz*aj[2,2])
            M[3*i+1, 3*j+0] = -1*(yx*aj[0,0] + yy*aj[1,0] + yz*aj[2,0])
            M[3*i+1, 3*j+2] = -1*(yx*aj[0,2] + yy*aj[1,2] + yz*aj[2,2])
            M[3*i+2, 3*j+0] = -1*(zx*aj[0,0] + zy*aj[1,0] + zz*aj[2,0])
            M[3*i+2, 3*j+1] = -1*(zx*aj[0,1] + zy*aj[1,1] + zz*aj[2,1])




### --- dyad class 3D non-retarded
class DyadsQuasistatic123(DyadsBaseClass):
    __name__ = "3-layer environment: quasistatic 3D '1-2-3' Green's tensors"
    
    def __init__(self, n1=None, n2=None, n3=None, spacing=5000, 
                 radiative_correction=True):
        super().__init__()
        
        ## Dyads
        self.G_EE = Gtot_EE_123
        self.G_HE = G_HE_123
        self.G_EE_ff = Gs_EE_asymptotic
        
        ## evaluate propagator routine
        self.eval_G = greens_tensor_evaluation
        
        ## coupling matrix constructor routines
        self.tsbs_EE = t_sbs_EE_123_quasistatic
        self.tsbs_HE = t_sbs_HE_123_quasistatic
        
        ## environment definition
        ## set ref. index values or material class of environment layers
        from pyGDM2 import materials
        if isinstance(n1, (int, float, complex)) and not isinstance(n1, bool):
            self.n1_material = materials.dummy(n1)
        else:
            self.n1_material = n1
            
        n2 = n2 or n1     # if None, use `n1`
        if isinstance(n2, (int, float, complex)) and not isinstance(n2, bool):
            from pyGDM2 import materials
            self.n2_material = materials.dummy(n2)
        else:
            self.n2_material = n2
            
        n3 = n3 or n2     # if None, use `n2`
        if isinstance(n3, (int, float, complex)) and not isinstance(n3, bool):
            from pyGDM2 import materials
            self.n3_material = materials.dummy(n3)
        else:
            self.n3_material = n3
        
        self.spacing = spacing
        self.radiative_correction = radiative_correction
    
    def __repr__(self, verbose=False):
        """description about simulation environment defined by set of dyads
        """
        out_str =  ' ------ environment -------'
        out_str += '\n ' + self.__name__
        out_str += '\n '
        out_str += '\n' + '   n3 = {}  <-- top'.format(self.n3_material.__name__)
        out_str += '\n' + '   n2 = {}  <-- structure zone (height "spacing" = {}nm)'.format(
                        self.n2_material.__name__, self.spacing)
        out_str += '\n' + '   n1 = {}  <-- substrate'.format(self.n1_material.__name__)
        return out_str
    
    
    def exceptionHandling(self, struct, efield):
        """Exception handling / consistency check for the set of tensors
        
        check if structure and incident field generator are compatible

        Parameters
        ----------
        struct : :class:`.structures.struct`
            instance of structure class
        efield : :class:`.fields.efield`
            instance of incident field class

        Returns
        -------
        bool : True if struct and field are compatible, False if they don't fit the tensors

        """
        if len(struct.geometry) > 0:
            z_min = struct.geometry.T[2].min()
            z_max = struct.geometry.T[2].max()
            ## if interface 1/2 exists, check if entire structure is below or above
            if self.n1_material.__name__ != self.n2_material.__name__:
                if z_min<0 and z_max>0:
                    warnings.warn("Structure in-between substrate and middle-layer. " +
                                  "This is not supported and will most likely falsify the simulation.")
            
            ## if interface 2/3 exists, check if entire structure is below or above
            if self.n2_material.__name__ != self.n3_material.__name__:
                if z_min<self.spacing and z_max>self.spacing:
                    warnings.warn("Structure in-between middle and top cladding layer. " +
                                  "This is not supported and will most likely falsify the simulation.")
            
        return True
    
    
    def getConfigDictG(self, wavelength, struct, efield):
        ## all data need to be same dtype, must be cast to correct type inside numba functions
        conf_dict = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                                           value_type=numba.types.complex64)
        
        conf_dict['eps1'] = np.complex64(self.n1_material.epsilon(wavelength))
        conf_dict['eps2'] = np.complex64(self.n2_material.epsilon(wavelength))
        conf_dict['eps3'] = np.complex64(self.n3_material.epsilon(wavelength))
        conf_dict['spacing'] = np.complex64(self.spacing)
        
        ## return a numba typed dictionary of "complex64" type,
        ## can be used to pass configuration to the green's functions
        return conf_dict
    
    
    def getEnvironmentIndices(self, wavelength, geo):
        """get environment permittivity for `wavelength` at each meshpoint"""
        self.n1 = self.n1_material.epsilon(wavelength)**0.5
        self.n2 = self.n2_material.epsilon(wavelength)**0.5
        self.n3 = self.n3_material.epsilon(wavelength)**0.5
        
        ## environment epsilon at every meshpoint
        eps_env = np.zeros(len(geo), dtype=self.dtypec)
        eps_env[geo.T[2].min() > self.spacing] = self.n3_material.epsilon(wavelength)
        eps_env[0 <= geo.T[2].min() <= self.spacing] = self.n2_material.epsilon(wavelength)
        eps_env[geo.T[2].min() < 0] = self.n1_material.epsilon(wavelength)
        
        return eps_env
        
        
    def getSelfTermEE(self, wavelength, struct):
        eps_env = self.getEnvironmentIndices(wavelength, struct.geometry)
        struct.setWavelength(wavelength)
        
        k0 = 2.0*np.pi / float(wavelength)
        
        if struct.normalization == 0:
            cnorm = np.zeros(len(eps_env))
        else:
            norm_nonrad = -4.0 * np.pi * struct.normalization / (3.0 * struct.step**3 * eps_env)
            
            if self.radiative_correction:
                norm_rad = 1j * 2.0 * struct.normalization * (k0**3)/3.0 * np.ones(len(norm_nonrad))
                cnorm = norm_nonrad + norm_rad
            else:
                cnorm = norm_nonrad
        
        self_term_tensors_EE = np.zeros([len(norm_nonrad), 3, 3], dtype=self.dtypec)
        self_term_tensors_EE[:,0,0] = cnorm
        self_term_tensors_EE[:,1,1] = cnorm
        self_term_tensors_EE[:,2,2] = cnorm
        
        return self_term_tensors_EE
        
    
    def getSelfTermHE(self, wavelength, struct):
        eps_env = self.getEnvironmentIndices(wavelength, struct.geometry)
        struct.setWavelength(wavelength)
        
        self_term_tensors_HE = np.zeros([len(eps_env), 3, 3], dtype=self.dtypec)
        
        return self_term_tensors_HE
        
        
    def getPolarizabilityTensor(self, wavelength, struct):
        eps_env = self.getEnvironmentIndices(wavelength, struct.geometry)
        struct.setWavelength(wavelength)
        normalization = struct.normalization
        eps = struct.epsilon_tensor 
        
        vcell_norm = struct.step**3 / float(normalization)
        
        eps_env_tensor = np.zeros(eps.shape, dtype=self.dtypec)
        eps_env_tensor[:,0,0] = eps_env
        eps_env_tensor[:,1,1] = eps_env
        eps_env_tensor[:,2,2] = eps_env
        
        ## --- isotropic polarizability
        alphatensor = np.asfortranarray((eps - eps_env_tensor) * 
                                      vcell_norm / (4.0 * np.pi), dtype=self.dtypec)
        
        return alphatensor





