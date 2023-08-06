import numpy as np
import pandas as pd
from scipy.optimize import minimize
from .modified_optimize import _minimize_powell
from .fit_tools import *
from .analyse_window import sidelob_param
from pathos.multiprocessing import ProcessPool
import sys
import numdifftools as nd
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import emcee
import corner

'''
This file is constituded with MLE tools used for fitting stellar 
background.
'''

def create_labels (n_harvey, frozen_param) :
  '''
  Create array of label to use when plotting MCMC.
  '''

  label = []
  for ii in range (n_harvey) :
    label.append ('A_H_' + str (ii+1))
    label.append ('nuc_H_' + str (ii+1))
    label.append ('alpha_H_' + str (ii+1))
  label.append ('a')
  label.append ('b')
  label.append ('A_Gauss')
  label.append ('numax')
  label.append ('Wenv')
  label.append ('noise')

  label = np.array (label)
  label = label[~frozen_param]

  return label

def get_low_bounds (full_param, n_harvey, freq, psd) :
  '''
  Low bound for background parameters. 
  '''
  low_bounds = 0.1 * full_param
  for ii in range (n_harvey) :
    if ii==1 :
      low_bounds[3*ii+1] = 1.e-8 #constraint on Harvey law cut frequency
    else :
      low_bounds[3*ii+1] = 0.5 * full_param[3*ii+1]
    low_bounds[3*ii+2] = 1.9 #constraint on Harvey law exponent
  low_bounds[-2:-5:-1] = 0.5 * full_param[-2:-5:-1] #constraint on gaussian envelope

  return low_bounds

def get_up_bounds (full_param, n_harvey, freq, psd) :
  '''
  Up bound for background parameters. 
  '''

  h = freq[2] - freq[1]
  rms = np.sqrt (np.sum (psd) * h)

  up_bounds = 10. * full_param
  for ii in range (n_harvey) :
    if ii > 1 :
      up_bounds[3*ii] = 0.5 * rms 
      up_bounds[3*ii+1] = freq[-1] #constraint on Harvey law cut frequency
    elif n_harvey > 1 :
      up_bounds[3*ii] = 2 * rms 
      up_bounds[3*ii+1] = 1.5 * full_param[3*ii+1] #constraint on Harvey law cut frequency
    up_bounds[3*ii+2] = 4.1 #constraint on Harvey law exponent 
  up_bounds[-2:-5:-1] = 2. * full_param[-2:-5:-1]  #constraint on gaussian envelope

  return up_bounds

def numax_scale (r, m, teff) :
  '''
  Return numax computed with the asteroseismic scale laws.
  Radius and mass must be given in solar radius and mass.
  '''
  numax_sun = 3050. 
  teff_sun = 5770.

  numax = numax_sun * np.power (r, -2) * m * np.power (teff/teff_sun, -0.5)

  return numax

def dnu_scale (r, m) :
  '''
  Return numax computed with the asteroseismic scale laws.
  Radius and mass must be given in solar radius and mass.
  '''

  dnu_sun = 135.
  dnu = dnu_sun * np.power (m, 0.5) * np.power (r, -1.5)

  return dnu

