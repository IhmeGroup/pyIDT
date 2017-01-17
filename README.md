# pyIDT #

pyIDT is a (parallel) Python code used to calculate ignition delay time (IDT) for candidate fuel-surrogate compositions. The space of candidate compositions is first evaluated using a set of linear constraints based on physical properties.

## How do I get set up? ##

First, setup the YAML file for the particular surrogate. Note that this requires the pyYAML package which can be installed trivially using pip. Sample YAML files are provided in the `data` directory. Also, some mechanism files have been provided in `mech` folder [1], [2]. The code, for example, can be run using

```
python test_idt.py data/violi.yaml
```

Other prerequisites for this code are 

* cantera - python
* multiprocessing
* numpy, itertools

## Who do I talk to? ##

* Repo owner or admin : [Pavan Bharadwaj](https://github.com/gpavanb)
* Other community or team contact : The code was developed at the Flow Physics and Computational Engineering group at Stanford University. Please direct any official queries to [Prof. Matthias Ihme](mailto:mihme@stanford.edu)

## References ##

[1] Frassoldati, Alessio, et al. "Kinetic modeling study of ethanol and dimethyl ether addition to premixed low-pressure propene–oxygen–argon flames." Combustion and Flame 158.7 (2011): 1264-1276.

[2] Wallington, T. J., P. Dagaut, and M. J. Kurylo. "UV absorption cross sections and reaction kinetics and mechanisms for peroxy radicals in the gas phase." Chemical reviews 92.4 (1992): 667-710.
