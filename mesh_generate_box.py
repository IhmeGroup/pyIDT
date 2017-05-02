import numpy as np
from global_constants import *
from support import numberToBase

def mesh_generate_box(gas,options):
    palette_size = len(options.palette)
    nx = options.nx
    mw_tol = options.mw_tol
    hc_tol = options.hc_tol
    target_mw = options.target_mw
    target_hc = options.target_hc
 
    mw_full_vec = gas.molecular_weights
    mw_vec = []
    h_vec = []
    c_vec = []
    for species in options.palette:
        sp_index = gas.species_index(species)
        mw_vec.append(mw_full_vec[sp_index])
        h_vec.append(gas.n_atoms(sp_index,'H'))
        c_vec.append(gas.n_atoms(sp_index,'C'))

    x = []
    for j in xrange(0, palette_size-1):
         lb = options.outer_center[j] - options.outer_intervals[j]
         ub = options.outer_center[j] + options.outer_intervals[j]
         x.append(np.linspace(lb, ub, nx)) 

    mesh_data = []
    max_idx = nx**(palette_size-1)

    for i in xrange(0,max_idx):
        indicator = numberToBase(i,nx,palette_size-1)
        mesh_point = []
        for j in xrange(0,palette_size-1):
            mesh_point.append(x[j][indicator[j]])
        
        if (sum(mesh_point) > 1.0):
            continue
     
        mesh_point.append(1.0 - sum(mesh_point))

        # Calculate molecular weight
        mw = np.dot(mesh_point, mw_vec) 
        if (mw <= (1+mw_tol)*target_mw and mw >= (1-mw_tol)*target_mw):

             # Calculate H/C ratio
             hc = np.dot(mesh_point, h_vec)/np.dot(mesh_point,c_vec)

             if (hc <= (1+hc_tol)*target_hc and hc >= (1-hc_tol)*target_hc):
                  mesh_data.append(np.array(mesh_point))

    return mesh_data

     
