import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from scipy.optimize import minimize
from .analyse_window import sidelob_param
from .fit_tools import *
from .modified_optimize import _minimize_powell
from pathos.multiprocessing import ProcessPool
import numdifftools as nd
import emcee
import corner


'''
Given some known input stellar parameters (DeltaNu, Numax), this file
contains necessary functions to fit global parameters and create
initial guess to give to the MLE/MCMC peakbagging pipeline for individual
mode fitting.
'''

def first_guess (Dnu, numax, Teff, Hmax, Wenv, mass=None, return_bounds=False) :
  '''
  Use input parameters to design a first guess to feed the global_pattern fit. 
  >>>> eps, alpha, Dnu, numax, Hmax, Wenv, w, d02, d01 (if needed) <<<<

  :param Dnu: large frequency separation. Must be given in muHz.
  :type Dnu: float

  :param numax: maximum of power in p-mode envelope. Must be given in muHz.
  :type numax: float
  '''
  global_param = np.zeros (9)
  low_bounds = np.zeros (9)
  up_bounds = np.zeros (9)
  # epsilon
  global_param[0] = - 6.e-4 * Teff + 4.8
  low_bounds[0] = 0.8 * global_param[0]
  up_bounds[0] = 1.2 * global_param[0]
  # alpha
  global_param[1] = 0.25
  low_bounds[1] = 0.15
  up_bounds[1] = 0.5
  # Dnu
  global_param[2] = Dnu
  low_bounds[2] = Dnu - Dnu/100.
  up_bounds[2] = Dnu + Dnu/100.
  # numax
  global_param[3] = numax
  low_bounds[3] = numax - numax/100.
  up_bounds[3] = numax + numax/100.
  # Hmax
  global_param[4] = Hmax
  low_bounds[4] = Hmax / 10 
  up_bounds[4] = 5 * Hmax 
  # Wenv
  global_param[5] = Wenv
  low_bounds[5] = 0.8 * Wenv
  up_bounds[5] = 1.2 * Wenv 
  # w 
  w = 6.2e-3 * Teff - 33.3
  global_param[6] = w 
  low_bounds[6] = 0.2 * w
  up_bounds[6] = 3 * w
  # d02
  if Dnu > 125. :
    d02 = 8.
  elif Dnu < 80. :
    d02 = 0.13*Dnu - 3.5
  else :
    if mass is None :
      d02 = 7.5
    elif mass < 1. :
      d02 = 5.
    else : 
      d02 = 9.
  global_param[7] = d02 
  low_bounds[7] = 0.5 * d02
  up_bounds[7] = 1.5 * d02
  # d01 
  global_param[8] = 0.5 * Dnu - 3.25
  low_bounds[8] = 0.5 * global_param[8]
  up_bounds[8] = 1.5 * global_param[8]

  if return_bounds:
    bounds = np.c_[low_bounds, up_bounds]
    bounds[bounds<0.] = 1.e-6 #all parameters have to be within positive bounds
    return global_param, bounds
  else :
    return global_param

