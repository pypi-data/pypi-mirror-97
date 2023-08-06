import numpy as np
import pandas as pd
import emcee
import corner
from .likelihood import log_likelihood, log_likelihood_wdw, cond_transf
from .fit_tools import a2z_df_to_param
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import dill
from pathos.multiprocessing import ProcessPool
from multiprocessing import Pool

def log_prior (bounds, param=None, param_type=None) :

  '''
  Compute the positive log prior probability of the parameters to estimate.
  By default, uniform distribution laws are assumed.

  :param bounds: for parameters with assumed prior uniform distribution, bounds of 
  the uniform distribution.
  :type bounds: ndarray

  :param param: parameters to fit. Optional, default None.
  :type param: 1d ndarray

  :param param_type: array of string giving the param type of the param to fit, eg
  'freq', 'height', 'width', 'amp_l', 'split'. Optional, default None.  
  :type param_type: ndarray

  :return: prior value for the given parameters.
  :rtype: float
  '''

  cond = (param<bounds[:,0])|(param>bounds[:,1])
  if np.any (cond) :
    return - np.inf

  extent = bounds[:,1] - bounds[:,0] 
  individual_prior = 1. / extent #assuming uniform law for all given parameters.
  prior = np.prod (individual_prior) 
  l_prior = np.log (prior)

  return l_prior

def log_probability (param_to_fit, param_type, freq, psd, back, df_a2z, transform, bounds, param_wdw=None,
                     norm=None, instr='kepler') :
  '''
  Compute the positive posterior log probability (unnormalised) of the parameters to fit. 

  :param_to_fit: parameter that scipy.optimize minimize will use to find the
  minimum of the function. Created by a2z_df_to_param function.
  :type param_to_fit: 1d ndarray
 
  :param param_type: array of string giving the param type of the param to fit, eg
  'freq', 'height', 'width', 'amp_l', 'split'. 
  :type param_type: ndarray

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param df_a2z: global pandas DataFrame wrapping global parameters needed to design the model.
  :type df_a2z: pandas DataFrame.

  :param transform: list of parameter that are given in natural log by the calling routine and that
  will be retransformed. If None, the function will consider that all parameters have been give as
  logarithm. 
  :type transform: tuple of strings

  :param bounds: for parameters with assumed prior uniform distribution, bounds of 
  the uniform distribution.
  :type bounds: ndarray

  :param param_wdw: parameters of the observation window timeseries. Optional, default None. 
  :type wdw: ndarray.

  :param norm: if given, the param_to_fit and bounds input vectors will be multiplied by this vector. 
  Optional, default None.
  :type norm: ndarray

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf', 'virgo'.
  :type instr: str

  :return: posterior probability value
  :rtype: float
  '''

  if norm is not None :
    param_to_fit = param_to_fit * norm
    bounds[:,0] = bounds[:,0] * norm
    bounds[:,1] = bounds[:,1] * norm

  l_prior = log_prior (bounds, param_to_fit)

  if not np.isfinite (l_prior) :
    return - np.inf 

  if param_wdw is None :
    l_likelihood = - log_likelihood (param_to_fit, param_type, freq, psd, back, df_a2z, transform, instr=instr)
  else :
    l_likelihood = - log_likelihood_wdw (param_to_fit, param_type, freq, psd, back, df_a2z, transform,
                                       param_wdw, instr=instr)

  l_proba = l_prior + l_likelihood

  return l_proba

def sort_chain (labels, degrees, flatchain) :

  aux_flat = np.copy (flatchain)

  sort1 = np.argsort (labels)
  labels = labels[sort1]
  degrees = degrees[sort1]
  aux_flat = aux_flat[:,sort1]

  sort2 = np.argsort(degrees)
  labels = labels[sort2]  
  degrees = degrees[sort2]
  aux_flat = aux_flat[:,sort2]

  return labels, degrees, aux_flat

