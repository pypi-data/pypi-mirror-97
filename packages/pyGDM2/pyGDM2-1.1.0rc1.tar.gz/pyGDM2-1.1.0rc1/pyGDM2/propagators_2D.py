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

## bessel functions to calc. hankel functions (required for 2D green tensor)
# import numba_scipy
from scipy.special import jv, yv
from scipy.special import iv, kv

from pyGDM2 import propagators



#==============================================================================
# globals
#==============================================================================
DTYPE_C = np.complex64


# =============================================================================
#               numba overloads for Bessel functions
#
# adapted for scipy>=1.4 from https://github.com/numba/numba-scipy
#
# =============================================================================
import ctypes
import scipy.special
from numba.extending import get_cython_function_address


## -- in future: add binding to complex hankel
## double complex hankel1(double, double complex)

name_to_numba_signatures = {
    'yv': [(numba.types.float64, numba.types.float64,), (numba.types.long_, numba.types.float64,)],
    'jv': [(numba.types.float64, numba.types.float64,), (numba.types.long_, numba.types.float64,)],
    
    'iv': [(numba.types.float64, numba.types.float64,), (numba.types.long_, numba.types.float64,)],
    'kv': [(numba.types.float64, numba.types.float64,), (numba.types.long_, numba.types.float64,)],
    }

name_and_types_to_pointer = {
    ('yv', numba.types.float64, numba.types.float64): ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double)(get_cython_function_address('scipy.special.cython_special', '__pyx_fuse_1yv')),
    ('jv', numba.types.float64, numba.types.float64): ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double)(get_cython_function_address('scipy.special.cython_special', '__pyx_fuse_1jv')),
    
    ('iv', numba.types.float64, numba.types.float64): ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double)(get_cython_function_address('scipy.special.cython_special', '__pyx_fuse_1iv')),
    ('kv', numba.types.float64, numba.types.float64): ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double)(get_cython_function_address('scipy.special.cython_special', '__pyx_fuse_1kv')),
    }

def choose_kernel(name, all_signatures):
    def choice_function(*args):
        for signature in all_signatures:
            if args == signature:
                f = name_and_types_to_pointer[(name, *signature)]
                return lambda *args: f(*args)
    return choice_function

def add_overloads():
    for name, all_signatures in name_to_numba_signatures.items():
        sc_function = getattr(scipy.special, name)
        numba.extending.overload(sc_function)(
            choose_kernel(name, all_signatures)
        )

add_overloads()



### --- non retarded 2D
# =============================================================================
# propagators for infinitely long dipole line, 2D
# 
# The 2D Green's tensors implementation is based on fortran code 
# written by G. Colas des Francs
#   
# requires numba-scipy (pip install numba-scipy)
# =============================================================================
@numba.njit()
def _numba_hankel1(n, x):
    ## numba-compatible first kind hankel functions
    ## only scipy-bessel functions are numba-compatible (via `numba-scipy` package)
    ## numba binding supports only real arguments so far (as of March 2020)
    
    ## purely real argument: Use Bessel functions
    if np.imag(x) == 0:
        Jn = jv(n, np.real(x))
        Yn = yv(n, np.real(x))
    
    ## purely imaginary argument: Use modified Bessel functions (first kind: I, second kind: K)
    elif np.real(x) == 0:
        ## identities: (modif. Bessel first kind: I, second kind: K)
        ## Jn(1j*z) = exp(n*1j*np.pi/2) * In(z)
        ## Jn(1j*z) = (j^n) * In(z)
        ## Yn(1j*z) = exp((n+1)*1j*np.pi/2) * In(z) - 2/np.pi * exp(-1*n*1j*np.pi/2) * Kn(z)
        Jn = (1j**n) * iv(n, np.imag(x))
        Yn = cmath.exp((n+1)*1j*np.pi/2) * iv(n, np.imag(x)) - \
              2/np.pi * cmath.exp(-1*n*1j*np.pi/2) * kv(n, np.imag(x))
        
    ## 'mixed' complex argument: not possible with numba
    else:
        raise Exception("2D Greens tensor calculation: " +
                        "Numba-hankel functions support only purely real / purely imaginary argument.")
    
    h1n = Jn + 1j*Yn
    return h1n


