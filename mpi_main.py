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
        opt.parse(config)

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
	    nEl_global = (np.array(mesh_data)).shape[0]
            print "Number of points = ", nEl_global

	    # Print number of processors used
	    nProcs = comm.Get_size()
	    print "Number of processors = ", nProcs

	    if (nProcs > nEl_global):
	        print "Too few points to scatter. Decrease number of processors"
		comm.Abort()

	    # Create sub-list for each processor
	    split = np.array_split(mesh_data, nProcs) 

	else:
	    split = None

	# Distribute sub-list
	data = comm.scatter(split, root=0)	    	

	# Each processor runs its sub-list
	dump_mat = []
	for x in data:
	    res = eval_idt([gas,opt,x])
            for idx, phi in enumerate(opt.phi):
	        dump_point = np.hstack((x, phi, res[idx]))
                dump_mat.append(dump_point)

	# Gather and write
	dump_mat = comm.gather(dump_mat, root=0)
	if (rank == 0):
	    dump_mat = np.vstack(tuple(dump_mat))
	    if (opt.write_output):
		f = open(opt.output_file, 'w')
                np.savetxt(f,dump_mat,fmt='%.3e')
		f.close()	

if __name__ == '__main__':
    main() 
