from global_constants import *


def create_comp_string(gas, options, x):
    final_string = ''

    assert(len(x) == palette_size)

    for idx, compound in enumerate(options.palette):
        final_string += compound + ":" + str(x[idx])
        if idx != len(x)-1:
            final_string += ","

    return final_string


def set_gas_using_palette(gas, options, t, p, x):
    comp_string = create_comp_string(gas, options, x)
    gas.TPX = t, p, comp_string
    return comp_string