@numba.njit()
def _s0_2D(Dx, Dz, wavelength, eps, ky0=0):
    ## the actual free space dyad calculation via dipole<-->observation distance
    eps = np.real(eps)   # numba bessel support only real arguments
    
    k0 = 2*np.pi / wavelength
    k02 = k0**2
    ## only real epsilon supported!
    kr = cmath.sqrt(eps * k02 - ky0**2)
    
    lR = math.sqrt(Dx**2 + Dz**2)
    if lR < 0.01:
       lR = 0.0
       raise ValueError("Points too close. Diverging free-space 2D Green's Tensor!")
    
    cop = Dx / lR
    sip = Dz / lR
    co2p = 2. * cop**2 - 1.0
    si2p = 2. * cop*sip
    
    h01 = _numba_hankel1(0.0, kr*lR)
    h11 = _numba_hankel1(1.0, kr*lR)
    h21 = _numba_hankel1(2.0, kr*lR)
    
    gxx = ( (k02 - kr**2 / (2.0*eps)) * h01 +
             kr**2 * co2p * h21 / (2.0*eps) )
    gxy = -1j * kr * ky0 * cop * h11 / eps
    gxz = (kr**2 * si2p)*h21 / (2.0*eps)  
    
    gyx = gxy
    gyy = (k02 - ky0**2/eps) * h01   
    gyz = -1j * kr * ky0 * sip * h11 / eps     
    
    gzx = gxz
    gzy = gyz
    gzz = ( (k02 - kr**2 / (2.0*eps)) * h01 -
             kr**2 * co2p * h21 / (2.0*eps) )
    
    ## cgs!
    return 1j*np.pi*gxx, 1j*np.pi*gyy, 1j*np.pi*gzz, \
           1j*np.pi*gxy, 1j*np.pi*gxz, 1j*np.pi*gyx, \
           1j*np.pi*gyz, 1j*np.pi*gzx, 1j*np.pi*gzy
    ## SI: *1/(4 pi)


    
@numba.njit()      
def _G0_2D(R1, R2, wavelength, eps, ky0=0):
    ## ky0=0.0: so far incidence || XZ plane
    
    Dx = R2[0] - R1[0]
    Dz = R2[2] - R1[2]
    # lR = math.sqrt(Dx**2 + Dz**2)
    
    return _s0_2D(Dx, Dz, wavelength, eps, ky0)


## 1-2-3 surface dyad via image-charge approximation
@numba.njit()
def _G_mirrorcharge_123_2D(R1, R2, wavelength, eps1, eps2, eps3, spacing, ky0=0.0):
    Dx = R2[0] - R1[0]
    
    ## init propagator variables
    sxx123, syy123, szz123, sxy123, sxz123, \
           syx123, syz123, szx123, szy123 = np.zeros(9, dtype=np.complex64)
    
    ## interface 1-2, evaluate only if present
    if eps1 != eps2:
        ## mirror charge z position 
        Dz12 = R2[2] + R1[2]
        
        if R1[2] <= 0:
            eps_dipole1 = eps2
            cdelta12 = (eps2-eps1)/(eps1+eps2)
        elif spacing >= R1[2] > 0:
            eps_dipole1 = eps1
            cdelta12 = (eps1-eps2)/(eps1+eps2)
        elif R1[2] > spacing:
            eps_dipole1 = eps1
            cdelta12 = (eps1-eps2)/(eps1+eps2)
        
        ## propagator
        sxx, syy, szz, sxy, sxz, \
              syx, syz, szx, szy = _s0_2D(Dx, Dz12, wavelength, eps_dipole1, ky0)
        sxx123 += -1*cdelta12 * sxx
        syy123 += -1*cdelta12 * syy
        szz123 += +1*cdelta12 * szz
        sxy123 += -1*cdelta12 * sxy
        sxz123 += -1*cdelta12 * sxz
        syx123 += -1*cdelta12 * syx
        syz123 += -1*cdelta12 * syz
        szx123 += -1*cdelta12 * szx
        szy123 += -1*cdelta12 * szy
        
    ## interface 2-3, evaluate only if present
    if eps2 != eps3:
        ## mirror charge z position 
        Dz23 = R2[2] + R1[2] - 2*spacing
        
        if R1[2] <= 0:
            eps_dipole2 = eps3
            cdelta23 = (eps3-eps2)/(eps3+eps2)
        elif spacing >= R1[2] > 0:
            eps_dipole2 = eps3
            cdelta23 = (eps3-eps2)/(eps3+eps2)
        elif R1[2] > spacing:
            eps_dipole2 = eps2
            cdelta23 = (eps2-eps3)/(eps3+eps2)
            
        ## propagator
        sxx, syy, szz, sxy, sxz, \
              syx, syz, szx, szy = _s0_2D(Dx, Dz23, wavelength, eps_dipole2, ky0)
        sxx123 += -1*cdelta23 * sxx
        syy123 += -1*cdelta23 * syy
        szz123 += +1*cdelta23 * szz
        sxy123 += -1*cdelta23 * sxy
        sxz123 += -1*cdelta23 * sxz
        syx123 += -1*cdelta23 * syx
        syz123 += -1*cdelta23 * syz
        szx123 += -1*cdelta23 * szx
        szy123 += -1*cdelta23 * szy
        
    return sxx123, syy123, szz123, \
           sxy123, sxz123, syx123, \
           syz123, szx123, szy123
    