def background_guess (freq, psd, numax, dnu, m_star=None, n_harvey=2) :
  '''
  Create a 1D vector with the initial guess to feed the MLE minimisation function.
  Scaling laws for nu_c and A are taken from Kallinger et al. 2014. 
  Prescriptions for white noise and power law follow Mathur et al. 2010. 

  :param n_harvey: number of Harvey laws to use to build the background
    model. Optional, default 2. 
  :type n_harvey: int

  :return: 1D vector of background initial parameter.
  :rtype: ndarray
  '''

  guess = np.zeros (n_harvey * 3 + 6)
  # First Harvey law
  nu_c_1 = 0.317 * np.power (numax, 0.97) 
  # A 
  if m_star is None :
    a = 3382 * np.power (numax, -0.609)  
  else :
    a = 3710 * np.power (numax, -0.613) * np.power (m_star, -0.26) 
  guess[0] = 2. * np.sqrt(2.) * a / (np.pi * nu_c_1)
  # nu_c
  guess[1] = nu_c_1  
  # alpha
  if n_harvey==1 :
    guess[2] = 2
  else :
    guess[2] = 4

  # Second Harvey law
  nu_c_2 = 0.948 * np.power (numax, 0.992) 
  # A
  guess[3] = 2. * np.sqrt(2.) * a / (np.pi * nu_c_2)
  # nu_c
  guess[4] = nu_c_2  
  # alpha
  guess[5] = 4

  # if the user set more than 2 harvey laws but did not provide himself
  # a guess (the initial guess will be the same as the second Harvey law
  # not recommendend)
  if n_harvey > 2 :
    for ii in range (2, n_harvey) :
      # A
      guess[6+ii*3] = 2. * np.sqrt(2.) * a / (np.pi * nu_c_2)
      # nu_c
      guess[7+ii*3] = nu_c_2  
      # alpha
      guess[8+ii*3] = 4

  # Power law
  #TODO
  print ('Power law guess need to be added to the function, this guess will build a null power law vector')
  guess[n_harvey*3] = 0
  guess[n_harvey*3+1] = -1

  # Gaussian parameters of the envelope
  # Hmax
  guess[n_harvey*3+2] = np.mean (psd[(freq>numax-dnu/4.)&(freq<numax+dnu/4.)]) #to adjust if needed 
  # numax
  guess[n_harvey*3+3] = numax 
  # Wenv
  guess[n_harvey*3+4] = 4 * dnu #to adjust if needed 

  # white noise estimation with high frequency region. 
  nu_nyq = freq[-1]
  nu_start = min (3 * numax, 0.8 * nu_nyq) #to adjust if needed 
  W = np.mean (psd[(freq>nu_start)])
  guess[n_harvey*3+5] = W

  return guess

def harvey (freq, A, nu_c, alpha) :
  '''
  Compute empirical Harvey law.
  '''
  num = A
  den = 1. + np.power (freq/nu_c , alpha)
  
  h = num / den

  return h

def power_law (freq, a, b) :
  '''
  Compute power law.
  ''' 
  return np.power (a*freq, -b)

def gauss_env (freq, Hmax, numax, Wenv) :
  '''
  Compute p-modes Gaussian envelope. 
  '''
  return Hmax * np.exp (- np.power ((freq-numax)/Wenv, 2))

