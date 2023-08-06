import numpy as np
import pandas as pd
from scipy.optimize import minimize
from .modified_optimize import _minimize_powell
from .fit_tools import *
from .analyse_window import sidelob_param
import sys
import numdifftools as nd
import matplotlib
import matplotlib.pyplot as plt

def cond_transf (a, transform=('height', 'width'), transform_all=False) :
  '''
  Allow to choose for which parameters the logarithm will be given to
  likelihood and prior parameters function rather than the parameter himself

  :param a: array containing the types of the parameters to fit (freq, width,
  height, split, amp_l)
  :type a: string array

  :param transform: the parameters that will be transformed
  :type transform: tuple of strings

  :return: boolean array to use as a mask to transform the parameter to fit.
  :rtype: boolean array
  '''

  cond = np.zeros (a.size).astype (bool)

  if transform_all:
    return np.ones (a.size).astype (bool)
  
  for elt in transform:
    cond = cond | (a==elt)
  
  return cond

def log_likelihood (param, param_type, freq, psd, back, df_a2z, transform, instr='kepler') :
  '''
  Compute logarithmic likelihood for a given power spectrum.

  :param param: parameter that scipy.optimize minimize will use to find the
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
  :type df_global: pandas DataFrame.

  :param transform: list of parameter that are given in natural log by the calling routine and that
  will be retransformed. If None, the function will consider that all parameters have been give as
  logarithm. 
  :type transform: tuple of strings

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf'
  :type instr: str

  :return: logarithmic likelihood of the model
  :rtype: ndarray
  '''

  df = df_a2z #just an alias
  param_to_fit = np.copy (param)

  #cond = (param_type=='height')|(param_type=='width')
  if transform is None :
    cond = cond_transf (param_type, transform_all=True)
  else :
    cond = cond_transf (param_type, transform=transform)
  param_to_fit[cond] = np.exp (param_to_fit[cond])

  #removing free parameter
  free = param_to_fit [-1]
  param_to_fit = param_to_fit[:param_to_fit.size-1]

  df.loc[df[6]==0, 4] = param_to_fit
  param_pkb = a2z_to_pkb (df)
 
  model = compute_model (freq, param_pkb, instr=instr)
  model = model / back
  model += free

  aux = psd / model + np.log (model)
  log_l = np.sum (aux)

  return log_l

def log_likelihood_wdw (param, param_type, freq, psd, back, df_a2z, transform, param_wdw, instr='kepler') :
  '''
  Compute logarithmic likelihood for a given power spectrum. The routine will
  also analyse the observation window and adapt consequently the model. 

  :param: parameter that scipy.optimize minimize will use to find the
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

  :param param_wdw: parameters of the observation window timeseries
  :type wdw: ndarray.

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf'
  :type instr: str

  :return: logarithmic likelihood of the model
  :rtype: ndarray
  '''

  df = df_a2z
  param_to_fit = np.copy (param)

  #removing free parameter
  free = param_to_fit [-1]
  param_to_fit = param_to_fit[:param_to_fit.size-1]

  #cond = (param_type=='height')|(param_type=='width')
  if transform is None :
    cond = cond_transf (param_type, transform_all=True)
  else :
    cond = cond_transf (param_type, transform=transform)
  param_to_fit[cond] = np.exp (param_to_fit[cond])
  df.loc[df[6]==0, 4] = param_to_fit

  param_pkb = a2z_to_pkb (df)
  model = compute_model (freq, param_pkb, param_wdw=param_wdw, instr=instr)
  model = model / back
  model += free

  aux = psd / model + np.log (model)
  log_l = np.sum (aux)

  return log_l


