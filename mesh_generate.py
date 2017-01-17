import numpy as np
from global_constants import *


def mesh_generate(gas, options):
    dx = options.dx

    x = np.arange(0.0, 1.0, dx)  # [0.0]
    y = np.arange(0.0, 1.0, dx)

    #######################
    # Constraints
    #######################

    # Molecular weight
    mw_full_vec = gas.molecular_weights

    mw_vec = []
    species_vec = []
    for species in options.palette:
        sp_index = gas.species_index(species)
        mw_vec.append(mw_full_vec[sp_index])
        species_vec.append(sp_index)

    # HC Ratio
    h_atoms_vec = np.zeros(palette_size)
    c_atoms_vec = np.zeros(palette_size)
    for i, idx in enumerate(species_vec):
        h_atoms_vec[i] = gas.n_atoms(idx, 'H')
        c_atoms_vec[i] = gas.n_atoms(idx, 'C')

    #######################
    # Mesh generation
    #######################
    # Solve for a3, a4, a5
    A = np.zeros((3, 3))

    A[0, :] = [1.0, 1.0, 1.0]
    A[1, :] = mw_vec[2:]

    # Construct HC constraint
    A[2, :] = h_atoms_vec[2:] - options.target_hc*c_atoms_vec[2:]

    mesh_data = []
    for a1 in x:
        for a2 in y:
            # Construct right hand side
            b = np.zeros(3)
            b[0] = 1.0-a1-a2
            b[1] = options.target_mw - np.dot(mw_vec[0:2], [a1, a2])
            b[2] = options.target_hc*np.dot([a1, a2], c_atoms_vec[0:2]) - \
                np.dot([a1, a2], h_atoms_vec[0:2])

            # Check if data point is valid
            sol = np.linalg.solve(A, b)
            tol = 1e-6

            mesh_point = np.hstack(([a1, a2], sol))

            if any(t < 0 for t in mesh_point):
                continue
            else:
                mesh_data.append(mesh_point)

    return mesh_data
