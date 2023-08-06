# apollinaire

Python tools for helioseismic and asteroseismic frameworks.
This package provides functions and framework designed for helioseismic and asteroseismic instruments data managing
and analysis.  

The core of the package is the ``peakbagging`` library, which provides a full framework to extract oscillation modes parameters 
from solar and stellar spectrum. 

## Getting Started

### Prerequisites

The apollinaire package core framework is written in Python 3.
The following Python package are necessary to use apollinaire : 
- numpy
- scipy
- pandas
- matplotlib
- h5py
- emcee
- numdifftools
- corner
- pathos
- dill
- statsmodels
- urllib3
- joblib
- numba
- george
- astropy

A few auxiliary codes of the Solar-SONG library are written in IDL but it is unlikely that you will need them. 

### Installing

With pip:

`pip install apollinaire` 

You can also install the most recent version of apollinaire by cloning the GitLab repository:

`git clone https://gitlab.com/sybreton/apollinaire.git`

### Documentation

Documentation is available on [Read the Docs](https://apollinaire.readthedocs.io).

## Authors

* **Sylvain N. Breton** - Maintainer - PhD student (Université de Paris/CEA Saclay)

## Additional content 

GOLF timeseries will soon be available on the LDE3 website :

`http://irfu.cea.fr/dap/LDEE/index.php`