@numba.njit()
def _G0_HE_2D(R1, R2, wavelength, eps, ky0=0):
    ## the actual free space dyad calculation via dipole<-->observation distance
    eps = np.real(eps)   # numba bessel support only real arguments
    Dx = R2[0] - R1[0]
    Dz = R2[2] - R1[2]
    
    k0 = 2*np.pi / wavelength
    k02 = k0**2
    ## only real epsilon supported!
    kr = cmath.sqrt(eps * k02 - ky0**2)
    
    lR = math.sqrt(Dx**2 + Dz**2)
    if lR < 0.01:
       lR = 0.0
       raise ValueError("Points too close. Diverging free-space 2D Green's Tensor!")
    
    if ky0 != 0:
        h01 = _numba_hankel1(0.0, kr*lR)
    else:
        h01 = 0
    h11 = _numba_hankel1(1.0, kr*lR)
    
    phase_y = np.exp(1j * ky0 * R2[1])
    
    gxy = k0 * np.pi * h11 * (kr / lR) * Dz * phase_y
    gxz = 1j * np.pi * k0 * ky0 * h01 * phase_y
    gyz = k0 * np.pi * h11 * (kr / lR) * Dx * phase_y
    
    gyx = -gxy
    gzx = -gxz
    gzy = -gyz
    
    gxx = 0
    gyy = 0
    gzz = 0
    
    return gxx, gyy, gzz, \
           gxy, gxz, gyx, \
           gyz, gzx, gzy



## --- the full propagator: vacuum + surface term -- nearfield approximation!
##     assuming emitter in center layer, to calcualte resulting field anywhere
@numba.njit()
def G0_EE_123_2D(R1, R2, wavelength, eps1, eps2, eps3, spacing, ky0=0):
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
            elif R2[2] > spacing:
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
            elif R2[2] > spacing:
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
            elif R2[2] > spacing:
                eps = eps3
                scr_f = 1.0
    
    ## ----- free space dyad
    xx, yy, zz, xy, xz, yx, yz, zx, zy = _G0_2D(R1, R2, wavelength, eps, ky0)

    return scr_f*xx, scr_f*yy, scr_f*zz, \
           scr_f*xy, scr_f*xz, scr_f*yx, \
           scr_f*yz, scr_f*zx, scr_f*zy


@numba.njit()
def Gs_EE_123_2D(R1, R2, wavelength, eps1, eps2, eps3, spacing, ky0=0):
    """evaluate field of mirror-charge in 1-2-3 layer environment (NF approx.)
    
    R1: dipole position
    R2: evaluation position
    """
    xx, yy, zz, xy, xz, yx, yz, zx, zy = [np.complex64(0)]*9
    
    ## ----- actual interface present
    if eps1!=eps2 or eps2!=eps3:
        ## mirror charges NF Green's tensor
        xx, yy, zz, xy, xz, yx, yz, zx, zy = _G_mirrorcharge_123_2D(R1, R2, wavelength, 
                                                    eps1, eps2, eps3, spacing, ky0)

    return xx, yy, zz, xy, xz, yx, yz, zx, zy


