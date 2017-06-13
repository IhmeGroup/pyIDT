from options import options
from eval_idt import eval_idt
from mesh_generate_box import mesh_generate_box
from support import check_override
from mpi4py import MPI
import global_var
import cantera as ct
import numpy as np
import os
import sys
import yaml

# MPI based parallelization of Cantera ignition delay time calculation

def main():

	# MPI starter
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()

	# Read config file over all processors from command line
	# Use only XML as CTI leads to conversion and thus race conditions
	config_file = sys.argv[1]
	if (rank == 0):
	    print "Reading options file..."
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
        if (rank == 0):
	    print "Reading mechanism file..."
	gas = ct.Solution(opt.mech_file)

	# Check override
	check_override(gas,opt)

	# Dump options (only Processor 0)
	if (rank == 0):
	    opt.dump()

	    # Generate mesh
	    # Only done using Processor 0
	    mesh_data = mesh_generate_box(gas,opt)
            print "Mesh generation complete!"
            print "Number of points = ", (np.array(mesh_data)).shape[0]

	    # Print number of processors used
	    print "Number of processors = ", comm.Get_size()

if __name__ == '__main__':
    main() 
