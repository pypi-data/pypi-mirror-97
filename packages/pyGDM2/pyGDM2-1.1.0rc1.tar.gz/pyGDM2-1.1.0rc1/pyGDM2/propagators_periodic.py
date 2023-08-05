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

from pyGDM2 import propagators


### --- 3D periodic Dyads - until now homogeneous environment only, normal incidence only
@numba.njit(cache=True)
def G0_periodic_123(R1, R2, wavelength, 
                    eps1=1.0+0j, eps2=1.0+0j, eps3=1.0+0j, spacing=5000, 
                    k_x=0.0, N_u=0, N_v=0, 
                    u=np.array([0., 0., 0.]), v=np.array([0., 0., 0.])):
    xx = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    yy = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    zz = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    xy = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    xz = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    yx = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    yz = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    zx = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    zy = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    
    for u_i in numba.prange(-N_u, N_u+1):
        for v_i in numba.prange(-N_v, N_v+1):
            _R1 = R1 + u*u_i + v*v_i     # position of emitter-copy from periodic cell [u_i, v_i]
            _xx, _yy, _zz, _xy, _xz, _yx, _yz, _zx, _zy = propagators.G0_EE_123(
                    _R1, R2, wavelength, eps1, eps2, eps3, spacing)
            xx[u_i, v_i] = _xx
            yy[u_i, v_i] = _yy
            zz[u_i, v_i] = _zz
            xy[u_i, v_i] = _xy
            xz[u_i, v_i] = _xz
            yx[u_i, v_i] = _yx
            yz[u_i, v_i] = _yz
            zx[u_i, v_i] = _zx
            zy[u_i, v_i] = _zy
    
    return np.sum(xx), np.sum(yy), np.sum(zz), \
           np.sum(xy), np.sum(xz), np.sum(yx), \
           np.sum(yz), np.sum(zx), np.sum(zy)


@numba.njit(cache=True)
def Gs_periodic_123(R1, R2, wavelength, 
                    eps1=1.0+0j, eps2=1.0+0j, eps3=1.0+0j, spacing=5000, 
                    k_x=0.0, N_u=0, N_v=0, 
                    u=np.array([0., 0., 0.]), v=np.array([0., 0., 0.])):
    xx = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    yy = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    zz = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    xy = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    xz = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    yx = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    yz = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    zx = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    zy = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    
    for u_i in numba.prange(-N_u, N_u+1):
        for v_i in numba.prange(-N_v, N_v+1):
            _R1 = R1 + u*u_i + v*v_i     # position of emitter-copy from periodic cell [u_i, v_i]
            _xx, _yy, _zz, _xy, _xz, _yx, _yz, _zx, _zy = propagators.Gs_EE_123(
                    _R1, R2, wavelength, eps1, eps2, eps3, spacing)
            xx[u_i, v_i] = _xx
            yy[u_i, v_i] = _yy
            zz[u_i, v_i] = _zz
            xy[u_i, v_i] = _xy
            xz[u_i, v_i] = _xz
            yx[u_i, v_i] = _yx
            yz[u_i, v_i] = _yz
            zx[u_i, v_i] = _zx
            zy[u_i, v_i] = _zy
    
    return np.sum(xx), np.sum(yy), np.sum(zz), \
           np.sum(xy), np.sum(xz), np.sum(yx), \
           np.sum(yz), np.sum(zx), np.sum(zy)


@numba.njit(cache=True)
def Gtot_periodic_123(R1, R2, wavelength, 
                      eps1=1.0+0j, eps2=1.0+0j, eps3=1.0+0j, spacing=5000, 
                      k_x=0.0, N_u=0, N_v=0, 
                      u=np.array([0., 0., 0.]), v=np.array([0., 0., 0.])):
    ## ----- free space term
    xx, yy, zz, xy, xz, yx, yz, zx, zy = G0_periodic_123(R1, R2, wavelength, 
                                eps1, eps2, eps3, spacing, k_x, N_u, N_v, u, v)
    
    ## ----- surface term
    xxs,yys,zzs,xys,xzs,yxs,yzs,zxs,zys = Gs_periodic_123(R1, R2, wavelength, 
                                eps1, eps2, eps3, spacing, k_x, N_u, N_v, u, v)

    return xx + xxs, yy + yys, zz + zzs, \
           xy + xys, xz + xzs, yx + yxs, \
           yz + yzs, zx + zxs, zy + zys


