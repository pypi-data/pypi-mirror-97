import h5py
import numpy as np
from emcee.emcee_version import __version__
from os import path
import glob
import os

def clean_empty_chains (workDir='./') :
  '''
  Clean files with empty chain in the working directory.
  Useful to clean fast the chains when the code has crashed.
  '''

  list_chain = glob.glob (path.join (workDir, '*.h5'))
  for filename in list_chain :
    f = h5py.File(filename, 'r')
    g = f['mcmc']
    try :
      iteration = g.attrs["iteration"]
      if iteration == 0 :
        f.close ()
        os.remove (filename)
        print ('Removed', filename)
    except :
      print (filename)
      print ('File group mcmc has no attribute "iteration"')

  return 

def save_sampled_chain (filename, sampler, ndim, nwalkers, nsteps, name='mcmc') :

  '''
  A function that save emcee-sampled chains to a file which will
  be readable by HDFBackend emcee methods. 
  '''

  if not path.exists (filename) :

    f = h5py.File(filename, 'a')
    g = f.create_group(name)
    g.attrs["nwalkers"] = nwalkers
    g.attrs["ndim"] = ndim
    g.attrs["has_blobs"] = False
    g.attrs["iteration"] = nsteps
    g.create_dataset("accepted", data=np.zeros(nwalkers)) 
    #not sure it is possible to get this information from sampler, I will it to zero
    #(probably the acceptance_fraction computed from those files will be wrong
    # but that is not important).
    g.create_dataset(
        "chain",
        (nsteps, nwalkers, ndim), 
        data = sampler.get_chain (),
        dtype=np.float64,
    )
    g.create_dataset(
        "log_prob",
        (nsteps, nwalkers),
        data = get_log_prob (),
        dtype=np.float64,
    )

  else :
  #consider an initialised empty file created by emcee HDFBackend at the beginning of the sampling. 
    f = h5py.File(filename, 'a')
    g = f[name]
    g["chain"].resize(nsteps, axis=0)
    g["log_prob"].resize(nsteps, axis=0) 
    g.attrs["iteration"] = nsteps

    g["chain"][:,:,:] = sampler.get_chain ()
    g["log_prob"][:,:] = sampler.get_log_prob ()

  f.close ()
  return 
