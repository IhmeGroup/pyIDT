from options import options
from eval_idt import eval_idt
from mesh_generate import mesh_generate
import global_var
import multiprocessing
import itertools
import cantera as ct
import numpy as np
import os
import sys
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
    test_comp = config["test_composition"]
    opt.cti_file = config["cti_file"]
    opt.mixture = config["mixture_name"]
    opt.dt = config["time_step"]
    opt.dx = config["palette_resolution"]
    opt.phi = config["equivalence_ratio"]
    opt.t_fin = config["final_time"]
    opt.target_mw = config["target_mw"]
    opt.target_hc = config["target_hc"]
    opt.output_file = config["output_file"] 

    # Close YAML file
    yaml_file.close()
  
    # Dump input options structure
    opt.dump()

    # Generate mesh
    gas = ct.Solution(opt.cti_file)
    mesh_data = mesh_generate(gas, opt)
    print "Mesh generation complete!"
    print "Number of points = ", (np.array(mesh_data)).shape[0]

    # Estimate number of processes
    nProcs = multiprocessing.cpu_count()
    print "Number of cores = ", nProcs

    # Create gas objects for all processes
    pool = multiprocessing.Pool(processes=nProcs,
                                initializer=init_process,
                                initargs=(opt.cti_file,))

    print "Gas objects created!"
 
    try:
        os.remove(opt.file_name)
    except OSError:
        pass
    # f = open(opt.file_name, 'a')

    res = pool.map(eval_idt,
                zip(itertools.repeat(opt.cti_file),
                    itertools.repeat(opt),
		    mesh_data))

    # End parallelism
    pool.close()
    pool.join()

    print "Computation finished!"

     #for mesh_point in mesh_data:
     #   idt = eval_idt(gas, opt, mesh_point)
     #   dump_vec = np.hstack((mesh_point, idt))
     #   print ",".join(map(str,dump_vec))
     #   f.write(",".join(map(str, dump_vec)))
     #   f.write("\n")

    # f.close()

if __name__ == '__main__':
    main()