@numba.njit(cache=True)
def G_HE_periodic(R1, R2, wavelength, 
                    eps1=1.0+0j, eps2=1.0+0j, eps3=1.0+0j, spacing=5000, 
                    k_x=0.0, N_u=0, N_v=0, 
                    u=np.array([0., 0., 0.]), v=np.array([0., 0., 0.])):
    xx = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    yy = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    zz = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    xy = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    xz = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    yx = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    yz = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    zx = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    zy = np.zeros((N_u*2 + 1, N_v*2 + 1), dtype=np.complex64)
    
    for u_i in numba.prange(-N_u, N_u+1):
        for v_i in numba.prange(-N_v, N_v+1):
            _R1 = R1 + u*u_i + v*v_i     # position of emitter-copy from periodic cell [u_i, v_i]
            ## additional phase, use x-component of wave-vector --> incidence in XZ plane!
            exp_term_k_x = np.exp(1j* k_x * (u*u_i + v*v_i)[0])
            _xx, _yy, _zz, _xy, _xz, _yx, _yz, _zx, _zy = propagators.G_HE_123(
                    _R1, R2, wavelength, eps1, eps2, eps3, spacing)
            xx[u_i, v_i] = _xx * exp_term_k_x
            yy[u_i, v_i] = _yy * exp_term_k_x
            zz[u_i, v_i] = _zz * exp_term_k_x
            xy[u_i, v_i] = _xy * exp_term_k_x
            xz[u_i, v_i] = _xz * exp_term_k_x
            yx[u_i, v_i] = _yx * exp_term_k_x
            yz[u_i, v_i] = _yz * exp_term_k_x
            zx[u_i, v_i] = _zx * exp_term_k_x
            zy[u_i, v_i] = _zy * exp_term_k_x
    
    return np.sum(xx), np.sum(yy), np.sum(zz), \
           np.sum(xy), np.sum(xz), np.sum(yx), \
           np.sum(yz), np.sum(zx), np.sum(zy)


# @numba.njit(cache=True)
# def G_EE_perdiodic(R1, R2, wavelength, conf_dict):
#     """evaluate field of dipole emitter in 1-2-3 layer environment (NF approx.)
    
#     R1: dipole position
#     R2: evaluation position
#     """
#     k_x = np.float32(conf_dict['k_x'].real)
#     # eps1 = conf_dict['eps1']
#     eps2 = conf_dict['eps2']
#     # eps3 = conf_dict['eps3']
#     # spacing = np.float32(conf_dict['spacing'].real)
#     cutoff_u = np.int(conf_dict['cutoff_u'].real)
#     cutoff_v = np.int(conf_dict['cutoff_v'].real)
#     u = np.array([np.float32(conf_dict['ux'].real), 
#                   np.float32(conf_dict['uy'].real), 
#                   np.float32(conf_dict['uz'].real)])
#     v = np.array([np.float32(conf_dict['vx'].real), 
#                   np.float32(conf_dict['vy'].real), 
#                   np.float32(conf_dict['vz'].real)])
    
#     return _G0_periodic(R1, R2, wavelength, eps2, k_x, cutoff_u, cutoff_v, u, v)


# @numba.njit(cache=True)
# def G_HE_perdiodic(R1, R2, wavelength, conf_dict):
#     """evaluate field of dipole emitter in 1-2-3 layer environment (NF approx.)
    
#     R1: dipole position
#     R2: evaluation position
#     """
#     k_x = np.float32(conf_dict['k_x'].real)
#     # eps1 = conf_dict['eps1']
#     eps2 = conf_dict['eps2']
#     # eps3 = conf_dict['eps3']
#     # spacing = np.float32(conf_dict['spacing'].real)
#     cutoff_u = np.int(conf_dict['cutoff_u'].real)
#     cutoff_v = np.int(conf_dict['cutoff_v'].real)
#     u = np.array([np.float32(conf_dict['ux'].real), 
#                   np.float32(conf_dict['uy'].real), 
#                   np.float32(conf_dict['uz'].real)])
#     v = np.array([np.float32(conf_dict['vx'].real), 
#                   np.float32(conf_dict['vy'].real), 
#                   np.float32(conf_dict['vz'].real)])
    
#     return _G0_HE_periodic(R1, R2, wavelength, eps2, k_x, cutoff_u, cutoff_v, u, v)



