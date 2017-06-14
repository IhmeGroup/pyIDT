import cantera as ct
import numpy as np
import global_var
import sys
from support import set_gas_using_palette


def eval_idt(args):
    #gas, options, x = args
    mech, options, x = args
    gas = global_var.gases[mech]
    t_fin = options.t_fin

    time_vec = []
    temp_vec = []

    # DCN Conditions
    p = options.pres  # Pa
    t = options.temp  # K
    phi = options.phi

    # Add air to the mixture
    stoich_o2 = 0.0
    for idx, species in enumerate(options.palette):
        stoich_o2 += x[idx]*(gas.n_atoms(species, 'C') + 0.25 * gas.n_atoms(species, 'H'))

    # Set gas composition with air
    x_mod = (options.phi/stoich_o2)*x
    comp_string = set_gas_using_palette(gas, options, t, p, x_mod)
    comp_string += ',O2:1,N2:3.76'
    gas.TPX = t, p, comp_string

    # Create reactor network
    r = ct.Reactor(gas)
    sim = ct.ReactorNet([r])
 
    # Advance the reactor
    time = 0.0
    time_vec.append(time)

    while time < t_fin:
        time = sim.step()
        time_vec.append(time)
        temp_vec.append(r.T)

    # Find maximum slope of temperature
    max_der = 0.0
    der = 0.0
    index = 0

    for idx, val in enumerate(temp_vec):
        der = (temp_vec[idx] - temp_vec[idx-1]) / \
              (time_vec[idx] - time_vec[idx-1])

        if abs(der) > max_der:
            max_der = der
            index = idx

    if temp_vec[index] < t:
        return -1
    else:
	print str(["{:0.3f}".format(y) for y in x]) +", "+ str("{:0.7e}".format(time_vec[index]))
        #print str(options.pres) + ", " + str(options.temp) + ", " + str(options.phi) + ", " + str("{:0.7e}".format(time_vec[index]))
	sys.stdout.flush()
        return time_vec[index]