def explore_distribution (result, param_type, freq, psd, back, 
                          df_a2z, bounds, low_bound_freq=1500, up_bound_freq=5000,
                          param_wdw=None, nsteps=1000, filename=None, parallelise=False,
                          progress=False, nwalkers=64, normalise=False, degrees=None, instr='kepler') :

  '''
  Use a MCMC to explore the distribution around the maximum likelihood estimation results. 

  :param result: result vector of the MLE process. Be careful that the right parameters are 
  given in log (those with assumed posterior log-normal distribution).
  :type result: ndarray

  :param param_type: array of string giving the param type of the param to fit, eg
  'freq', 'height', 'width', 'amp_l', 'split'. 
  :type param_type: ndarray

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param df_a2z: global pandas DataFrame wrapping global parameters needed to design the model.
  :type df_a2z: pandas DataFrame.

  :param transform: list of parameter that are given in natural log by the calling routine and that
  will be retransformed. If None, the function will consider that all parameters have been give as
  logarithm. 
  :type transform: tuple of strings

  :param bounds: for parameters with assumed prior uniform distribution, bounds of 
  the uniform distribution.
  :type bounds: ndarray

  :param param_wdw: parameters of the observation window timeseries. Optional, default None. 
  :type wdw: ndarray.

  :param filename: name of the hdf5 where to store the chain. If filename is None, the name will not
  be stored. Optional, default None.
  :type filename: string

  :param parallelise: If set to True, use Python multiprocessing tool to parallelise process.
  Optional, default False.
  :type parallelise: bool

  :param degrees: vector containing degrees of the parameters to fit. If given, will be stored in the .dat
  file. Optional, default None.
  :type degrees: ndarray

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf', 'virgo'.
  :type instr: str

  :return: the MCMC sampler after exploring the distribution.
  :rtype: emcee.EnsembleSampler
  '''
 
  psd_to_fit = psd / back

  aux_freq = freq[(freq>low_bound_freq)&(freq<up_bound_freq)]
  aux_psd = psd_to_fit[(freq>low_bound_freq)&(freq<up_bound_freq)]
  aux_back = back[(freq>low_bound_freq)&(freq<up_bound_freq)]

  transform = ('height', 'width')
  cond = cond_transf (param_type, transform=transform)
  result[cond] = np.log (result[cond])

  lower_bounds = bounds [:,0]
  upper_bounds = bounds [:,1]
  lower_bounds[cond] = np.log(lower_bounds[cond])
  upper_bounds[cond] = np.log(upper_bounds[cond])

  # adding free constant for background
  result = np.append (result, 1.)
  lower_bounds = np.append (lower_bounds, 1e-6)
  upper_bounds = np.append (upper_bounds, 3.)
  param_type = np.append (param_type, 'background')
  degrees = np.append (degrees, 'a')

  #normalisation step
  if normalise :
    norm = np.abs (result)
  else :
    norm = np.ones (result.size)
  result = result / norm
  lower_bounds = lower_bounds / norm
  upper_bounds = upper_bounds / norm

  bounds = np.c_[lower_bounds, upper_bounds]

  pos = result + 1e-4 * np.random.randn(nwalkers, result.size)
  nwalkers, ndim = pos.shape

  if filename is not None :
    backend = emcee.backends.HDFBackend(filename)
    backend.reset(nwalkers, ndim) 
    #saving parameters name and normalisation information
    filename_info = filename[:len(filename)-3] + '.dat'
    if degrees is not None :
      np.savetxt (filename_info, np.c_[param_type, norm, degrees], fmt='%-s') 
    else :
      np.savetxt (filename_info, np.c_[param_type, norm], fmt='%-s') 
  else :
    backend = None

  if parallelise :
    pool = ProcessPool ()
  else :
    pool = None

  sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, 
                                  args=(param_type, aux_freq, aux_psd, aux_back, 
                                        df_a2z, transform, bounds, param_wdw, norm, instr),
                                  backend=backend, pool=pool)
  sampler.run_mcmc(pos, nsteps, progress=progress)

  return sampler, norm 

def show_chain (filename, thin=1000, read_info=False, save=False, discard=0) :
  '''
  Framework to plot chains saved as hdf5 files.

  :param filename: name of the chain. The name format is the following
  'mcmc_sampler_order_[n_order]_degrees_[n_degrees].h5' with n_degrees being '13' or '02'.
  :type filename: str

  :return: None
  '''

  reader = emcee.backends.HDFBackend(filename, read_only=True)
  
  if read_info :
    labels = np.loadtxt (filename[:len(filename)-3]+'.dat', dtype=str, usecols=0)
    degrees = np.loadtxt (filename[:len(filename)-3]+'.dat', dtype=str, usecols=2)
    labels = np.char.add (labels, np.full (labels.size, '_', dtype=str))
    labels = np.char.add (labels, degrees)
    norm = np.loadtxt (filename[:len(filename)-3]+'.dat', usecols=1)
  else :
    labels=None

  flatchain = reader.get_chain(flat=True, thin=thin, discard=discard)
  quantiles = [0.16, 0.84]

  if read_info :
    flatchain = flatchain * norm
    labels, degrees, flatchain = sort_chain (labels, degrees, flatchain)
    fig = corner.corner(flatchain, labels=labels, quantiles=quantiles, show_titles=True, title_fmt='.4f', bins=100)
  else :
    fig = corner.corner(flatchain, labels=labels, quantiles=quantiles, show_titles=True, title_fmt='.4f', bins=100)
  fig.set_size_inches(24,24)

  if save :
    plt.savefig (filename[:len(filename)-3]+'.pdf', format='pdf')

  return

