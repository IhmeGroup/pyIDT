from options import options
from eval_idt import eval_idt
from mesh_generate_box import mesh_generate_box
from support import check_override
import global_var
import multiprocessing
import itertools
import cantera as ct
import numpy as np
import os
import sys
import timeit
import yaml

# Refer to pyCantera tutorials for multiprocessing example
# for further details regarding parallelizing. Note that
# only one machine can be used using multiprocessing

# Global storage for Cantera Solution objects
global_var.init()

def init_process(mech):
    global_var.gases[mech] = ct.Solution(mech)

def main():

    # Read config file from command line
    config_file = sys.argv[1] 
    yaml_file = open(config_file)
    config = yaml.safe_load(yaml_file)  
 
    # Set options structure
    opt = options()
    opt.palette = config["test_palette"]
    opt.test_comp = config["test_composition"]
    opt.outer_center = config["outer_center"]
    opt.outer_intervals = config["outer_intervals"]
    opt.mech_file = config["mech_file"]
    opt.mixture = config["mixture_name"]
    opt.nx = config["palette_resolution"]
    opt.pres = config["pressure"]
    opt.temp = config["temperature"]
    opt.phi = config["equivalence_ratio"]
    opt.t_fin = config["final_time"]
    opt.target_mw = config["target_mw"]
    opt.target_hc = config["target_hc"]
    opt.output_file = config["output_file"]
    opt.override_targets = config["override_targets"]
    opt.write_output = config["write_output"]

    # Close YAML file
    yaml_file.close()

    # Set gas
    gas = ct.Solution(opt.cti_file)

    # Check override
    check_override(gas, opt)

    # Dump options
    opt.dump()         

    # Generate mesh
    mesh_data = mesh_generate_box(gas,opt)
    print "Mesh generation complete!"
    print "Number of points = ", (np.array(mesh_data)).shape[0]

    # Estimate number of processes
    nProcs = multiprocessing.cpu_count()
    print "Number of cores = ", nProcs

    # Create gas objects for all processes
    pool = multiprocessing.Pool(processes=nProcs,
                                initializer=init_process,
                                initargs=(opt.mech_file,))
 
    try:
        os.remove(opt.output_file)
    except OSError:
        pass
    f = open(opt.output_file, 'a')

    # Start timing
    t0 = timeit.default_timer()

    res = pool.map(eval_idt,
                zip(itertools.repeat(opt.mech_file),
                    itertools.repeat(opt),
		    mesh_data))

    # End parallelism
    pool.close()
    pool.join()

    # End timing
    t1 = timeit.default_timer()

    print "Computation finished!"
    print "Time elapsed: ", t1-t0

    dump_mat = []
    if (opt.write_output): 
        for idx,mesh_point in enumerate(mesh_data):
       	    dump_point = np.hstack((mesh_point, res[idx]))
            dump_mat.append(dump_point)            
        np.savetxt(f,dump_mat,fmt='%.4e')

      
    f.close()

if __name__ == '__main__':
    main()
