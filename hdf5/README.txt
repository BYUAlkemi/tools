-External Packages Needed:
-h5py
-http://www.h5py.org/
-numpy
-http://www.numpy.org/


FILE csv_to_h5.py
-----------------

Required files:
At least one CSV with format of ExtractedZoneParamters_0_1.txt
Different amounts of features, zone numbers, or timesteps should work
Note: Currently skips the first three columns in the header and first two in the data


Imported Libraries:
h5py, numpy, csv, argparse, sys, time


Usage: csv_to_h5.py [-h] [-t [TIMESTEP]] [-f FILE [FILE ...]]

optional arguments:
  -h, --help            show this help message and exit
  -t [TIMESTEP], --timestep [TIMESTEP]
                        Enter an integer value representing the range of
                        timesteps to slice the data into
  -f FILE [FILE ...], --file FILE [FILE ...]
                        Enter any number of file names to convert to HDF5
                        format




FILE h5_to_array.py
-------------------

Required files:
Some HDF5 File created with the csv_to_h5.py script

Imported Libraries:
h5py, numpy, argparse, sys, time


Usage: h5_to_array.py [-h] [-f FILE] [-t TIMESTEP [TIMESTEP ...]]
                      [-s [SWITCH]]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Enter the file name of your HDF5 file.
  -t TIMESTEP [TIMESTEP ...], --timestep TIMESTEP [TIMESTEP ...]
                        Enter one integer to return array from single
                        timestep, two to return a range of timesteps.
  -s [SWITCH], --switch [SWITCH]
                        Enter a 0 to use the faster block read method, or a 1
                        to use slower mult_step method for testing. Defaults
                        to 0.

FILE axes_h5_to_array.py
-------------------

Required files:
Some HDF5 File created with the csv_to_h5.py script

Imported Libraries:
h5py, numpy, argparse, sys, time


Usage: axes_h5_to_array.py [-h] [-i INFILE] [-t TIMESTEP] [-m [{1,2}]]
                           {step,feat,zone} ...

positional arguments:
  
  {step,feat,zone}      <- Commands
    
	
	step                Return Array from selected timestep
		optional arguments:
		  -h, --help  show this help message and exit
		
	
    feat                Return array from selected feature
		optional arguments:
		  -h, --help            show this help message and exit
		  -f [FEATURE], --feature [FEATURE]
		                        Enter the name of a feature to return
	
    zone                Return array from selected zone
		optional arguments:
		  -h, --help            show this help message and exit
		  -z [ZONEID], --zoneID [ZONEID]
		                        Enter an integer value representing a zone to return

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        Enter the file name of your HDF5 file.
  -t TIMESTEP, --timestep TIMESTEP
                        Enter one integer to return array from a single
                        timestep.
  -m [{1,2}], --mode [{1,2}]
                        Enter a 1 for a single timestep, a 2 for all steps in
                        Dataset.
