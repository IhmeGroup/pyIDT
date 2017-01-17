class options:
    cti_file = ''
    mixture = ''
    dt = 0.0
    dx = 0.01
    t_fin = 0.0
    palette = ''
    phi = 1.0
    target_mw = 0.0
    target_hc = 0.0
    output_file = ''

    def dump(self):
	print "test_palette: ", self.palette
	print "cti_file: ", self.cti_file
	print "mixture_name: ", self.mixture
	print "time_step: ", self.dt
	print "palette_resolution: ", self.dx
	print "final_time: ", self.t_fin
	print "equivalence_ratio: ", self.phi
	print "target_mw: ", self.target_mw
	print "target_hc: ", self.target_hc

