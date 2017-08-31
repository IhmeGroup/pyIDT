class options:
    mech_file = ''
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

    def parse(self,config):
        self.palette = config["test_palette"]
	self.test_comp = config["test_composition"]
	self.outer_center = config["outer_center"]
	self.outer_intervals = config["outer_intervals"]
	self.mech_file = config["mech_file"]
	self.mixture = config["mixture_name"]
	self.nx = config["palette_resolution"]
	self.pres = config["pressure"]
	self.temp = config["temperature"]
	self.phi = config["equivalence_ratio"]
	self.t_fin = config["final_time"]
	self.target_mw = config["target_mw"]
	self.target_hc = config["target_hc"]
        self.mw_tol = config["mw_tolerance"]
        self.hc_tol = config["hc_tolerance"]
	self.output_file = config["output_file"]
	self.override_targets = config["override_targets"]
	self.write_output = config["write_output"]

    def dump(self):
	print "test_palette: ", self.palette
        print "test_composition: ", self.test_comp
	print "cti_file: ", self.mech_file
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
