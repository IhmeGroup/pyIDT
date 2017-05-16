class options:
    cti_file = ''
    mixture = ''
    nx = 20
    t_fin = 0.0
    palette = ''
    test_comp = ''
    pres = 2239282.0
    temp = 833.0
    phi = 1.0
    target_mw = 0.0
    target_hc = 0.0
    outer_center = ''
    outer_intervals = ''
    output_file = ''
    override_targets = ''
    write_output = False
    mw_tol = 0.5
    hc_tol = 0.5

    def dump(self):
	print "test_palette: ", self.palette
        print "test_composition: ", self.test_comp
	print "cti_file: ", self.cti_file
	print "mixture_name: ", self.mixture
	print "palette_resolution: ", self.nx
	print "final_time: ", self.t_fin
        print "pressure: ", self.pres
        print "temperature", self.temp
	print "equivalence_ratio: ", self.phi

        if (self.override_targets):
             print "TARGETS OVERRIDDEN"

	print "target_mw: ", self.target_mw
	print "target_hc: ", self.target_hc
        print "outer_center: ", self.outer_center
        print "outer_intervals: ", self.outer_intervals
        print "mw_tolerance: ", self.mw_tol
        print "hc_tolerance: ", self.hc_tol
        print "write_output: ", self.write_output