@numba.njit()
def Gtot_EE_123_2D(R1, R2, wavelength, eps1, eps2, eps3, spacing, ky0=0):
    """evaluate field of dipole emitter in 1-2-3 layer environment (NF approx.)
    
    R1: dipole position
    R2: evaluation position
    """
    ## ----- free space term
    xx, yy, zz, xy, xz, yx, yz, zx, zy = G0_EE_123_2D(R1, R2, wavelength, 
                                                   eps1, eps2, eps3, spacing, ky0)
    
    ## ----- surface term
    xxs,yys,zzs,xys,xzs,yxs,yzs,zxs,zys = Gs_EE_123_2D(R1, R2, wavelength, 
                                                    eps1, eps2, eps3, spacing, ky0)

    return xx + xxs, yy + yys, zz + zzs, \
           xy + xys, xz + xzs, yx + yxs, \
           yz + yzs, zx + zxs, zy + zys

# @numba.njit()
# def G_EE_123_2D(R1, R2, wavelength, eps1, eps2, eps3, spacing, ky0=0.0):
#     """TODO: G0+Gs, conditions for source / observation position"""
#     ## ky0=0.0: so far incidence || XZ plane
#     xx, yy, zz, xy, xz, yx, yz, zx, zy = _G0_2D(R1, R2, wavelength, eps2)
    
#     xxs,yys,zzs,xys,xzs,yxs,yzs,zxs,zys = _Gs123_2D(R1, R2, wavelength, eps1, eps2, eps3, spacing)
    
#     ## dummy screening factor
#     scr_f = 1.0
#     return scr_f*xx + xxs, scr_f*yy + yys, scr_f*zz + zzs, \
#            scr_f*xy + xys, scr_f*xz + xzs, scr_f*yx + yxs, \
#            scr_f*yz + yzs, scr_f*zx + zxs, scr_f*zy + zys



@numba.njit()
def G_HE_123_2D(R1, R2, wavelength, eps1, eps2, eps3, spacing, ky0=0.0):
    """TODO: G0+Gs, conditions for source / observation position"""
    ## ky0=0.0: so far incidence || XZ plane. Should be added to parameters
    
    ## field evaluated in bottom layer ("substrate")
    if R2[2] < 0:
        eps = eps1
    ## field evaluated in center layer (same as emitter dipole)
    elif 0 <= R2[2] <= spacing:
        eps = eps2
    ## field evaluated in top cladding layer
    elif spacing <= R2[2]:
        eps = eps3
        
    xx, yy, zz, xy, xz, yx, yz, zx, zy = _G0_HE_2D(R1, R2, wavelength, eps, ky0)
    
    ## dummy screening factor
    return xx, yy, zz, \
           xy, xz, yx, \
           yz, zx, zy


# =============================================================================
# ensemble-propagator routines
# =============================================================================
## --- multi-dipole field propagation
@numba.njit(parallel=True)
def greens_tensor_evaluation_2D(dp_pos, r_probe, G_func, wavelength, conf_dict, M,
                                selfterm=np.zeros((3,3)).astype(np.complex64), 
                                dist_div_G=0.5):
    eps1 = conf_dict['eps1']
    eps2 = conf_dict['eps2']
    eps3 = conf_dict['eps3']
    spacing = np.float32(conf_dict['spacing'].real)
    ky0 = np.float32(conf_dict['ky0'].real)
    
    for i in numba.prange(len(dp_pos)):   # explicit parallel loop
        _pos = dp_pos[i]
        for j in range(len(r_probe)):
            _r = r_probe[j]
            if np.sqrt((_r[0]-_pos[0])**2 + (_r[1]-_pos[1])**2 + (_r[2]-_pos[2])**2)<dist_div_G:
                xx, xy, xz = selfterm[0]
                yx, yy, yz = selfterm[1]
                zx, zy, zz = selfterm[2]
            else:
                xx, yy, zz, xy, xz, yx, yz, zx, zy = G_func(_pos, _r, wavelength, 
                                                            eps1, eps2, eps3, spacing, ky0)
            ## return list of Greens tensors
            M[i,j,0,0], M[i,j,1,1], M[i,j,2,2] = xx, yy, zz
            M[i,j,1,0], M[i,j,2,0], M[i,j,0,1] = yx, zx, xy
            M[i,j,2,1], M[i,j,0,2], M[i,j,1,2] = zy, xz, yz




### --- coupling matrix setup
@numba.njit(parallel=True)
def t_sbs_EE_123_2D(geo, wavelength, selfterms, alpha, conf_dict, M):
    eps1 = conf_dict['eps1']
    eps2 = conf_dict['eps2']
    eps3 = conf_dict['eps3']
    spacing = np.float32(conf_dict['spacing'].real)
    ky0 = np.float32(conf_dict['ky0'].real)    
    