def pattern_to_a2z (eps, alpha, Dnu, numax, Hmax, Wenv, w, d02, d01=None, 
                    split=0, angle=0, n_order=3) :
  '''
  Compute param_a2z that will be used to feed a2z_to_pkb function and then compute_model
  function.
  Lorentzian parameters are inferred from global_parameters given as input. 

  :param eps: phase term epsilon
  :type eps: float

  :param alpha: second order curvature term alpha
  :type alpha: float

  :param Dnu: large frequency separation. Must be given in muHz.
  :type Dnu: float

  :param numax: maximum of power in p-mode envelope. Must be given in muHz.
  :type numax: float

  :param Hmax: amplitude of p-mode envelope
  :type Hmax: float

  :param Wenv: width of p-mode envelope
  :type Wenv: float

  :param w: width of indiviudal p-modes
  :type w: float

  :param d02: small separation between l=0 and l=2 peaks.
  :type d02: float

  :param d01: separation between l=0 and l=1 terms. If an input is given, the function will
  compute guess for l=1 modes. Optional, default None.
  :type d01: float

  :n_order: number of orders for which to create the guess frame. Optional, default 3. 
  :type n_order: int

  :return: a2z guess as a pandas DataFrame
  :rtype: pandas DataFrame
  '''

  # the first step is to compute order closest to Numax. 
  ref_order = int (numax / Dnu) 
  
  #dataframe is build order by order and then concatenated
  orders = list (range (ref_order - n_order//2, ref_order+n_order//2+1))

  nmax = numax / Dnu - eps 

  for counter, n in enumerate (orders) :
    if d01 is None :
      k = 4
      index_l = np.array (['2', '0', 'a', 'a'])
      index_n = np.array ([str(n-1), str(n), str(n), str(n)])
      param = np.array (['freq', 'freq', 'height', 'width'])
      extent = np.array (['mode', 'mode', 'order', 'order'])
    else :
      k = 5
      index_l = np.array (['1', '2', '0', 'a', 'a'])
      index_n = np.array ([n, n-1, n, n, n])
      param = np.array (['freq', 'freq', 'freq', 'height', 'width'])
      extent = np.array (['mode', 'mode', 'mode', 'order', 'order'])
    value = np.zeros (k)
    err = np.zeros (k)
    fixed = np.zeros (k)
    l_bound = np.zeros (k)
    h_bound = np.zeros (k)
    data = np.c_[index_n, index_l, param, extent, value, err, fixed, l_bound, h_bound]
    if counter==0 :
      df = pd.DataFrame (data=data)
      df = df.astype (dtype={0:np.int_, 4:np.float_, 5:np.float_, 6:np.float_, 7:np.float_, 8:np.float_})
    else :
      aux_df = pd.DataFrame (data=data)
      aux_df = aux_df.astype (dtype={0:np.int_, 4:np.float_, 5:np.float_, 6:np.float_, 7:np.float_, 8:np.float_})
      df = pd.concat ([df, aux_df])

  # compute values and bounds
  df.loc [df[1]=='0', 4] = (df.loc[df[1]=='0', 0] + eps) * Dnu + alpha / 2. * np.power (df.loc[df[1]=='0', 0] - nmax, 2)
  nu0 = df.loc [df[1]=='0', 4].to_numpy ()
  df.loc [df[1]=='2', 4] = nu0 - d02 
  if d01 is not None :
    df.loc [df[1]=='1', 4] = nu0 - d01
  df.loc [df[2]=='height', 4] = Hmax * np.exp (-0.5 * np.power ((nu0 - numax)/Wenv, 2))
  df.loc [df[2]=='width', 4] = w
  #bounds for freq
  df.loc[df[2]=='freq',7] = df.loc[df[2]=='freq',4] - 3.e-3 * numax #this parameter is arbitrary and maybe will
  df.loc[df[2]=='freq',8] = df.loc[df[2]=='freq',4] + 3.e-3 * numax #have to be modified in the future
  # bounds for width and height
  df.loc[df[2]=='width',7] = 0.5 * df.loc[df[2]=='width',4]
  df.loc[df[2]=='width',8] = 2. * df.loc[df[2]=='width',4]
  df.loc[df[2]=='height',7] = 0.5 * df.loc[df[2]=='height',4]
  df.loc[df[2]=='height',8] = 4. * df.loc[df[2]=='height',4]

  # creating global part of the dataframe
  index_n = np.array (['a', 'a', 'a', 'a', 'a']) 
  index_l = np.array (['a', 'a', '1', '2', '0']) 
  param = np.array (['split', 'angle', 'amp_l', 'amp_l', 'amp_l'])
  extent = np.array (['global', 'global', 'global', 'global', 'global'])
  value = np.array ([split, angle, 1.5, 0.7, 1.])
  err = np.zeros (5)
  fixed = np.zeros (5)
  l_bound = np.zeros (5)
  h_bound = np.array ([max (1., 0.5*split), 90., 0., 0., 0.])
  data = np.c_[index_n, index_l, param, extent, value, err, fixed, l_bound, h_bound]
  df_glob = pd.DataFrame (data=data) 
  df_glob = df_glob.astype (dtype={4:np.float_, 5:np.float_, 6:np.float_, 7:np.float_, 8:np.float_})

  # concatenate and return
  df = pd.concat ([df, df_glob])

  return df

def pattern_to_pkb (eps, alpha, Dnu, numax, Hmax, Wenv, w, d02, d01=None,
                    split=0, angle=0, n_order=3) :

  '''
  This function is just a wrapper of pattern_to_a2z and a2z_to_pkb.
  '''

  df = pattern_to_a2z (eps, alpha, Dnu, numax, Hmax, Wenv, w, d02, d01=d01,
                       split=split, angle=angle, n_order=n_order)
  param_pkb = a2z_to_pkb (df)

  return param_pkb


def log_prior (param, bounds) :
  '''
  Compute positive log_prior probability for MCMC framework. Uninformative priors are used.  

  :param param: parameters to fit. Optional, default None.
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

def log_likelihood_pattern (param_pattern, freq, psd, back, n_order, split=0, angle=0, param_wdw=None, 
                            fit_log=False) :
  '''
  Compute logarithmic likelihood for a given power spectrum, with a model built only with a global
  pattern (no fit of individual mode).

  :param param_pattern: param of the global pattern to adjust. They must be given in the following order:
  >>>> eps, alpha, Dnu, numax, Hmax, Wenv, w, d02, d01 (if needed) <<<<
  :type param_pattern: ndarray

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param fit_log: if set to True, will transform exponentially input parameters (considered to have been
  given in log). Optional, default False.
  :type fit_log: bool

  :return: logarithmic likelihood of the model
  :rtype: ndarray
  '''

  if fit_log :
    param_pattern = np.exp (param_pattern)

  param_pkb = pattern_to_pkb (*param_pattern, split=split, angle=angle, n_order=n_order)

  model = compute_model (freq, param_pkb, param_wdw=param_wdw)
  model = model / back
  model += 1. #we fit on SNR

  aux = psd / model + np.log (model)
  log_l = np.sum (aux)

  return log_l

def log_probability_pattern (param_to_fit, freq, psd, bounds, back, n_order, split=0, angle=0, param_wdw=None,
                             fit_log=False, norm=None) : 
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

  :param fit_log: if set to True, parameters will be considered to have been given as logarithm
  and will be transformed with an exponential. Optional, default False.
  :type fit_log: bool

  :param norm: if given, the param_to_fit and bounds input vectors will be multiplied by this vector. 
  Optional, default None.
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

  l_likelihood = - log_likelihood_pattern (param_to_fit, freq, psd, back, n_order, split, angle, param_wdw, 
                                           fit_log=False)

  l_proba = l_prior + l_likelihood

  return l_proba

def visualise (param_pattern, freq, psd, back, param_pattern_2=None, filename=None, 
               n_order=3, split=0, angle=0, snr=True, param_wdw=None, show=False) :
  '''
  Allow to visualise the considered global_model. May take an optional argument 
  param_pattern_2 to compare two patterns (for example guess and model fitted). 

  :param param_pattern: param of the global pattern. They must be given in the following order:
  >>>> eps, alpha, Dnu, numax, Hmax, Wenv, w, d02, d01 (if needed) <<<<
  :type param_pattern: ndarray

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param back: activity background vector that will be used to complete the model to fit. 
  Must have the same length than freq and psd. 
  :type back: ndarray

  :param param_pattern_2: param of an additionnal global pattern. They must be given in the following order:
  >>>> eps, alpha, Dnu, numax, Hmax, Wenv, w, d02, d01 (if needed) <<<<
  Optional, default None. 
  :type param_pattern: ndarray

  :param filename: if given, will save the shown figure at the following destination. 'show'
  argument must have been set to True. Optional, default None.  
  :type filename: str

  :param n_order: number of fitted orders. Optional, default 3. 
  :type n_order: int
  :type back: ndarray.

  :param snr: whether to plot or not on signal to noise data representation. Optional, default True.
  :type snr: bool
  '''

  fig = plt.figure (figsize=(12,6))
  ax = fig.add_subplot (111)

  param_pkb = pattern_to_pkb (*param_pattern, split=split, angle=angle, n_order=n_order)
  model = compute_model (freq, param_pkb, param_wdw=param_wdw)
  if snr :
    model = model / back + 1.
    psd = psd/back
  else : 
    model += back
  
  psd_s = smooth (psd, 50) #smoothing of psd

  ax.plot (freq, psd, color='darkgrey')
  ax.plot (freq, psd_s, color='black')

  if param_pattern_2 is not None :
    param_pkb_2 = pattern_to_pkb (*param_pattern_2, split=split, angle=angle, n_order=n_order)
    model_2 = compute_model (freq, param_pkb_2, param_wdw=param_wdw)
    if snr :
      model_2 = model_2 / back + 1.
    else : 
      model_2 += back
    ax.plot (freq, model_2, '--', color='green')

  ax.plot (freq, model, color='red')

  ax.set_xlabel (r'Frequency ($\mu$Hz)')

  if snr :
    ax.set_ylabel ('PSD (signal to noise ratio)')
  else :
    ax.set_ylabel ('PSD')

  if filename is not None :
    plt.savefig (filename)

  if show :
    plt.show ()

  plt.close ()

  return

def perform_mle_pattern (Dnu, numax, Hmax, Wenv, Teff, freq, psd, back=None, wdw=None, method=_minimize_powell,
                         n_order=3, split=0, angle=0, fit_l1=False, mass=None, guess=None, show=True, filename=None,
                         fit_log=False) :
                        
  '''
  Perform minimization of the log likelihood function according to the parameters set to vary.

  :param Dnu: large frequency separation. Must be given in muHz.
  :type Dnu: float

  :param numax: maximum of power in p-mode envelope. Must be given in muHz.
  :type numax: float

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param back: activity background vector that will be used to complete the model to fit. Optional default None.
  Must have the same length than freq and psd. 
  :type back: ndarray.

  :n_order: number of orders for which to create the guess frame. Optional, default 3. 
  :type n_order: int

  :param fit_l1: set to True to fit the d01 param and create guess for l=1 modes. Optional, default False.
  :type fit_l1: bool

  :param mass: mass of the star, in solar mass. Optional, default None.
  :type mass: float

  :param guess: MLE will take it as first guess of param if given. Optional, default None.
  Parameters must be given in the following order:
  >>>> eps, alpha, Dnu, numax, Hmax, Wenv, w, d02, d01 (if fit_l1 is set to True) <<<<
  :type guess: array-like

  :param show: if set to True, will plot a summary plot of guess (blue) and fitted (red) 
  pattern.
  :type show: bool

  :param filename: if given, will save the shown figure at the following destination. 'show'
  argument must have been set to True. Optional, default None.  
  :type filename: str

  :param fit_log: if set to True, will fit natural logarithm of parameters. Optional, default False.
  :type fit_log: bool

  :return: updated df_a2z
  :rtype: pandas DataFrame
  '''

  if guess is None :
    guess, bounds = first_guess (Dnu, numax, Teff, Hmax, Wenv, mass=mass, return_bounds=True)

  param = np.copy (guess)

  print ('Guess')
  cp_guess = np.reshape (guess, (1,9))
  summary_guess = pd.DataFrame (data=cp_guess, columns=['eps', 'alpha', 'Dnu', 'numax', 'Hmax', 'Wenv', 'w', 'd02', 'd01'])
  print (summary_guess)

  df_guess = pattern_to_a2z (*param, split=split, angle=angle, n_order=n_order)
  print (df_guess)

  if fit_log :
    param = np.log (param)
    bounds = np.log (bounds)

  if not fit_l1 :
    guess = guess[:guess.size-1]
    param = param[:param.size-1]
    bounds = bounds[:bounds.shape[0]-1,:]

  if method is _minimize_powell :
    lb = bounds[:,0]
    ub = bounds[:,1]
    bounds = (lb, ub)

  if back is None :
    back = np.full (psd.size, 1.)

  psd_to_fit = psd / back

  jac=None
  options=None
  tol=None

  if (method=='TNC') :
    options = {'disp':True, 'maxiter':30, 'ftol':10.}
    jac = nd.Jacobian (log_likelihood_pattern)   
    print ('Jacobian computed')

  if wdw is not None :
    dt = 1 / (2*freq[-1])
    param_wdw = sidelob_param (wdw, dt=dt)
  else :
    param_wdw = None

  low_bound_freq = np.amin (df_guess.loc[df_guess[2]=='freq',4].to_numpy ()) - 0.2*Dnu
  up_bound_freq = np.amax (df_guess.loc[df_guess[2]=='freq',4].to_numpy ()) + 0.2*Dnu

  aux_freq = freq[(freq>low_bound_freq)&(freq<up_bound_freq)]
  aux_psd = psd_to_fit[(freq>low_bound_freq)&(freq<up_bound_freq)]
  aux_back = back[(freq>low_bound_freq)&(freq<up_bound_freq)]

  result = minimize (log_likelihood_pattern, param, 
            args=(aux_freq, aux_psd, aux_back, n_order, split, angle, param_wdw, fit_log),
            bounds=bounds, method=method, jac=jac, options=options, tol=tol)

  print (result.message)

  param_fitted = result.x

  if fit_log :
    param_fitted = np.exp (param_fitted)

  print ('Fitted parameters') 
  if fit_l1 :
    summary_result = pd.DataFrame (data=np.reshape (param_fitted, (1,9)), columns=['eps', 'alpha', 'Dnu', 'numax', 'Hmax', 'Wenv', 'w', 'd02', 'd01'])
  else :
    summary_result = pd.DataFrame (data=np.reshape (param_fitted, (1,8)), columns=['eps', 'alpha', 'Dnu', 'numax', 'Hmax', 'Wenv', 'w', 'd02'])
  print (summary_result)

  df_a2z = pattern_to_a2z (*param_fitted, split=split, angle=angle, n_order=n_order)

  visualise (param_fitted, aux_freq, aux_psd, aux_back, param_pattern_2=guess, filename=filename,
               n_order=n_order, split=split, angle=angle, snr=True, param_wdw=param_wdw, show=show) 

  return df_a2z, param_fitted

def explore_distribution_pattern (Dnu, numax, Hmax, Wenv, Teff, freq, psd, back=None, wdw=None,
                         n_order=3, split=0, angle=0, fit_l1=False, mass=None, guess=None, show=True,
                         fit_log=False, show_corner=False, nsteps=1000, filename=None, parallelise=False, progress=False, 
                         nwalkers=64, filemcmc=None, coeff_discard=50, thin=1) :
                        
  '''
  Perform minimization of the log likelihood function according to the parameters set to vary.

  :param Dnu: large frequency separation. Must be given in muHz.
  :type Dnu: float

  :param numax: maximum of power in p-mode envelope. Must be given in muHz.
  :type numax: float

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param back: activity background vector that will be used to complete the model to fit. Optional default None.
    Must have the same length than freq and psd. 
  :type back: ndarray.

  :n_order: number of orders for which to create the guess frame. Optional, default 3. 
  :type n_order: int

  :param fit_l1: set to True to fit the d01 param and create guess for l=1 modes. Optional, default False.
  :type fit_l1: bool

  :param mass: mass of the star, in solar mass. Optional, default None.
  :type mass: float

  :param guess: MCMC will take it as first guess of param if given. Optional, default None.
    Parameters must be given in the following order:
    >>>> eps, alpha, Dnu, numax, Hmax, Wenv, w, d02, d01 (if fit_l1 is set to True) <<<<
  :type guess: array-like

  :param show: if set to True, will plot a summary plot of guess (blue) and fitted (red) 
    pattern.
  :type show: bool

  :param filename: if given, will save the shown figure at the following destination. 'show'
    argument must have been set to True. Optional, default None.  
  :type filename: str

  :param fit_log: if set to True, will fit natural logarithm of parameters. Optional, default False.
  :type fit_log: bool

  :param filemcmc: name of the hdf5 where to store the chain. If filename is None, the name will not
    be stored. Optional, default None.
  :type filename: string

  :param parallelise: If set to True, use Python multiprocessing tool to parallelise process.
    Optional, default False.
  :type parallelise: bool

  :param show: if set to True, will show at the end a plot summarising the fit. Optional, default True.
  :type show: bool

  :param coeff_discard: coeff used to compute the number of values to discard: total amount of
    sampled values will be divided by coeff_discard. Optional, default 50.
  :type coeff_discard: int

  :param thin: take only every ``thin`` steps from the chain. Optional, default 1. 
  :type thin: int

  :return: updated df_a2z with relevant sigmas as determined by the MCMC walks.
  :rtype: pandas DataFrame
  '''

  if guess is None :
    guess, bounds = first_guess (Dnu, numax, Teff, Hmax, Wenv, mass=mass, return_bounds=True)
  else :
    xxx, bounds = first_guess (Dnu, numax, Teff, Hmax, Wenv, mass=mass, return_bounds=True)

  param = np.copy (guess)

  print ('Guess')
  cp_guess = np.reshape (guess, (1,9))
  summary_guess = pd.DataFrame (data=cp_guess, columns=['eps', 'alpha', 'Dnu', 'numax', 'Hmax', 'Wenv', 'w', 'd02', 'd01'])
  print (summary_guess)

  df_guess = pattern_to_a2z (*param, split=split, angle=angle, n_order=n_order)
  print (df_guess)

  if fit_log :
    param = np.log (param)
    bounds = np.log (bounds)

  if not fit_l1 :
    guess = guess[:guess.size-1]
    param = param[:param.size-1]
    bounds = bounds[:bounds.shape[0]-1,:]

  if back is None :
    back = np.full (psd.size, 1.)

  psd_to_fit = psd / back

  if wdw is not None :
    dt = 1 / (2*freq[-1])
    param_wdw = sidelob_param (wdw, dt=dt)
  else :
    param_wdw = None

  low_bound_freq = np.amin (df_guess.loc[df_guess[2]=='freq',4].to_numpy ()) - 0.2*Dnu
  up_bound_freq = np.amax (df_guess.loc[df_guess[2]=='freq',4].to_numpy ()) + 0.2*Dnu

  aux_freq = freq[(freq>low_bound_freq)&(freq<up_bound_freq)]
  aux_psd = psd_to_fit[(freq>low_bound_freq)&(freq<up_bound_freq)]
  aux_back = back[(freq>low_bound_freq)&(freq<up_bound_freq)]

  print ('Beginning fit')

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

  print (n_order)
  sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability_pattern, 
                                  args=(aux_freq, aux_psd, bounds_to_pass, aux_back, n_order, split, angle, param_wdw, 
                                  fit_log, norm), 
                                  backend=backend, pool=pool)
  sampler.run_mcmc(pos, nsteps, progress=progress)

  discard = nsteps // coeff_discard

  if show_corner :
    sample_to_plot = sampler.get_chain(discard=discard, thin=thin, flat=True)
    if fit_l1 :
      labels = ['epsilon', 'alpha', 'dnu', 'numax', 'Hmax', 'Wenv', 'w', 'd02', 'd01']
    else :
      labels = ['epsilon', 'alpha', 'dnu', 'numax', 'Hmax', 'Wenv', 'w', 'd02']
    fig = corner.corner(sample_to_plot*norm, labels=labels, bins=100)
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

  param_fitted = centiles[1,:]
  sigma_fitted = centiles[2,:] - centiles[0,:]

  if fit_log :
    param_fitted = np.exp (param_fitted)

  print ('Fitted parameters') 
  if fit_l1 :
    summary_result = pd.DataFrame (data=np.reshape (param_fitted, (1,9)), columns=['eps', 'alpha', 'Dnu', 'numax', 'Hmax', 'Wenv', 'w', 'd02', 'd01'])
  else :
    summary_result = pd.DataFrame (data=np.reshape (param_fitted, (1,8)), columns=['eps', 'alpha', 'Dnu', 'numax', 'Hmax', 'Wenv', 'w', 'd02'])
  print (summary_result)

  df_a2z = pattern_to_a2z (*param_fitted, split=split, angle=angle, n_order=n_order)

  visualise (param_fitted, aux_freq, aux_psd, aux_back, param_pattern_2=guess, filename=filename,
               n_order=n_order, split=split, angle=angle, snr=True, param_wdw=param_wdw, show=show) 

  return df_a2z, param_fitted