def perform_mle (df_a2z, freq, psd, back=None, wdw=None, method=_minimize_powell, show_prior=True,
                 show_result=True, spectro=True, low_bound_freq=1500, up_bound_freq=5000, instr='kepler') : 
  '''
  Perform minimization of the log likelihood function according to the parameters set to vary.

  :param df_a2z: input parameters as a pandas DataFrame with the a2z syntax.
  :type df_a2z: pandas DataFrame

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param back: activity background vector that will be used to complete the model to fit. Optional default None.
  Must have the same length than freq and psd. 
  :type back: ndarray.

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf'
  :type instr: str

  :return: updated df_a2z
  :rtype: pandas DataFrame
  '''

  df_ref = df_a2z.copy () #it seems that scipy minimize is able to modify the frame when given in arguments

  if show_prior == True :
    param_prior = a2z_to_pkb (df_a2z)
    plot_from_param (param_prior, freq, psd, back=back, wdw=None, smoothing=10, spectro=spectro, correct_width=1.,
                   show=True, save=False)

  param_to_fit, param_type, bounds_to_fit = a2z_df_to_param (df_a2z)
  print ('Input param to fit')
  print (np.c_[param_to_fit, param_type])

  transform = None
  cond = cond_transf (param_type, transform_all = True)
  param_to_fit[cond] = np.log (param_to_fit[cond])

  lower_bounds = bounds_to_fit [:,0]
  upper_bounds = bounds_to_fit [:,1]

  lower_bounds[cond] = np.log(lower_bounds[cond])
  upper_bounds[cond] = np.log(upper_bounds[cond])
  lower_bounds[np.isinf (lower_bounds)] = None
  upper_bounds[np.isinf (upper_bounds)] = None

  # adding free constant to adjust local background
  param_to_fit = np.append (param_to_fit, 1.)
  lower_bounds = np.append (lower_bounds, 0.)
  upper_bounds = np.append (upper_bounds, 2.)

  bounds_to_fit = (lower_bounds, upper_bounds)

  if method=='TNC' :
    bounds_to_fit = np.c_[lower_bounds, upper_bounds]

  if back is None :
    back = np.full (psd.size, 1.)

  psd_to_fit = psd / back

  jac=None
  options=None
  tol=None

  if (method=='TNC') :
    options = {'disp':True, 'maxiter':30, 'ftol':10.}
    if wdw is None :
      jac = nd.Jacobian (log_likelihood)   
    else :
      jac = nd.Jacobian (log_likelihood_wdw)   
    print ('Jacobian computed')

  if wdw is not None :
    dt = 1 / (2*freq[-1])
    param_wdw = sidelob_param (wdw, dt=dt)
    # only consider a given interval of frequency (ideally center around the
    # p-mode region) to compute the likelihood values when performing the fit.
    aux_freq = freq[(freq>low_bound_freq)&(freq<up_bound_freq)]
    aux_psd = psd_to_fit[(freq>low_bound_freq)&(freq<up_bound_freq)]
    aux_back = back[(freq>low_bound_freq)&(freq<up_bound_freq)]
    result = minimize (log_likelihood_wdw, param_to_fit, 
              args=(param_type, aux_freq, aux_psd, aux_back, df_a2z, transform, param_wdw, instr),
              bounds=bounds_to_fit, method=method, jac=jac, options=options, tol=tol)
  else :
    # only consider a given interval of frequency (ideally center around the
    # p-mode region) to compute the likelihood values when performing the fit.
    aux_freq = freq[(freq>low_bound_freq)&(freq<up_bound_freq)]
    aux_psd = psd_to_fit[(freq>low_bound_freq)&(freq<up_bound_freq)]
    aux_back = back[(freq>low_bound_freq)&(freq<up_bound_freq)]
    result = minimize (log_likelihood, param_to_fit, 
              args=(param_type, aux_freq, aux_psd, aux_back, df_a2z, transform, instr),
              bounds=bounds_to_fit, method=method, jac=jac, options=options, tol=tol)
    
  print (result.message)

  param_fitted = result.x

  # taking apart free constant
  free = param_fitted[-1]
  param_fitted = param_fitted[:param_fitted.size-1]

  param_fitted[cond] = np.exp (param_fitted[cond])
  
  df_compare = pd.DataFrame (data = np.c_[df_ref.loc[df_a2z[6]==0, 4].to_numpy(), param_fitted],
                             columns = ['prior', 'fitted'])
  print (df_compare)
  df_a2z.loc[df_a2z[6]==0, 4] = param_fitted

  if show_result == True :
    param_result = a2z_to_pkb (df_a2z)
    plot_from_param (param_result, freq, psd, back=back, wdw=wdw, smoothing=10, spectro=spectro, correct_width=1.,
                   show=True, save=False)

  return df_a2z