### --- coupling matrix gen. non-retarded 
# =============================================================================
# multi-dp-propagation / coupling matrix generators non-retarded 3D
# =============================================================================
## --- multi-dipole field propagation
@numba.njit(parallel=True)
def greens_tensor_evaluation_periodic(dp_pos, r_probe, G_func, wavelength, conf_dict, M,
                                      selfterm=None, dist_div_G=None):
    k_x = np.float32(conf_dict['k_x'].real)
    
    eps1 = conf_dict['eps1']
    eps2 = conf_dict['eps2']
    eps3 = conf_dict['eps3']
    spacing = np.float32(conf_dict['spacing'].real)
    
    cutoff_u = np.int(conf_dict['cutoff_u'].real)
    cutoff_v = np.int(conf_dict['cutoff_v'].real)
    u = np.array([np.float32(conf_dict['ux'].real), 
                  np.float32(conf_dict['uy'].real), 
                  np.float32(conf_dict['uz'].real)])
    v = np.array([np.float32(conf_dict['vx'].real), 
                  np.float32(conf_dict['vy'].real), 
                  np.float32(conf_dict['vz'].real)])
    
    for i in numba.prange(len(dp_pos)):   # explicit parallel loop
        _pos = dp_pos[i]
        for j in range(len(r_probe)):
            _r = r_probe[j]
            xx, yy, zz, xy, xz, yx, yz, zx, zy = G_func(
                                        _pos, _r, wavelength, eps1, eps2, eps3, 
                                        spacing, k_x, cutoff_u, cutoff_v, u, v
                                        )
            ## return list of Greens tensors
            M[i,j,0,0], M[i,j,1,1], M[i,j,2,2] = xx, yy, zz
            M[i,j,1,0], M[i,j,2,0], M[i,j,0,1] = yx, zx, xy
            M[i,j,2,1], M[i,j,0,2], M[i,j,1,2] = zy, xz, yz



@numba.njit(parallel=True, cache=True)
def t_sbs_EE_123_quasistatic_periodic(geo, wavelength, selfterms, alpha, conf_dict, M):
    k_x = np.float32(conf_dict['k_x'].real)
    
    eps1 = conf_dict['eps1']
    eps2 = conf_dict['eps2']
    eps3 = conf_dict['eps3']
    spacing = np.float32(conf_dict['spacing'].real)
    
    cutoff_u = np.int(conf_dict['cutoff_u'].real)
    cutoff_v = np.int(conf_dict['cutoff_v'].real)
    u = np.array([np.float32(conf_dict['ux'].real), 
                  np.float32(conf_dict['uy'].real), 
                  np.float32(conf_dict['uz'].real)])
    v = np.array([np.float32(conf_dict['vx'].real), 
                  np.float32(conf_dict['vy'].real), 
                  np.float32(conf_dict['vz'].real)])
    
    for i in numba.prange(len(geo)):    # explicit parallel loop
        R2 = geo[i]       # "observer"
        for j in numba.prange(len(geo)):
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
                xx, yy, zz, xy, xz, yx, yz, zx, zy = G0_periodic_123(
                                        R1, R2, wavelength, eps1, eps2, eps3, 
                                        spacing, k_x, cutoff_u, cutoff_v, u, v
                                        )
            
            ## --- 1-2-3 surface dyad (non retarded NF approximation)
            if eps1!=eps2 or eps2!=eps3:
                xxs,yys,zzs,xys,xzs,yxs,yzs,zxs,zys = Gs_periodic_123(
                                        R1, R2, wavelength, eps1, eps2, eps3, 
                                        spacing, k_x, cutoff_u, cutoff_v, u, v
                                        )
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
def t_sbs_HE_123_quasistatic_periodic(geo, wavelength, selfterms, alpha, conf_dict, M):
    k_x = np.float32(conf_dict['k_x'].real)
    
    eps1 = conf_dict['eps1']
    eps2 = conf_dict['eps2']
    eps3 = conf_dict['eps3']
    spacing = np.float32(conf_dict['spacing'].real)
    
    cutoff_u = np.int(conf_dict['cutoff_u'].real)
    cutoff_v = np.int(conf_dict['cutoff_v'].real)
    u = np.array([np.float32(conf_dict['ux'].real), 
                  np.float32(conf_dict['uy'].real), 
                  np.float32(conf_dict['uz'].real)])
    v = np.array([np.float32(conf_dict['vx'].real), 
                  np.float32(conf_dict['vy'].real), 
                  np.float32(conf_dict['vz'].real)])
    
    for i in numba.prange(len(geo)):    # explicit parallel loop
        R2 = geo[i]        # "observer"
        st = selfterms[i]
        for j in numba.prange(len(geo)):
            R1 = geo[j]    # emitter
            aj = alpha[j]
            ## --- vacuum dyad
            if i==j:
                ## self term
                xx, yy, zz = st[0,0], st[1,1], st[2,2]
                xy, xz, yx = st[0,1], st[0,2], st[1,0]
                yz, zx, zy = st[1,2], st[2,0], st[2,1]
            else:
                xx, yy, zz, xy, xz, yx, yz, zx, zy = G_HE_periodic(
                                        R1, R2, wavelength, eps1, eps2, eps3, 
                                        spacing, k_x, cutoff_u, cutoff_v, u, v
                                        )
            
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