# =============================================================================
#     SBS coupling-matrix setup with 2d propagators
# =============================================================================
    for i in numba.prange(len(geo)):    # explicit parallel loop
        R2 = geo[i]
        for j in range(len(geo)):
            R1 = geo[j]
            aj = alpha[j]
            st = selfterms[j]
            ## --- vacuum dyad
            if i==j:
                ## self term
                xx, yy, zz = st[0,0], st[1,1], st[2,2]
                xy, xz, yx = st[0,1], st[0,2], st[1,0]
                yz, zx, zy = st[1,2], st[2,0], st[2,1]
            else:
                xx, yy, zz, xy, xz, yx, yz, zx, zy = G0_EE_123_2D(R1, R2, wavelength, 
                                                       eps1, eps2, eps3, spacing, ky0)
            
            ## --- 1-2-3 surface dyad (non retarded NF approximation)
            if eps1!=eps2 or eps2!=eps3:
                xxs,yys,zzs,xys,xzs,yxs,yzs,zxs,zys = Gs_EE_123_2D(
                            R1, R2, wavelength, eps1, eps2, eps3, spacing, ky0)
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

@numba.njit(parallel=True)
def t_sbs_HE_123_2D(geo, wavelength, selfterms, alpha, conf_dict, M):
    eps2 = conf_dict['eps2']
    ky0 = np.float32(conf_dict['ky0'].real)
    
    for i in numba.prange(len(geo)):    # explicit parallel loop
        R2 = geo[i]        # "observer"
        for j in numba.prange(len(geo)):
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
                xx, yy, zz, xy, xz, yx, yz, zx, zy = _G0_HE_2D(R1, R2, wavelength, eps2, ky0)
            
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




