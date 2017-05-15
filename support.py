import numpy as np

def create_comp_string(gas, options, x):
    final_string = ''

    for idx, compound in enumerate(options.palette):
        final_string += compound + ":" + str(x[idx])
        if idx != len(x)-1:
            final_string += ","

    return final_string

def set_gas_using_palette(gas, options, t, p, x):
    comp_string = create_comp_string(gas, options, x)
    gas.TPX = t, p, comp_string
    return comp_string

def check_override(gas, options):
    test_comp = options.test_comp
    mw_full_vec = gas.molecular_weights
    mw_vec = []
    h_vec = []
    c_vec = []
    for species in options.palette:
        sp_index = gas.species_index(species)
        mw_vec.append(mw_full_vec[sp_index])
        h_vec.append(gas.n_atoms(sp_index,'H'))
        c_vec.append(gas.n_atoms(sp_index,'C'))

    # Override properties if specified
    if (options.override_targets):
         options.target_mw = np.dot(mw_vec, test_comp)
         options.target_hc = np.dot(h_vec, test_comp)/np.dot(c_vec, test_comp)     

def numberToBase(n, b, length):
    if n == 0:
        return [0]*length
    digits = []
    while n:
        digits.append(int(n % b))
        n /= b
    
    # Pad till length
    if (length - len(digits) > 0):
        vec = np.hstack(([0]*(length - len(digits)),digits[::-1]))
    else:
        vec = digits[::-1]
    return vec