### --- dyad class 3D non-retarded, 1D or 2D periodic
class DyadsQuasistaticPeriodic123(propagators.DyadsBaseClass):
    __name__ = "Quasistatic 3D '1-2-3' Green's tensors with periodicity"
    
    def __init__(self, n1=None, n2=None, n3=None, spacing=5000, 
                 u=np.array([0,0,0]), v=np.array([0,0,0]), 
                 cutoff_u=10, cutoff_v=10, 
                 radiative_correction=True):
        """ 
        u or v: period vectors
        set np.array([0,0,0]) for no periodicity in this dimension
        
        incident wavevector must be in XZ plane
        
        """
        super().__init__()
        
        self.u = u.astype(self.dtypef)
        self.v = v.astype(self.dtypef)
        
        self.cutoff_u = cutoff_u
        self.cutoff_v = cutoff_v
        if np.linalg.norm(u)==0: 
            self.cutoff_u = 0
        if np.linalg.norm(v)==0: 
            self.cutoff_v = 0
            
        ## Dyads
        self.G_EE = Gtot_periodic_123
        self.G_HE = G_HE_periodic
        self.G_EE_ff = Gtot_periodic_123    # using full propagator here for the moment
        
        ## evaluate propagator routine
        self.eval_G = greens_tensor_evaluation_periodic
        
        ## coupling matrix constructor routines
        self.tsbs_EE = t_sbs_EE_123_quasistatic_periodic
        self.tsbs_HE = t_sbs_HE_123_quasistatic_periodic
        
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

    
    def getConfigDictG(self, wavelength, struct, efield):
        if 'theta_inc' in efield.kwargs_permutations[0].keys():
            inc_angle = np.pi * efield.kwargs_permutations[0]['theta_inc'] / 180.0
        elif 'kSign' in efield.kwargs_permutations[0].keys():
            if efield.kwargs_permutations[0]['kSign'] == 1:
                inc_angle = 0.0    # bottom incidence
            else:
                inc_angle = np.pi  # top incidence
        else:
                inc_angle = np.pi  # top incidence
        
        
        ## all data need to be same dtype, must be cast to correct type inside numba functions
        conf_dict = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                                           value_type=numba.types.complex64)
        
        conf_dict['eps1'] = np.complex64(self.n1_material.epsilon(wavelength))
        conf_dict['eps2'] = np.complex64(self.n2_material.epsilon(wavelength))
        conf_dict['eps3'] = np.complex64(self.n3_material.epsilon(wavelength))
        conf_dict['spacing'] = np.complex64(self.spacing)
        conf_dict['ux'] = np.complex64(self.u[0])
        conf_dict['uy'] = np.complex64(self.u[1])
        conf_dict['uz'] = np.complex64(self.u[2])
        conf_dict['vx'] = np.complex64(self.v[0])
        conf_dict['vy'] = np.complex64(self.v[1])
        conf_dict['vz'] = np.complex64(self.v[2])
        conf_dict['cutoff_u'] = np.complex64(self.cutoff_u)
        conf_dict['cutoff_v'] = np.complex64(self.cutoff_v)
        
        n2 = (self.n2_material.epsilon(wavelength)**0.5)
        k_x = np.sin(inc_angle) * 2*np.pi * np.sqrt(n2**2) / wavelength
        conf_dict['k_x'] = np.complex64(k_x)
        
        ## return a numba typed dictionary of "complex64" type,
        ## can be used to pass configuration to the green's functions
        return conf_dict
    
    
    def exceptionHandling(self, struct, efield):
        """Exception handling / consistency and compatibility check
        
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
        if efield.field_generator.__name__ not in ['planewave', 'evanescent_planewave']:
            raise Exception("periodic structures only work with plane wave illumination. " +
                            "Please use 'planewave' or 'evanescent_planewave' field generator!")
        
        # if struct.n1_material.__name__ != struct.n2_material.__name__ or \
        #         struct.n1_material.__name__ != struct.n3_material.__name__:
        #     raise Exception("So far only a homogeneous environment is supported.")
        
        all_inc_angles = []
        for k in efield.kwargs_permutations:
            if 'theta_inc' in k.keys():
                all_inc_angles.append(k['theta_inc'])
        if len(np.unique(all_inc_angles)) > 1:
            raise Exception("Periodic simulations can treat only a single incident angle. " + 
                            "Please configure multiple simulations instead.")
        
        return True
    
    
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



