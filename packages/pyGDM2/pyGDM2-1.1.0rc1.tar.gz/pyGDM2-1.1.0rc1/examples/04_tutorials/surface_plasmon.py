from __future__ import print_function, division

import cmath

import numpy as np
import matplotlib.pyplot as plt

from pyGDM2 import fields
from pyGDM2 import tools
from pyGDM2 import materials
from pyGDM2 import visu

#%%
## incident field generato --> code 3-layer of Christian
field_generator = fields.evanescent_planewave

## wavelegnths / angles to evaluate
wavelengths = np.linspace(400, 800, 41)
teta_list = np.linspace(35,55, 35)

## layer material and thickness
layer_material = materials.gold()
#layer_material = materials.silicon()
spacing = 50      # layer thinkness

## environment
n1 = 1.5  # substrate
n3 = 1.0  # top


## 2D evaluation plane
projection = 'XZ'

## transmitted --> integrate intensity in some region far above layer
r_probe_T = tools.generate_NF_map(-1000,1000,11, 3500,4500,11,0, projection=projection)

## reflected --> integrate intensity in some region below layer
r_probe_R = tools.generate_NF_map(-1000,1000,11, -4500,-3500,11,0, projection=projection)



# =============================================================================
# evaluate fields
# =============================================================================
I_T = []
I_R = []
## loop over wavelengths
for wl in wavelengths:
    _IT = []
    _IR = []
    ## loop over incident angles
    for t in teta_list:
        kwargs = dict(theta_inc=t, polar='p')

        ## gold refractive index at current wavelength
        n2 = cmath.sqrt(layer_material.epsilon(wl))
        
        ## NF above (transmission)
        NF_T = tools.evaluate_incident_field(field_generator, wl, kwargs, r_probe_T,
                                           n1=n1,n2=n2,n3=n3, spacing=spacing)
        
        ## NF below (incidence + reflection)
        NF_below = tools.evaluate_incident_field(field_generator, wl, kwargs, r_probe_R,
                                           n1=n1,n2=n2,n3=n3, spacing=spacing)
        ## NF_inc0: get incident field in a homogeneous environment (substrate ref.index)
        NF_inc0 = tools.evaluate_incident_field(field_generator, wl, kwargs, r_probe_R,
                                           n1=n1,n2=n1,n3=n1, spacing=spacing)
        ## reflected = NF_inc - NF_inc0
        NF_R = NF_below.copy()
        NF_R[:,3:] -= NF_inc0[:,3:]
        
        ## calculate intensity at each point and take average of entire evaluation region
        I_tot_T = np.average(np.sum( np.abs(NF_T[:,3:])**2, axis=1 ))
        I_tot_R = np.average(np.sum( np.abs(NF_R[:,3:])**2, axis=1 ))
        _IT.append(I_tot_T)
        _IR.append(I_tot_R)
    I_T.append(_IT)
    I_R.append(_IR)
I_T = np.flipud(I_T)
I_R = np.flipud(I_R)
    
#%%
# =============================================================================
# plot results
# =============================================================================

plt.figure(figsize=(12,3))
## --- field intensity transmitted
plt.subplot(131)
plt.title("transmitted")
plt.imshow(I_T, extent=(min(teta_list), max(teta_list), min(wavelengths), max(wavelengths)), aspect='auto')
plt.colorbar(label="|E|^2 / |E0|^2")
plt.xlabel("incident angle (deg)")
plt.ylabel("wavelength (nm)")

## --- field intensity reflected
plt.subplot(132)
plt.title("reflected")
plt.imshow(I_R, extent=(min(teta_list), max(teta_list), min(wavelengths), max(wavelengths)), aspect='auto')
plt.colorbar(label="|E|^2 / |E0|^2 above")
plt.xlabel("incident angle (deg)")
plt.ylabel("wavelength (nm)")

## --- one selected wavelength
plt.subplot(133)
plt.title("wavelength = {}nm".format(wavelengths[40]))
plt.plot(teta_list, I_R[40])
plt.xlabel("incident angle (deg)")
plt.ylabel("reflectance")


plt.tight_layout()
#plt.savefig("surface_plasmon_gold.png")
plt.show()

#%%
# =============================================================================
# plot real part of electric field across layer
# =============================================================================
wl = 600
teta = 45
kwargs = dict(theta_inc=teta, polar='p')
n2 = cmath.sqrt(layer_material.epsilon(wl))


#r_probe = tools.generate_NF_map(-1000,1000,100, -200,350,50,0, p7rojection=projection)
r_probe = tools.generate_NF_map(-2000,2000,61, -1500,1500,41,0, projection=projection)

NF = tools.evaluate_incident_field(field_generator, wl, kwargs, r_probe,
                                           n1=n1,n2=n2,n3=n3, spacing=spacing)

v = visu.vectorfield(NF, complex_part='real', projection=projection,
                     tit=projection+' real part, full (inc+r)', show=1, scale=15)




#%%
# =============================================================================
# 3D animation
# =============================================================================
#from pyGDM2 import visu3d
#visu3d.animate_vectorfield(NF, scale=10)