def wrap_explore_distribution (df_a2z, freq, psd, back, low_bound_freq=1500, up_bound_freq=5000, wdw=None,
                               nsteps=1000, show_corner=False, filename=None, parallelise=False, progress=False,
                               nwalkers=64, normalise=False, instr='kepler', coeff_discard=50) :

  '''
  A small wrapper to call and exploit restult of the explore_distribution function inside the peakbagging
  framework.

  :param df_a2z: global pandas DataFrame wrapping global parameters needed to design the model.
  :type df_a2z: pandas DataFrame.

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param filename: name of the hdf5 where to store the chain. If filename is None, the name will not
  be stored. Optional, default None.
  :type filename: string

  :param parallelise: If set to True, use Python multiprocessing tool to parallelise process.
  Optional, default False.
  :type parallelise: bool

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf'
  :type instr: str

  :param coeff_discard: coeff used to compute the number of values to discard: total amount of
  sampled values will be divided by coeff_discard. Optional, default 50.
  :type coeff_discard: int

  :return: the 16, 50 and 84th percentiles values for each parameter 
  :rtype: ndarray
  '''

  df_to_pass = df_a2z.copy ()

  result, param_type, bounds, degrees = a2z_df_to_param (df_a2z, give_degree=True)

  param_wdw = None
  if wdw is not None :
    dt = 1 / (2*freq[-1])
    param_wdw = sidelob_param (wdw, dt=dt)

  cp_result = np.copy (result)
  cp_bounds = np.copy (bounds)

  sampler, norm = explore_distribution (cp_result, param_type, freq, psd, back,
                            df_to_pass, cp_bounds, low_bound_freq=low_bound_freq, filename=filename, 
                            up_bound_freq=up_bound_freq, param_wdw=param_wdw, nsteps=nsteps, 
                            parallelise=parallelise, progress=progress, nwalkers=nwalkers, normalise=normalise,
                            degrees=degrees, instr=instr)

  # Now exploiting results from the sampler

  discard = nsteps // coeff_discard
  thin = 1

  flat_samples = sampler.get_chain(discard=discard, thin=thin, flat=True)
  labels = np.append (param_type, 'background')
  truths = np.append (result, 1.)

  if show_corner :
    labels = np.loadtxt (filename[:len(filename)-3]+'.dat', dtype=str, usecols=0)
    degrees = np.loadtxt (filename[:len(filename)-3]+'.dat', dtype=str, usecols=2)
    labels = np.char.add (labels, np.full (labels.size, '_', dtype=str))
    labels = np.char.add (labels, degrees)
    norm = np.loadtxt (filename[:len(filename)-3]+'.dat', usecols=1)
    quantiles = [0.16, 0.84]

    flat_samples = flat_samples * norm
    labels, degrees, flatchain = sort_chain (labels, degrees, flat_samples)

    fig = corner.corner(flatchain, labels=labels, quantiles=quantiles, show_titles=True, title_fmt='.4f', bins=100)
    fig.set_size_inches(24,24)
    if filename is not None :
      plt.savefig (filename[:len(filename)-3]+'.pdf', format='pdf')

  centiles = np.percentile(flat_samples, [16, 50, 84], axis=0) * norm 

  return centiles

def chain_to_a2z (filename, thin=1, discard=500) :
  '''
  Function to create an a2z dataframe from a sampled chain.

  :param filename: name of the chain. The name format is the following
  'mcmc_sampler_order_[n_order]_degrees_[n_degrees].h5' with n_degrees being '13' or '02'.
  :type filename: str

  :return: a2z style dataframe.
  :rtype: pandas DataFrame
  '''

  reader = emcee.backends.HDFBackend(filename, read_only=True)

  order = filename[19:21]
  order = int (order)
  
  labels = np.loadtxt (filename[:len(filename)-3]+'.dat', dtype=str, usecols=0)
  degrees = np.loadtxt (filename[:len(filename)-3]+'.dat', dtype=str, usecols=2)
  norm = np.loadtxt (filename[:len(filename)-3]+'.dat', usecols=1)

  flatchain = reader.get_chain(flat=True, thin=thin)
  centiles = np.percentile (flatchain, [16, 50, 84], axis=0) * norm
  bounds = np.percentile (flatchain, [0,100], axis=0) * norm

  columns = list (range (9))
  aux_index = list (range (labels.size))

  df = pd.DataFrame (index=aux_index, columns=columns)
  df.loc[:,0] = order
  df.loc[:,1] = degrees
  df.loc[:,2] = labels
  df.loc[labels!='a',3] = 'mode'
  df.loc[labels=='a',3] = 'order'
  df.loc[:,4] = centiles[1,:]

  #Computing (symmetric) sigmas
  sigma_1 = centiles[1,:] - centiles[0,:]
  sigma_2 = centiles[2,:] - centiles[1,:]
  sigma = (sigma_1 + sigma_2) / 2.

  df.loc[:,5] = sigma
  df.loc[:,6] = 0.

  #Adding bounds
  df.loc[:,7] = bounds[0,:]
  df.loc[:,8] = bounds[1,:]

  return df