### --- dyad class 2D non-retarded
class DyadsQuasistatic2D123(propagators.DyadsBaseClass):
    __name__ = "3-layer environment: Quasistatic 2D '1-2-3' Green's tensors"
    
    def __init__(self, n1=None, n2=None, n3=None, spacing=5000, ky0=None):
        super().__init__()
        
        ## Dyads
        self.G_EE = Gtot_EE_123_2D   # !!! todo: test the 1-2-3 interface tensor
        self.G_HE = G_HE_123_2D
        self.G_EE_ff = Gtot_EE_123_2D   # !!! todo: 2d-ff propagator here
        
        ## evaluate propagator routine
        self.eval_G = greens_tensor_evaluation_2D
        
        ## coupling matrix constructor routines
        self.tsbs_EE = t_sbs_EE_123_2D
        self.tsbs_HE = t_sbs_HE_123_2D
        
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
        self.ky0 = ky0
        
    def __repr__(self, verbose=False):
        """description about simulation environment defined by set of dyads"""
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
        from pyGDM2 import fields_py
        if efield.field_generator not in [fields_py.planewave, 
                                          fields_py.evanescent_planewave,
                                          fields_py.plane_wave,
                                          field_dipole_line_2d]:
            raise Exception("Incompatible incident field. "+
                            "2D Dyads are only compatible with fields `plane_wave` and `planewave`.")
        
        all_inc_angles = []
        for k in efield.kwargs_permutations:
            if 'inc_plane' in k.keys():
                if k['inc_plane'].lower() in ['yz', 'zy'] and 'theta_inc' in k.keys():
                    all_inc_angles.append(k['theta_inc'])
            if 'ky0' in k.keys():
                all_inc_angles.append(k['ky0'])
        if len(np.unique(all_inc_angles)) > 1:
            raise Exception("2D simulations can treat only a single incident angle in the 'YZ' plane" + 
                            " (k_y!=0). Please use multiple simulations instead.")
        if len(np.unique(all_inc_angles)) == 1 and self.ky0 is not None:
            warnings.warn("'ky' is defined in Dyad but also an oblique incidence is used. "+
                          "The oblique incidence will be overridden, "+
                          "leading to potentially incorrect results.")
        
        if np.abs(struct.geometry.T[1].max()) != 0:
            raise Exception("2D structure meshpoints must be in the plane Y=0.")
        
        if struct.normalization != 1:
            raise Exception("2D supports so far only cubic mesh.")
            
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
        from pyGDM2 import fields
        conf_dict = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                                           value_type=numba.types.complex64)
        
        conf_dict['eps1'] = np.complex64(self.n1_material.epsilon(wavelength))
        conf_dict['eps2'] = np.complex64(self.n2_material.epsilon(wavelength))
        conf_dict['eps3'] = np.complex64(self.n3_material.epsilon(wavelength))
        conf_dict['spacing'] = np.complex64(self.spacing)
        
        if self.ky0 is not None:
            conf_dict['ky0'] = np.complex64(self.ky0)
        elif efield.field_generator.__name__ == fields.plane_wave.__name__:
            if 'inc_plane' in efield.kwargs_permutations[0].keys():
                if efield.kwargs_permutations[0]['inc_plane'].lower() in ['yz', 'zy']:
                    
                    ## k-vector component parallel to y
                    inc_angle = np.pi * efield.kwargs_permutations[0]['inc_angle'] / 180.0
                    n2 = (self.n2_material.epsilon(wavelength)**0.5)
                    k_y = np.sin(inc_angle) * 2*np.pi * np.sqrt(n2**2) / wavelength
                    conf_dict['ky0'] = np.complex64(k_y)
                else:
                    conf_dict['ky0'] = np.complex64(0) # ky=0 --> inc. normal to XY plane
            else:
                conf_dict['ky0'] = np.complex64(0) # ky=0 --> inc. normal to XY plane
        elif efield.field_generator.__name__ == fields.planewave.__name__:
            conf_dict['ky0'] = np.complex64(0) # ky=0 --> inc. normal to XY plane
        elif efield.field_generator.__name__ == field_dipole_line_2d.__name__:
            if 'ky0' in efield.kwargs_permutations[0].keys():
                conf_dict['ky0'] = np.complex64(efield.kwargs_permutations[0]['ky0'])
            else:
                conf_dict['ky0'] = np.complex64(0)
        else:
            raise ValueError("2D-incompatible incident field.")
        
        ## return a numba typed dictionary of "complex64" type,
        ## can be used to pass configuration to the green's functions
        return conf_dict
    
    
    def getEnvironmentIndices(self, wavelength, geo):
        """set environment layers refractive index at 'wavelength'"""
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
        k02 = k0**2
        
        if struct.normalization == 0:
            norm_xz = 0
            norm_y = 0
        else:
            from scipy.special import hankel1
            ky0 = 0    # no y-component of wavevector supported so far
            kr = np.sqrt(eps_env*k02 - ky0**2)
            h11 = hankel1(1, kr*struct.step/np.sqrt(np.pi))
            norm01 = (struct.step/np.sqrt(np.pi) * h11/kr + 2j / (np.pi*kr**2))
            
            norm_xz_nonrad = -1 * struct.normalization / (2.0 * struct.step**2 * eps_env)
            norm_y_nonrad = 0
            norm_xz_rad = 1j*np.pi * (2*k02 - kr**2/eps_env) * \
                               norm01 / (4*struct.step**2)
            norm_y_rad =  1j*np.pi * (k02 - ky0**2/eps_env) * \
                               norm01 / (2*struct.step**2)
                           
            norm_xz = 4.0 * np.pi * (norm_xz_nonrad + norm_xz_rad)
            norm_y = 4.0 * np.pi * (norm_y_nonrad + norm_y_rad)
        
        
        self_term_tensors_EE = np.zeros([len(eps_env), 3, 3], dtype=struct.dtypec)
        self_term_tensors_EE[:,0,0] = norm_xz
        self_term_tensors_EE[:,1,1] = norm_y
        self_term_tensors_EE[:,2,2] = norm_xz
        
        return self_term_tensors_EE
        
    
    def getSelfTermHE(self, wavelength, struct):
        struct.setWavelength(wavelength)
        eps_env = self.getEnvironmentIndices(wavelength, struct.geometry)
        self_term_tensors_HE = np.zeros([len(eps_env), 3, 3], dtype=self.dtypec)
        
        return self_term_tensors_HE
        
        
    def getPolarizabilityTensor(self, wavelength, struct):
        eps_env = self.getEnvironmentIndices(wavelength, struct.geometry)
        struct.setWavelength(wavelength)
        eps = struct.epsilon_tensor 
        
        S_cell_norm = struct.step**2 / float(struct.normalization)
        
        eps_env_tensor = np.zeros(eps.shape, dtype=self.dtypec)
        eps_env_tensor[:,0,0] = eps_env
        eps_env_tensor[:,1,1] = eps_env
        eps_env_tensor[:,2,2] = eps_env
        
        ## --- isotropic polarizability
        alphatensor = np.asfortranarray((eps - eps_env_tensor) * 
                                      S_cell_norm / (4.0 * np.pi), dtype=self.dtypec)
        
        return alphatensor