def background_model (freq, param_harvey=None, param_plaw=None, 
                      param_gaussian=None, noise=0, n_harvey=2) :
  '''
  Compute background model.
  '''
  model = np.zeros (freq.size)
  if param_harvey is not None :
    param_harvey = np.reshape (param_harvey, (n_harvey, param_harvey.size//n_harvey))
    for elt in param_harvey :
      model += harvey (freq, *elt) 
  if param_plaw is not None :
    model += power_law (freq, *param_plaw) 
  if param_gaussian is not None :
    model += gauss_env (freq, *param_gaussian) 
  model += noise

  return model

def extract_param (param, n_harvey) :
  '''
  Extract param_harvey, param_plaw, param_gaussian and white noise
  from global input parameters. 

  :type param: 1D vector with backgrounds parameters given in the following order
  >>>> param_harvey (3*), param_plaw (2), param_gaussian (3), white noise (1) <<<<
  :type param: array like

  :param n_harvey: number of Harvey laws to use to build the background
  model.  
  :type n_harvey: int
  '''
  lenparam = n_harvey * 3 + 6

  if len (param) != lenparam :
    raise Exception ('Param vector length is not consistent')

  param_harvey = param[:n_harvey*3]
  param_plaw = param[n_harvey*3:n_harvey*3+2]
  param_gaussian = param[n_harvey*3+2:n_harvey*3+5]
  white_noise = param[-1]

  return param_harvey, param_plaw, param_gaussian, white_noise

def log_prior (param, bounds) :
  '''
  Compute positive log_prior probability for MCMC framework. Uninformative priors are used.  

  :param param: parameters to fit. Optional, default ``None``.
  :type param: 1d ndarray

  :param bounds: for parameters with assumed prior uniform distribution, bounds of 
  the uniform distribution.
  :type bounds: ndarray

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

def log_likelihood_back (param, freq, psd, full_param, frozen_param, n_harvey, fit_log=False) :
  '''
  Compute negative log_likelihood for fitting model on 
  background.

  :param param: param to fit passed by perform_mle_back. Param are given in 
  the following order: Harvey law parameters, power law parameters, Gaussian p-mode 
  envelope parameters, noise constant. 

  :param freq: frequency vector in muHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/muHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param full_param: full vector necessary to define background model. 'param' element will
  be inserted according to the 'frozen_param' mask. 
  :type full_param: ndarray

  :param frozen_param: boolean array of the same size as full_param. Components set to True
  will not be fitted.
  :type frozen_param: boolean array

  :param n_harvey: number of Harvey laws to use to build the background
  model.  
  :type n_harvey: int

  :param fit_log: if set to True, parameters will be considered to have been given as logarithm
  and will be transformed with an exponential. Optional, default False.
  :type fit_log: bool
  '''

  if fit_log :
    param = np.exp (param)

  full_param[~frozen_param] = param
  param_harvey, param_plaw, param_gaussian, noise = extract_param (full_param, n_harvey)
  model = background_model (freq, param_harvey, param_plaw, param_gaussian, noise, n_harvey)

  aux = psd / model + np.log (model)
  log_l = np.sum (aux)

  return log_l

def log_probability_back (param_to_fit, freq, psd, bounds, full_param, frozen_param, n_harvey, fit_log=False, norm=None) :
  '''
  Compute the positive posterior log probability (unnormalised) of the parameters to fit. 

  :param_to_fit: backgrounds parameters to fit.
  :type param_to_fit: 1d ndarray
 
  :param param: param to fit passed by perform_mle_back. Param are given in 
  the following order: Harvey law parameters, power law parameters, Gaussian p-mode 
  envelope parameters, noise constant. 

  :param freq: frequency vector in muHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/muHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param full_param: full vector necessary to define background model. 'param' element will
  be inserted according to the 'frozen_param' mask. 
  :type full_param: ndarray

  :param frozen_param: boolean array of the same size as full_param. Components set to True
  will not be fitted.
  :type frozen_param: boolean array

  :param n_harvey: number of Harvey laws to use to build the background
  model.  
  :type n_harvey: int

  :param fit_log: if set to True, parameters will be considered to have been given as logarithm
  and will be transformed with an exponential. Optional, default False.
  :type fit_log: bool

  :param norm: if given, the param_to_fit and bounds input vectors will be multiplied by this vector. 
  Optional, default ``None``.
  :type norm: ndarray

  :return: posterior probability value
  :rtype: float
  '''

  param_to_fit = np.copy (param_to_fit) #make a copy to not modify the reference array
  bounds = np.copy (bounds)

  if norm is not None :
    param_to_fit = param_to_fit * norm
    bounds[:,0] = bounds[:,0] * norm
    bounds[:,1] = bounds[:,1] * norm

  if fit_log :
    param_to_fit = np.exp (param_to_fit)
    bounds = np.exp (bounds)

  l_prior = log_prior (param_to_fit, bounds)

  if not np.isfinite (l_prior) :
    return - np.inf

  l_likelihood = - log_likelihood_back (param_to_fit, freq, psd, full_param, frozen_param, n_harvey, fit_log=False)

  l_proba = l_prior + l_likelihood

  return l_proba

def visualise_background (freq, psd, param_fitted=None, guess=None, low_cut=100., n_harvey=2, 
                          filename=None, spectro=True, alpha=1., show=False) :
  '''
  Plot fitted background against real PSD (and possibly against initial guess).
  '''

  if guess is not None :
    guess_harvey, guess_plaw, guess_gaussian, guess_noise = extract_param (guess, n_harvey)
    guess_model = background_model (freq, guess_harvey, guess_plaw, guess_gaussian, guess_noise, n_harvey)
  if param_fitted is not None :
    fitted_harvey, fitted_plaw, fitted_gaussian, fitted_noise = extract_param (param_fitted, n_harvey)
    fitted_back = background_model (freq, fitted_harvey, fitted_plaw, fitted_gaussian, fitted_noise, n_harvey)

  fig = plt.figure (figsize=(12,6))
  ax = fig.add_subplot (111)

  ax.plot (freq, psd, color='darkgrey')
  ax.plot (freq[freq>low_cut], psd[freq>low_cut], color='black')
  if guess is not None :
    ax.plot (freq, guess_model, color='green')
    guess_harvey = np.reshape (guess_harvey, (n_harvey, guess_harvey.size//n_harvey))
    for elt in guess_harvey :
      ax.plot (freq, harvey (freq, *elt), ':', color='green') 
    ax.plot (freq, gauss_env (freq, *guess_gaussian), ':', color='green')
  if param_fitted is not None :
    ax.plot (freq, fitted_back, color='red', alpha=alpha)
    fitted_harvey = np.reshape (fitted_harvey, (n_harvey, fitted_harvey.size//n_harvey))
    for elt in fitted_harvey :
      ax.plot (freq, harvey (freq, *elt), '--', color='red', alpha=alpha) 
    ax.plot (freq, gauss_env (freq, *fitted_gaussian), '--', color='red')

  ax.set_xlabel (r'Frequency ($\mu$Hz)')
  if spectro :
    ax.set_ylabel (r'PSD ((m/s)$^2$/$\_mu$Hz)')
  else :
    ax.set_ylabel (r'PSD (ppm$^2$/$\mu$Hz)')

  ax.set_xscale ('log')
  ax.set_yscale ('log')

  ax.set_ylim (0.9*np.amin(psd), 1.1*np.amax(psd))

  if filename is not None:
    plt.savefig (filename, format='pdf')

  if show :
    plt.show ()

  plt.close ()
  
  return

def perform_mle_background (freq, psd, n_harvey=2, r=1., m=1., teff=5770., guess=None, frozen_param=None, power_law=False,
                            frozen_harvey_exponent=False, fmin=None, fmax=None, low_cut=100., method=_minimize_powell, fit_log=False,
                            low_bounds=None, up_bounds=None, no_bounds=False, show=True, show_guess=False, filename=None, spectro=True) :
  '''
  Perform MLE over background model. 

  :param freq: frequency vector in muHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/muHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param n_harvey: number of Harvey laws to use to build the background
    model. Optional, default 2. With more than two Harvey laws, it is strongly recommended
    to manually feed the 'guest' parameter.  
  :type n_harvey: int

  :param r: stellar radius. Given in solar radius. Optional, default 1.
  :type r: float

  :param m: stellar mass. Given in solar mass. Optional, default 1.
  :type m: float

  :param teff: stellar effective temperature. Given in K. Optional, default 5770. 
  :type teff: float

  :param guess: first guess directly passed by the users. If guess is ``None``, the 
    function will automatically infer a first guess. Optional, default ``None``.
    Backgrounds parameters given in the following order:
    *param_harvey (3 n_harvey), param_plaw (2), param_gaussian (3), white noise (1)*
  :type guess: array-like.

  :param frozen_param: boolean array of the same size as guess. Components set to True
    will not be fitted.
  :type frozen_param: boolean array

  :param power_law: set to True to fit a power law on the background. Optional, default 
    False.
  :type power_law: bool

  :param frozen_harvey_exponent: set to True to freeze and not fit Harvey laws exponent to
    4. Optional, default False. 
  :type frozen_harvey_exponent: bool 

  :param fmin: Lower bound of the p-mode region that will be smoothed. Optional, default ``None``.
  :type fmin:

  :param fmax: Upper bound of the p-mode region that will be smoothed. Optional, default ``None``.
  :type fmax: float

  :param low_cut: Spectrum below this frequency will be ignored for the fit. The frequency value
    must be given in muHz. Optional, default 100.
  :type low_cut: float

  :param method: minimization method used by the scipy minimize function. Optional, default _minimize_powell
    (modified version allowing to use bounds)

  :param fit_log: if set to True, fit natural logarithm of the parameters. Optional, default False.
  :type fit_log: bool

  :param low_bounds: lower bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type low_bounds: ndarray

  :param up_bounds: upper bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type up_bounds: ndarray

  :param no_bounds: If set to True, no bounds will be considered for the parameter space exploration.
    Optional, default False.
  :type no_bounds: bool

  :param show: if set to True, will show at the end a plot summarising the fit. Optional, default True.
  :type show: bool

  :param show_guess: if set to True, will show at the beginning a plot summarising the guess. Optional, default False.
  :type show_guess: bool

  :param filename: if given, the summary plot will be saved under this filename. Optional, default ``None``.
    ``show`` argument must have been set to True. 
  :type filename: str

  :param spectro: if set to True, make the plot with unit consistent with radial velocity, else with 
    photometry. Optional, default True.
  :type spectro: bool

  :return: fitted background and fitted background parameters.  
  :rtype: tuple of array
  '''

  dnu = dnu_scale (r, m)
  numax = numax_scale (r, m, teff)
  print ('Dnu computed with scale law:', dnu) 
  print ('numax computed with scale law:', numax)

  lenguess = n_harvey * 3 + 6

  if guess is None :
    guess = background_guess (freq, psd, numax, dnu, m_star=m, n_harvey=n_harvey) 

  elif len (guess) != lenguess :
    raise Exception ('guess length is not consistent')

  if frozen_param is None :
    frozen_param = np.zeros (guess.size, dtype=bool)

  if frozen_harvey_exponent :
    for ii in range (n_harvey) :
      frozen_param[3*(ii+1)-1] = True

  if not power_law :
    guess[3*n_harvey] = 0     # with those adjustement, the power law component
    guess[3*n_harvey+1] = -1  # will be equal to 0
    frozen_param[3*n_harvey] = True 
    frozen_param[3*n_harvey+1] = True

  param = np.copy (guess[~frozen_param])
  full_param = np.copy (guess)

  if show_guess :
    visualise_background (freq, psd, guess=guess, low_cut=low_cut, n_harvey=n_harvey, spectro=spectro) 

  print ('Guess param')
  print (full_param)

  #Bounds
  if  no_bounds :
    bounds = None
    fit_log = True #the only condition considered is thus that we want positive parameters. 
  else :
    if low_bounds is None :
      low_bounds = get_low_bounds (full_param, n_harvey, freq, psd)
    if up_bounds is None :
      up_bounds = get_up_bounds (full_param, n_harvey, freq, psd)

    print ('Low bound for fit')
    print (low_bounds)
    print ('Up bound for fit')
    print (up_bounds)

    low_bounds = low_bounds[~frozen_param]
    up_bounds = up_bounds[~frozen_param]

    if fit_log :
      low_bounds = np.log (low_bounds)
      up_bounds = np.log (up_bounds)

    if method is _minimize_powell :
      bounds = (low_bounds, up_bounds)
    else :
      bounds = np.c_[low_bounds, up_bounds]

  if fit_log :
    param = np.log (param)

  # Cut under low_cut
  aux_freq = freq[freq>low_cut]
  aux_psd = psd[freq>low_cut]

  print ('Beginning fit')

  result = minimize (log_likelihood_back, param,
                     args=(aux_freq, aux_psd, full_param, frozen_param, n_harvey, fit_log), bounds=bounds, 
                     method=method)

  print (result)

  param_back = result.x

  if fit_log :
    param_back = np.exp (param_back)

  full_param[~frozen_param] = param_back
  param_harvey, param_plaw, param_gaussian, noise = extract_param (full_param, n_harvey)
  # We want the background without the gaussian envelope
  fitted_back = background_model (freq, param_harvey, param_plaw, param_gaussian=None, noise=noise, n_harvey=n_harvey)

  visualise_background (freq, psd, param_fitted=full_param, guess=guess, low_cut=low_cut, n_harvey=n_harvey, 
                          filename=filename, spectro=spectro, show=show) 


  return fitted_back, full_param

def explore_distribution_background (freq, psd,  
                                     n_harvey=2, r=1., m=1., teff=5770., guess=None, frozen_param=None, power_law=False,
                                     frozen_harvey_exponent=False, fmin=None, fmax=None, low_cut=100., fit_log=False,
                                     low_bounds=None, up_bounds=None, spectro=True, show=True, show_guess=False, show_corner=False,
                                     nsteps=1000, filename=None, parallelise=False, progress=False, nwalkers=64, filemcmc=None,
                                     coeff_discard=50, thin=1) :

  '''
  Use a MCMC framework to fit the background.  

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param n_harvey: number of Harvey laws to use to build the background
    model. Optional, default 2. With more than two Harvey laws, it is strongly recommended
    to manually feed the ``guess`` parameter.  
  :type n_harvey: int

  :param r: stellar radius. Given in solar radius. Optional, default 1.
  :type r: float

  :param m: stellar mass. Given in solar mass. Optional, default 1.
  :type m: float

  :param teff: stellar effective temperature. Given in K. Optional, default 5770. 
  :type teff: float

  :param guess: first guess directly passed by the user. If guess is ``None``, the 
    function will automatically infer a first guess. Optional, default ``None``.
    Backgrounds parameters given in the following order:
    *param_harvey (3 ``n_harvey``), param_plaw (2), param_gaussian (3), white noise (1)*
  :type guess: array-like.

  :param frozen_param: boolean array of the same size as guess. Components set to True
    will not be fitted.
  :type frozen_param: boolean array

  :param power_law: set to True to fit a power law on the background. Optional, default 
    False.
  :type power_law: bool

  :param frozen_harvey_exponent: set to True to freeze and not fit Harvey laws exponent to
    4. Optional, default False. 
  :type frozen_harvey_exponent: bool 

  :param fmin: Lower bound of the p-mode region that will be smoothed. Optional, default ``None``.
  :type fmin:

  :param fmax: Upper bound of the p-mode region that will be smoothed. Optional, default ``None``.
  :type fmax: float

  :param low_cut: Spectrum below this frequency will be ignored for the fit. The frequency value
    must be given in muHz. Optional, default 100.
  :type low_cut: float

  :param fit_log: if set to True, fit natural logarithm of the parameters. Optional, default False.
  :type fit_log: bool

  :param low_bounds: lower bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type low_bounds: ndarray

  :param up_bounds: upper bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type up_bounds: ndarray

  :param filename: Name of the file to save the summary plot. If filename is ``None``, the name will not
    be stored. Optional, default ``None``.
  :type filename: string

  :param filemcmc: name of the hdf5 where to store the chain. If filename is ``None``, the name will not
    be stored. Optional, default ``None``.
  :type filename: string

  :param parallelise: If set to True, use Python multiprocessing tool to parallelise process.
    Optional, default False.
  :type parallelise: bool

  :param show: if set to True, will show at the end a plot summarising the fit. Optional, default True.
  :type show: bool

  :param show_guess: if set to True, will show at the beginning a plot summarising the guess. Optional, default False.
  :type show_guess: bool

  :param coeff_discard: coeff used to compute the number of values to discard: total amount of
    sampled values will be divided by coeff_discard. Optional, default 50.
  :type coeff_discard: int

  :param thin: take only every ``thin`` steps from the chain. Optional, default 1. 
  :type thin: int

  :return: the fitted param, its param and their sigma values as determined by the MCMC walk.
  :rtype: tuple of array
  '''

  dnu = dnu_scale (r, m)
  numax = numax_scale (r, m, teff)

  lenguess = n_harvey * 3 + 6

  if guess is None :
    guess = background_guess (freq, psd, numax, dnu, m_star=m, n_harvey=n_harvey) 

  elif len (guess) != lenguess :
    raise Exception ('guess length is not consistent')

  if frozen_param is None :
    frozen_param = np.zeros (guess.size, dtype=bool)

  if frozen_harvey_exponent :
    for ii in range (n_harvey) :
      frozen_param[3*(ii+1)-1] = True

  if not power_law :
    guess[3*n_harvey] = 0     # with those adjustement, the power law component
    guess[3*n_harvey+1] = -1  # will be equal to 0
    frozen_param[3*n_harvey] = True 
    frozen_param[3*n_harvey+1] = True

  param = np.copy (guess[~frozen_param])
  full_param = np.copy (guess)

  if show_guess :
    visualise_background (freq, psd, guess=guess, low_cut=low_cut, n_harvey=n_harvey, spectro=spectro) 

  print ('Guess param')
  print (full_param)

  #Bounds
  if low_bounds is None :
    low_bounds = get_low_bounds (full_param, n_harvey, freq, psd)
  if up_bounds is None :
    up_bounds = get_up_bounds (full_param, n_harvey, freq, psd)

    print ('Low bound for fit')
    print (low_bounds)
    print ('Up bound for fit')
    print (up_bounds)

    low_bounds = low_bounds[~frozen_param]
    up_bounds = up_bounds[~frozen_param]

  if fit_log :
    low_bounds = np.log (low_bounds)
    up_bounds = np.log (up_bounds)

  bounds = np.c_[low_bounds, up_bounds]

  if fit_log :
    param = np.log (param)


  # Cut under low_cut
  aux_freq = freq[freq>low_cut]
  aux_psd = psd[freq>low_cut]

  print ('Beginning fit')

  bounds = np.c_[low_bounds, up_bounds]

  norm = np.abs (param)

  if parallelise :
    pool = ProcessPool ()
  else :
    pool = None

  param_to_pass = np.copy (param)
  bounds_to_pass = np.copy (bounds)

  #normalisation step
  param_to_pass = param_to_pass / norm
  bounds_to_pass[:,0] = bounds_to_pass[:,0] / norm
  bounds_to_pass[:,1] = bounds_to_pass[:,1] / norm

  pos = param_to_pass + 1e-4 * np.random.randn(nwalkers, param_to_pass.size)
  nwalkers, ndim = pos.shape

  if filemcmc is not None :
    backend = emcee.backends.HDFBackend(filemcmc)
    backend.reset(nwalkers, ndim) 
    #saving parameters name and normalisation information
    filemcmc_info = filemcmc[:len(filemcmc)-3] + '.dat'
    np.savetxt (filemcmc_info, np.c_[norm], fmt='%-s') 
  else :
    backend = None

  sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability_back, 
                                  args=(aux_freq, aux_psd, bounds_to_pass, full_param, frozen_param, n_harvey, 
                                  fit_log, norm), 
                                  backend=backend, pool=pool)
  sampler.run_mcmc(pos, nsteps, progress=progress)

  discard = nsteps // coeff_discard

  if show_corner :
    labels = create_labels (n_harvey, frozen_param)
    sample_to_plot = sampler.get_chain(discard=discard, thin=thin, flat=True)
    fig = corner.corner(sample_to_plot*norm, bins=100, labels=labels)
    fig.set_size_inches(24,24)
    axes = np.array(fig.axes).reshape((ndim, ndim))
    for yi in range(ndim):
      for xi in range(yi):
        ax = axes[yi, xi]
        ax.tick_params (labelsize=6)
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        ax.ticklabel_format (scilimits=(0,0), useOffset=False)
        if xi!=0 :
          ax.yaxis.set_ticklabels ([])
        if yi!=ndim-1 :
          ax.xaxis.set_ticklabels ([])
    if filemcmc is not None :
      plt.savefig (filemcmc[:len(filemcmc[:-3])]+'_cornerplot.pdf', format='pdf') 

  flat_samples = sampler.get_chain(discard=discard, thin=thin, flat=True)
  centiles = np.percentile(flat_samples, [16, 50, 84], axis=0) * norm 

  param_back = centiles[1,:]
  sigma_back = centiles[2,:] - centiles[0,:]

  if fit_log :
    param_back = np.exp (param_back)

  full_param[~frozen_param] = param_back
  full_sigma = np.zeros (full_param.size)
  full_sigma[~frozen_param] = sigma_back
  param_harvey, param_plaw, param_gaussian, noise = extract_param (full_param, n_harvey)
  # We want the background without the gaussian envelope
  fitted_back = background_model (freq, param_harvey, param_plaw, param_gaussian=None, noise=noise, n_harvey=n_harvey)

  visualise_background (freq, psd, param_fitted=full_param, guess=guess, low_cut=low_cut, n_harvey=n_harvey, 
                          filename=filename, spectro=spectro, alpha=0.8, show=show) 

  return fitted_back, full_param, full_sigma