### --- dipole-line incident field
def field_dipole_line_2d(pos, env_dict, wavelength, 
                    x0,z0, mx,my,mz, ky0=0,
                    dp_type="electric", returnField='E', 
                    R_farfield_approx=9000):
    """field emitted by a 2D dipole line at (x0,z0) with complex amplitude (mx,my,mz)
    
    The dipole line is infinitely long in y-direction
    
    mandatory kwargs along with `wavelength` are: `x0`, `z0`, `mx`, `my`, `mz`
    
    To take into account a dielectric interface, a quasistatic
    mirror-charge approximation is used
    
    
    Parameters
    ----------
    pos : np.array
        list of 3-tuple coordinates to evaluate field at: [[x1,y1,z1], [x2,y2,z2], ... ]
    
    env_dict : dict
        Must be compatible with `sim.dyads.getConfigDictG` typed numba dict.
        description of environment. Must contain either "eps_env" or ["eps1", "eps2", "eps3", "spacing""]. 
    
    wavelength : float
        Wavelength in nm
    
    x0,z0 : float
        dipole-line position
          
    mx,my,mz : float
        x/y/z amplitude of elec. dipole vector
    
    ky0 : float, default: 0
        parallel wavevector component of emitter-line
    
    dp_type : str, default: "electric"
        type of dipole emitter: "electric" or "magnetic"
    
    returnField : str, default: 'E'
        if 'E': returns electric field; if 'B' or 'H': magnetic field
          
    Returns
    -------
    E0/H0:   Complex field at each position ( (Ex,Ey,Ez)-tuples )
    
    Notes
    -----
    
    for 2D free-space propagators, see e.g. 
    Martin & Piller
    *Electromagnetic scattering in polarizable backgrounds*
    Phys. Rev. E 58, 3909–3915 (1998)
    
    """
    
    if 'eps_env' in env_dict.keys():
        eps1 = eps2 = eps3 = env_dict['eps_env']
        spacing = 5000
    else:
        eps1 = env_dict['eps1']
        eps2 = env_dict['eps2']
        eps3 = env_dict['eps3']
        spacing = np.float32(env_dict['spacing'].real)
    
    
    R1 = np.array([x0, 0, z0])  # emitter location
    p = np.array([mx, my, mz])   # emitter dipole moment
    
    Ex = np.zeros(len(pos), dtype=DTYPE_C)
    Ey = np.zeros(len(pos), dtype=DTYPE_C)
    Ez = np.zeros(len(pos), dtype=DTYPE_C)
    
    ## calc propagator
    for i, R2 in enumerate(pos):
        if np.linalg.norm(R1-R2)<0.01:
            warnings.warn("Divergence of Green's tensor in line-dipole field: Evaluation position too close to dipole line. Field is set to zero.")
            xx, yy, zz, xy, xz, yx, yz, zx, zy = [np.complex64(0)]*9
        else:
            if ((dp_type.lower()=="electric" and returnField.lower() == 'e') or 
                (dp_type.lower()=="magnetic" and returnField.lower() == 'h')):
                ## --- emitted electric field
                ## mirror-charge NF approximation
                xx, yy, zz, xy, xz, yx, yz, zx, zy \
                        = Gtot_EE_123_2D(R1, R2, wavelength, eps1, eps2, eps3, spacing, ky0=ky0)
            else:
                ## --- emitted magnetic field (or electric field by m-dipole)
                xx, yy, zz, xy, xz, yx, yz, zx, zy \
                        = G_HE_123_2D(R1, R2, wavelength, eps1, eps2, eps3, spacing, ky0=ky0)
        
        ## propagate the dipole
        G = np.array([[xx,xy,xz],
                      [yx,yy,yz],
                      [zx,zy,zz]])
        E = np.matmul(G, p)
        
        Ex[i] = E[0]
        Ey[i] = E[1]
        Ez[i] = E[2]
    
    return np.transpose([Ex, Ey, Ez])



